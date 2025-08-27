# CMS Setup Guide for GitHub Pages

## Current Status
Your website is now fully functional with:
- ✅ Working local development server at http://127.0.0.1:4000/
- ✅ Complete navigation between all pages (Home, About, Categories, Tags)
- ✅ GitHub Pages deployment at https://harryluoo.github.io/gzluosite/
- ✅ Decap CMS interface available at /admin/
- ⚠️ CMS authentication requires additional setup (see below)

## CMS Authentication Setup

The CMS requires OAuth authentication to edit your site. Since GitHub Pages doesn't provide server-side functionality, you have several options:

### Option 1: Use GitHub Personal Access Token (Simplest for single user)

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` scope
3. Use this token to authenticate (Note: This is only suitable for personal use, not for multiple editors)

### Option 2: Set up a Free OAuth Backend Service

You can use one of these free services:

#### A. Netlify (Recommended - Most Reliable)
1. Create a free Netlify account at https://netlify.com
2. Deploy your site to Netlify (you can keep GitHub Pages as well)
3. Enable Netlify Identity in your Netlify site settings
4. Update `admin/config.yml`:
```yaml
backend:
  name: git-gateway
  branch: main
```
5. Add the Netlify Identity Widget to your site

#### B. Use Vite-plugin-decap-cms-oauth
1. Create a new GitHub OAuth App:
   - Go to GitHub Settings > Developer settings > OAuth Apps
   - Click "New OAuth App"
   - Application name: Your Site CMS
   - Homepage URL: https://harryluoo.github.io/gzluosite
   - Authorization callback URL: https://your-oauth-provider.vercel.app/callback
2. Deploy the OAuth provider to Vercel (free):
   - Fork https://github.com/marcodallaba/netlify-cms-github-oauth-provider
   - Deploy to Vercel
   - Set environment variables with your GitHub OAuth App credentials
3. Update `admin/config.yml`:
```yaml
backend:
  name: github
  repo: HarryLuoo/gzluosite
  branch: main
  base_url: https://your-oauth-provider.vercel.app
  auth_endpoint: auth
```

### Option 3: Use GitHub.dev (Alternative Editor)

For quick edits without CMS:
1. Press `.` (period) on your GitHub repository page
2. This opens GitHub.dev - a web-based VS Code editor
3. Make edits directly and commit from the browser

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
├── _config.yml           # Jekyll configuration
├── _config-local.yml     # Local development config
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
2. Run `bundle exec jekyll serve --config _config.yml,_config-local.yml`
3. Make changes locally
4. Push to GitHub

### With CMS (After OAuth Setup)
1. Go to https://harryluoo.github.io/gzluosite/admin/
2. Login with GitHub
3. Edit content through the visual interface
4. Save and publish changes

## Troubleshooting

### Issue: "404: NOT_FOUND" when logging in
- This means the OAuth provider isn't set up yet
- Follow one of the authentication setup options above

### Issue: Local server shows errors
- Make sure Ruby and Jekyll are installed
- Run `bundle install` to install dependencies
- Use the dual config command: `bundle exec jekyll serve --config _config.yml,_config-local.yml`

### Issue: Changes not showing on GitHub Pages
- Wait a few minutes for GitHub Pages to rebuild
- Check the Actions tab in your repository for build status
- Clear browser cache and refresh

## Next Steps

1. Choose and implement an authentication method from the options above
2. Consider adding more content to your site
3. Customize the theme and styling
4. Add a custom domain if desired
