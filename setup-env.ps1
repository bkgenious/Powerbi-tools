# Power BI Tools Environment Setup Script
# This script helps you set up environment variables for deployment

Write-Host "🚀 Power BI Tools Environment Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Create .env file
$envContent = @"
# Power BI Tools Environment Variables

# Flask Configuration
SECRET_KEY=powerbi-tools-secret-key-2024
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///powerbi_tools.db

# OpenAI Configuration
OPENAI_API_KEY=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

# Netlify Configuration
NODE_VERSION=18.19.0
PYTHON_VERSION=3.9

# Security Settings
JWT_SECRET_KEY=powerbi-tools-jwt-secret-2024
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,https://*.netlify.app
"@

# Write .env file
$envContent | Out-File -FilePath ".env" -Encoding UTF8
Write-Host "✅ Created .env file with your OpenAI API key" -ForegroundColor Green

# Test the setup
Write-Host "🧪 Testing OpenAI API connection..." -ForegroundColor Yellow
try {
    $env:OPENAI_API_KEY="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"
    python -c "from models.ai_models import DAXGenerator; dax = DAXGenerator(); result = dax.generate('calculate total sales'); print('✅ OpenAI API working!')"
    Write-Host "✅ OpenAI API test successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ OpenAI API test failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
Write-Host "2. Install Node.js dependencies: npm install" -ForegroundColor White
Write-Host "3. Test locally: python app.py" -ForegroundColor White
Write-Host "4. Build for deployment: npm run build" -ForegroundColor White
Write-Host "5. Deploy to GitHub and Netlify" -ForegroundColor White
Write-Host ""
Write-Host "📖 See DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan
