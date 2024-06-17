import requests


class AzureFunctionInterface(object):
    def __init__(self, service_url="https://carl-test.azurewebsites.net/api/"):
        self.service_url = service_url

    def execute(self, code_text, problem_id):
        path = f"codeExecute/{problem_id[: 8]}"
        response = requests.post(self.service_url + path, json={"code_text": code_text})
        return response.text

    def get_data(self, table_name, record_id):
        path = f"getProblem/{record_id}" if table_name == "problem" else f"getSubmission/{record_id}"
        response = requests.get(self.service_url + path)
        return response.text

    def insert_submission(self, record):
        path = f"insertSubmission"
        response = requests.post(self.service_url + path, json=record)
        return response.text


if __name__ == "__main__":
    url = "http://localhost:7071/api/"
    interface = AzureFunctionInterface()
    code_text = """
class Solution:
    def print_str(self, input_str):
        return f"Hello, {input_str}!"
    """
    res = interface.execute(code_text, "d5516315-3dec-4d7a-959b-021cfe99bae3")
    print(res)


