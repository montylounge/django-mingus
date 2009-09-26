from django.db.models import get_model
from django.template import Node, TemplateSyntaxError, Library, Variable
from django.utils.translation import ugettext as _
from tagging.models import TaggedItem
register = Library()

class TaggedGetRelatedNode(Node):
    def __init__(self, obj, queryset_or_model, context_var, **kwargs):
        self.obj = Variable(obj)
        self.queryset_or_model = queryset_or_model
        self.context_var = context_var
        self.kwargs = kwargs

    def render(self, context):
        try:
            param = get_model(*self.queryset_or_model.split('.'))
        except:
            param = Variable(self.queryset_or_model).resolve(context)

        if param is None:
            raise TemplateSyntaxError(_('tagged_get_related tag was given an invalid input: %s') % self.queryset_or_model)

        context[self.context_var] = TaggedItem.objects.get_related(self.obj.resolve(context), param, **self.kwargs)
        return ''


@register.tag
def tagged_get_related(parser, token):
    """
    {% tagged_get_related [obj] in ([appname]).[queryset_or_model] as [varname] with num=10 %}
    """
    kwargs = {}
    bits = token.contents.split()
    if len(bits) != 6 and len(bits) != 8:
        raise TemplateSyntaxError(_('%s tag requires either five or seven arguments') % bits[0])
    if bits[2] != 'in':
        raise TemplateSyntaxError(_("second argument to %s tag must be 'in'") % bits[0])
    if bits[4] != 'as':
        raise TemplateSyntaxError(_("fourth argument to %s tag must be 'as'") % bits[0])
    if len(bits) == 8:
        if bits[6] != 'with':
            raise TemplateSyntaxError(_("if given, fourth argument to %s tag must be 'with'") % bits[0])
        try:
            name, value = bits[7].split('=')
            if name == 'num':
                try:
                    kwargs[str(name)] = int(value)
                except ValueError:
                    raise TemplateSyntaxError(_("%(tag)s tag's '%(option)s' option was not a valid integer: '%(value)s'") % {
                        'tag': bits[0],
                        'option': name,
                        'value': value,
                    })
            else:
                raise TemplateSyntaxError(_("%(tag)s tag was given an invalid option: '%(option)s'") % {
                    'tag': bits[0],
                    'option': name,
                })
        except ValueError:
            raise TemplateSyntaxError(_("%(tag)s tag was given a badly formatted option: '%(option)s'") % {
                'tag': bits[0],
                'option': bits[i],
            })

    return TaggedGetRelatedNode(bits[1], bits[3], bits[5], **kwargs)

