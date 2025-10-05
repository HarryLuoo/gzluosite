# Assistant Notes

## Summary of changes
- Simplified the `/admin` bootstrap to rely on Decap’s native config loader while wrapping the GitHub backend so the PAT login card renders first and the stock auth component stays available behind a collapsible fallback.
- Registered a `configLoaded` listener to normalize any lingering `github-pat` backend names and keep the alias registration without depending on manual YAML parsing.
- Updated `admin/README.md` to describe the primary PAT flow, the hidden fallback login, and the new normalization strategy.

## Outstanding actions for the site owner
1. Generate a classic GitHub personal access token with the `repo` scope at <https://github.com/settings/tokens> and store it securely.
2. Visit <https://harryluoo.github.io/admin/>, paste the token into the **GitHub personal access token** field, and click **Log in with token**.
3. Rotate or revoke the token in GitHub if it is ever exposed or when you choose to cycle credentials.

- The GitHub OAuth button is tucked inside an expandable fallback so future providers (or the local proxy) remain usable without crowding the main PAT workflow.
- Cached configs that still mention `github-pat` are cleared on load, then normalized via the `configLoaded` listener before CMS initialization continues, so older bundles no longer block login.
- All of the existing local-development hooks (proxy saves, file listings, `localStorage` mirroring) were carried forward into the new `/admin` entry point so the `npx @decapcms/proxy-server` workflow continues to function.
- Future-dated posts (for example the 2025 entry) stay hidden on the public site until their dates arrive unless `future: true` is added to `_config.yml`.
