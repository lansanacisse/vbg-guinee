import os
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

API_URL = os.getenv('API_URL', 'http://localhost:8000')


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/form')
def form():
    """Rapport form page"""
    return render_template('form.html')


@app.route('/stats')
def stats():
    """Statistics page"""
    return render_template('stats.html')

@app.route('/profil')
def profil():
    "Connexion option for association"
    return render_template('profil.html')

@app.route('/who')
def why():
    "Who we are"
    return render_template('why.html')

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get reports from API"""
    try:
        headers = {'Authorization': f"Bearer {session.get('token')}"}
        response = requests.get(f'{API_URL}/api/v1/reports/', headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports', methods=['POST'])
def create_report():
    """Create new report"""
    try:
        data = request.json
        headers = {'Authorization': f"Bearer {session.get('token')}"}
        response = requests.post(f'{API_URL}/api/v1/reports/', json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics/latest', methods=['GET'])
def get_statistics():
    """Get latest statistics"""
    try:
        headers = {'Authorization': f"Bearer {session.get('token')}"}
        response = requests.get(f'{API_URL}/api/v1/statistics/latest/', headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=5000, debug=debug)