from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging
import traceback
from datetime import datetime
import hashlib
import hmac
import base64
import time
import json # Added for Power BI Desktop friendly endpoints

# Import enhanced models
from models.enhanced_ai_models import (
    SecurityManager,
    AutoErrorRecovery,
    EnhancedDAXGenerator,
    EnhancedChartRecommender,
    EnhancedInsightGenerator,
    EnhancedAnomalyDetector,
    EnhancedForecastingModel,
    EnhancedSQLGenerator
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'powerbi-tools-secret-2024')
API_KEY = os.getenv('PBI_DESKTOP_API_KEY', 'dev-key')

# Enable CORS with enhanced security
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "x-api-key"]
    }
})

# Initialize enhanced components
security_manager = SecurityManager()
error_recovery = AutoErrorRecovery()

# Initialize enhanced AI models
enhanced_dax_generator = EnhancedDAXGenerator()
enhanced_chart_recommender = EnhancedChartRecommender()
enhanced_insight_generator = EnhancedInsightGenerator()
enhanced_anomaly_detector = EnhancedAnomalyDetector()
enhanced_forecasting_model = EnhancedForecastingModel()
enhanced_sql_generator = EnhancedSQLGenerator()

# Global performance monitoring
performance_metrics = {}
error_log = []

def log_performance(endpoint: str, execution_time: float, success: bool, error: str = None):
    """Log performance metrics for monitoring"""
    if endpoint not in performance_metrics:
        performance_metrics[endpoint] = []
    
    performance_metrics[endpoint].append({
        'timestamp': datetime.now(),
        'execution_time': execution_time,
        'success': success,
        'error': error
    })
    
    # Keep only last 1000 entries
    if len(performance_metrics[endpoint]) > 1000:
        performance_metrics[endpoint] = performance_metrics[endpoint][-1000:]

def log_error(error: Exception, context: dict = None):
    """Log errors for monitoring and debugging"""
    error_entry = {
        'timestamp': datetime.now(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'traceback': traceback.format_exc(),
        'context': context or {}
    }
    error_log.append(error_entry)
    
    # Keep only last 1000 errors
    if len(error_log) > 1000:
        error_log.pop(0)
    
    logger.error(f"Error logged: {error_entry}")

def validate_request(request_data: dict) -> tuple[bool, str]:
    """Validate incoming request data"""
    if not request_data:
        return False, "No data provided"
    
    # Check for required fields based on endpoint
    if 'requirement' in request_data and not str(request_data['requirement']).strip():
        return False, "Requirement field is empty"
    
    if 'dataset' in request_data and request_data.get('dataset') is None:
        return False, "Dataset is empty"
    
    return True, ""

def generate_user_id(request) -> str:
    """Generate a unique user ID for rate limiting"""
    # Use IP address and user agent for identification
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    return hashlib.md5(f"{ip}:{user_agent}".encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

# -------------------------
# Power BI Desktop friendly endpoints (/api/powerbi/*)
# Accept either POST JSON or GET with query params and simple x-api-key
# -------------------------

def _check_api_key() -> bool:
    key = request.headers.get('x-api-key') or request.args.get('api_key')
    return (API_KEY and key == API_KEY)

@app.route('/api/powerbi/generate-dax', methods=['GET', 'POST'])
def pbi_generate_dax():
    if not _check_api_key():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        if request.method == 'POST':
            data = request.get_json(force=True, silent=True) or {}
            requirement = data.get('requirement', '')
        else:
            requirement = request.args.get('requirement', '')
        result = enhanced_dax_generator.generate(requirement)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/powerbi/recommend-chart', methods=['GET', 'POST'])
def pbi_recommend_chart():
    if not _check_api_key():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        if request.method == 'POST':
            data = request.get_json(force=True, silent=True) or {}
            dataset = data.get('dataset', [])
        else:
            # For GET, allow dataset as JSON string
            dataset_str = request.args.get('dataset', '[]')
            try:
                dataset = json.loads(dataset_str)
            except Exception:
                dataset = []
        result = enhanced_chart_recommender.analyze(dataset)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/powerbi/generate-insights', methods=['GET', 'POST'])
def pbi_generate_insights():
    if not _check_api_key():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        if request.method == 'POST':
            data = request.get_json(force=True, silent=True) or {}
            dataset = data.get('dataset', [])
        else:
            dataset_str = request.args.get('dataset', '[]')
            try:
                dataset = json.loads(dataset_str)
            except Exception:
                dataset = []
        result = enhanced_insight_generator.analyze(dataset)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/powerbi/detect-anomalies', methods=['GET', 'POST'])
def pbi_detect_anomalies():
    if not _check_api_key():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        if request.method == 'POST':
            data = request.get_json(force=True, silent=True) or {}
            dataset = data.get('dataset', [])
        else:
            dataset_str = request.args.get('dataset', '[]')
            try:
                dataset = json.loads(dataset_str)
            except Exception:
                dataset = []
        result = enhanced_anomaly_detector.detect(dataset)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/powerbi/forecast', methods=['GET', 'POST'])
def pbi_forecast():
    if not _check_api_key():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        if request.method == 'POST':
            data = request.get_json(force=True, silent=True) or {}
            dataset = data.get('dataset', [])
            horizon = int(data.get('horizon', 30))
        else:
            dataset_str = request.args.get('dataset', '[]')
            try:
                dataset = json.loads(dataset_str)
            except Exception:
                dataset = []
            horizon = int(request.args.get('horizon', 30))
        result = enhanced_forecasting_model.predict(dataset, horizon)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/powerbi/generate-sql', methods=['GET', 'POST'])
def pbi_generate_sql():
    if not _check_api_key():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        if request.method == 'POST':
            data = request.get_json(force=True, silent=True) or {}
            requirement = data.get('requirement', '')
        else:
            requirement = request.args.get('requirement', '')
        result = enhanced_sql_generator.generate(requirement)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# -------------------------
# Existing website JSON endpoints (/api/*) remain below
# -------------------------

@app.route('/api/generate-dax', methods=['POST'])
def generate_dax():
    """Enhanced DAX generation with security and error recovery"""
    start_time = time.time()
    user_id = generate_user_id(request)
    
    try:
        data = request.get_json()
        is_valid, error_msg = validate_request(data)
        
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        requirement = data.get('requirement', '').strip()
        
        # Use enhanced DAX generator
        result = enhanced_dax_generator.generate(requirement, user_id)
        
        execution_time = time.time() - start_time
        log_performance('generate-dax', execution_time, True)
        
        return jsonify(result)
        
    except Exception as e:
        execution_time = time.time() - start_time
        log_performance('generate-dax', execution_time, False, str(e))
        log_error(e, {'endpoint': 'generate-dax', 'data': data})
        
        # Auto-error recovery
        recovered_result = error_recovery.auto_recover(e, {'requirement': data.get('requirement', '')})
        return jsonify(recovered_result)

@app.route('/api/recommend-chart', methods=['POST'])
def recommend_chart():
    """Enhanced chart recommendation with ML analysis"""
    start_time = time.time()
    user_id = generate_user_id(request)
    
    try:
        data = request.get_json()
        is_valid, error_msg = validate_request(data)
        
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        dataset = data.get('dataset', [])
        
        # Use enhanced chart recommender
        result = enhanced_chart_recommender.analyze(dataset, user_id)
        
        execution_time = time.time() - start_time
        log_performance('recommend-chart', execution_time, True)
        
        return jsonify(result)
        
    except Exception as e:
        execution_time = time.time() - start_time
        log_performance('recommend-chart', execution_time, False, str(e))
        log_error(e, {'endpoint': 'recommend-chart', 'data': data})
        
        # Auto-error recovery
        recovered_result = error_recovery.auto_recover(e, {'dataset': data.get('dataset', [])})
        return jsonify(recovered_result)

@app.route('/api/generate-insights', methods=['POST'])
def generate_insights():
    """Enhanced AI insights with advanced analytics"""
    start_time = time.time()
    user_id = generate_user_id(request)
    
    try:
        data = request.get_json()
        is_valid, error_msg = validate_request(data)
        
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        dataset = data.get('dataset', [])
        
        # Use enhanced insight generator
        result = enhanced_insight_generator.analyze(dataset, user_id)
        
        execution_time = time.time() - start_time
        log_performance('generate-insights', execution_time, True)
        
        return jsonify(result)
        
    except Exception as e:
        execution_time = time.time() - start_time
        log_performance('generate-insights', execution_time, False, str(e))
        log_error(e, {'endpoint': 'generate-insights', 'data': data})
        
        # Auto-error recovery
        recovered_result = error_recovery.auto_recover(e, {'dataset': data.get('dataset', [])})
        return jsonify(recovered_result)

@app.route('/api/detect-anomalies', methods=['POST'])
def detect_anomalies():
    """Enhanced anomaly detection with multiple ML algorithms"""
    start_time = time.time()
    user_id = generate_user_id(request)
    
    try:
        data = request.get_json()
        is_valid, error_msg = validate_request(data)
        
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        dataset = data.get('dataset', [])
        
        # Use enhanced anomaly detector
        result = enhanced_anomaly_detector.detect(dataset, user_id)
        
        execution_time = time.time() - start_time
        log_performance('detect-anomalies', execution_time, True)
        
        return jsonify(result)
        
    except Exception as e:
        execution_time = time.time() - start_time
        log_performance('detect-anomalies', execution_time, False, str(e))
        log_error(e, {'endpoint': 'detect-anomalies', 'data': data})
        
        # Auto-error recovery
        recovered_result = error_recovery.auto_recover(e, {'dataset': data.get('dataset', [])})
        return jsonify(recovered_result)

@app.route('/api/forecast', methods=['POST'])
def forecast():
    """Enhanced forecasting with ensemble methods"""
    start_time = time.time()
    user_id = generate_user_id(request)
    
    try:
        data = request.get_json()
        is_valid, error_msg = validate_request(data)
        
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        dataset = data.get('dataset', [])
        horizon = data.get('horizon', 30)
        
        # Use enhanced forecasting model
        result = enhanced_forecasting_model.predict(dataset, horizon, user_id)
        
        execution_time = time.time() - start_time
        log_performance('forecast', execution_time, True)
        
        return jsonify(result)
        
    except Exception as e:
        execution_time = time.time() - start_time
        log_performance('forecast', execution_time, False, str(e))
        log_error(e, {'endpoint': 'forecast', 'data': data})
        
        # Auto-error recovery
        recovered_result = error_recovery.auto_recover(e, {
            'dataset': data.get('dataset', []),
            'horizon': data.get('horizon', 30)
        })
        return jsonify(recovered_result)

@app.route('/api/generate-sql', methods=['POST'])
def generate_sql():
    """Enhanced SQL generation with optimization"""
    start_time = time.time()
    user_id = generate_user_id(request)
    
    try:
        data = request.get_json()
        is_valid, error_msg = validate_request(data)
        
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        requirement = data.get('requirement', '').strip()
        
        # Use enhanced SQL generator
        result = enhanced_sql_generator.generate(requirement, user_id)
        
        execution_time = time.time() - start_time
        log_performance('generate-sql', execution_time, True)
        
        return jsonify(result)
        
    except Exception as e:
        execution_time = time.time() - start_time
        log_performance('generate-sql', execution_time, False, str(e))
        log_error(e, {'endpoint': 'generate-sql', 'data': data})
        
        # Auto-error recovery
        recovered_result = error_recovery.auto_recover(e, {'requirement': data.get('requirement', '')})
        return jsonify(recovered_result)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check with system status"""
    try:
        # Check system components
        system_status = {
            'api_status': 'healthy',
            'security_manager': 'active',
            'error_recovery': 'active',
            'ai_models': 'active',
            'timestamp': datetime.now().isoformat(),
            'version': '3.0.0',
            'features': [
                'Enhanced DAX Generation',
                'ML-based Chart Recommendation',
                'Advanced AI Insights',
                'Multi-algorithm Anomaly Detection',
                'Ensemble Forecasting',
                'Optimized SQL Generation',
                'Enterprise Security',
                'Auto Error Recovery'
            ]
        }
        
        # Add performance metrics summary
        if performance_metrics:
            system_status['performance_summary'] = {
                endpoint: {
                    'total_requests': len(metrics),
                    'success_rate': sum(1 for m in metrics if m['success']) / len(metrics),
                    'avg_execution_time': sum(m['execution_time'] for m in metrics) / len(metrics)
                }
                for endpoint, metrics in performance_metrics.items()
            }
        
        return jsonify(system_status)
        
    except Exception as e:
        log_error(e, {'endpoint': 'health-check'})
        return jsonify({
            'status': 'degraded',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/system-status', methods=['GET'])
def system_status():
    """Get detailed system status and metrics"""
    try:
        status = {
            'performance_metrics': performance_metrics,
            'recent_errors': error_log[-10:] if error_log else [],
            'security_status': {
                'encryption_active': True,
                'rate_limiting_active': True,
                'token_validation_active': True
            },
            'ai_models_status': {
                'dax_generator': 'active',
                'chart_recommender': 'active',
                'insight_generator': 'active',
                'anomaly_detector': 'active',
                'forecasting_model': 'active',
                'sql_generator': 'active'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(status)
        
    except Exception as e:
        log_error(e, {'endpoint': 'system-status'})
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    log_error(error, {'endpoint': 'internal_error'})
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(error):
    log_error(error, {'endpoint': 'unhandled_exception'})
    return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
