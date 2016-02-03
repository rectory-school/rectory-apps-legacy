#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Student, Enrollment, AcademicYear, Dorm, Teacher, Grade
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Enrollments"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the enrollments from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning enrollment import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        with transaction.atomic():
            for row in results:
                fields = row['parsed_fields']
                
                studentID = fields['IDStudent']
                academicYear = fields['AcademicYear']
                boarderDay = fields['BoarderDay']
                dormName = fields['DormName'] or ""
                grade_code = fields['Grade']
                division = fields['Division'] or ""
                section = fields["Section Letter"] or ""
                advisorID = fields["IDAdvisor"]
                statusEnrollment = fields["StatusEnrollment"] or ""
                statusAttending = fields["StatusAttending"] or ""
                enrolledDate = fields["EnrollmentDate"]
                
                if not studentID or not academicYear:
                    continue
                
                try:
                    academicYear = AcademicYear.objects.get(year=academicYear)
                except AcademicYear.DoesNotExist:
                    academicYear = AcademicYear(year=academicYear)
                    academicYear.save()
                
                
                try:
                    student = Student.objects.get(student_id=studentID)
                except Student.DoesNotExist:
                    logger.error("Student {studentID:} is in enrollments but not in permrecs".format(studentID=studentID))
                    continue
                
                if boarderDay and boarderDay.upper() == "B":
                    boarder = True
                else:
                    boarder = False
                
                if dormName:
                    try:
                        dorm = Dorm.objects.get(dorm_name=dormName)
                    except Dorm.DoesNotExist:
                        logger.error("Dorm {dorm:} does not exist".format(dorm=dormName))
                        dorm = None
                else:
                    dorm = None
                
                
                if advisorID:
                    try:
                        advisor = Teacher.objects.get(teacher_id = advisorID)
                    except Teacher.DoesNotExist:
                        logger.error("Advisor {advisorID:} does not exist".format(advisorID=advisorID))
                        advisor = None
                else:
                    advisor = None
                
                if grade_code:
                  try:
                    grade = Grade.objects.get(grade=grade_code)
                  except Grade.DoesNotExist:
                    grade = Grade()
                    grade.grade = grade_code
                    grade.description = "Grade {grade:}".format(grade=grade_code)
                    grade.save()
                
                try:
                    enrollment = Enrollment.objects.get(student = student, academic_year = academicYear)
                    logger.info("Found enrollment {studentID:}/{academicYear:}".format(studentID=studentID, academicYear=academicYear))
                    forceSave = False
                    
                except Enrollment.DoesNotExist:
                    logger.info("Creating enrollment {studentID:}/{academicYear:}".format(studentID=studentID, academicYear=academicYear))
                    enrollment = Enrollment()
                    enrollment.student = student
                    enrollment.academic_year = academicYear
                    forceSave = True
                                        
                attrMap = {
                    'boarder': boarder,
                    'dorm': dorm,
                    'grade': grade,
                    'division': division,
                    'section': section,
                    'advisor': advisor,
                    'status_enrollment': statusEnrollment,
                    'status_attending': statusAttending,
                    'enrolled_date': enrolledDate
                }
                
                for attr in attrMap:
                    dbValue = getattr(enrollment, attr)
                    
                    if dbValue != attrMap[attr]:
                        setattr(enrollment, attr, attrMap[attr])
                        logger.info("Updating {attr:} on {studentID:}/{academicYear:} from {oldValue:} to {newValue:}".format(attr=attr, studentID=studentID, academicYear=academicYear, oldValue=dbValue, newValue=attrMap[attr]))
                        forceSave = True
                    
                if forceSave:
                    enrollment.save()

            #TODO: Delete the extra records
