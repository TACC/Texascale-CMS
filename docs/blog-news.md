# Texascale - Blog/News

This feature, though [enabled](https://pprd.texascale.tacc.utexas.edu/testing/news/?edit), is **not** used because sole content editor has more freedom using regular pages. It is retained solely to rapidly begin to support possibility of story writers themselves becoming editors.

## To Customize

### Styles

To customize Blog/News styles per year, create a `/cms/src/taccsite_cms/templates/djangocms_blog/base.html` and override `{% block assets_app %}` similar to how `cms/src/taccsite_custom/texascale_cms/templates/base.html` overrides `{% block assets %}`.

### Markup

To customize Blog/News markup, follow [djangocms-blog: Templates](https://github.com/nephila/djangocms-blog/blob/1.2.3/docs/features/templates.rst).
