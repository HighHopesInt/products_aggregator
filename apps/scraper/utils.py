def set_field_html_name(cls, new_name):
    """
    This function set name of field in generate html-code.
    Use it if you want special name for you html-element 
    which generates django.

    cls: name of object in forms of Django
    new_name: name which you want set for cls
    """
    old_render = cls.widget.render

    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    cls.widget.render = _widget_render_wrapper
