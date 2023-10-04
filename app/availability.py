import datetime 
import re
import requests
import json
import numpy as np

GITHUB_API_URL = "https://api.github.com"

def get_repo_contents(api_token, repo, path=''):
    headers = {'Authorization': f'token {api_token}', 'Accept': 'application/vnd.github+json'}
    url = f'{GITHUB_API_URL}//{repo}/contents/{path}' #needs changes to a correct endpoint
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def check_documents_and_links(contents, file_name):
    scores = {}
    if contents:
        for content in contents:
            if content['name'].lower().rstrip('.md') == file_name.lower().rstrip('.md'):
                scores[file_name] = 1
                if file_name == 'readme.md':
                    readme_response = requests.get(content['download_url'])
                    if readme_response.status_code == 200:
                        readme_content = readme_response.text
                        scores['documentation_link'] = int(re.search(r'\[.*\]\(https?://.*\)', readme_content) is not None)
    return scores

def calculate_total_score(file_scores, link_scores):
    combined_scores = {**file_scores, **link_scores}
    total_score = sum(combined_scores.values())

    return total_score

def get_document_availability(api_token, repositories):
    file_names = ['license.md', 'licence.md', 'readme.md', 'contributing.md', 'pull_request_template.md', 'codeowners']
    all_scores = []

    high_availability_repos = {}
    low_availability_repos = {}

    for repo in repositories:
        
        contents = get_repo_contents(api_token, repo)
        github_contents = get_repo_contents(api_token, repo, '.github')

        file_scores = {}
        
        link_scores = {}

        for file_name in file_names:
            file_scores.update(check_documents_and_links(contents, file_name))
            link_scores.update(check_documents_and_links(github_contents, file_name))

        total_score = calculate_total_score(file_scores, link_scores)
        all_scores.append(total_score)

        if total_score >= 3:
            high_availability_repos[repo] = total_score
        elif total_score <= 3:
            low_availability_repos[repo] = total_score

    average_score = round(np.mean(all_scores), 1)
    
    return {"average_avail_score": average_score, "high_availability": high_availability_repos, "low_availability": low_availability_repos}
