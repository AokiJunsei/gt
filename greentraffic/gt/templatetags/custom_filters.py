from django import template
register = template.Library()

@register.filter(name='attr')
def add_attribute(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d.strip()
        else:
            key, val = d.split(':')
            attrs[key.strip()] = val.strip()

    return field.as_widget(attrs=attrs)
