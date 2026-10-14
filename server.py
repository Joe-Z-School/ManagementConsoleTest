#!/usr/bin/env python3

from flask import Flask, jsonify, request, Response
import io
import argparse
import base64
import logParser
from pathlib import Path


# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

LOG_DIRECTORY = Path("./logs").resolve()

def getLogPath(filename):
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string")

    # Accept filenames only, not arbitrary paths.
    if filename != Path(filename).name or filename in (".", ".."):
        raise ValueError("Only log filenames are allowed")

    path = (LOG_DIRECTORY / filename).resolve()

    # Ensure the resolved path stays inside the log directory.
    if not path.is_relative_to(LOG_DIRECTORY):
        raise ValueError("Invalid log filename")

    return path

@app.route('/api/listStories', methods=['POST'])
def listStories():
    files = logParser.list_files(LOG_DIRECTORY, recursive=True)

    filenames = [Path(file).name for file in files]

    return jsonify({"files": filenames}),200


@app.route('/api/countWords', methods=['POST'])
def countWords():
    data = request.get_json()
    path = getLogPath(data.get("filename"))

    result = logParser.count_words(path)

    return jsonify({"filename": path.name, "word_count": result}), 200


@app.route('/api/wordSearch', methods=['POST'])
def wordSearch():
    data = request.get_json()
    path = getLogPath(data.get("filename"))
    word = data.get("word")
    recursive = data.get("recursive", False)
    case_sensitive = data.get("case_sensitive", False)

    result = logParser.search_word(path, word, recursive, case_sensitive)

    return jsonify({"filename": path.name, "matches": result}), 200


@app.route('/api/getModifiedDate', methods=['POST'])
def getModifiedDate():
    data = request.get_json()
    path = getLogPath(data.get("filename"))

    result = logParser.get_modified_date(path)

    return jsonify({"filename": path.name, "modified_date": result.isoformat()}), 200


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Flask REST server'
    )

    parser.add_argument(
        '-p', '--port',
        type=int,
        default=5000,
        help='Port on which to run the server (default: 5000)'
    )

    args = parser.parse_args()

    # Start Flask app
    app.run(host='0.0.0.0', port=args.port)
