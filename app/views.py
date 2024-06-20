from flask import render_template, request, jsonify
from app import app, db
from app.controllers.ide import *
from app.src.af_interface import AzureFunctionInterface  
from .models import Problem, Submission, User

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
    try:
        data = request.get_json()
        code_text = data.get('code_text')
        problem_id = data.get('problem_id')
        user_id = '444D6FB7-FAE7-4472-8B2C-B34135634633' 

        short_problem_id = problem_id[:8]
        # Call the Azure function to execute the code
        response = azure_interface.execute(code_text, short_problem_id)
        
        # Retrieve the problem from the database
        problem = Problem.query.filter_by(id=problem_id).first()
        if problem is None:
            return jsonify({"error": "Problem not found"}), 404
        
        # Retrieve the user from the database
        user = User.query.filter_by(userId=user_id).first()
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Increment totalSubmissions for both Problem and User
        problem.totalSubmissions += 1
        user.totalSubmissions += 1

        # If the Azure function returned a successful response, increment successfulSubmissions
        #print(response)
        
        if "PASS" in response:
            problem.successfulSubmissions += 1
            user.successfulSubmissions += 1

        # Commit the changes to the database
        db.session.commit()

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

@app.route('/api/users/<userId>', methods=['GET'])
def get_user_profile(userId):
    try:
        # Retrieve the user from the database
        user = User.query.filter_by(userId=userId).first()
        if user is None:
            return jsonify({"error": "User not found"}), 404
        
        # Format the user information into a dictionary
        user_info = {
            "userId": user.userId,
            "username": user.username,
            "email": user.email,
            "totalSubmissions": user.totalSubmissions,
            "successfulSubmissions": user.successfulSubmissions
        }
        return jsonify(user_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/problems/<problemId>/acceptance', methods=['GET'])
def get_problem_acceptance_rate(problemId):
    try:
        # Retrieve the problem from the database
        problem = Problem.query.filter_by(id=problemId).first()
        if problem is None:
            return jsonify({"error": "Problem not found"}), 404
        
        # Calculate the acceptance rate
        if problem.totalSubmissions == 0:
            acceptance_rate = 0.0
        else:
            acceptance_rate = (problem.successfulSubmissions / problem.totalSubmissions) * 100
        
        # Format the acceptance rate information into a dictionary
        acceptance_info = {
            "problemId": problem.id,
            "acceptanceRate": acceptance_rate,
            "totalSubmissions": problem.totalSubmissions,
            "successfulSubmissions": problem.successfulSubmissions
        }
        return jsonify(acceptance_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
