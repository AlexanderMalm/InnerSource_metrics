from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from visibility import get_visibility
from Checks import get_checks
from availability import get_document_availability
from timeToClose import get_time_to_close
from repoitoriesOfTeams import get_repositories, get_team
import os

def combine_data(team_name, availability, visibility, time_to_close, checks, num_repos):
    combined_dict = {
        "Team_name": team_name,
        "Number_repos": num_repos,
        "availability": availability,
        "visibility": visibility,
        "time_to_close": time_to_close,
        "checks": checks
    }

    return combined_dict

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'test'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

days = 90
api_token1 = os.environ.get('GH_TOKEN')


@app.errorhandler(Exception)
def handle_error(e):
    return jsonify(error=str(e)), 500

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/getTeam', methods=['POST'])
def getTeam():
    key = request.json['key']
    print(request.json)
    team = get_team(api_token1, key)
    if team:
        return jsonify({"Team_name": key}), 200
    else:
        return jsonify({"error": "Team not found"}), 404
    
@app.route('/static/<path:path>')
def send_html(path):
    return send_from_directory('static', path)

@app.route('/getRepos', methods=['POST'])
def getRepos():
    key = request.json['key']
    repositories = get_repositories(api_token2, key)
    session['repositories'] = repositories
    repoToClient = [repo.replace('https://github.com/ingka-group-digital/', '') for repo in repositories]
    
    return jsonify({"Team_name": key, "repositories": repoToClient}), 200

@app.route('/process', methods=['POST'])
def process():
    key = request.json['key']
    repositories = request.json['repositories']

    print("Getting visibility")
    visibility = get_visibility(api_token1, repositories)
    print("Getting ttc")
    ttc = get_time_to_close(api_token1, repositories, days)
    print("Getting availability")
    availability = get_document_availability(api_token2, repositories)
    print("Getting checks")
    checks = get_checks(api_token2, repositories, days)

    combined_data = combine_data(key, availability, visibility, ttc, checks, len(repositories))
    print(combined_data)
    return jsonify(combined_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
