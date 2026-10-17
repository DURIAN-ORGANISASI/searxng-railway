# Official SearXNG container; keep application updates controlled by the upstream image.
FROM searxng/searxng:latest

# Enable JSON results so n8n's SearXNG tool can consume the search API.
COPY settings.yml /etc/searxng/settings.yml
