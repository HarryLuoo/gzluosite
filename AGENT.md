# Assistant Notes

## Summary of changes
- Replaced the `/admin` entry point with a custom GitHub backend wrapper that surfaces an on-page personal access token form for Decap CMS.
- Kept the CMS configuration aligned with the built-in `github` backend while enhancing the bootstrap script to decorate its auth component via `CMS.React` so the token helper renders reliably.
- Refreshed `admin/README.md` so the day-to-day workflow matches the embedded token login form.

## Outstanding actions for the site owner
1. Generate a classic GitHub personal access token with the `repo` scope at <https://github.com/settings/tokens> and store it securely.
2. Visit <https://harryluoo.github.io/admin/>, paste the token into the **GitHub personal access token** field, and click **Log in with token**.
3. Rotate or revoke the token in GitHub if it is ever exposed or when you choose to cycle credentials.

## Observations
- The GitHub OAuth button remains available for future multi-user setups, but the embedded PAT form now handles the single-maintainer flow without relying on hidden UI options.
- All of the existing local-development hooks (proxy saves, file listings, `localStorage` mirroring) were carried forward into the new `/admin` entry point so the `npx @decapcms/proxy-server` workflow continues to function.
- Future-dated posts (for example the 2025 entry) stay hidden on the public site until their dates arrive unless `future: true` is added to `_config.yml`.
