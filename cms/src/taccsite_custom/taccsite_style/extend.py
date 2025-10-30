def extendStylePlugin():
    from djangocms_style.models import Style

    attributes_field = Style._meta.get_field('attributes')

    if hasattr(attributes_field, 'excluded_keys'):
        if 'style' in attributes_field.excluded_keys:
            attributes_field.excluded_keys.remove('style')
