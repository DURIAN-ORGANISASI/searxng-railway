# Generate a cryptographically random 256-bit secret for Railway's SEARXNG_SECRET variable.
$bytes = [System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32)
[Convert]::ToHexString($bytes).ToLowerInvariant()
