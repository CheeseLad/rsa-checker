from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

with open('data.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', initial_data=data)

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
    app.run(debug=True)