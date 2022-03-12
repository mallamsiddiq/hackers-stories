from django import template

register = template.Library()

@register.filter()
def to_int(value):
    return int(value)


@register.filter()
def tem_check_len(value):
	if type(value)==list:
		return 0 if value[0]=='' else len(value)
	else:
		return len(value)