# CUSTOM SETTINGS VALUES.
# TACC WMA (SAD) CMS SITE:
# *.TEXASCALE.TACC.UTEXAS.EDU

import os

from django.utils.translation import gettext_lazy as _

########################
# TEXASCALE
########################

TEXASCALE_PUBLISHED_YEAR = 2024

########################
# DJANGO
########################

from glob import glob

BASE_DIR = '/code'

# https://github.com/TACC/Core-CMS/blob/v4.35.0/taccsite_cms/settings.py#L39
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'taccsite_cms', 'static'),
    os.path.join(BASE_DIR, 'taccsite_custom', 'static'), # NEW
) + tuple(glob(
    # XXX: Strange and from my ignorant implementation
    os.path.join(BASE_DIR, 'taccsite_custom', '*', 'static')
))

########################
# DJANGO_CMS
########################

CMS_TEMPLATES = (
    ('texascale_cms/templates/standard.html', 'Standard'),
    ('texascale_cms/templates/fullwidth.html', 'Fullwidth'),
    ('texascale_cms/templates/category.html', 'Category'),
    ('texascale_cms/templates/article.html', 'Article'),
    ('texascale_cms/templates/article.freeform.html', 'Article (Free-Form)'),
    ('texascale_cms/templates/article.sidebar-right.html', 'Article (Right Sidebar)'),
    ('texascale_cms/templates/article.visual.html', 'Article (Full-Size Visual)'),
    ('texascale_cms/templates/article.image-map.html', 'Article (Image Map)'),
)

# IDEA: Suggest this for TACC/Core-CMS
CMS_PLACEHOLDER_CONF = {
    None: {
        'plugin_labels': {
            # Side effect of djangocms-transfer Import/Export
            'PluginImporter': 'PluginImporter (Unable to Hide This Utility)',
        },
    },
    'footer-content': {
        'name': 'Footer Content',
    },
    'global-assets': {
        'plugins': ['SnippetPlugin'],
        'name': 'Global Assets',
    },
}

########################
# TACC: LOGO & FAVICON
########################

PORTAL_LOGO = {
    "is_remote": False,
    "img_file_src": "texascale_cms/img/org_logos/texascale-wordmark.png",
    "img_class": "",  # additional class names
    "link_href": "/",
    "link_target": "_self",
    "img_alt_text": "Texascale Logo",
    "img_crossorigin": "anonymous",
}

########################
# TACC: PORTAL
########################

PORTAL_IS_TACC_CORE_PORTAL = False
PORTAL_HAS_LOGIN = False
PORTAL_HAS_SEARCH = False

########################
# TACC: CORE STYLES
########################

# Only use integer numbers (not "v1", not "0.11.0")
TACC_CORE_STYLES_VERSION = 2

########################
# TACC: SOCIAL MEDIA
########################

PORTAL_SOCIAL_SHARE_PLATFORMS = ['facebook', 'linkedin', 'email']

########################
# DJANGOCMS_BLOG
# (Unused but Available)
########################

# Paths for alternate templates that user can choose for blog-specific plugin
# - Devs can customize core templates at `templates/djangocms_blog/`.
# - Users can choose alt. templates from `templates/djangocms_blog/plugins/*`.
# - Devs can customize alt. templates at `templates/djangocms_blog/plugins/*`.
BLOG_PLUGIN_TEMPLATE_FOLDERS = (
    ('plugins', 'Default'),
    # ('plugins/alternate', 'Alternate'),
)

# Change default values for the auto-setup of one `BlogConfig`
# SEE: https://github.com/nephila/djangocms-blog/issues/629
BLOG_AUTO_SETUP = False # Set to False after setup (to minimize server overhead)
BLOG_AUTO_HOME_TITLE ='Home'
BLOG_AUTO_BLOG_TITLE = 'News'
BLOG_AUTO_APP_TITLE = 'News'
BLOG_AUTO_NAMESPACE = 'News'

# Miscellaneous settings
BLOG_ENABLE_COMMENTS = False

########################
# DJANGOCMS_BOOTSTRAP
# https://github.com/django-cms/djangocms-bootstrap4
########################

# # Add ".container-padded" to container options
# # TODO: Integrate into Core-CMS
# DJANGOCMS_BOOTSTRAP4_GRID_CONTAINERS = [
#     ('container', _('Container')),
#     ('container-fluid', _('Fluid container')),
#     ('container-padded', _('Padded container')),
#     ('_', _('None')),
# ]

# WARNING: Fails on deploy to remote server —
#          taccsite_cms._settings.djangocms_plugins
#          — not found
# Add ".container-padded" to container options
# TODO: Integrate into Core-CMS
def get_custom_grid_containers():
    from ._settings.djangocms_plugins import DJANGOCMS_BOOTSTRAP4_GRID_CONTAINERS as CONTAINERS

    fluid_container_index = CONTAINERS.index(('container-fluid', _('Fluid container')))
    padded_container_index = fluid_container_index + 1

    return [
        *CONTAINERS[:padded_container_index],
        ('container-padded', _('Padded container')),
        *CONTAINERS[padded_container_index:],
    ]

from django.utils.functional import lazy
DJANGOCMS_BOOTSTRAP4_GRID_CONTAINERS = lazy(get_custom_grid_containers, list)()

########################
# DJANGOCMS_ICON
# https://github.com/django-cms/djangocms-icon
########################

ICON_PATH = os.path.join('taccsite_cms', 'static', 'site_cms', 'img', 'icons')

LOGO_ICONFILE = os.path.join(BASE_DIR, ICON_PATH, 'logos.json')
with open(LOGO_ICONFILE, 'r') as f:
    LOGO_ICONS = f.read()

CORTAL_ICONFILE = os.path.join(BASE_DIR, ICON_PATH, 'cortal.json')
with open(CORTAL_ICONFILE, 'r') as f:
    CORTAL_ICONS = f.read()

TEXASCALE_ICONFILE = os.path.join(BASE_DIR, 'taccsite_custom', 'texascale_cms', 'static', 'texascale_cms', 'img', 'icons', 'texascale.json')
with open(TEXASCALE_ICONFILE, 'r') as f:
    TEXASCALE_ICONS = f.read()

DJANGOCMS_ICON_SETS = [
    # IMPORTANT: Sync properties & Order of sets matters
    # https://github.com/TACC/Core-CMS/pull/995
    (TEXASCALE_ICONS, '', _('Texascale Icons')),
    (LOGO_ICONS, '', _('Logo SVGs')),
    (CORTAL_ICONS, 'icon', _('TACC "Cortal" Icons')),
]
