CUSTOM_APPS = [

    # TEXASCALE
    # Auto-loaded because `taccsite_custom/*/` dirs are assumed to be apps
    # https://github.com/TACC/Core-CMS/blob/v4.36.1/taccsite_cms/settings.py#L522-L524
    # 'taccsite_custom.taccsite_bootstrap4_tabs.apps.TaccsiteBootstrap4TabsConfig',
    # 'taccsite_custom.taccsite_style.apps.TaccsiteStyleConfig

    # DJANGOCMS_BLOG
    'parler',
    'taggit',
    'taggit_autosuggest',
    'sortedm2m',
    'djangocms_blog',

]

CUSTOM_MIDDLEWARE = []
STATICFILES_DIRS = ()
