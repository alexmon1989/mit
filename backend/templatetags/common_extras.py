from django import template
from apps.contacts.models import SocialLinksModel

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


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def social_links():
    return SocialLinksModel.objects.first()
