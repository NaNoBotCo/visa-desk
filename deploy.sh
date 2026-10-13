#!/bin/sh
# Publish chiangmaivisadesk.com: the site Worker (site/ as assets) and, with
# "worker", the intake Worker at api.chiangmaivisadesk.com.
# A merge to main does this on its own from motdang-server within ~5 minutes.
set -e
cd "$(dirname "$0")"
npx wrangler deploy
[ "${1:-}" = worker ] && (cd worker && npx wrangler deploy)
