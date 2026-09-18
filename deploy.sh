#!/bin/sh
# Publish site/ to Cloudflare Pages.
# First run: wrangler pages project create visa-desk
set -e
cd "$(dirname "$0")"
npx wrangler pages deploy site --project-name="${1:-visa-desk}"
