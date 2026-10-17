#!/usr/bin/env sh
set -eu
if command -v openssl >/dev/null 2>&1; then
  openssl rand -hex 32
else
  printf '%s\n' 'Install OpenSSL or use scripts/generate-secret.ps1 on Windows.' >&2
  exit 1
fi
