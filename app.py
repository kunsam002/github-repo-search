import os
from os.path import join, dirname
import json
from multiprocessing.pool import ThreadPool
from time import time as timer
from flask import Flask, request, render_template, jsonify
import requests
from datetime import date
import math
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__, template_folder='templates', static_folder='static')

base_search_url = 'https://api.github.com/search/repositories'


@app.context_processor
def main_context():
    """ Include some basic assets in the startup page """
    today = date.today()
    current_year = today.strftime('%Y')
    minimum = min

    return locals()


@app.route('/fetch_repo_details', methods=['POST'])
def fetch_repo_details():
    """
    fetch latest 3 commits, last fork and fork user's bio
    :param api_url:
    :return: payload structure json object of (commits, fork, forkOwnerBio)
    """

    if request.method == "GET":
        return jsonify({})

    _data = {}
    if request.data:
        _data = request.data
        _data = json.loads(_data)
    elif request.form:
        _data = json.dumps(request.form)
        _data = json.loads(_data)

    api_url = _data.get('apiUrl')
    results = {}

    commit_url = "{}/commits?per_page=3".format(api_url)
    fork_url = "{}/forks?per_page=1".format(api_url)

    header = {'username': os.environ.get('GitHub_USERNAME'), 'password': os.environ.get('GitHub_PASSWORD')}

    try:
        commit_resp = requests.get(commit_url, headers=header)
        commit_data = json.loads(commit_resp.content)
    except Exception as e:
        print('Error fetching commits ', e)
        commit_data = []
        pass

    if type(commit_data) == dict:
        results["commits"] = []
    else:
        results["commits"] = commit_data

    try:
        fork_resp = requests.get(fork_url, headers=header)
        fork_json_resp = json.loads(fork_resp.content)
    except Exception as e:
        print('Error fetching fork ', e)
        fork_json_resp = []
        pass

    fork_data = fork_json_resp[0] if len(fork_json_resp) >= 1 else None

    results["fork"] = fork_data
    fork_owner_bio = ""

    if fork_data:
        try:
            fork_owner_resp = requests.get(fork_data.get('url', ''), headers=header)
            fork_owner_data = json.loads(fork_owner_resp.content)
            fork_owner_bio = fork_owner_data.get("bio", None)
        except Exception as e:
            print('Error fetching fork user details ', e)
            fork_owner_bio = None
            pass

    results['fork_owner_bio'] = fork_owner_bio
    return jsonify(results)


@app.route('/')
def index():
    """
    :return: renders a template view of tablubar display showing repositories matching the search term
    """
    search_query = request.args.get('q', '')
    page = int(request.args.get('page', 1))

    results = dict(total_count=0, items=[])

    # query github repository using search term
    url_args = '?sort=stargazers_count&order=desc&page={}&per_page=10&q={}'.format(
        page, search_query)

    url = base_search_url + url_args

    headers = {'Accept': 'application/vnd.github.v3+json'}
    try:
        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            results = json.loads(resp.content)
    except Exception as e:
        print('Error connecting to GitHub search ', e)
        raise e

    total_count = int(results.get('total_count'))

    pages = int(math.ceil(float(total_count) / 10))

    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(debug=True)
