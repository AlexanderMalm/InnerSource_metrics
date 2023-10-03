import requests
import json

def get_visibility(api_token, repositories):
    print(f"\n {repositories} \n")
    headers = {'Authorization': f'token {api_token}', 'Accept': 'application/vnd.github+json'}

    output_data = {
        "forks": 0,
        "stars": 0,
        "watchers": 0,
        "low_visibility": {},
        "high_visibility": {}
    }

    for repo in repositories:
       # print(repo)
       
        print(f"  Processing repo: {repo}")

        repo_info_url = f'https://api.github.com/repos//{repo}' #needs correct endpoint
        response = requests.get(repo_info_url, headers=headers)
      
        if response.status_code == 200:
            repo_info = response.json()
            forks = repo_info['forks_count']
            stars = repo_info['stargazers_count']
            watchers = repo_info['subscribers_count']

            output_data["forks"] += forks
            output_data["stars"] += stars
            output_data["watchers"] += watchers

            total_visibility = forks + stars + watchers

            if total_visibility < 5:
                output_data["low_visibility"][repo] = total_visibility
            if total_visibility > 15:
                output_data["high_visibility"][repo] = total_visibility

    return output_data