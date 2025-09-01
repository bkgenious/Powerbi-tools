#!/bin/bash

# Power BI Tools Build Script
# This script handles the build process for Netlify deployment

set -e  # Exit on any error

echo "🚀 Starting Power BI Tools build process..."

# Check Python version
echo "📋 Checking Python version..."
python --version

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm ci

# Build the project
echo "🔨 Building project..."
npm run build

echo "✅ Build completed successfully!"
echo "📁 Output directory: dist/"
