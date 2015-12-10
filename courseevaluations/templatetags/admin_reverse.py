from django.core import urlresolvers
from django import template

register = template.Library()

@register.simple_tag
def admin_url_for(obj):
    app_label = obj._meta.app_label
    model_label = obj._meta.model_name
    
    admin_view = "admin:{app_label:}_{model_label:}_change".format(app_label=app_label, model_label=model_label)
    
    return urlresolvers.reverse(admin_view, args=(obj.id, ))
    