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


@register.filter(name='custom_pagination')
def custom_pagination(range, args):
    current_page, total_pages = map(int, args.split(','))
    start = max(current_page - 2, 1)
    end = min(current_page + 2, total_pages)
    if start == 1:
        end = min(5, total_pages)
    if end == total_pages:
        start = max(total_pages - 4, 1)
    return range(start, end+1)

    

