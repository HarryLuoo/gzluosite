# Assistant Notes

## Summary of changes
- Added an informational banner to `/admin` explaining the personal access token (PAT) login workflow for Decap CMS.
- Rewrote `admin/README.md` to focus on the PAT-based authentication process and day-to-day editing steps.
- Confirmed that existing Decap CMS configuration (`admin/config.yml`) already targets the repository's `main` branch and requires no additional changes.

## Outstanding actions for the site owner
1. Generate a classic GitHub personal access token with the `repo` scope by visiting <https://github.com/settings/tokens>.
2. Store the token securely (for example in a password manager).
3. Use the token when clicking **Log in with token** on <https://harryluoo.github.io/admin/>.
4. Revoke and regenerate the token if it is ever exposed or when you want to rotate credentials.

## Observations
- Future-dated posts (e.g., the 2025 entry) will stay hidden on the public site until their dates arrive unless `future: true` is added to `_config.yml`.
- The custom local-development script embedded in `admin/index.html` is untouched and continues to support the local proxy workflow described in `admin/README.md`.
