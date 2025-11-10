## Texascale CMS

https://texascale.org/

## Quick Start

1. Follow [Core CMS Template's "Start Project"][core-cms-template-start].
2. Create/Replace `/cms/src/taccsite_cms/settings_custom.py` with [Texascale Custom Settings].

## Documentation

> [!TIP]
> This project is built as a customization of a TACC <abbr title="Content Management System">CMS</abbr> website. To manage this project's CMS, reference [Core-CMS-Template Docs][core-cms-template-docs]. To develop this project's custom code, keep reading.

## Contributing

To contribute, first read [How to Contirbute][Contributing].

### Publish New Magazine Each Year

To publish a new year online:

1. In [Texascale Custom Settings], set `TEXASCALE_PUBLISHED_YEAR` to the current year.
2. [Deploy](https://tacc-main.atlassian.net/wiki/x/cwVv) that setting change.

> [!IMPORTANT]
> **If neglected**, then homepage[^1] might have **incorrect styles**.

[^1]: And other pages with no year in their path.

### Styles

Learn about [Texascale Stylesheets](./cms/src/taccsite_custom/texascale_cms/static/texascale_cms/css/README.md).

> [!IMPORTANT]
> If you change a `.postcss` file,  run **`npm run build`**.

### Blog/News Feature

This feature is [enabled](https://pprd.texascale.tacc.utexas.edu/testing/news/?edit) but **not** used.

<!-- Link Aliases -->

[Core CMS]: https://github.com/TACC/Core-CMS
[Core CMS Template]: https://github.com/TACC/Core-CMS-Template
[Core Portal Deployments]: https://github.com/TACC/Core-Portal-Deployments
[Texascale Custom Settings]: https://github.com/TACC/Core-Portal-Deployments/blob/main/texascale/camino/cms.settings_custom.py

[core-cms-template-setup]: https://github.com/TACC/Core-CMS-Template/blob/v0.3.1/docs/create-project.md#set-up-project
[core-cms-template-start]: https://github.com/TACC/Core-CMS-Template/blob/v0.3.1/docs/start-project.md#start-project
[core-cms-template-docs]: https://github.com/TACC/Core-CMS-Template/blob/v0.3.1/docs/README.md#tacc-custom-cms

[Contributing]: ./contributing.md
