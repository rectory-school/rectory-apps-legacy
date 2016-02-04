#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Student, Parent, StudentParentRelation
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Permrecs"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the students from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning student import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        seen_ids = set()
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                nameFirst = fields['NameFirst'] or ""
                nameLast = fields['NameLast'] or ""
                nameNickname = fields['NameNickname'] or ""
                email = fields['EMailSchool'] or ""
                studentID = fields['IDSTUDENT']
                password = fields["PasswordActiveDirctory"] or ""
                username = fields["Network_User_Name"] or ""
                gender = fields["Sex"] or ""
                
                if not studentID:
                    continue
                
                seen_ids.add(studentID)
                
                if username:
                    if len(username) > 20:
                        username = username[0:20]
                        logger.warn("Username {username:} was truncated to 20 characters".format(username=username))
                
                if email:
                    validEmail = validate_email(email)
                
                    if not validEmail:
                        email = ""
                        logger.warn("E-mail address {email:} for {id:} ({first:} {last:}) is invalid; address blanked".format(email=email, id=studentID, first=nameFirst, last=nameLast))
                
                try:
                    student = Student.objects.get(student_id=studentID)
                    logger.info("Found student {studentID:}".format(studentID=studentID))
                    forceSave = False
                    
                except Student.DoesNotExist:
                    student = Student(student_id=studentID)
                    logger.info("Creating student {studentID:}".format(studentID=studentID))
                    forceSave = True
                    
                attrMap = {
                    'first_name': nameFirst,
                    'last_name': nameLast,
                    'nickname': nameNickname,
                    'email': email,
                    'rectory_password': password,
                    'username': username,
                    'gender': gender,
                }
                
                for attr in attrMap:
                    dbValue = getattr(student, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(student, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {studentID:} from {oldValue:} to {newValue:}".format(attr=attr, studentID=studentID, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    student.save()
                
                self.sync_relations(student, fields)
                    
            extra_students = Student.objects.exclude(student_id__in=seen_ids)
            for extra_student in extra_students:
                logger.warn("Deleting extra student {}".format(extra_student.id))
                extra_student.delete()

    def sync_relations(self, student, fields):
      relevant_parent_ids = set()
      
      for family_number in ('1', '2', '3', '4'):
        family_id_key = "IDFamily" + family_number
        family_id = fields[family_id_key]
        
        if not family_id:
          continue
        
        for parent_code in ('a', 'b'):
          relation_field = "P" + family_number + parent_code + "_Relation"
          full_parent_id = family_id + "P" + parent_code
          
          relationship = fields[relation_field] or ""
          
          try:
            parent = Parent.objects.get(full_id=full_parent_id)
          except Parent.DoesNotExist:
            continue
          
          do_save = False
          
          try:
            student_parent_relation = StudentParentRelation.objects.get(parent=parent, student=student)
          except StudentParentRelation.DoesNotExist:
            student_parent_relation = StudentParentRelation(parent=parent, student=student)
            do_save = True
          
          attr_map = {
            'relationship': relationship,
            'family_id_key': family_id_key
          }
          
          for attr, desired_value in attr_map.items():
            db_value = getattr(student_parent_relation, attr)
            
            if db_value != desired_value:
              setattr(student_parent_relation, attr, desired_value)
              do_save = True
          
          if do_save:
            student_parent_relation.save()
            
          relevant_parent_ids.add(parent.id)

      extra_parents = student.parents.exclude(pk__in=relevant_parent_ids)
      for extra_parent in extra_parents:
        logger.warn("Deleting parent {:}".format(extra_parent.id))