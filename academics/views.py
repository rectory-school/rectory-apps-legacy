from io import StringIO

from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from academics.models import StudentParentRelation

import vobject


#Checks if a parent has any attribute we care about
def parent_is_relevant(parent):
    desired_attrs = ('phone_cell', 'phone_work', 'phone_home', 'email')
    
    for attr in desired_attrs:
        value = getattr(parent, attr)
        if value:
            return True
    
    return False

@permission_required("academics.can_download_family_data")
def get_vcards(request):
    active_relations = StudentParentRelation.objects.filter(student__current=True).prefetch_related('student', 'parent')
    
    # {parent: [(student, relationship)]}
    parents = {}
    
    for relationship in active_relations:
        parent = relationship.parent
        student = relationship.student
        
        #Make sure the parent has something we care about
        if not parent_is_relevant(parent):
            continue
        
        if parent not in parents:
            parents[parent] = []
        
        parents[parent].append(relationship)
    
    response = HttpResponse(content_type="text/vcard")
    response["Content-Disposition"] = "attachment; filename=\"family_contact_data.vcf\""
        
    for parent, relationships in parents.items():
        students = set([relationship.student for relationship in relationships])
        
        card = vobject.vCard()
        
        card.add('n')
        card.n.value = vobject.vcard.Name(family=parent.last_name, given=parent.first_name)
        
        card.add('fn')
        card.fn.value = parent.name
        
        for vcard_tel_type, parent_attr in (("cell", "phone_cell"), ("work", "phone_work"), ("home", "phone_home")):
            parent_value = getattr(parent, parent_attr)
            
            if parent_value:
                vcard_tel = card.add('tel')
                vcard_tel.type_param = vcard_tel_type
                vcard_tel.value = parent_value
        
        if parent.email:
            vcard_email = card.add('email')
            vcard_email.value = parent.email
        
        vcard_org = card.add('ORG')
        vcard_org.value = [", ".join([student.name for student in students])]
        
        note_data = StringIO()
        note_data.write("{family_id}-{parent_id}\n".format(family_id=parent.family_id, parent_id=parent.parent_id))
        
        for relationship in relationships:
            if relationship.relationship:
                note_data.write("{name:}: {relationship:} ({family_id_key:})\n".format(name=relationship.student.name,
                                                                                       relationship=relationship.relationship,
                                                                                       family_id_key=relationship.family_id_key))
            else:
                note_data.write("{name:} ({family_id_key:})\n".format(name=relationship.student.name,
                                                                      family_id_key=relationship.family_id_key))
        vcard_note = card.add('NOTE')
        vcard_note.value = note_data.getvalue()
        
        response.write(card.serialize())
    
    return response