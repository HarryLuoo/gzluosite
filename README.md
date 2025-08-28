# Jekyll Blog Manager

**Complete standalone solution for managing Jekyll blog posts with full Git integration**

## Overview

This project provides a comprehensive Python GUI application for managing Jekyll blog posts. The blog manager handles everything from creating and editing posts to publishing them online, eliminating the need for complex CMS setups or manual Git operations.

## Features

### ✨ Complete Blog Post Management
- **Create New Posts**: Full GUI with metadata fields (title, date, category, tags)
- **Import Existing Markdown**: Support for both Jekyll and plain markdown files
- **Edit Posts**: Rich text editor with live preview
- **Delete Posts**: Safe deletion with confirmation

### 🎨 Rich Markdown Editor
- **Live Preview**: Real-time HTML rendering with syntax highlighting
- **Toolbar**: Quick access to common formatting (Bold, Italic, Headings, Lists)
- **Advanced Features**: 
  - Insert links, images, code blocks
  - File attachments with automatic copying to assets
  - Full markdown syntax support
  - Undo/Redo functionality

### 🚀 Git Integration
- **Automatic Publishing**: One-click publish to GitHub Pages
- **Smart Commits**: Automatic staging and customizable commit messages
- **Repository Detection**: Auto-detects existing Git repositories
- **Status Tracking**: Visual indicators for repository status

### 🏷️ Organization
- **Categories**: Organize posts by category
- **Tags**: Add multiple tags to posts
- **Search & Filter**: Find posts quickly
- **Auto-generated Slugs**: Clean URLs from post titles

## Installation

### Prerequisites
- Python 3.7+ installed on your system
- Git installed and configured
- Your Jekyll site repository cloned locally

### Quick Start

1. **Navigate to your Jekyll site directory**:
   ```bash
   cd /path/to/your/jekyll/site
   ```

2. **Run the blog manager**:
   ```bash
   python blog_manager.py
   ```

3. **Dependencies will install automatically** on first run:
   - `markdown` - For rendering previews
   - `pillow` - For image handling  
   - `gitpython` - For Git integration

## Usage

### Creating Your First Post

1. **Launch the application**: `python blog_manager.py`
2. **Click "New Post"** or press `Ctrl+N`
3. **Fill in metadata**:
   - Title: Your post title
   - Date: Auto-filled (editable)
   - Category: Default "blog" (customizable)
   - Tags: Comma-separated list
4. **Write your content** in the Markdown editor
5. **Save**: `Ctrl+S` or click "Save"
6. **Publish**: `Ctrl+P` or click "Publish"

### Importing Existing Markdown Files

1. **File → Import Markdown** or `Ctrl+O`
2. **Select your markdown file**
3. **Metadata will be parsed automatically** if Jekyll frontmatter exists
4. **Edit as needed and save**

### Publishing Workflow

The blog manager handles the complete publishing workflow:

1. **Auto-detects changes** in your repository
2. **Stages all modified files** for commit
3. **Prompts for commit message** with smart defaults
4. **Commits and pushes** to your GitHub repository
5. **GitHub Pages automatically rebuilds** your site

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Post |
| `Ctrl+O` | Import Markdown |
| `Ctrl+S` | Save Post |
| `Ctrl+P` | Publish to GitHub |
| `F5` | Refresh Preview |
| `Ctrl+B` | Bold selected text |
| `Ctrl+I` | Italic selected text |
| `Ctrl+L` | Insert Link |

## Project Structure

After cleanup, your Jekyll site structure is now clean and organized:

```
/
├── blog_manager.py          # ← Your new blog management tool
├── _config.yml             # Jekyll configuration
├── _posts/                 # Blog posts directory
├── assets/img/            # Images and attachments
├── admin/                 # Simplified admin (optional)
│   ├── index.html         # CMS entry point
│   ├── config.yml         # CMS configuration  
│   └── README.md          # CMS setup guide
├── _data/
│   └── navigation.yml     # Site navigation
├── about.md               # About page
├── posts.md               # Posts page
├── categories.md          # Categories page
├── tags.md               # Tags page
├── index.md              # Homepage
├── Gemfile               # Ruby dependencies
└── .gitignore           # Git ignore rules
```

## Removed Files

The following redundant and unnecessary files have been cleaned up:

### Duplicate Blog Managers (Removed)
- `blog_manager_complete.py` 
- `blog_manager_final.py`
- `jekyll_blog_manager.py`

### JavaScript Tools (Replaced by Python)
- `create-post.js`
- `manage-posts.js` 

### Complex Admin Backend (Simplified)
- `admin/backend-server.js`
- `admin/simple-backend.js`
- `admin/package.json`
- `admin/config-local.yml`

### Documentation (Consolidated)
- `README-SITE-MANAGEMENT.md`

## Advanced Features

### Image Management
- **Automatic copying** to `assets/img/` directory
- **Duplicate handling** with automatic renaming
- **Alt text prompts** for accessibility
- **Proper Jekyll paths** for GitHub Pages

### Git Workflow
- **Smart staging**: Only stages relevant files
- **Commit messages**: Customizable with sensible defaults
- **Push automation**: Direct to GitHub with error handling
- **Status monitoring**: Visual feedback on repository state

### Content Support
- **Full Markdown**: All standard markdown syntax
- **Jekyll Frontmatter**: Proper YAML metadata
- **Code Highlighting**: Syntax highlighting in preview
- **Tables and Extensions**: Enhanced markdown rendering
- **File Attachments**: Any file type with proper linking

## Troubleshooting

### Common Issues

**"No Git repository found"**
- Ensure you're running from your Jekyll site directory
- Initialize with: `git init` if needed

**"Failed to push to GitHub"**  
- Check your Git credentials are configured
- Verify remote origin is set correctly
- Ensure you have write access to the repository

**"Dependencies not installing"**
- Run manually: `pip install markdown pillow gitpython`
- Check your Python/pip installation

**"Preview not working"**
- Verify markdown syntax in your post
- Check the preview console for specific errors

## Site Management

### GitHub Pages Deployment
Your site automatically deploys to GitHub Pages when you publish changes through the blog manager. The deployment URL is configured in `_config.yml`:

```yaml
url: "https://harryluoo.github.io"
baseurl: ""
```

**Your site is now live at: https://harryluoo.github.io**

### Local Development
To test your site locally:
```bash
bundle exec jekyll serve
```

Visit: `http://localhost:4000/`

## Support

### CMS Alternative
The `admin/` directory still contains a simplified Decap CMS setup if you prefer web-based editing. See `admin/README.md` for setup instructions.

### Manual Editing
You can always edit posts manually in the `_posts/` directory using any text editor. The blog manager will detect and load these changes.

## License

This tool is provided as-is for managing your Jekyll blog. Feel free to modify and distribute according to your needs.
