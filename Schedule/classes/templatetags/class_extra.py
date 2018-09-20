from django import template                                                                                                              
from django.conf import settings                                                                                                         
import uuid
register = template.Library()                                                                                                            

@register.simple_tag(name='cache_bust')                                                                                                  
def cache_bust():                                                                                                                        

    if settings.DEBUG:                                                                                                                   
        version = uuid.uuid4()                                                                                                           
    else:                                                                                                                                
        version = os.environ.get('PROJECT_VERSION')                                                                                       
        if version is None:                                                                                                              
            version = '1'                                                                                                                

    return '__v__={version}'.format(version=version)

def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)

class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return ''

    def decrement(self):
        self.count -= 1
        return ''

    def double(self):
        self.count *= 2
        return ''