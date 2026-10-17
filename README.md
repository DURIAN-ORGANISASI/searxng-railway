# SearXNG Railway Installer (n8n)

Repository starter to deploy a private SearXNG search service on Railway and connect it to n8n's built-in **SearXNG** tool. JSON search output is enabled in `settings.yml`.

## Important: `SEARXNG_SECRET` is not an API key

SearXNG's official search API is an HTTP endpoint. Its `SEARXNG_SECRET` environment variable is an internal/session secret and does **not** authenticate API requests. The built-in n8n SearXNG credential asks for an **API URL**, not an API-key field. Do not paste `SEARXNG_SECRET` into n8n.

For this setup, keep SearXNG on Railway's private network and put it in the **same Railway project/environment as n8n**. This is preferable to exposing an unauthenticated search endpoint publicly.

## Deploy on Railway

1. Create a new GitHub repository, for example `searxng-railway-installer`, and upload the files from this package.
2. In Railway, open the **same project and environment that contains n8n**.
3. Add a new service from your GitHub repository. Name the service `searxng` so the private hostname below is predictable.
4. Open the service's **Variables** tab and add exactly one secret variable:

   - `SEARXNG_SECRET` = a long random secret

   Generate the value on Windows PowerShell:

   ```powershell
   $bytes = [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)
   [Convert]::ToHexString($bytes).ToLowerInvariant()
   ```

   Or on Linux/macOS:

   ```sh
   openssl rand -hex 32
   ```

   Paste the generated value into Railway Variables. Do not commit it to GitHub and do not put it in this README.

5. Deploy. If Railway needs a health check configured manually, set the health-check path to `/healthz` and port `8080`.
6. **Do not generate a public domain** for the private setup. n8n can reach the service through Railway's private network when both services are in the same project/environment.

## Connect to n8n

1. Open your n8n **SearXNG account** credential.
2. In **API URL**, enter:

   ```text
   http://searxng.railway.internal:8080
   ```

3. Save the credential and select it in the SearXNG node.
4. In the SearXNG node connected to the AI Agent, start with 5–10 results. The node uses the endpoint internally; don't add `/search` to the credential's base URL.

If you use a different Railway service name, use that service's private hostname instead of `searxng.railway.internal`.

## Test the JSON API

From a service in the same Railway private network, the search endpoint is:

```text
http://searxng.railway.internal:8080/search?q=n8n&format=json
```

Expected response: JSON containing `query` and `results`. If `format=json` returns HTTP 403, verify that `settings.yml` was included in the deployed image and that `search.formats` includes `json`.

## Notes

- This template is intended for a **private, single-project deployment**. `limiter: false` is set for that use case. Do not expose the service publicly without adding access control and rate limiting.
- Railway hosting/resource usage may incur charges. Search engines upstream of SearXNG may throttle or block requests; no search service can guarantee unlimited successful queries.
- The secret variable protects SearXNG's internal/session configuration, not the HTTP search endpoint. If you specifically require header-based API-key authentication, the native n8n SearXNG node cannot send that key through its credential; use a separately authenticated HTTP Request Tool or a custom n8n node instead.

## Source references

- SearXNG Search API: <https://docs.searxng.org/dev/search_api.html>
- SearXNG installation/configuration: <https://docs.searxng.org/admin/installation-searxng.html>
- Railway networking: <https://docs.railway.com/reference/private-networking>
