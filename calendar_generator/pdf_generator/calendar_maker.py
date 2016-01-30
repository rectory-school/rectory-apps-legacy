from datetime import date, timedelta
import calendar
import os
import math

from copy import copy, deepcopy

from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

myFolder = os.path.dirname(os.path.realpath(__file__))
fontFolder = os.path.join(myFolder, "fonts")

for fontFile in os.listdir(fontFolder):
    fontName, extension = os.path.splitext(fontFile)
    if (extension) == ".ttf":
        pdfmetrics.registerFont(TTFont(fontName, os.path.join(fontFolder, fontFile)))

HEADERMAPPING = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

class GridFormatter(object):
    AVAILABLE_ARGS = {
        'grid_day_color': colors.black,
        'line_color': colors.black,
        'header_color': colors.black,
        'day_color': colors.black,
        'date_color': colors.black,
        'header_line_color': colors.black,
        'header_background': None,
        'day_background': None,
    }
    
    def __init__(self, header_font, day_font, date_font, **kwargs):
        self.header_font = header_font
        self.day_font = day_font
        self.date_font = date_font
        
        for kwarg in self.AVAILABLE_ARGS:
            val = kwargs.get(kwarg, self.AVAILABLE_ARGS[kwarg])
            setattr(self, kwarg, val)
            
class GridDrawer(object):
    def __init__(self, grid, days, formatter):
        self.days = days
        self.formatter = formatter
        
        self.grid = []
        
        #Strip the grid of things we don't want to process
        for week in grid:
            #Throw out and days we don't consider
            week = [week[day] for day in self.days]
            
            #If the week isn't crap, add it to the grid
            if not week == [None] * len(self.days):
                self.grid.append(week)
        
    def draw_on(self, canvas, grid_x, grid_y, grid_width, grid_height, line_width):
        cell_width = grid_width / len(self.days)
        
        running_y = grid_y
        
        header_font_size = self.header_font_size(cell_width * .8)
        header_height = header_font_size * 1.5
        
        row_count = len(self.grid)
        
        #Always plan for at least 5 rows, with 6 being a very special case
        cell_height = (grid_height - header_height) / max(5, row_count)

        day_font_size = cell_height
        date_font_size = cell_height * .35
        
        canvas.setLineWidth(line_width)
        
        running_y -= header_height
        
        #Frame
        canvas.setStrokeColor(self.formatter.line_color)
        canvas.rect(grid_x + line_width/2, grid_y+line_width/2-grid_height, grid_width-line_width, grid_height-line_width)
        
        #Header
        #Header background
        if self.formatter.header_background:
            fill=1
            canvas.setFillColor(self.formatter.header_background)
        else:
            fill=0
        
        canvas.setStrokeColor(self.formatter.line_color)
        canvas.rect(grid_x+line_width/2, grid_y-header_height+line_width/2, grid_width-line_width, header_height-line_width, stroke=1, fill=fill)
        
        #Header text
        canvas.setFont(self.formatter.header_font, header_font_size)
        canvas.setFillColor(self.formatter.header_color)
        
        for i in range(len(self.days)):
            cell_x = grid_x + i * cell_width
            cell_mid = cell_x + cell_width / 2
            
            #Monday, Tuesday, etc
            canvas.drawCentredString(cell_mid, grid_y - header_height * .75, HEADERMAPPING[self.days[i]])
        
        #Lines between Monday, Tuesday, etc
        if self.formatter.header_line_color:
            canvas.setStrokeColor(self.formatter.header_line_color)
           
            for i in range(1, len(self.days)):
                #The stroke width of the header rectangle has to be accounted for
                cell_x = grid_x + i * cell_width
                canvas.line(cell_x, grid_y-line_width, cell_x, grid_y - header_height+line_width)
        
        #Inner lines
        canvas.setStrokeColor(self.formatter.line_color)
        
        #Week lines
        for i in range(row_count-1):
            y = grid_y - header_height - (i+1) * cell_height
            canvas.line(grid_x, y, grid_x + grid_width, y)
        
        #Day lines
        for i in range(len(self.days)-1):
            x = grid_x + cell_width * (i+1)
            canvas.line(x, grid_y-header_height + line_width/2, x, grid_y-grid_height)
                
        #Weeks
        for week in self.grid:
            running_y -= cell_height
                        
            for i, day_data in enumerate(week):
                cell_x = grid_x + i * cell_width
                cell_right = cell_x + cell_width
                
                date_right = cell_right - cell_width*.05
                
                if not day_data:
                    continue
                    
                date, day = day_data
                
                #Date
                canvas.setFillColor(self.formatter.date_color)
                canvas.setFont(self.formatter.date_font, date_font_size)
                canvas.drawRightString(date_right, running_y + cell_height - date_font_size, str(date.day))

                #Day letter                
                if day:
                    canvas.setFillColor(self.formatter.day_color)
                    canvas.setFont(self.formatter.day_font, day_font_size)
                    canvas.drawString(cell_x + cell_width*.1, running_y + cell_height *.15 , day.letter)
        

        
        
    def header_font_size(self, maximum_width):
        day_headers = [HEADERMAPPING[day] for day in self.days]
        
        return int(min([self.individual_header_font_size(header, maximum_width) for header in day_headers]))
        
    def individual_header_font_size(self, header, maximum_width):
        font_size = maximum_width
        
        width = stringWidth(header, self.formatter.header_font, font_size)
                
        while width > maximum_width:
            font_size -= 1
            width = stringWidth(header, self.formatter.header_font, font_size)
        
        return font_size