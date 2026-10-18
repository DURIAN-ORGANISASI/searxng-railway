# Sources, attribution, and licensing

This repository is a Railway deployment template built around the upstream SearXNG container. The references below document behavior and license scope; they do not imply endorsement.

## SearXNG upstream

- [SearXNG source repository](https://github.com/searxng/searxng) — source code, releases, configuration, and issue tracker.
- [SearXNG license](https://github.com/searxng/searxng/blob/master/LICENSE) — GNU Affero General Public License, version 3 (AGPL-3.0).
- [Official Docker installation guide](https://docs.searxng.org/admin/installation-docker.html) — container installation and configuration.
- [Official settings reference](https://docs.searxng.org/admin/settings/settings.html) — supported settings and defaults.
- [Official Search API reference](https://docs.searxng.org/dev/search_api.html) — search endpoint, parameters, and response formats.
- [Official container image](https://hub.docker.com/r/searxng/searxng) — upstream image and tags.

The Dockerfile uses searxng/searxng:latest and copies this repository's settings.yml into the container. The upstream image is not republished by this project. Since latest is mutable, separate builds can use different upstream versions; production deployments should pin and test a known tag or digest.

## Platforms and integration

- [Railway private networking](https://docs.railway.com/networking/private-networking) — private service discovery and environment-scoped connectivity.
- [Railway health checks](https://docs.railway.com/guides/healthchecks) — health-check configuration.
- [n8n SearXNG node](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.toolsearxng/) — native node and credential setup.
- [n8n documentation](https://docs.n8n.io/) — workflow platform documentation.

The example hostname searxng.railway.internal assumes the Railway service is named searxng. If you rename the service, update the base URL in the n8n credential. Keep both services in the same Railway project and environment for this private-network setup.

## Repository-owned files and artwork

- Dockerfile — selects the upstream SearXNG image and copies the local settings file.
- settings.yml — deployment configuration based on SearXNG's documented settings; enables JSON output and keeps public-instance behavior disabled.
- scripts/generate-secret.ps1 and scripts/generate-secret.sh — original helpers to generate a random secret.
- docs/brand.svg, docs/hero.id.svg, docs/hero.en.svg, and docs/architecture.svg — original documentation illustrations created for this repository. They are not official SearXNG, Railway, or n8n assets or screenshots.

## License scope

- The root LICENSE file is the MIT license for original installer and documentation materials owned by this repository's copyright holder, within the scope stated in that file.
- SearXNG itself is licensed under AGPL-3.0. The MIT license in this repository does not replace or relicense SearXNG or the upstream Docker image.
- Other software and services may carry separate license terms. Review the precise upstream version you deploy and comply with the terms that apply to your use or distribution.
- This repository is independent and is not affiliated with or endorsed by SearXNG, Railway, n8n, or search providers. Their names and marks belong to their respective owners.

This document is informational and is not legal advice. Review applicable licenses before redistributing upstream software or operating a modified public instance.
