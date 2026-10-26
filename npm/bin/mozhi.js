#!/usr/bin/env node
/*
 * Mozhi interpreter launcher (npm distribution).
 *
 * The official prebuilt interpreter binaries ship inside this package
 * under bin/. This launcher picks the right one for the current
 * platform and hands over the process — arguments, stdio, exit codes
 * and signals all pass through, so `mozhi` behaves exactly like a
 * native binary.
 *
 * Bundled (v3.1.1, fully static musl builds with SQLite vendored):
 *   bin/mozhi-linux-x86_64
 *   bin/mozhi-linux-arm64
 *
 * macOS / Windows / other platforms:
 *   see https://github.com/crossberry-in/mozhi-doc#installation
 */
'use strict';

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// npm's process.arch uses "x64"; our asset naming uses "x86_64".
const arch = process.arch === 'x64' ? 'x86_64' : process.arch;
const bin = path.join(__dirname, 'mozhi-' + process.platform + '-' + arch);

if (!fs.existsSync(bin)) {
  console.error('[mozhi] No bundled interpreter for ' + process.platform + '-' + process.arch + '.');
  console.error('[mozhi] This package ships official v3.1.1 binaries for:');
  console.error('[mozhi]   linux-x86_64, linux-arm64 (fully static — works on glibc, Alpine, Termux)');
  console.error('[mozhi] For macOS, Windows and other platforms use the installer:');
  console.error('[mozhi]   curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash');
  process.exit(1);
}

const child = spawn(bin, process.argv.slice(2), { stdio: 'inherit' });

child.on('error', (err) => {
  console.error('[mozhi] Failed to start interpreter: ' + err.message);
  process.exit(1);
});

child.on('exit', (code, signal) => {
  if (signal) {
    // propagate fatal signals (SIGINT/SIGTERM...) with the correct exit status
    process.kill(process.pid, signal);
  } else {
    process.exit(code === null ? 0 : code);
  }
});
