from django import template

register = template.Library()


@register.filter
def duration(td):
    if td:
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return '{} час. {} мин.'.format(hours, minutes)
    return ''


@register.filter
def in_list(value, the_list):
    value = str(value)
    return value in the_list.split(',')
