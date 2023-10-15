from django import template
import re

register = template.Library()

@register.filter
def first_half(value):
    
    length = len(value)
    
    first_half_text = value[:length // 2]
   
    lines = first_half_text.splitlines()
    
    first_two_lines = '\n'.join(lines[:2])

    first_two_lines = first_two_lines[: len(first_two_lines)//2]
    return first_two_lines
