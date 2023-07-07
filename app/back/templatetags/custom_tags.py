from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='user_in_group')
def user_in_group(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
    
@register.filter(name='user_in_colaboradores_group')
def user_in_colaboradores_group(user):
    return user.groups.filter(name='colaboradores').exists()