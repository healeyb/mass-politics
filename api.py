import os
import json
import markdown2
from markdown_it import MarkdownIt

from support import SupportService
from flask import Flask, make_response, request

from openai import OpenAI
client = OpenAI()

from dotenv import load_dotenv
load_dotenv(override=True)

app = Flask(__name__)
support_service = SupportService()

def jsonify(output, status=200, indent=4, sort_keys=True):
    response = make_response(json.dumps(output, indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "OK",
        "message": "API is operational"
    }, status=200)

@app.route('/latest', methods=['GET'])
def search():
    output = support_service.compose_language()
    if output:
        return jsonify(output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ["API_PORT"])