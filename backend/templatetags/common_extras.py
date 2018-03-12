from django import template
from django.utils.safestring import mark_safe
from apps.contacts.models import SocialLinksModel
from apps.news.models import News
from apps.contacts.models import ContactFooter
from apps.settings.models import Setting

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


@register.simple_tag
def last_news():
    return News.objects.published().order_by('-created_at')[:3]


@register.simple_tag
def contacts_footer():
    return ContactFooter.objects.filter(is_enabled=True).all()


@register.inclusion_tag('disqus_comments.html', takes_context=True)
def comments_widget(context, identifier, identifier_id):
    """Виджет комментариев Disqus."""
    return {
        'is_secure': context['request'].is_secure(),
        'host': context['request'].get_host(),
        'full_path': context['request'].get_full_path(),
        'identifier': identifier,
        'identifier_id': identifier_id
    }


@register.simple_tag
def get_setting(key):
    """Возвращает значение настройки."""
    setting = Setting.objects.filter(key=key).first()
    if setting:
        return mark_safe(setting.value)
    return ''
