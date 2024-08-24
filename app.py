import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

with open('data.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', initial_data=data)

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(directory=app.root_path, path='sitemap.xml', mimetype='application/xml')

@app.route('/api/test-centers')
def get_test_centers():
    search = request.args.get('search', '').lower()
    sort = request.args.get('sort', 'az')
    order = request.args.get('order', 'asc')

    filtered_data = [center for center in data if search in center['Test Centre'].lower()]

    if sort == 'date':
        filtered_data.sort(key=lambda x: datetime.strptime(x['Expected Invite'], '%m/%d/%Y %I:%M:%S %p'), reverse=(order == 'desc'))
    else:
        filtered_data.sort(key=lambda x: x['Test Centre'], reverse=(order == 'desc'))

    return jsonify(filtered_data)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    print(f"Debug mode is {'ON' if debug_mode else 'OFF'}")

    app.run(debug=debug_mode)
