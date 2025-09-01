# Power BI Tools - Deployment Guide

This guide will help you deploy the Power BI Tools application to GitHub and Netlify.

## 🚀 Quick Start

### 1. Prepare Your Repository

1. **Fork or Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/power-bi-tools.git
   cd power-bi-tools
   ```

2. **Set Up Environment Variables**
   ```bash
   cp env.template .env
   # Edit .env with your actual values
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

### 2. Test Locally

1. **Run the Development Server**
   ```bash
   python app.py
   # Or use the start script
   ./start.bat  # Windows
   ```

2. **Build for Production**
   ```bash
   npm run build
   # This creates the dist/ folder
   ```

3. **Test the Build**
   ```bash
   python -m http.server --directory dist
   # Visit http://localhost:8000
   ```

## 📦 Deploy to GitHub

### 1. Create a New Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `power-bi-tools` or similar
3. Make it public (for free Netlify deployment)

### 2. Push Your Code

```bash
git init
git add .
git commit -m "Initial commit: Power BI Tools"
git branch -M main
git remote add origin https://github.com/yourusername/power-bi-tools.git
git push -u origin main
```

### 3. Set Up GitHub Secrets (Optional)

For automated deployment, add these secrets to your GitHub repository:

1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `NETLIFY_AUTH_TOKEN`: Your Netlify API token
   - `NETLIFY_SITE_ID`: Your Netlify site ID

## 🌐 Deploy to Netlify

### Method 1: Connect GitHub Repository (Recommended)

1. **Sign Up for Netlify**
   - Go to [Netlify](https://netlify.com)
   - Sign up with your GitHub account

2. **Create New Site**
   - Click "New site from Git"
   - Choose GitHub
   - Select your `power-bi-tools` repository

3. **Configure Build Settings**
   ```
   Build command: pip install -r requirements.txt && npm ci && npm run build
   Publish directory: dist
   ```

4. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add your environment variables from `.env`

5. **Deploy**
   - Click "Deploy site"
   - Netlify will automatically build and deploy your site

### Method 2: Manual Deployment

1. **Build Locally**
   ```bash
   npm run build
   ```

2. **Deploy to Netlify**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Login to Netlify
   netlify login
   
   # Deploy
   netlify deploy --prod --dir=dist
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with these variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///powerbi_tools.db

# OpenAI Configuration (Optional)
OPENAI_API_KEY=your-openai-api-key-here

# Security Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=https://your-site.netlify.app
```

### Netlify Configuration

The `netlify.toml` file is already configured for:
- Build commands
- Publish directory
- API redirects
- Security headers

## 🧪 Testing

### Run Tests Locally

```bash
# Install test dependencies
pip install pytest flake8 black

# Run linting
npm run lint

# Run tests
npm run test

# Format code
npm run format
```

### Automated Testing

The GitHub Actions workflow will:
- Run tests on multiple Python versions
- Check code formatting
- Lint the codebase
- Deploy to Netlify on successful tests

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check Python version (3.9+ required)
   - Ensure all dependencies are installed
   - Check for syntax errors

2. **API Not Working**
   - Verify Netlify functions are deployed
   - Check environment variables
   - Test API endpoints locally

3. **Static Files Not Loading**
   - Check file paths in templates
   - Verify build output in `dist/` folder
   - Check Netlify redirects

### Debug Commands

```bash
# Test Python imports
python -c "import app; print('App imports successfully')"

# Test AI models
python -c "from models.ai_models import DAXGenerator; print('AI models work')"

# Test build process
python build.py

# Check Netlify functions
netlify functions:list
```

## 📚 Additional Resources

- [Netlify Functions Documentation](https://docs.netlify.com/functions/overview/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the GitHub Actions logs
3. Check Netlify deployment logs
4. Open an issue on GitHub with:
   - Error messages
   - Steps to reproduce
   - Environment details

## 🎉 Success!

Once deployed, your Power BI Tools will be available at:
`https://your-site-name.netlify.app`

The application includes:
- ✅ DAX Measure Generator
- ✅ Chart Recommendation Engine
- ✅ AI Insights & Narratives
- ✅ Anomaly Detection
- ✅ Predictive Forecasting
- ✅ SQL Query Generator
- ✅ Responsive UI
- ✅ API endpoints
- ✅ Security headers
- ✅ Automated deployment
