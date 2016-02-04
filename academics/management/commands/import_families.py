#!/usr/bin/python

import logging
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from validate_email import validate_email

from academics.models import Parent
from academics.utils import fmpxmlparser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Import Permrecs"
    
    def add_arguments(self, parser):
        parser.add_argument('filename', metavar='FILENAME', help='The filename to process the families from')
    
    def handle(self, *args, **kwargs):
        logger.info("Beginning family import routine")
        
        data = fmpxmlparser.parse_from_file(kwargs['filename'])

        results = data['results']    
        
        seen_ids = set()
        
        with transaction.atomic():
          for row in results:
            fields = row['parsed_fields']
            
            family_id = fields["IDFAMILY"]
            
            parents = {}
            
            address = fields['P_address_full'] or ""
            address_lines = address.splitlines()
            address = "\n".join([line.strip() for line in address_lines])
            
            parent_attr_map = {              
              'Pa': {
                'first_name': (fields['Pa_first'] or "").strip(),
                'last_name': (fields['Pa_last'] or "").strip(),
                'email': (fields['Pa_email'] or "").strip(),
                'phone_home': (fields['P_phone_H'] or "").strip(),
                'phone_work': (fields['Pa_phone_W'] or "").strip(),
                'phone_cell': (fields['Pa_phone_cell'] or "").strip(),
                'address': address,
                'family_id': family_id,
                'parent_id': 'Pa',
              },
              'Pb': {
                'first_name': (fields['Pb_first'] or "").strip(),
                'last_name': (fields['Pb_last'] or "").strip(),
                'email': (fields['Pb_email'] or "").strip(),
                'phone_home': (fields['P_phone_H'] or "").strip(),
                'phone_work': (fields['Pb_phone_W'] or "").strip(),
                'phone_cell': (fields['Pb_phone_cell'] or "").strip(),
                'address': address,
                'family_id': family_id,
                'parent_id': 'Pa',
              }
            }
            
            for parent_code, parent_attrs in parent_attr_map.items():
              full_id = family_id + parent_code
              seen_ids.add(full_id)
              
              do_save = False
              
              if not (parent_attrs['first_name'] and parent_attrs['last_name']):
                #First and last name is the criteria for me to import
                continue
              
              try:
                parent = Parent.objects.get(full_id=full_id)
              except Parent.DoesNotExist:
                logger.info("Creating parent {parent_id:}".format(parent_id=full_id))
                
                do_save = True
                parent = Parent()
                parent.full_id = full_id
            
              for attr, desired_value in parent_attrs.items():
                db_value = getattr(parent, attr)
                if db_value != desired_value:
                  logger.info("Updating {attr:} on {parent_id:} from {db_value} to {desired_value:}".format(attr=attr, parent_id=full_id, db_value=db_value, desired_value=desired_value))
                  do_save = True
                  setattr(parent, attr, desired_value)
              
              if do_save:
                parent.save()
          
          extra_parents = Parent.objects.exclude(full_id__in=seen_ids)
          for extra_parent in extra_parents:
              logger.warn("Deleting extra parent {}".format(extra_parent.id))
              extra_parent.delete()