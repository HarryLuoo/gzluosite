#!/usr/bin/env python3
"""
Jekyll Blog Manager - Complete standalone solution for blog post management
Features: Create, edit, preview, and publish Jekyll posts with full Git integration
Requirements: Run `pip install markdown pillow gitpython` before first use
Usage: python blog_manager.py
"""

import os
import sys
import json
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
from datetime import datetime
from pathlib import Path
import webbrowser
import tempfile
import re
import urllib.parse

# Try to import required modules
try:
    import markdown
    from PIL import Image, ImageTk
    import git
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "pillow", "gitpython"])
    import markdown
    from PIL import Image, ImageTk
    import git

class BlogManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Jekyll Blog Manager")
        self.root.geometry("1500x1000")
        self.root.minsize(1200, 700)
        
        # Configuration
        self.posts_dir = Path("_posts")
        self.assets_dir = Path("assets/img")
        self.current_file = None
        self.unsaved_changes = False
        self.repo = None
        self.auto_preview = tk.BooleanVar(value=True)
        
        # Initialize git repository
        self.init_git_repo()
        
        # Ensure directories exist
        self.posts_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Categories and tags management
        self.categories = set(['blog'])
        self.tags = set()
        self.load_existing_categories_tags()
        
        # Set up UI
        self.setup_ui()
        self.load_posts_list()
        
        # Bind shortcuts
        self.setup_shortcuts()
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)
        
    def init_git_repo(self):
        """Initialize or detect Git repository"""
        try:
            self.repo = git.Repo(".")
            print("✓ Git repository detected")
        except git.InvalidGitRepositoryError:
            print("⚠ Not a Git repository")
        except Exception as e:
            print(f"❌ Git error: {e}")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-s>', lambda e: self.save_post())
        self.root.bind('<Control-n>', lambda e: self.new_post())
        self.root.bind('<Control-o>', lambda e: self.import_markdown())
        self.root.bind('<Control-p>', lambda e: self.publish_to_github())
        self.root.bind('<F5>', lambda e: self.refresh_preview())
        self.root.bind('<Control-b>', lambda e: self.wrap_text("**"))
        self.root.bind('<Control-i>', lambda e: self.wrap_text("*"))
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setup_menu()
        
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.setup_posts_panel(main_paned)
        self.setup_editor_panel(main_paned)
        self.setup_status_bar()
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Post (Ctrl+N)", command=self.new_post)
        file_menu.add_command(label="Import Markdown (Ctrl+O)", command=self.import_markdown)
        file_menu.add_separator()
        file_menu.add_command(label="Save (Ctrl+S)", command=self.save_post)
        file_menu.add_separator()
        file_menu.add_command(label="Delete Post", command=self.delete_post)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        
        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Bold (Ctrl+B)", command=lambda: self.wrap_text("**"))
        edit_menu.add_command(label="Italic (Ctrl+I)", command=lambda: self.wrap_text("*"))
        edit_menu.add_command(label="Insert Link", command=self.insert_link)
        edit_menu.add_command(label="Insert Image", command=self.insert_image)
        edit_menu.add_command(label="Insert Code Block", command=self.insert_code_block)
        
        # Publish Menu
        publish_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Publish", menu=publish_menu)
        publish_menu.add_command(label="Publish to GitHub (Ctrl+P)", command=self.publish_to_github)
        publish_menu.add_command(label="Preview in Browser", command=self.preview_in_browser)
        publish_menu.add_command(label="Refresh Preview (F5)", command=self.refresh_preview)
    
    def setup_posts_panel(self, parent):
        """Setup posts list panel"""
        left_frame = ttk.Frame(parent, width=350)
        parent.add(left_frame, weight=0)
        
        ttk.Label(left_frame, text="Posts", font=("Arial", 14, "bold")).pack(pady=(0, 10))
        
        # Search
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(search_frame, text="Search:").pack(anchor=tk.W)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_posts)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(fill=tk.X, pady=(2, 0))
        
        # Posts list
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.posts_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 9))
        self.posts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.posts_listbox.yview)
        self.posts_listbox.bind('<<ListboxSelect>>', self.load_selected_post)
        
        # Buttons
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(buttons_frame, text="New Post", command=self.new_post).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Import", command=self.import_markdown).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_post).pack(side=tk.LEFT, padx=2)
    
    def setup_editor_panel(self, parent):
        """Setup editor and preview panel"""
        right_paned = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        parent.add(right_paned, weight=1)
        
        # Metadata section
        metadata_frame = ttk.LabelFrame(right_paned, text="Post Metadata")
        right_paned.add(metadata_frame, weight=0)
        
        # Title and date row
        row1 = ttk.Frame(metadata_frame)
        row1.pack(fill=tk.X, padx=10, pady=8)
        
        ttk.Label(row1, text="Title:").pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(row1, font=("Arial", 10))
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 15))
        self.title_entry.bind('<KeyRelease>', self.on_change)
        
        ttk.Label(row1, text="Date:").pack(side=tk.LEFT)
        self.date_entry = ttk.Entry(row1, width=20)
        self.date_entry.pack(side=tk.LEFT, padx=(5, 0))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.date_entry.bind('<KeyRelease>', self.on_change)
        
        # Category and tags row
        row2 = ttk.Frame(metadata_frame)
        row2.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        ttk.Label(row2, text="Category:").pack(side=tk.LEFT)
        self.category_entry = ttk.Entry(row2, width=15)
        self.category_entry.pack(side=tk.LEFT, padx=(5, 15))
        self.category_entry.insert(0, "blog")
        self.category_entry.bind('<KeyRelease>', self.on_change)
        
        ttk.Label(row2, text="Tags:").pack(side=tk.LEFT)
        self.tags_entry = ttk.Entry(row2)
        self.tags_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.tags_entry.bind('<KeyRelease>', self.on_change)
        
        # Editor section
        editor_frame = ttk.LabelFrame(right_paned, text="Markdown Editor")
        right_paned.add(editor_frame, weight=2)
        
        # Toolbar
        toolbar = ttk.Frame(editor_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Bold", command=lambda: self.wrap_text("**")).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="Italic", command=lambda: self.wrap_text("*")).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="Link", command=self.insert_link).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="Image", command=self.insert_image).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="Code", command=self.insert_code_block).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="H1", command=lambda: self.insert_heading(1)).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="H2", command=lambda: self.insert_heading(2)).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="List", command=self.insert_list).pack(side=tk.LEFT, padx=1)
        
        # Text editor
        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            undo=True
        )
        self.editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.editor.bind('<KeyRelease>', self.on_editor_change)
        
        # Preview section
        preview_frame = ttk.LabelFrame(right_paned, text="Live Preview")
        right_paned.add(preview_frame, weight=1)
        
        preview_controls = ttk.Frame(preview_frame)
        preview_controls.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(preview_controls, text="Refresh (F5)", command=self.refresh_preview).pack(side=tk.LEFT)
        ttk.Button(preview_controls, text="Open in Browser", command=self.preview_in_browser).pack(side=tk.LEFT, padx=5)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            state=tk.DISABLED
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
    
    def setup_status_bar(self):
        """Setup status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_bar = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        button_frame = ttk.Frame(status_frame)
        button_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        
        ttk.Button(button_frame, text="Save", command=self.save_post).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Publish", command=self.publish_to_github).pack(side=tk.LEFT, padx=2)
    
    def load_existing_categories_tags(self):
        """Load existing categories and tags from posts"""
        self.categories = set(['blog'])
        self.tags = set()
        
        if self.posts_dir.exists():
            for post_file in self.posts_dir.glob("*.md"):
                try:
                    with open(post_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if content.startswith("---"):
                        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
                        if frontmatter_match:
                            frontmatter = frontmatter_match.group(1)
                            
                            cat_match = re.search(r'categories?:\s*(.+)', frontmatter)
                            if cat_match:
                                self.categories.add(cat_match.group(1).strip())
                            
                            tag_match = re.search(r'tags:\s*\[(.*?)\]', frontmatter)
                            if tag_match:
                                tags_str = tag_match.group(1)
                                tags = [t.strip().strip('"\'') for t in tags_str.split(',') if t.strip()]
                                self.tags.update(tags)
                except:
                    continue
    
    def on_change(self, event=None):
        """Handle metadata changes"""
        if not self.unsaved_changes:
            self.unsaved_changes = True
            self.update_title()
    
    def on_editor_change(self, event=None):
        """Handle editor content changes"""
        if not self.unsaved_changes:
            self.unsaved_changes = True
            self.update_title()
        
        if self.auto_preview.get():
            if hasattr(self, '_preview_after_id'):
                self.root.after_cancel(self._preview_after_id)
            self._preview_after_id = self.root.after(1000, self.refresh_preview)
    
    def update_title(self):
        """Update window title"""
        title = "Jekyll Blog Manager"
        if self.current_file:
            title += f" - {self.current_file.name}"
        if self.unsaved_changes:
            title += " *"
        self.root.title(title)
    
    def load_posts_list(self):
        """Load posts list"""
        self.posts_listbox.delete(0, tk.END)
        self.all_posts = []
        
        if self.posts_dir.exists():
            for post in sorted(self.posts_dir.glob("*.md"), reverse=True):
                try:
                    with open(post, 'r', encoding='utf-8') as f:
                        content = f.read()
                        title = post.name
                        
                        if content.startswith("---"):
                            match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
                            if match:
                                title = match.group(1)
                        
                        self.all_posts.append({
                            'filename': post.name,
                            'title': title,
                            'path': post
                        })
                except:
                    self.all_posts.append({
                        'filename': post.name,
                        'title': post.name,
                        'path': post
                    })
        
        self.filter_posts()
    
    def filter_posts(self, *args):
        """Filter posts by search term"""
        search_term = self.search_var.get().lower()
        self.posts_listbox.delete(0, tk.END)
        
        for post in self.all_posts:
            if (search_term in post['filename'].lower() or 
                search_term in post['title'].lower()):
                self.posts_listbox.insert(tk.END, f"{post['filename']} - {post['title']}")
        
        self.status_bar.config(text=f"Showing {self.posts_listbox.size()} posts")
    
    def load_selected_post(self, event=None):
        """Load selected post"""
        selection = self.posts_listbox.curselection()
        if not selection:
            return
        
        if self.unsaved_changes:
            result = messagebox.askyesnocancel("Unsaved Changes", "Save changes before loading another post?")
            if result is None:
                return
            elif result:
                self.save_post()
        
        filename = self.posts_listbox.get(selection[0]).split(" - ")[0]
        post = next((p for p in self.all_posts if p['filename'] == filename), None)
        if not post:
            return
        
        try:
            with open(post['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter = parts[1].strip()
                    body = parts[2].strip()
                    
                    # Clear fields
                    self.title_entry.delete(0, tk.END)
                    self.category_entry.delete(0, tk.END)
                    self.tags_entry.delete(0, tk.END)
                    self.date_entry.delete(0, tk.END)
                    
                    # Parse metadata
                    for line in frontmatter.split('\n'):
                        line = line.strip()
                        if line.startswith("title:"):
                            title = re.sub(r'title:\s*["\']?([^"\'\n]+)["\']?', r'\1', line)
                            self.title_entry.insert(0, title)
                        elif line.startswith("categories:"):
                            cat = line.replace("categories:", "").strip()
                            self.category_entry.insert(0, cat)
                        elif line.startswith("tags:"):
                            tags = line.replace("tags:", "").strip().strip("[]")
                            tags = re.sub(r'["\']', '', tags)
                            self.tags_entry.insert(0, tags)
                        elif line.startswith("date:"):
                            date = line.replace("date:", "").strip()
                            self.date_entry.insert(0, date)
                    
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(1.0, body)
            else:
                self.editor.delete(1.0, tk.END)
                self.editor.insert(1.0, content)
                
            self.current_file = post['path']
            self.unsaved_changes = False
            self.update_title()
            self.refresh_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load post: {str(e)}")
    
    def new_post(self):
        """Create new post"""
        if self.unsaved_changes:
            result = messagebox.askyesnocancel("Unsaved Changes", "Save before creating new post?")
            if result is None:
                return
            elif result:
                self.save_post()
        
        self.title_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.category_entry.insert(0, "blog")
        self.tags_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.editor.delete(1.0, tk.END)
        self.editor.insert(1.0, "# Your Post Title\n\nWrite your content here...")
        
        self.current_file = None
        self.unsaved_changes = False
        self.update_title()
        self.refresh_preview()
    
    def save_post(self):
        """Save current post"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required!")
            return
        
        # Generate filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = self.create_slug(title)
        filename = f"{date_str}-{slug}.md"
        
        filepath = self.current_file if self.current_file else self.posts_dir / filename
        
        # Build content
        content = "---\n"
        content += f'layout: post\n'
        content += f'title: "{title}"\n'
        content += f'date: {self.date_entry.get()}\n'
        content += f'categories: {self.category_entry.get()}\n'
        
        tags = self.tags_entry.get().strip()
        if tags:
            tags_list = [t.strip() for t in tags.split(",") if t.strip()]
            content += f'tags: [{", ".join(tags_list)}]\n'
        
        content += "---\n\n"
        content += self.editor.get(1.0, tk.END).strip()
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.current_file = filepath
            self.unsaved_changes = False
            self.update_title()
            self.load_posts_list()
            self.status_bar.config(text=f"Saved: {filepath.name}")
            messagebox.showinfo("Success", f"Post saved: {filepath.name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def create_slug(self, title):
        """Create URL slug from title"""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        return slug.strip('-')
    
    def delete_post(self):
        """Delete current post"""
        if not self.current_file:
            messagebox.showerror("Error", "No post selected!")
            return
        
        if messagebox.askyesno("Delete Post", f"Delete {self.current_file.name}?"):
            try:
                self.current_file.unlink()
                self.new_post()
                self.load_posts_list()
                messagebox.showinfo("Success", "Post deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
    
    def import_markdown(self):
        """Import markdown file"""
        file_path = filedialog.askopenfilename(
            title="Import Markdown",
            filetypes=[("Markdown", "*.md *.markdown"), ("Text", "*.txt"), ("All", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        body = parts[2].strip()
                        
                        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)', frontmatter)
                        if title_match:
                            self.title_entry.delete(0, tk.END)
                            self.title_entry.insert(0, title_match.group(1))
                        
                        self.editor.delete(1.0, tk.END)
                        self.editor.insert(1.0, body)
                else:
                    title = Path(file_path).stem.replace("-", " ").replace("_", " ").title()
                    self.title_entry.delete(0, tk.END)
                    self.title_entry.insert(0, title)
                    self.editor.delete(1.0, tk.END)
                    self.editor.insert(1.0, content)
                
                self.current_file = None
                self.unsaved_changes = True
                self.update_title()
                self.refresh_preview()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {str(e)}")
    
    def wrap_text(self, wrapper):
        """Wrap selected text with markdown"""
        try:
            sel_start = self.editor.index(tk.SEL_FIRST)
            sel_end = self.editor.index(tk.SEL_LAST)
            selected = self.editor.get(sel_start, sel_end)
            
            wrapped = f"{wrapper}{selected}{wrapper}"
            self.editor.delete(sel_start, sel_end)
            self.editor.insert(sel_start, wrapped)
        except tk.TclError:
            self.editor.insert(tk.INSERT, f"{wrapper}{wrapper}")
            cursor = self.editor.index(tk.INSERT)
            line, col = cursor.split('.')
            self.editor.mark_set(tk.INSERT, f"{line}.{int(col) - len(wrapper)}")
    
    def insert_heading(self, level):
        """Insert heading"""
        prefix = "#" * level + " "
        cursor = self.editor.index(tk.INSERT)
        line_start = f"{cursor.split('.')[0]}.0"
        self.editor.insert(line_start, prefix)
    
    def insert_link(self):
        """Insert link"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Insert Link")
        dialog.geometry("400x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Link Text:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        text_entry = ttk.Entry(dialog, width=40)
        text_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="URL:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        url_entry = ttk.Entry(dialog, width=40)
        url_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def insert():
            text = text_entry.get()
            url = url_entry.get()
            if text and url:
                link = f"[{text}]({url})"
                self.editor.insert(tk.INSERT, link)
                dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Insert", command=insert).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        text_entry.focus()
    
    def insert_image(self):
        """Insert image"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"), ("All", "*.*")]
        )
        
        if file_path:
            try:
                filename = Path(file_path).name
                dest = self.assets_dir / filename
                
                counter = 1
                while dest.exists():
                    name, ext = Path(filename).stem, Path(filename).suffix
                    filename = f"{name}_{counter}{ext}"
                    dest = self.assets_dir / filename
                    counter += 1
                
                shutil.copy2(file_path, dest)
                
                alt = simpledialog.askstring("Alt Text", "Enter alt text:", initialvalue=Path(filename).stem)
                alt = alt or Path(filename).stem
                
                image_md = f"![{alt}](/assets/img/{filename})\n"
                self.editor.insert(tk.INSERT, image_md)
                self.status_bar.config(text=f"Image inserted: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to insert image: {str(e)}")
    
    def insert_code_block(self):
        """Insert code block"""
        lang = simpledialog.askstring("Code Block", "Enter language (optional):")
        lang = lang or ""
        
        code_block = f"```{lang}\n\n```"
        self.editor.insert(tk.INSERT, code_block)
        
        cursor = self.editor.index(tk.INSERT)
        line, col = cursor.split('.')
        self.editor.mark_set(tk.INSERT, f"{int(line) - 1}.0")
    
    def insert_list(self):
        """Insert list item"""
        self.editor.insert(tk.INSERT, "- ")
    
    def refresh_preview(self):
        """Refresh markdown preview"""
        try:
            content = self.editor.get(1.0, tk.END).strip()
            if content:
                html = markdown.markdown(content, extensions=['codehilite', 'tables', 'toc'])
                
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.insert(1.0, html)
                self.preview_text.config(state=tk.DISABLED)
            else:
                self.preview_text.config(state=tk.NORMAL)
                self.preview_text.delete(1.0, tk.END)
                self.preview_text.config(state=tk.DISABLED)
                
        except Exception as e:
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, f"Preview error: {str(e)}")
            self.preview_text.config(state=tk.DISABLED)
    
    def preview_in_browser(self):
        """Preview post in browser"""
        try:
            content = self.editor.get(1.0, tk.END).strip()
            html_content = markdown.markdown(content, extensions=['codehilite', 'tables', 'toc'])
            
            html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{self.title_entry.get() or 'Preview'}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; 
               max-width: 800px; margin: 0 auto; padding: 2rem; line-height: 1.6; }}
        pre {{ background: #f5f5f5; padding: 1rem; overflow-x: auto; }}
        code {{ background: #f5f5f5; padding: 0.2rem; }}
        blockquote {{ border-left: 4px solid #ccc; margin: 1rem 0; padding-left: 1rem; color: #666; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
        th {{ background: #f5f5f5; }}
    </style>
</head>
<body>{html_content}</body>
</html>"""
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_template)
                temp_path = f.name
            
            webbrowser.open(f"file://{temp_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview: {str(e)}")
    
    def publish_to_github(self):
        """Publish changes to GitHub"""
        if not self.repo:
            messagebox.showerror("Error", "No Git repository found!")
            return
        
        if self.unsaved_changes:
            result = messagebox.askyesno("Unsaved Changes", "Save current post before publishing?")
            if result:
                self.save_post()
        
        try:
            # Check if there are changes to commit
            if not self.repo.is_dirty():
                messagebox.showinfo("Info", "No changes to publish!")
                return
            
            # Add all changes
            self.repo.git.add(A=True)
            
            # Commit with message
            commit_msg = simpledialog.askstring(
                "Commit Message", 
                "Enter commit message:",
                initialvalue=f"Updated blog post: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            
            if not commit_msg:
                return
            
            self.repo.index.commit(commit_msg)
            
            # Push to remote
            try:
                origin = self.repo.remotes.origin
                origin.push()
                messagebox.showinfo("Success", "Published to GitHub successfully!")
                self.status_bar.config(text="Published successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to push: {str(e)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to publish: {str(e)}")
    
    def quit_app(self):
        """Quit application"""
        if self.unsaved_changes:
            result = messagebox.askyesnocancel("Unsaved Changes", "Save before exiting?")
            if result is None:
                return
            elif result:
                self.save_post()
        
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = BlogManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
