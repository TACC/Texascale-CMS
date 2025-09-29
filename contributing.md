# Contributing

## Linting and Formatting

Not standardized. Read [(internal) Formatting & Linting](https://tacc-main.atlassian.net/wiki/x/VwNv).

## Best Practices

- [Sign your commits.](https://help.github.com/en/github/authenticating-to-github/managing-commit-signature-verification)
- [Learn Markdown.](https://bitbucket.org/tutorials/markdowndemo)

## Development Workflow

We use a modifed version of [GitFlow](https://datasift.github.io/gitflow/IntroducingGitFlow.html).

- "feature branches" have a specific prefix:
  - `feat/` for features and updates
  - `fix/` for bugfixes and hotfixes
  - `refactor/` for large internal changes
  - `chore/` for no-op changes
  - `docs/` for documentation
  - `perf/` for performance improvements
  - `test/` for test case updates
  - or other "types" from [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- "develop" branch is usually `main`,\
    <sup>but can exist as a long-lived multi-feature branch prefixed with `dev/`</sup>
- "release branches" (as needed) are prefixed with `release/`
- "hotfix branches" are prefixed `fix/`
- "master branch" is always `main`

Our [development site] is always up-to-date with `main` branch.

> **Note**
> The [development site] is only accessible behind the TACC Network.

Our [production site] is built from a specific commit.

## Release Workflow

Only appointed team members may release versions.

0. Navigate to `cms/` dir:\
    `cd cms/`
1. Update version:\
    `npm version vN.N.N`
2. Build styles:\
    `npm run build`
3. Review. Commit. Push.
4. Create release and tag, `vN.N.N` on GitHub.
5. [Build project](https://github.com/TACC/Texascale-CMS/actions/workflows/build.yml) tag `vN.N.N`.

## Build Project

Follow [Core CMS: Build & Deploy Project](https://github.com/TACC/Core-CMS#build--deploy-project).

## Deploy Project

Follow "Deploy" section of [How To Build & Deploy][Deploy Project].

[^1]: So that new CMS image is tagged `latest` and `vN.N.N`.

<!-- Link Aliases -->

[development site]: https://dev.cep.tacc.utexas.edu
[production site]: https://prod.cep.tacc.utexas.edu
