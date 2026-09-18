# Contributing

Issues and pull requests are welcome. There is no build step and no test
framework to install.

```sh
make dev      # http://localhost:4173
make check    # run before opening a pull request
```

## What fits here

- Accessibility, performance, and anything that helps assistants answer
  accurately from the page.
- Structured data, `llms.txt` and crawler behaviour.
- Making the template easier to clone: fewer hardcoded strings, better
  `tools/brand.py` coverage, more useful checks.
- Translations, as sibling directories with their own `hreflang` links.

## What does not

- Statements of immigration law, in any country. This template deliberately
  carries none, and a clone that adds them takes on the job of keeping them
  current at the moment someone is relying on them to cross a border.
- Analytics, tracking pixels or third-party scripts. The pages load nothing
  from another host; a pull request that adds one needs to say why in the
  description.
- Published prices in the template itself. Your own clone is yours.

## Style

Two-space indent in HTML and CSS, four in Python. Keep the copy short and in
the present tense. No framework, no dependency that has to be installed before
`site/index.html` will open.
