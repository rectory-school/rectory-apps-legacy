from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from calendar_generator.models import Calendar
from calendar_generator.lib import get_days

# Create your views here.
def calendar_days_text(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    response = HttpResponse(content_type="text/plain")
    
    for date in sorted(days.keys()):
        line = "{date:}: {day:}\n".format(date=date.strftime("%Y-%m-%d"), day=days[date].letter)
        
        response.write(line)
    
    return response