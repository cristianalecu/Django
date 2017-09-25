import re
from django.template import Library, Node
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)

@register.simple_tag
def get_verbose_object_field_name(instance, field_name):
    """
    Returns verbose_name for an object field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@register.simple_tag
def get_verbose_field_name(objs, field_name):
    """
    Returns verbose_name for a field.
    """
    for instance in objs.model._meta.fields :
        if instance.name == field_name:
            return instance.verbose_name
    return field_name
   
class PdbNode(Node):

    def render(self, context):
        for v in context.dicts:
            if 'obj' in v.keys(): 
                x = v['obj']
                for a in x._meta.concrete_fields:
                    if a.attname == 'id':
                        return a._verbose_name
        return ''

@register.tag
def pdb(parser, token):
    return PdbNode()
