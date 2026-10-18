# Contributing

Thanks for helping improve SearXNG Railway. Keep changes focused, reproducible, and safe for a private internal deployment.

## Before opening a pull request

1. Explain the problem and expected behavior.
2. Keep secrets, tokens, credentials, private queries, and deployment logs out of commits and screenshots.
3. Update both README.md and README.en.md when user-facing behavior changes.
4. Update docs/SOURCES.md when adding upstream dependencies, configuration assumptions, or third-party assets.
5. State clearly whether a change was statically validated or tested on a live Railway deployment.

## Local checks

Run from the repository root:

```sh
python3 scripts/validate_repo.py
python3 scripts/check_docs.py
sh -n scripts/generate-secret.sh
```

These checks require no external Python packages. They validate repository consistency, not a live SearXNG instance or n8n workflow.

## Pull request checklist

- [ ] Deployment steps match the actual files and configuration.
- [ ] Both README language versions are updated where appropriate.
- [ ] Local links, heading anchors, and SVG assets validate.
- [ ] No active secrets or personal data are included.
- [ ] License and attribution notes are updated if applicable.
- [ ] Live deployment testing is reported accurately.
