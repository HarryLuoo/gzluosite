# CMS Setup Guide for GitHub Pages

## Current Status
Your website is now fully functional with:
- ✅ Working local development server at http://127.0.0.1:4000/
- ✅ Complete navigation between all pages (Home, About, Categories, Tags)
- ✅ GitHub Pages deployment at https://harryluoo.github.io/
- ✅ Decap CMS interface available at /admin/
- ⚠️ CMS authentication requires a personal access token (see below)

## CMS Authentication Setup

For a single editor you can sign in using a GitHub personal access token (PAT). This keeps hosting on
GitHub Pages and avoids running a separate OAuth service.

### One-time token creation (manual step)

1. Visit <https://github.com/settings/tokens>.
2. Choose **Generate new token (classic)**.
3. Give the token a descriptive name (for example `Decap CMS PAT`).
4. Tick the **repo** scope so the CMS can read and write content in this repository.
5. Create the token and copy it somewhere safe (a password manager is recommended).

### Day-to-day editing

1. Open <https://harryluoo.github.io/admin/>.
2. Paste your PAT into the **GitHub personal access token** field and click **Log in with token**.
3. Edit content and click **Publish**. Decap CMS commits straight to `main`.

The PAT form is now the primary login path. A collapsible “Need the standard Decap login instead?”
section is available underneath if you ever restore OAuth or test against the local proxy—the default
component still renders there so nothing is lost.

Behind the scenes the admin bootstrap clears cached configs that reference the legacy `github-pat`
backend and normalizes any stray references during the `configLoaded` event before initialization
continues. If you still see an error mentioning `github-pat`, perform a hard refresh in your browser
(for example, **Shift+Reload** or **Cmd+Shift+R**) to ensure the latest bundle is downloaded.

If you ever revoke or rotate the token, just mint a new one with the same scope and reuse the workflow
above.

### Alternative backends (optional)

If you later decide to add more collaborators, consider wiring the CMS to a multi-user backend such as
Netlify Identity/Git Gateway or a self-hosted OAuth proxy. The previous revision of this document captured
those options and can be recovered from Git history when needed.

## Local Development with CMS

For local development, you can use the test backend:

1. Install and run the local proxy:
```bash
npx @decapcms/proxy-server
```

2. Update your local CMS config to use test backend:
```yaml
backend:
  name: proxy
  proxy_url: http://localhost:8081
```

## Current File Structure

```
/
├── blog_manager.py      # Python blog management tool
├── _config.yml          # Jekyll configuration
├── index.md             # Homepage content
├── about.md             # About page
├── categories.md        # Categories page
├── tags.md              # Tags page
├── _data/
│   └── navigation.yml   # Site navigation menu
├── _posts/              # Blog posts folder
│   └── 2025-08-27-welcome-to-my-website.md
├── admin/               # CMS admin interface
│   ├── index.html       # CMS entry point
│   └── config.yml       # CMS configuration
└── assets/
    └── img/             # Images folder
```

## Making Updates to Your Site

### Without CMS (Direct GitHub Edit)
1. Navigate to your repository on GitHub
2. Click on any file to edit it
3. Click the pencil icon to edit
4. Make changes and commit

### With Local Development
1. Clone your repository
2. Run `bundle exec jekyll serve`
3. Make changes locally
4. Push to GitHub

### With CMS (Using PAT)
1. Go to https://harryluoo.github.io/admin/
2. Log in with your personal access token
3. Edit content through the visual interface
4. Save and publish changes
