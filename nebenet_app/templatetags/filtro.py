from django import template

register = template.Library()

@register.filter
def tiene_rol_o_grupo(user):
    return user.groups.filter(name='dependiente').exists() or user.is_staff
