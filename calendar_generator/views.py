from datetime import date

from io import BytesIO
from zipfile import ZipFile, ZIP_STORED
import math

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors

from calendar_generator.models import Calendar
from calendar_generator.lib import get_days, structured_calendar_layout
from calendar_generator.pdf_generator.calendar_maker import GridDrawer, GridFormatter

color_accent = colors.Color(83/256, 123/256, 156/256)

color_formatter = GridFormatter(header_font="HelveticaNeue-Bold", day_font = "HelveticaNeue-Light", date_font="HelveticaNeue-Light")
color_formatter.header_background = color_accent
color_formatter.header_line_color = colors.white
color_formatter.header_color = colors.white

black_formatter = GridFormatter(header_font="HelveticaNeue-Bold", day_font = "HelveticaNeue-Light", date_font="HelveticaNeue-Light")
black_formatter.header_background = colors.black
black_formatter.header_line = colors.white
black_formatter.header_color = colors.white

line_width = 1

def calendar_days_text(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    response = HttpResponse(content_type="text/plain")
    
    for date in sorted(days.keys()):
        line = "{date:}: {day:}\n".format(date=date.strftime("%Y-%m-%d"), day=days[date].letter)
        
        response.write(line)
    
    return response

def full_calendar_pdf(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    if "color" in request.GET:
        formatter = color_formatter
        color = True
    else:
        formatter = black_formatter
        color = False
        
    header_days = calendar.numeric_days
    
    structured_data = structured_calendar_layout(days)
    
    response = HttpResponse(content_type="application/pdf")
    
    pdf = canvas.Canvas(response, pagesize=(11*inch, 8.5*inch))
    
    pdf.setTitle("{title:}".format(title=calendar.title))
    
    for year, month in sorted(structured_data.keys()):
        grid = structured_data[(year, month)]
        
        first_of_month = date(year, month, 1)
        month_title = first_of_month.strftime("%B %Y")
        
        grid_drawer = GridDrawer(grid, header_days, formatter)
        
        if color:
            pdf.setFillColor(color_accent)
        else:
            pdf.setFillColor(colors.black)
            
        pdf.setFont("HelveticaNeue-Bold", 72)
        pdf.drawString(.5*inch, 7.25*inch, month_title)

        grid_drawer.draw_on(pdf, .5*inch, 7*inch, 10*inch, 6.5*inch, line_width)
        pdf.showPage()
        
        
        
    pdf.save()
    
    response['Content-Disposition'] = 'filename="{title:}.pdf"'.format(title=calendar.title)
    return response

def one_page_calendar(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    header_days = calendar.numeric_days
    
    structured_data = structured_calendar_layout(days)
    
    response = HttpResponse(content_type="application/pdf")
    
    pdf = canvas.Canvas(response, pagesize=(8.5*inch, 11*inch))
    pdf.setTitle("{title:}".format(title=calendar.title))
    
    cols = 2
    col_width = 7.5 * inch/cols
    
    rows = math.ceil(len(structured_data)/cols)
    row_height = 10*inch / rows
    
    inner_cell_height = (11 - 1) / rows * inch
    
    for i, (year, month) in enumerate(sorted(structured_data.keys())):
        col = i % cols
        row = math.floor(i/cols)
        
        x = .5 * inch + col * col_width
        y = 11*inch - (.5 * inch + row * row_height)
        
        grid = structured_data[(year, month)]
        
        first_of_month = date(year, month, 1)
        month_title = first_of_month.strftime("%B %Y")
        
        grid_drawer = GridDrawer(grid, header_days, black_formatter)
        
        pdf.setFont("HelveticaNeue-Bold", 12)
        pdf.setFillColor(colors.black)
        pdf.drawString(x+.25 * inch, y-6, month_title)

        grid_drawer.draw_on(pdf, x+.25*inch, y-.035*inch-6, col_width-.5*inch, row_height-.25*inch, .5)
    
    pdf.showPage()
    pdf.save()
    
    return response
    
    

def full_zip(request, id):
    calendar = get_object_or_404(Calendar, pk=id)
    days = get_days(calendar)
    
    header_days = calendar.numeric_days
    
    structured_data_unfilled = structured_calendar_layout(days)
    structured_data_filled = structured_calendar_layout(days, prefill_calendar=True, postfill_calendar=True)
    structured_data_prefilled = structured_calendar_layout(days, prefill_calendar=True, postfill_calendar=False)
    structured_data_postfilled = structured_calendar_layout(days, prefill_calendar=False, postfill_calendar=True)
    
    print (structured_data_unfilled)
    
    response = HttpResponse(content_type="application/zip")
    
    with ZipFile(response, mode='w', compression=ZIP_STORED) as zip_file:
        #Generate ALL the possibilities
        for formatter in (("Color", (color_formatter, color_accent)), ("Black", (black_formatter, colors.black))):
            for embed in ("Print", "Embed", "Embed without titles"):
                for full_grid in (("Fully filled", structured_data_filled), ("Month only", structured_data_unfilled), ("Month with prefill", structured_data_prefilled), ("Month with postfill", structured_data_postfilled)):
                    
                    structured_data = full_grid[1]
                    
                    for year, month in sorted(structured_data.keys()):
                        file_name = "{embed:}/{formatter:}/{grid:}/{year:}-{month:0>2}.pdf".format(
                            embed = embed, formatter=formatter[0], grid=full_grid[0],
                            year=year, month=month)
                    
                        out = BytesIO()
                        pdf = canvas.Canvas(out, pagesize=(11*inch, 8.5*inch))
                        
                        grid_formatter = formatter[1][0]
                        title_color = formatter[1][1]
                    
                        grid = structured_data[(year, month)]
        
                        first_of_month = date(year, month, 1)
                        month_title = first_of_month.strftime("%B %Y")
        
                        grid_drawer = GridDrawer(grid, header_days, grid_formatter)
                        
                        if embed == "Print":
                            pdf.setFillColor(title_color)
                            pdf.setFont("HelveticaNeue-Bold", 72)
                            pdf.drawString(.5*inch, 7.25*inch, month_title)
        
                            grid_drawer.draw_on(pdf, .5*inch, 7*inch, 10*inch, 6.5*inch, line_width)
                            pdf.showPage()
                            pdf.save()
                            
                        elif embed == "Embed":
                            pdf.setFillColor(title_color)
                            pdf.setFont("HelveticaNeue-Bold", 72)
                            pdf.drawString(1, 7.75*inch, month_title)
        
                            grid_drawer.draw_on(pdf, 0, 7.5*inch, 11*inch, 7.5*inch, line_width)
                            pdf.showPage()
                            pdf.save()
                        
                        elif embed == "Embed without titles":
                            grid_drawer.draw_on(pdf, 0, 8.5*inch, 11*inch, 8.5*inch, line_width)
                            pdf.showPage()
                            pdf.save()
                            
                        zip_file.writestr(file_name, out.getvalue())

    response['Content-Disposition'] = 'filename="{title:}.zip"'.format(title=calendar.title)
    return response
                    
                    