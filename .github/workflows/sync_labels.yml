name: Sync Labels

on:
  workflow_dispatch:

permissions:
  issues: write

jobs:
  sync:
    name: Run EndBug/label-sync
    runs-on: ubuntu-latest
    steps:
      - uses: EndBug/label-sync@v2
        with:
          config-file: 'https://raw.githubusercontent.com/TACC/Core-CMS/main/.github/labels_basic.yml'
          delete-other-labels: true
