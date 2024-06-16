import requests
from config import Config

def receive_code(data):
    code = data['sourceCode']
    language_id = data['language']
    problem_id = data['problemId']
    user_id = data['userId']
    submission_data = {
        'source_code': code,
        'language_id': language_id,
        'problem_id': problem_id,
        'user_id': user_id
    }
    response = requests.post(f"{Config.JUDGE0_API_URL}/submissions", json=submission_data)
    return response.json()

def evaluate_code(data):
    submission_id = data['submissionId']
    source_code = data['sourceCode']
    language_id = data['language']
    problem_id = data['problemId']
    evaluate_data = {
        'submission_id': submission_id,
        'source_code': source_code,
        'language_id': language_id,
        'problem_id': problem_id
    }
    response = requests.post(f"{Config.JUDGE0_API_URL}/evaluate", json=evaluate_data)
    return response.json()

def get_problem_details(problem_id):
    response = requests.get(f"{Config.JUDGE0_API_URL}/problems/{problem_id}")
    return response.json()

def get_submission_status(submission_id):
    response = requests.get(f"{Config.JUDGE0_API_URL}/submissions/{submission_id}")
    return response.json()

def trigger_animation(data):
    submission_id = data['submissionId']
    user_id = data['userId']
    animation_data = {
        'submission_id': submission_id,
        'user_id': user_id
    }
    response = requests.post(f"{Config.JUDGE0_API_URL}/animations/accepted", json=animation_data)
    return response.json()

def get_hints(submission_id):
    response = requests.get(f"{Config.JUDGE0_API_URL}/hints/{submission_id}")
    return response.json()
