#!/usr/bin/env node

/** Build CSS using the Core-Styles API */

const buildStylesheets = require('@tacc/core-styles').buildStylesheets;
const minimist = require('minimist');
const gitDescribe = require('./git-describe');

const ROOT = __dirname + '/..';
const ARGS = minimist( process.argv.slice( 2 ) );
const BUILD_ID = ARGS['build-id'] || gitDescribe();

/** Build stylesheets */
(() => {
  const stylePath = 'src/taccsite_custom/texascale_cms/static/texascale_cms/css';
  const options = {
    verbose: _shouldBeVerbose(),
    buildId: BUILD_ID,
    fileExt: '.min.css',
    // If custom configuration is desired, then create and pass this file
    // customConfigs: [`${ROOT}/.postcssrc.extra.yml`],
  }

  // Build styles
  buildStylesheets(
    `${ROOT}/${stylePath}/legacy/*.postcss`,
    `${ROOT}/${stylePath}/legacy`,
    options
  );
  buildStylesheets(
    `${ROOT}/${stylePath}/2025/*.postcss`,
    `${ROOT}/${stylePath}/2025`,
    options
  );
})();

/**
 * Whether to log verbose output
 * @return {boolean}
 */
function _shouldBeVerbose() {
  const supressionFlags = ['quiet', 'silent', 'no-verbose'];
  const hasSupressionFlag = supressionFlags.some(flag => ARGS[flag]);

  return !hasSupressionFlag;
}
