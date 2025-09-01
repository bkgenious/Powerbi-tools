from waitress import serve
from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server...")
    print(f"You can access the application at:")
    print(f"* Local:            http://localhost:{port}")
    print(f"* On Your Network:  http://127.0.0.1:{port}")
    serve(app, host='0.0.0.0', port=port, threads=4, url_scheme='http')
