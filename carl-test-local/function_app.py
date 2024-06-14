import logging
import azure.functions as func
import subprocess
from azure.functions.decorators.core import DataType
import uuid
import json
import os
import random


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="codeExecute/{sample_path}")
@app.blob_input(arg_name="inputblob",
                path="problem-samples/{sample_path}",
                connection="AzureWebJobsStorage")
def codeExecute(req: func.HttpRequest, inputblob: str) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    code_text = req.params.get('code_text')
    if not code_text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            code_text = req_body.get('code_text')

    if code_text:
        file_path = f"/tmp/code_{random.randint(0,99)}.py"

        # Write the code to a .py file
        with open(file_path, "w") as code_file:
            code_file.write(code_text)
            code_file.write("\n")
            code_file.write(inputblob)
            code_file.write("\n")


        # Execute the .py file and capture the output
        try:
            result = subprocess.run(["python3", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            output = result.stdout
            print(output)
        except subprocess.CalledProcessError as e:
            output = e.stderr
            print(output)
        finally:
            if os.path.exists(file_path):
                            os.remove(file_path)
                            logging.info(f"File {file_path} deleted")
        # Return the output as the response
        return func.HttpResponse(output, status_code=200)
    else:
        return func.HttpResponse(
            "Please pass a code parameter in the query string or in the request body",
            status_code=400
        )

# @app.route(route="codeExecute/{sample_path}")
# @app.blob_input(arg_name="inputblob",
#                 path="problem-samples/{sample_path}",
#                 connection="AzureWebJobsStorage")
# def codeExecute(req: func.HttpRequest, inputblob: str) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')
#
#     code_text = req.params.get('code_text')
#     if not code_text:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             code_text = req_body.get('code_text')
#
#     if code_text:
#         file_path = f"/tmp/code_{random.randint(0,99)}.py"
#
#         # Write the code to a .py file
#         with open(file_path, "w") as code_file:
#             logging.info(f"File {file_path} created")
#             code_file.write(code_text)
#             code_file.write("\n")
#             code_file.write(inputblob)
#             code_file.write("\n")
#
#         process = None
#         # Execute the .py file and capture the output
#         try:
#             interpreter = ".venv/bin/python"
#             # result = subprocess.run(["python3", file_path], capture_output=True, text=True, check=True)
#             process = subprocess.run([interpreter, file_path], capture_output=True, text=True, check=True)
#             output = process.stdout
#             print(output)
#         except subprocess.CalledProcessError as e:
#             output = e.stderr
#             print(output)
#         finally:
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#                 logging.info(f"File {file_path} deleted")
#
#         # Return the output as the response
#         return func.HttpResponse(output, status_code=200)
#     else:
#         return func.HttpResponse(
#             "Please pass a code parameter in the query string or in the request body",
#             status_code=400
#         )


@app.route(route="getProblem/{problemId}", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_input_binding(arg_name="problemItems", type="sql", CommandText="SELECT * FROM dbo.problem WHERE id = @problemId", parameters="@problemId={problemId}", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def getProblem(req: func.HttpRequest, problemItems: func.SqlRowList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    rows = list(map(lambda r: json.loads(r.to_json()), problemItems))[0]

    return func.HttpResponse(
        json.dumps(rows),
        status_code=200,
        mimetype="application/json"
    )


@app.route(route="getSubmission/{submissionId}", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_input_binding(arg_name="submissionItems", type="sql", CommandText="SELECT * FROM dbo.submission WHERE id = @submissionId", parameters="@submissionId={submissionId}", ConnectionStringSetting="SqlConnectionString", data_type=DataType.STRING)
def getSubmission(req: func.HttpRequest, submissionItems: func.SqlRowList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    rows = list(map(lambda r: json.loads(r.to_json()), submissionItems))[0]

    return func.HttpResponse(
        json.dumps(rows),
        status_code=200,
        mimetype="application/json"
    )


@app.route(route="insertSubmission", auth_level=func.AuthLevel.ANONYMOUS)
@app.generic_output_binding(arg_name="submissionItems", type="sql", CommandText="dbo.submission", ConnectionStringSetting="SqlConnectionString",data_type=DataType.STRING)
def insertSubmission(req: func.HttpRequest, submissionItems: func.Out[func.SqlRow]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # {"problemId": "387793d1-cd6a-43a4-962b-94afedb8d0c4", "codeText": "sample code", "status": 0, "result": "", "runtime": 1, "memory": 1}

    query = req.get_json()
    query.update({"Id": str(uuid.uuid4())})
    print(query.get('problemId'))

    if submissionItems:
        submissionItems.set(func.SqlRow(query))
        return func.HttpResponse(f"source code inserted for problem {query.get('problemId')}")
    else:
        return func.HttpResponse(
                    "Please pass a name on the query string or in the request body",
                    status_code=400
                )

