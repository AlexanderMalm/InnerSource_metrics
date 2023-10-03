import requests
import datetime

GITHUB_ENTERPRISE_URL = "https://api.github.com"  

def get_team(api_token, team_name):
    team_id = get_team_id(api_token, team_name)
    if team_id is None:
        return False
    else:
        return True


def get_team_id(api_token, team_name):
    headers = {'Authorization': f'token {api_token}', 'Accept': 'application/vnd.github+json'}
    page = 1
   
    while True:
        url = f"{GITHUB_ENTERPRISE_URL}/orgs//teams?per_page=100&page={page}" #needs correct endpoint
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching teams: {response.status_code}")
            return None
        team_batch = response.json()
        if not team_batch:
            break
        for team in team_batch:
            if team["name"].lower() == team_name.lower():
                return team["id"]
        page += 1
    print(f"Team '{team_name}' not found")
    return None

def get_repositories(api_token, team_name):
    
    team_id = get_team_id(api_token, team_name)
    if team_id is None:
        return None

    headers = {'Authorization': f'token {api_token}', 'Accept': 'application/vnd.github+json'}
    all_repos = []
    page = 1

    one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

    while True:
        url = f"{GITHUB_ENTERPRISE_URL}/teams/{team_id}/repos?per_page=100&page={page}"
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            return None
        repo_batch = response.json()
        if not repo_batch:
            break
       
        for repo in repo_batch:
            print(repo['html_url'])
            #print("vafan!!")main_branch_url = f"{GITHUB_ENTERPRISE_URL}/repos/{repo['full_name']}/branches/main"
            #main_branch_response = requests.get(main_branch_url, headers=headers)
            #if main_branch_response.status_code != 200:
           #     print("vafan0")
          #      continue
            pull_requests_url = f"{GITHUB_ENTERPRISE_URL}/repos/{repo['full_name']}/pulls?state=all"
            pull_requests_response = requests.get(pull_requests_url, headers=headers)
            if pull_requests_response.status_code != 200:
                
                continue
            pull_requests = pull_requests_response.json()
            if len(pull_requests) <= 1:
               
                continue
          #  last_updated = datetime.datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
          #  if last_updated < one_year_ago:
           #     print("vafan3")
            #    continue
            all_repos.append(repo['html_url'])
        page += 1
    return all_repos