# Texascale - Stylesheets

## Table of Contents

- [How to Load Stylesheets](#how-to-load-stylesheets)
- [When to Build Stylesheets](#when-to-build-stylesheets)
- [How to Build Stylesheets](#how-to-build-stylesheets)

## How to Load Stylesheets

### Global, via [Core Portal Deployments]

> [!TIP]
> This is the preferred method.

1. Add your new styles to a new or existing stylesheet.
2. Import your styles:
    - **Either** `@import` into `site.css`/`cms.css`.[^1]
    - **Or** add another entry [`PORTAL_STYLES` in Texascale's CMS settings to load from a CDN][PORTAL_STYLES].[^2]

[^1]: For most styles.
[^2]: For unique styles independent of CMS body e.g. for the header.

#### Styles per Page, Page Template, or Content

Scope global styles.

| Scope to What | How to Scope | Requirement |
| - | - | - |
| one page | `#page-___` | set page "Id" in Django CMS admin[^1] |
| all pages using a specific template | `[data-page-template="___"]` |
| specific content | `.___` or `#___` | set attribtue on block in page Structure |

[^1]: [Rendered as `<html>`'s `id` attribute.](https://github.com/TACC/Core-CMS/blob/v4.34.0/taccsite_cms/templates/base.html#L5)

### Ad-Hoc via a [Snippet][djangocms-snippet]

> [!WARNING]
> Do this **only** during development. Styles cannot be as well versioned controlled via a snippet.

Via the CMS, add a snippet that links the stylesheet from a CDN e.g. `<link id="css-___" rel="stylesheet" href="https://cdn.jsdelivr.net/gh/TACC/Texascale-CMS@123...ABC/texascale_cms/css/___.css" />`.

## When to Build Stylesheets

- If you change `.postcss` files.

## How to Build Stylesheets

1. Install dependencies.

    > [!NOTE]
    > Only necessary for initial clone **or** relevant Node package changes.

    ```sh
    npm ci
    ```

2. Build styles.

    ```sh
    npm run build
    ```

3. Check/Update stylehseets imported from a CDN.

    Examples:
    - [CMS setting `PORTAL_STYLES`][PORTAL_STYLES]
    - inside a [snippet](#ad-hoc-via-a-snippet)

    Reminders:
    - If URL is pinned to a commit hash, use new hash.
    - If URL is pinned to branch, test stylesheet has expected changes.
    - If stylehseet does not have expected changes, use a commit hash.

<!-- Link Aliases -->

[Core CMS]: https://github.com/TACC/Core-CMS
[Core Styles]: https://github.com/TACC/Core-Styles
[Core Portal Deployments]: https://github.com/TACC/Core-Portal-Deployments/blob/main/texascale/camino/cms.settings_custom.py

[PORTAL_STYLES]: https://github.com/TACC/Core-Portal-Deployments/blob/e7d2496/texascale/camino/cms.settings_custom.py#L57

[PostCSS]: https://postcss.org/
[djangocms-snippet]: https://github.com/django-cms/djangocms-snippet
