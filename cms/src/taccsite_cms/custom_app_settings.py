# import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CUSTOM_APPS = [

    # TEXASCALE_CUSTOM
    # !!!: Independent app to customize site cuz texascale_cms did not let me
    'texascale_custom.apps.TexascaleCustomConfig',

    # DJANGOCMS_BLOG
    'parler',
    'taggit',
    'taggit_autosuggest',
    'sortedm2m',
    'djangocms_blog',

]

CUSTOM_MIDDLEWARE = []

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'texascale_custom', 'static'),
# )
