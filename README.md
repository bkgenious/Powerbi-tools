# Power BI Tools v2.0 🚀

**AI-powered analytics tools for Power BI developers and data analysts**

[![Netlify Status](https://api.netlify.com/api/v1/badges/your-site-id/deploy-status)](https://app.netlify.com/sites/your-site/deploys)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

### 🤖 AI-Powered Tools
- **DAX Generator**: Convert natural language to DAX measures
- **Chart Recommender**: Get intelligent chart suggestions for your data
- **AI Insights**: Extract meaningful insights from datasets
- **Anomaly Detection**: Identify outliers and anomalies automatically
- **Forecasting**: Generate time series predictions
- **SQL Generator**: Create SQL queries from plain English

### 🎨 Modern Interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Dark/Light Theme**: Beautiful, modern UI with smooth animations
- **Real-time Feedback**: Instant notifications and loading states
- **File Upload Support**: Drag & drop CSV/JSON files
- **Interactive Charts**: Powered by Plotly.js

### ⚡ Performance Optimized
- **Static Site Generation**: Fast loading and SEO-friendly
- **Serverless Functions**: Scalable API endpoints on Netlify
- **Minimal Dependencies**: Streamlined for faster builds
- **Caching Strategy**: Optimized for repeat visits

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/power-bi-tools.git
   cd power-bi-tools
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.template .env
   # Edit .env with your OpenAI API key
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

### Production Deployment

1. **Build the project**
   ```bash
   python build.py
   ```

2. **Deploy to Netlify**
   ```bash
   netlify deploy --prod --dir=dist
   ```

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with CSS Grid, Flexbox, and custom properties
- **JavaScript (ES6+)**: Modular, class-based architecture
- **Plotly.js**: Interactive data visualizations
- **Font Awesome**: Beautiful icons

### Backend
- **Python 3.11+**: Modern Python with type hints
- **Flask**: Lightweight web framework
- **OpenAI API**: GPT-3.5 for AI-powered features
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning algorithms

### Deployment
- **Netlify**: Static site hosting with serverless functions
- **GitHub Actions**: Automated testing and deployment
- **Python 3.11**: Optimized for Netlify's build environment

## 📁 Project Structure

```
power-bi-tools/
├── app.py                 # Main Flask application
├── build.py              # Build script for production
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
├── netlify.toml         # Netlify configuration
├── runtime.txt          # Python version specification
├── models/
│   └── ai_models.py     # AI model implementations
├── static/
│   ├── css/
│   │   └── main.css     # Modern, responsive styles
│   └── js/
│       └── main.js      # Interactive functionality
├── templates/
│   └── index.html       # Main application template
├── netlify/
│   └── functions/
│       └── api.py       # Serverless API functions
└── dist/                # Production build output
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# Netlify Configuration
NODE_VERSION=18.19.0
PYTHON_VERSION=3.11
```

### Netlify Settings

In your Netlify dashboard:

- **Build command**: `python -m pip install --upgrade pip && pip install -r requirements.txt && npm ci && python build.py`
- **Publish directory**: `dist`
- **Node version**: `18.19.0`
- **Python version**: `3.11`

## 🎯 Usage Examples

### DAX Generation
```
Input: "Calculate total sales by region with year-over-year growth"
Output: 
Total Sales by Region YoY = 
VAR CurrentYear = YEAR(TODAY())
VAR PreviousYear = CurrentYear - 1
RETURN
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL(DimDate),
        YEAR(DimDate[Date]) = CurrentYear
    )
) / 
CALCULATE(
    SUM(Sales[Amount]),
    FILTER(
        ALL(DimDate),
        YEAR(DimDate[Date]) = PreviousYear
    )
) - 1
```

### Chart Recommendation
```
Input: Sales data with date, region, and amount columns
Output: 
- Recommended: Line Chart
- Reason: Time series data with multiple regions
- Configuration: Date on X-axis, Amount on Y-axis, Region as series
```

### AI Insights
```
Input: Customer purchase dataset
Output:
- "Average order value is $127.45 with 15% standard deviation"
- "Top 3 regions account for 67% of total sales"
- "Customer retention rate is 78% over 12 months"
- "Seasonal peak in Q4 with 40% higher sales"
```

## 🔒 Security Features

- **CORS Protection**: Configured for secure cross-origin requests
- **Input Validation**: All user inputs are sanitized
- **Rate Limiting**: API endpoints protected against abuse
- **Security Headers**: XSS protection and content security policies
- **Environment Variables**: Sensitive data kept secure

## 📊 Performance Metrics

- **Bundle Size**: < 500KB (gzipped)
- **Load Time**: < 2 seconds on 3G
- **Lighthouse Score**: 95+ (Performance, Accessibility, Best Practices, SEO)
- **API Response Time**: < 500ms average

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write tests for new features
- Update documentation for API changes
- Ensure responsive design works on all devices

## 🧪 Testing

```bash
# Run Python tests
python -m pytest tests/

# Run linting
python -m flake8 .
python -m black --check .

# Run JavaScript tests
npm test

# Build test
python build.py
```

## 📈 Roadmap

### v2.1 (Next Release)
- [ ] Advanced chart customization
- [ ] Export functionality (PDF, Excel)
- [ ] User authentication system
- [ ] Saved projects and templates
- [ ] Real-time collaboration

### v2.2 (Future)
- [ ] Natural language query interface
- [ ] Advanced ML models integration
- [ ] Custom visualization builder
- [ ] API rate limiting dashboard
- [ ] Multi-language support

## 🐛 Troubleshooting

### Common Issues

**Build fails on Netlify**
- Check Python version (should be 3.11)
- Verify all dependencies in requirements.txt
- Ensure netlify.toml is properly configured

**API calls failing**
- Verify OPENAI_API_KEY is set
- Check CORS configuration
- Ensure serverless functions are deployed

**Charts not rendering**
- Check Plotly.js is loaded
- Verify data format is correct
- Check browser console for errors

### Getting Help

- 📖 [Documentation](https://your-site.netlify.app/docs)
- 🐛 [Issue Tracker](https://github.com/yourusername/power-bi-tools/issues)
- 💬 [Discussions](https://github.com/yourusername/power-bi-tools/discussions)
- 📧 [Email Support](mailto:support@yourdomain.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT API
- **Netlify** for hosting and serverless functions
- **Plotly** for interactive charting
- **Font Awesome** for beautiful icons
- **Contributors** who help improve this project

---

**Made with ❤️ for the Power BI community**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/power-bi-tools?style=social)](https://github.com/yourusername/power-bi-tools)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/power-bi-tools?style=social)](https://github.com/yourusername/power-bi-tools)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/power-bi-tools)](https://github.com/yourusername/power-bi-tools/issues)
