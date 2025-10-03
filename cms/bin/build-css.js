#!/usr/bin/env node

const buildStylesheets = require('@tacc/core-styles').buildStylesheets;

const ROOT = __dirname + '/../';
const BUILD_ID = process.env.BUILD_ID || process.env.npm_package_version;
const ASSET_PATH = ROOT + 'src/taccsite_custom/texascale_cms/static/texascale_cms/';

const argv = process.argv.slice(2);

const supportedVerboseFlags = [
  '--quiet', '--silent', '--no-verbose'
];
const hasVerboseFlag = argv.some(flag => supportedVerboseFlags.includes(flag));
const verbose = (!hasVerboseFlag);

const options = {
  verbose,
  fileExt: '.min.css',
  buildId: BUILD_ID,
  // If custom configuration is desired, then create and pass this file
  // customConfigs: [`${ROOT}/.postcssrc.extra.yml`],
};

buildStylesheets(
  `${ASSET_PATH}css/legacy/*.postcss`,
  `${ASSET_PATH}css/legacy`,
  options
);
buildStylesheets(
  `${ASSET_PATH}css/2025/*.postcss`,
  `${ASSET_PATH}css/2025`,
  options
);
