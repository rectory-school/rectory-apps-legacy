from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors

from calendar_generator.models import Calendar
from calendar_generator.lib import get_days, structured_calendar_layout
from calendar_generator.pdf_generator.calendar_maker import GridDrawer, GridFormatter

# Create your views here.
def calendar_days_text(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    response = HttpResponse(content_type="text/plain")
    
    for date in sorted(days.keys()):
        line = "{date:}: {day:}\n".format(date=date.strftime("%Y-%m-%d"), day=days[date].letter)
        
        response.write(line)
    
    print(structured_calendar_layout(days, False))
    
    return response

def full_calendar_pdf(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    header_days = calendar.numeric_days
    
    structured_data = structured_calendar_layout(days, False)
    
    response = HttpResponse(content_type="application/pdf")
    
    pdf = canvas.Canvas(response, pagesize=(11*inch, 8.5*inch))
    
    for year, month in sorted(structured_data.keys()):
        grid = structured_data[(year, month)]
        
        first_of_month = date(year, month, 1)
        month_title = first_of_month.strftime("%B")
        
        grid_formatter = GridFormatter(header_font="HelveticaNeue-Bold", day_font = "HelveticaNeue-Light", date_font="HelveticaNeue-Light")
        grid_formatter.header_background = colors.black
        grid_formatter.header_line = colors.white
        grid_formatter.header_color = colors.white
        
        grid_drawer = GridDrawer(grid, header_days, grid_formatter)
        
        grid_drawer.draw_on(pdf, .5*inch, 8*inch, 10*inch, 7.5*inch, 1)
        pdf.showPage()
        
    pdf.save()
    
    return response