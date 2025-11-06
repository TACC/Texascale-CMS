from django.urls import path, re_path, include

custom_urls = [

    # DJANGO
    # To allow CMS user to change or reset password
    # TODO: Make CMS-only Portal Use TAPIs Auth & Do Not Do This
    path('accounts/', include('django.contrib.auth.urls')),

    # To support `taggit_autosuggest` (from `djangocms-blog`)
    re_path(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
]
