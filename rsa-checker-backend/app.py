import os
from flask import Flask, request, send_from_directory
from flask_restx import Api, Resource, fields
from datetime import datetime
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Unofficial RSA Driving Test Booking Checker API',
    description='API for finding out when you can book your RSA driving test')

ns = api.namespace('api', description='Test Center operations')

# Load data
with open('data.json') as f:
    data = json.load(f)

# Define models
test_center = api.model('TestCenter', {
    'Test Centre': fields.String(required=True, description='Name of the test center'),
    'Expected Invite': fields.String(required=True, description='Expected invite date'),
    'Last Updated': fields.String(required=True, description='Last update date')
})

# Parser for query parameters
parser = api.parser()
parser.add_argument('search', type=str, help='Search string for test centers')
parser.add_argument('sort', type=str, choices=('az', 'date'), help='Sort method')
parser.add_argument('order', type=str, choices=('asc', 'desc'), help='Sort order')

@ns.route('/test-centers')
class TestCenterList(Resource):
    @api.doc(parser=parser)
    @api.marshal_list_with(test_center)
    def get(self):
        """List all test centers"""
        args = parser.parse_args()
        search = args['search'].lower() if args['search'] else ''
        sort = args['sort'] or 'az'
        order = args['order'] or 'asc'

        filtered_data = [center for center in data if search in center['Test Centre'].lower()]

        if sort == 'date':
            filtered_data.sort(key=lambda x: datetime.strptime(x['Expected Invite'], '%m/%d/%Y %I:%M:%S %p'), 
                               reverse=(order == 'desc'))
        else:
            filtered_data.sort(key=lambda x: x['Test Centre'], reverse=(order == 'desc'))

        return filtered_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)