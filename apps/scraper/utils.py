def set_field_html_name(cls, new_name):
    """
    Give custom name in html template
    :param cls:
    :param new_name:
    :return:
    """

    old_render = cls.widget.render

    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    cls.widget.render = _widget_render_wrapper
