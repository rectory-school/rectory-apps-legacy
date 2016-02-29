import xml.etree.ElementTree as ET

from datetime import date
from decimal import Decimal

import logging
import warnings
import dateparser

log = logging.getLogger(__name__)

NAMESPACES = {
    'fmpxmlresult': 'http://www.filemaker.com/fmpxmlresult'
}

PARSE_MODE_ABSOLUTE = 0
PARSE_MODE_RELATIVE = 1

def parse_from_file(f):
    tree = ET.parse(f)
    root = tree.getroot()
    
    return parse_from_root(root)

def parse_from_string(s):
    root = ET.fromstring(s)
    
    return parse_from_root(root)
    
def parse_from_root(root):
    data = {}
    
    database_node = root.find('fmpxmlresult:DATABASE', NAMESPACES)
    
    data['ERRORCODE'] = root.find('fmpxmlresult:ERRORCODE', NAMESPACES).text
    data['PRODUCT'] = root.find('fmpxmlresult:PRODUCT', NAMESPACES).attrib
    
    data['DATABASE'] = database_node.attrib

    date_parser = get_date_parser(database_node.attrib['DATEFORMAT']).parse_date
    
    field_map = []
    
    metadata_node = root.find('fmpxmlresult:METADATA', NAMESPACES)
    fields = metadata_node.findall('fmpxmlresult:FIELD', NAMESPACES)
    
    converter_map = {
        'TEXT': str.strip,
        'NUMBER': Decimal,
        'DATE': date_parser,
        'TIME': lambda c: None,
        'TIMESTAMP': lambda c: None,
        'CONTAINER': lambda c: None
    }
    
    for field in fields:
        field_name = field.attrib['NAME']
        field_type = field.attrib['TYPE']
        converter = converter_map[field_type]
        
        field_map.append({'name': field_name, 'type': field_type, 'converter': converter})
        
    resultset_node = root.find('fmpxmlresult:RESULTSET', NAMESPACES)
    rows = resultset_node.findall('fmpxmlresult:ROW', NAMESPACES)
    
    data['results'] = []
    
    for row in rows:
        data_row = {'RECORDID': row.attrib["RECORDID"], 'fields': {}, 'parsed_fields': {}}
        
        for i, col_node in enumerate(row.findall('fmpxmlresult:COL', NAMESPACES)):
            
            try:
                value = col_node.find('fmpxmlresult:DATA', NAMESPACES).text
            except AttributeError:
                value = None
                
            field = field_map[i]
            
            col_name = field["name"]
            col_type = field["type"]
            
            converter = field['converter']
            converted_value = value and converter(value) or None
            
            result_row = {'name': col_name, 'type': col_type, 'original_value': value, 'converted_value': converted_value}
            data_row['fields'][col_name] = result_row
            
            data_row['parsed_fields'][col_name] = converted_value
            
        data['results'].append(data_row)
    
    return(data)


def get_date_parser(date_format):
    if date_format == "yyyy-mm-dd":
        return ISO8601DateParser()
    
    if "mm" in date_format and "dd" in date_format:
        return FilemakerAbsoluteDateParser(date_format)
    
    else:
        return FilemakerFuzzyDateParser(date_format)

class ISO8601DateParser(object):
    def parse_date(self, s):
        year, month, day = [int(part) for part in s.split("-")]
        return date(year, month, day)
        

class FilemakerAbsoluteDateParser(object):
    def __init__(self, date_format):
        for attr in ("yy", "mm", "dd"):
            if attr not in date_format:
                raise ParameterNotFoundException(attr)
                
        self.date_format = date_format
        
        if "yyyy" in date_format:
            self.year_start = date_format.find("yyyy")
            self.year_length = 4
        else:
            self.year_start = date_format.find("yy")
            self.year_length = 2
        
        self.month_start = date_format.find("mm")
        self.day_start = date_format.find("dd")
    
    def parse_date(self, s):
        year = int(s[self.year_start:self.year_start + self.year_length])
        if self.year_length == 2:
            year = year + 2000
            
        month = int(s[self.month_start:self.month_start+2])
        day = int(s[self.day_start:self.day_start+2])
        
        return date(year, month, day)

class FilemakerFuzzyDateParser(object):
    @staticmethod
    def change_one_time(s, changes):
        for change_from, change_to in changes:
            if change_from in s:
                return s.replace(change_from, change_to)
        
        return s
            
    def __init__(self, date_format):
        #Mangle the Filemaker date format into a Python date format
        change_groups = [
            [
                ("yyyy", "%y"),
                ("yy", "%y"),
            ],
            [
                ("mm", "%m"),
                ("M", "%m"),
            ],
            [
                ("dd", "%d"),
                ("d", "%d")
            ]
        ]
        
        converted_date_format = date_format
        
        for change_group in change_groups:
            converted_date_format = self.change_one_time(converted_date_format, change_group)
        
        if not "%y" in converted_date_format:
            raise ParameterNotFoundException("yyyy")
        
        if not "%m" in converted_date_format:
            raise ParameterNotFoundException("mm")
        
        if not "%d" in converted_date_format:
            raise ParameterNotFound("dd")
        
        self.parse_date_format = converted_date_format
        self.date_format = date_format
    
    def parse_date(self, s):
        dt = dateparser.parse(s, date_formats=[self.parse_date_format])
        return date(dt.year, dt.month, dt.day)
        
class ParameterNotFoundException(Exception):
    def __init__(self, parameter, *args, **kwargs):
        super(ParameterNotFoundException, self).__init__(self, *args, **kwargs)
        self.parameter = parameter
    
    def __str__(self):
        return "Parameter {parameter:} was not found".format(parameter=self.parameter)
        
class ShortDateWarning(Warning):
    pass