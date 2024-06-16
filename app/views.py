from flask import render_template, request, jsonify
from app import app
from app.controllers.ide import *
from app.src.af_interface import AzureFunctionInterface  
from .models import Problem

# Initialize the AzureFunctionInterface
azure_interface = AzureFunctionInterface()

@app.route('/')
def index():
    # Test database connection
    try:
        # Try to query the database
        return f"Hello, this is the backend! Database connected successfully. Number of problems: "
    except Exception as e:
        return f"Hello, this is the backend! Database connection failed: {str(e)}"

@app.route('/api/problems/<problem_id>', methods=['GET'])
def get_problem(problem_id):
    response = azure_interface.get_data('problem', problem_id)
    return jsonify(response)

@app.route('/api/submissions', methods=['POST'])
def submit_code():
    data = request.get_json()
    response = azure_interface.insert_submission(data)
    return jsonify(response)

@app.route('/api/submissions/<submission_id>', methods=['GET'])
def get_submission(submission_id):
    response = azure_interface.get_data('submission', submission_id)
    return jsonify(response)

@app.route('/api/evaluate', methods=['POST'])
def evaluate_submission():
    data = request.get_json()
    code_text = data.get('code_text')
    problem_id = data.get('problem_id')
    response = azure_interface.execute(code_text, problem_id)
    return jsonify(response)
'''
@app.route('/api/animations/accepted', methods=['POST'])
def trigger_accept_animation():
    data = request.get_json()
    response = trigger_animation(data)
    return jsonify(response)

@app.route('/api/hints/<submission_id>', methods=['GET'])
def get_submission_hints(submission_id):
    response = get_hints(submission_id)
    return jsonify(response)
'''
