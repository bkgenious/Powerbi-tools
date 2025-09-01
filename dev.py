from app import app

if __name__ == '__main__':
    try:
        print("Starting development server on http://0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        import sys
        sys.exit(1)
