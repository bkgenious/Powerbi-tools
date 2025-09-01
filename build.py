#!/usr/bin/env python3
"""
Power BI Tools Build Script
Creates a production-ready static site for Netlify deployment
"""

import os
import re
import shutil
import json
from pathlib import Path

def main():
    print("🚀 Starting Power BI Tools build process...")
    
    # Configuration
    source_dir = Path(".")
    dist_dir = Path("dist")
    
    # Clean and create dist directory
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # Copy static files
    print("📁 Copying static files...")
    static_src = source_dir / "static"
    static_dest = dist_dir / "static"
    if static_src.exists():
        shutil.copytree(static_src, static_dest)
        print("✓ Static files copied")
        # Minify CSS/JS in-place for space efficiency
        for root, _, files in os.walk(static_dest):
            for name in files:
                path = Path(root) / name
                try:
                    if name.endswith('.css'):
                        content = path.read_text(encoding='utf-8', errors='ignore')
                        content = re.sub(r"/\*.*?\*/", "", content, flags=re.S)
                        content = re.sub(r"\s+", " ", content)
                        content = content.replace(" {", "{").replace("} ", "}")
                        path.write_text(content.strip(), encoding='utf-8')
                    elif name.endswith('.js'):
                        content = path.read_text(encoding='utf-8', errors='ignore')
                        content = re.sub(r"/\*.*?\*/", "", content, flags=re.S)
                        content = re.sub(r"\n+", "\n", content)
                        content = re.sub(r"\s{2,}", " ", content)
                        path.write_text(content.strip(), encoding='utf-8')
                except Exception:
                    # Non-fatal; keep original if minify fails
                    pass
    
    # Copy templates and export index.html at root
    print("📄 Processing HTML templates...")
    templates_src = source_dir / "templates"
    if templates_src.exists():
        templates_dest = dist_dir / "templates"
        shutil.copytree(templates_src, templates_dest)
        print("✓ HTML templates copied")
        index_src = templates_src / "index.html"
        if index_src.exists():
            try:
                html = index_src.read_text(encoding='utf-8')
                # Light HTML minify
                html = re.sub(r">\s+<", "><", html)
                html = re.sub(r"\n+", "\n", html)
                (dist_dir / "index.html").write_text(html, encoding='utf-8')
                print("✓ index.html exported to dist/")
            except Exception:
                shutil.copy2(index_src, dist_dir / "index.html")
    
    # Copy Netlify functions
    print("⚡ Copying Netlify functions...")
    functions_src = source_dir / "netlify" / "functions"
    if functions_src.exists():
        functions_dest = dist_dir / ".netlify" / "functions"
        functions_dest.mkdir(parents=True)
        shutil.copytree(functions_src, functions_dest / "api")
        print("✓ Netlify functions copied")
    
    # Create _redirects file
    print("🔄 Creating redirects...")
    redirects_content = """# API redirects
/api/* /.netlify/functions/api/:splat 200

# SPA fallback
/* /index.html 200
"""
    with open(dist_dir / "_redirects", "w") as f:
        f.write(redirects_content)
    print("✓ _redirects file created")
    
    # Create _headers file
    print("🔒 Creating headers...")
    headers_content = """# Security headers
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

# Cache static assets
/static/*
  Cache-Control: public, max-age=31536000, immutable

# Don't cache HTML
/*.html
  Cache-Control: no-cache, no-store, must-revalidate
"""
    with open(dist_dir / "_headers", "w") as f:
        f.write(headers_content)
    print("✓ _headers file created")
    
    # Copy netlify.toml
    print("⚙️ Copying Netlify configuration...")
    netlify_config = source_dir / "netlify.toml"
    if netlify_config.exists():
        shutil.copy2(netlify_config, dist_dir)
        print("✓ netlify.toml copied")
    
    # Create package.json for Netlify
    print("📦 Creating package.json...")
    package_json = {
        "name": "powerbi-tools",
        "version": "2.0.0",
        "description": "AI-powered Power BI tools",
        "scripts": {
            "build": "echo 'Build completed'",
            "start": "echo 'Static site ready'"
        },
        "engines": {
            "node": ">=18.0.0"
        }
    }
    with open(dist_dir / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    print("✓ package.json created")
    
    # Create README
    print("📖 Creating README...")
    readme_content = """# Power BI Tools

AI-powered tools for Power BI developers and analysts.

## Features

- **DAX Generator**: Generate DAX measures from natural language
- **Chart Recommender**: Get chart recommendations based on your data
- **AI Insights**: Extract insights from your datasets
- **Anomaly Detection**: Detect anomalies in your data
- **Forecasting**: Generate time series forecasts
- **SQL Generator**: Create SQL queries from natural language

## Deployment

This is a static site built for Netlify deployment.

## API Endpoints

- `/api/generate-dax` - Generate DAX measures
- `/api/recommend-chart` - Recommend chart types
- `/api/generate-insights` - Generate AI insights
- `/api/detect-anomalies` - Detect anomalies
- `/api/forecast` - Generate forecasts
- `/api/generate-sql` - Generate SQL queries

## Environment Variables

Set these in your Netlify dashboard:

- `OPENAI_API_KEY` - Your OpenAI API key
- `SECRET_KEY` - Flask secret key
- `FLASK_ENV` - Set to 'production'
"""
    with open(dist_dir / "README.md", "w") as f:
        f.write(readme_content)
    print("✓ README created")
    
    # Create robots.txt
    print("🤖 Creating robots.txt...")
    robots_content = """User-agent: *
Allow: /

Sitemap: https://your-site.netlify.app/sitemap.xml
"""
    with open(dist_dir / "robots.txt", "w") as f:
        f.write(robots_content)
    print("✓ robots.txt created")
    
    # Create sitemap.xml
    print("🗺️ Creating sitemap...")
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://your-site.netlify.app/</loc>
    <lastmod>2024-01-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    with open(dist_dir / "sitemap.xml", "w") as f:
        f.write(sitemap_content)
    print("✓ sitemap.xml created")
    
    print("\n🎉 Build completed successfully!")
    print(f"📁 Output directory: {dist_dir.absolute()}")
    print("\n📋 Next steps:")
    print("1. Test locally: python -m http.server --directory dist")
    print("2. Deploy to Netlify: netlify deploy --prod --dir=dist")
    print("3. Or connect your GitHub repository to Netlify for automatic deployments")

if __name__ == "__main__":
    main()
