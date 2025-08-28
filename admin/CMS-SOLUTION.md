# CMS Solution for GZLuoSite

## ✅ What's Working

### Custom Backend Server
- **Location**: `admin/simple-backend.js`
- **Port**: 8081
- **Features**:
  - Direct file saving to local filesystem
  - No OAuth/authentication required for local development
  - Automatic Jekyll frontmatter generation
  - CORS support for CMS integration

### Backend API Endpoints
1. `GET /api/files` - Lists files in _posts directory
2. `GET /api/file?path=...` - Reads file content
3. `POST /api/save` - Saves files with proper Jekyll formatting

## 🔧 Setup Instructions

### 1. Start Jekyll Server
```bash
bundle exec jekyll serve
```

### 2. Start Custom Backend
```bash
cd admin
node simple-backend.js
```

### 3. Access CMS
Open browser to: http://127.0.0.1:4000/gzluosite/admin/

## ⚠️ Known Issues

### Markdown Editor Validation Issue
The CMS markdown editor has a validation bug with the test-repo backend where typed content isn't properly registered as valid input.

### Workarounds:

#### Option 1: Direct API Usage
Use the test script to create posts programmatically:
```javascript
// Save this as create-post.js
const http = require('http');

const newPost = {
  path: `_posts/${new Date().toISOString().split('T')[0]}-your-post-title.md`,
  content: `---
layout: post
title: "Your Post Title"
date: ${new Date().toISOString()}
categories: blog
tags: update
---

Your post content here...
`
};

const req = http.request({
  hostname: 'localhost',
  port: 8081,
  path: '/api/save',
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
}, (res) => {
  res.on('data', d => console.log(d.toString()));
});

req.write(JSON.stringify(newPost));
req.end();
```

#### Option 2: Make Body Field Optional
Edit `admin/config.yml`:
```yaml
fields:
  - {label: "Body", name: "body", widget: "markdown", required: false}
```

#### Option 3: Use Alternative CMS Solutions
Consider these alternatives that work better with custom backends:
- **Forestry.io** - Git-based CMS with better local support
- **Tina CMS** - Modern CMS with local development mode
- **NetlifyCMS with GitHub backend** - Use proper GitHub OAuth

## 📝 Creating Posts Without CMS

### Manual Method
1. Create file in `_posts/` with format: `YYYY-MM-DD-title.md`
2. Add Jekyll frontmatter:
```markdown
---
layout: post
title: "Post Title"
date: 2025-08-27 18:00:00
categories: blog
tags: [tag1, tag2]
---

Post content here...
```

### Using the Backend API
```bash
# Using curl
curl -X POST http://localhost:8081/api/save \
  -H "Content-Type: application/json" \
  -d '{
    "path": "_posts/2025-08-27-my-post.md",
    "content": "---\nlayout: post\ntitle: \"My Post\"\n---\n\nContent here..."
  }'
```

## 🚀 Future Improvements

1. **Fix CMS Editor**: Implement custom widget or modify fetch intercept to handle markdown editor better
2. **Add Authentication**: Implement basic auth for production use
3. **File Upload Support**: Add endpoint for handling images/attachments
4. **Auto-git Commit**: Automatically commit changes to Git after saving
5. **Preview Support**: Add preview functionality to backend

## 📂 File Structure

```
admin/
├── index.html           # CMS entry point with fetch intercepts
├── config.yml           # CMS configuration
├── simple-backend.js    # Custom backend server
├── test-post.js        # Test script for backend
├── CMS-SOLUTION.md     # This documentation
└── README-CUSTOM-BACKEND.md  # Original backend docs
```

## 💡 Summary

The custom backend successfully allows you to:
- Save posts directly to your local filesystem
- Bypass GitHub authentication requirements
- Work offline with your Jekyll site

While the CMS UI has limitations with the markdown editor, the backend API is fully functional and can be used programmatically or with alternative interfaces to manage your content effectively.
