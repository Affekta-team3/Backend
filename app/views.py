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

@app.route('/api/problems', methods=['GET'])
def get_all_problems():
    try:
        # Retrieve all problems from the database
        problems = Problem.query.all()
        # Format the problems into a list of dictionaries
        problems_list = [{
            "problem_id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "input_format": problem.input_format,
            "output_format": problem.output_format,
            "difficulty": problem.difficulty
        } for problem in problems]
        return jsonify(problems_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

