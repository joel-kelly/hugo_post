import os
import re
import json
import requests
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session
from PIL import Image
from io import BytesIO
import urllib.parse
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import base64
from github import Github
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# Configuration
API_TOKEN = os.environ.get('LINK_POSTER_TOKEN', 'change-this-token-in-production')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'your-username/your-repo')
MAX_IMAGE_WIDTH = 1200
JPEG_QUALITY = 85
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hugo Link Poster</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        input[type="text"],
        input[type="password"],
        input[type="url"],
        textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            font-family: inherit;
        }
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #95a5a6;
            cursor: not-allowed;
        }
        .alert {
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .image-selector {
            margin-top: 20px;
        }
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }
        .image-option {
            position: relative;
            cursor: pointer;
            border: 3px solid transparent;
            border-radius: 5px;
            overflow: hidden;
            background-color: #f0f0f0;
        }
        .image-option img {
            width: 100%;
            height: 120px;
            object-fit: cover;
            display: block;
        }
        .image-option.selected {
            border-color: #3498db;
        }
        .image-option input[type="radio"] {
            position: absolute;
            opacity: 0;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .help-text {
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }
        #logout {
            background-color: #e74c3c;
            margin-top: 30px;
        }
        #logout:hover {
            background-color: #c0392b;
        }
        .debug-output {
            background-color: #f8f9fa;
            border: 2px dashed #6c757d;
            border-radius: 5px;
            padding: 20px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .debug-notice {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        {% if not authenticated %}
        <h1>Login</h1>
        <form id="loginForm">
            <div class="form-group">
                <label for="token">Access Token</label>
                <input type="password" id="token" name="token" required>
            </div>
            <button type="submit">Login</button>
        </form>
        {% else %}
        <h1>Create New Link Post</h1>
        
        {% if debug_mode %}
        <div class="debug-notice">
            🚧 DEBUG MODE - Posts will not be pushed to GitHub
        </div>
        {% endif %}
        
        <div id="alerts"></div>
        
        <form id="linkForm">
            <div class="form-group">
                <label for="url">URL</label>
                <input type="url" id="url" name="url" required placeholder="https://example.com/article">
                <button type="button" id="fetchMetadata">Fetch Metadata</button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Fetching metadata...</p>
            </div>
            
            <div class="form-group">
                <label for="title">Title</label>
                <input type="text" id="title" name="title" required>
            </div>
            
            <div class="form-group">
                <label for="source">Source (optional)</label>
                <input type="text" id="source" name="source" placeholder="via HackerNews">
                <p class="help-text">Leave empty to auto-generate from domain</p>
            </div>
            
            <div class="form-group">
                <label for="excerpt">Excerpt (optional)</label>
                <textarea id="excerpt" name="excerpt" placeholder="A brief quote or description..."></textarea>
            </div>
            
            <div class="form-group">
                <label for="content">Your Commentary</label>
                <textarea id="content" name="content" placeholder="Your thoughts about this link..."></textarea>
            </div>
            
            <div class="image-selector" id="imageSelector" style="display: none;">
                <label>Select Featured Image (optional)</label>
                <div class="image-grid" id="imageGrid"></div>
            </div>
            
            <button type="submit" id="submitButton">Create Post</button>
        </form>
        
        <button id="logout">Logout</button>
        {% endif %}
    </div>
    
    <script>
        {% if not authenticated %}
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const token = document.getElementById('token').value;
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({token})
                });
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Invalid token');
                }
            } catch (error) {
                alert('Login failed: ' + error.message);
            }
        });
        {% else %}
        function showAlert(message, type = 'success') {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type}`;
            alertDiv.textContent = message;
            document.getElementById('alerts').appendChild(alertDiv);
            setTimeout(() => alertDiv.remove(), 5000);
        }
        
        document.getElementById('fetchMetadata').addEventListener('click', async () => {
            const url = document.getElementById('url').value;
            if (!url) {
                showAlert('Please enter a URL first', 'error');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch('/fetch-metadata', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url})
                });
                
                const data = await response.json();
                
                if (data.error) {
                    showAlert(data.error, 'error');
                } else {
                    if (data.title) {
                        document.getElementById('title').value = data.title;
                    }
                    if (data.source && !document.getElementById('source').value) {
                        document.getElementById('source').value = data.source;
                    }
                    
                    // Display images if found
                    if (data.images && data.images.length > 0) {
                        const imageGrid = document.getElementById('imageGrid');
                        imageGrid.innerHTML = '';
                        
                        data.images.forEach((img, index) => {
                            const div = document.createElement('div');
                            div.className = 'image-option';
                            div.innerHTML = `
                                <input type="radio" name="selectedImage" value="${img}" id="img${index}">
                                <label for="img${index}">
                                    <img src="${img}" alt="Option ${index + 1}" loading="lazy">
                                </label>
                            `;
                            div.addEventListener('click', () => {
                                document.querySelectorAll('.image-option').forEach(el => el.classList.remove('selected'));
                                div.classList.add('selected');
                                div.querySelector('input').checked = true;
                            });
                            imageGrid.appendChild(div);
                        });
                        
                        document.getElementById('imageSelector').style.display = 'block';
                    }
                    
                    showAlert('Metadata fetched successfully!');
                }
            } catch (error) {
                showAlert('Failed to fetch metadata: ' + error.message, 'error');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        document.getElementById('linkForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitButton = document.getElementById('submitButton');
            submitButton.disabled = true;
            submitButton.textContent = 'Creating post...';
            
            const formData = {
                url: document.getElementById('url').value,
                title: document.getElementById('title').value,
                source: document.getElementById('source').value,
                excerpt: document.getElementById('excerpt').value,
                content: document.getElementById('content').value,
                image: document.querySelector('input[name="selectedImage"]:checked')?.value || null
            };
            
            try {
                const response = await fetch('/create-post', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.error) {
                    showAlert(data.error, 'error');
                } else {
                    showAlert('Post created successfully!');
                    
                    // In debug mode, show the generated content
                    if (data.debug_content) {
                        const debugDiv = document.createElement('div');
                        debugDiv.className = 'debug-output';
                        debugDiv.innerHTML = `
                            <h3>Generated Markdown File: ${data.filename}</h3>
                            <pre>${data.debug_content}</pre>
                            ${data.image_info ? `<h3>Image would be saved as: ${data.image_info}</h3>` : ''}
                        `;
                        document.querySelector('.container').appendChild(debugDiv);
                    }
                    
                    document.getElementById('linkForm').reset();
                    document.getElementById('imageSelector').style.display = 'none';
                }
            } catch (error) {
                showAlert('Failed to create post: ' + error.message, 'error');
            } finally {
                submitButton.disabled = false;
                submitButton.textContent = 'Create Post';
            }
        });
        
        document.getElementById('logout').addEventListener('click', async () => {
            await fetch('/logout', {method: 'POST'});
            window.location.reload();
        });
        {% endif %}
    </script>
</body>
</html>
'''

def slugify(text):
    """Create a slug from text"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')

def fetch_url_metadata(url):
    """Fetch metadata from URL including Open Graph data"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = None
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            title = og_title['content']
        else:
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.strip()
        
        # Extract images
        images = []
        
        # Open Graph image
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            img_url = og_image['content']
            if not img_url.startswith('http'):
                img_url = urllib.parse.urljoin(url, img_url)
            images.append(img_url)
        
        # Twitter image
        twitter_image = soup.find('meta', {'name': 'twitter:image'})
        if twitter_image and twitter_image.get('content'):
            img_url = twitter_image['content']
            if not img_url.startswith('http'):
                img_url = urllib.parse.urljoin(url, img_url)
            if img_url not in images:
                images.append(img_url)
        
        # Regular images (limit to first 10)
        for img in soup.find_all('img', src=True)[:10]:
            img_url = img['src']
            if not img_url.startswith('http'):
                img_url = urllib.parse.urljoin(url, img_url)
            if img_url not in images and not any(skip in img_url for skip in ['logo', 'icon', 'avatar']):
                images.append(img_url)
        
        # Extract source from domain
        domain = urllib.parse.urlparse(url).netloc
        source = domain.replace('www.', '')
        
        return {
            'title': title,
            'images': images[:10],  # Limit to 10 images
            'source': source
        }
    except Exception as e:
        return {'error': str(e)}

def download_and_process_image(image_url, filename):
    """Download and process image"""
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if wider than max width
        if img.width > MAX_IMAGE_WIDTH:
            ratio = MAX_IMAGE_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
        
        # Save as JPEG or PNG
        output = BytesIO()
        if filename.lower().endswith('.png'):
            img.save(output, 'PNG', optimize=True)
        else:
            img.save(output, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        
        return output.getvalue()
    except Exception as e:
        raise Exception(f"Failed to process image: {str(e)}")

@app.route('/')
def index():
    authenticated = session.get('authenticated', False) or DEBUG_MODE
    return render_template_string(HTML_TEMPLATE, authenticated=authenticated, debug_mode=DEBUG_MODE)

@app.route('/login', methods=['POST'])
def login():
    if DEBUG_MODE:
        session['authenticated'] = True
        return jsonify({'success': True})
    
    data = request.json
    if data.get('token') == API_TOKEN:
        session['authenticated'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid token'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    return jsonify({'success': True})

@app.route('/fetch-metadata', methods=['POST'])
def fetch_metadata():
    if not DEBUG_MODE and not session.get('authenticated'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    metadata = fetch_url_metadata(url)
    return jsonify(metadata)

@app.route('/create-post', methods=['POST'])
def create_post():
    if not DEBUG_MODE and not session.get('authenticated'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not DEBUG_MODE and not GITHUB_TOKEN:
        return jsonify({'error': 'GitHub token not configured'}), 500
    
    data = request.json
    
    # Generate filename
    slug = slugify(data['title'])
    filename = f"{slug}.md"
    
    # Format date
    date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    # Add timezone offset if not present
    if not date.endswith(('-', '+')):
        date += '-0700'  # Pacific time
    
    # Build front matter
    front_matter = f'''---
title: "{data['title']}"
date: {date}
externalLink: "{data['url']}"
sourceUrl: "{data.get('source', '')}"'''
    
    image_filename = None
    if data.get('image'):
        # Process and save image
        try:
            ext = '.jpg'
            if data['image'].lower().endswith('.png'):
                ext = '.png'
            image_filename = f"{slug}{ext}"
            
            if not DEBUG_MODE:
                # Download and process image
                image_data = download_and_process_image(data['image'], image_filename)
            
            front_matter += f'\nfeaturedImage: "/images/{image_filename}"'
        except Exception as e:
            return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
    elif data.get('excerpt'):
        # Only add excerpt if no featured image
        front_matter += f'\nexcerpt: "{data["excerpt"]}"'
    
    front_matter += '\n--- '
    
    # Build content
    content = front_matter + '\n'
    if data.get('content'):
        content += f"\n{data['content']}"
    
    # In debug mode, just return the generated content
    if DEBUG_MODE:
        response = {
            'success': True,
            'filename': filename,
            'debug_content': content
        }
        if image_filename:
            response['image_info'] = f"/static/images/{image_filename}"
        return jsonify(response)
    
    try:
        # Connect to GitHub
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        
        # Create the markdown file
        file_path = f"content/links/{filename}"
        commit_message = f"Add link: {data['title']}"
        
        # Check if file already exists
        try:
            existing_file = repo.get_contents(file_path)
            # If we're here, file exists - append timestamp to make unique
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{slug}_{timestamp}.md"
            file_path = f"content/links/{filename}"
        except:
            # File doesn't exist, which is what we want
            pass
        
        # Create the post
        repo.create_file(file_path, commit_message, content)
        
        # Upload image if provided
        if image_filename and 'image_data' in locals():
            image_path = f"static/images/{image_filename}"
            try:
                # Check if image already exists
                repo.get_contents(image_path)
            except:
                # Image doesn't exist, create it
                repo.create_file(
                    image_path,
                    f"Add image for: {data['title']}",
                    image_data,
                    branch="main"
                )
        
        return jsonify({'success': True, 'filename': filename})
        
    except Exception as e:
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500

if __name__ == '__main__':
    # Check configuration
    print(f"DEBUG_MODE environment variable: {os.environ.get('DEBUG_MODE')}")
    print(f"DEBUG_MODE evaluated: {DEBUG_MODE}")
    
    if DEBUG_MODE:
        print("🚧 RUNNING IN DEBUG MODE - GitHub integration disabled")
        print("✓ No authentication required")
        print("✓ Posts will be displayed but not pushed to GitHub")
    else:
        print("🚀 RUNNING IN PRODUCTION MODE")
        if not GITHUB_TOKEN:
            print("WARNING: GITHUB_TOKEN not set in environment variables")
        else:
            print("✓ GitHub token configured")
            print(f"✓ Repository: {GITHUB_REPO}")
        if API_TOKEN == 'change-this-token-in-production':
            print("WARNING: Using default API token - please set LINK_POSTER_TOKEN")
    
    app.run(debug=True, host='127.0.0.1', port=5001)