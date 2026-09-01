from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    """
        function to transform query to make sure that
        search and filter queries work with pagination
    """
    updated = request.GET.copy()
    for key, value in kwargs.items():
        if value is not None:
            updated[key] = value
        else:
            updated.pop(key, 0)

    return updated.urlencode()
