import json
import requests
from datetime import datetime, timedelta
import numpy as np

def get_time_to_close(api_token, repositories, days):
    headers = {'Authorization': f'token {api_token}', 'Accept': 'application/vnd.github+json'}

    days = (datetime.utcnow() - timedelta(days))

    total_time_to_close = []
    pr_count = 0  
    
    fastPR = {}
    slowPR = {}

    for repo in repositories:   
       
        
        repo = repo.split('/')[-1]
        repo_time_to_close = []
         
        page = 1
        has_more_data = True

        while has_more_data:  
            has_more_data = False

           
            pulls_url = f"https://api.github.com/repos//{repo}/pulls" # needs correct endpoints
            params = {
                'state': 'closed',
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 100,
                'page': page,
            }

            response = requests.get(pulls_url, headers=headers, params=params)
            
         
            if response.status_code != 200:
                print(f"Error with status code: {response.status_code}, message: {response.text}")
                break

            pull_requests = response.json()
            
           
            if not isinstance(pull_requests, list):
                print(f"Unexpected response: {pull_requests}") 
                break

            for pr in pull_requests:
                
                has_more_data = True

                closed_at = datetime.strptime(pr['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                # If the pull request is open, skip it
                if pr['state'] == 'open' or closed_at is None or closed_at < days:
                    continue

                # Calculate time to close in seconds
                time_to_close = (closed_at - created_at).total_seconds()

                # Add time_to_close to the running totals
                total_time_to_close.append(time_to_close)  # Add to the list

                # Add time_to_close to repo_time_to_close
                repo_time_to_close.append(time_to_close)

                pr_count += 1

            page += 1

        # Calculate the average time to close for the repo
        if repo_time_to_close:
            median_repo_time_to_close = np.median(repo_time_to_close) / 3600  # Convert seconds to hours

            if median_repo_time_to_close < 0.003:
                fastPR[repo] = round(median_repo_time_to_close, 2)
            elif median_repo_time_to_close > 3:
                slowPR[repo] = round(median_repo_time_to_close, 2)

    project_data = {
       # "average_time_to_close": None,
        "median_time_to_close": None,
        "total_closed_PRs": pr_count
    }

    if total_time_to_close:
      #  average_project_time_to_close = round(sum(total_time_to_close) / len(total_time_to_close) /3600, 2)  # Convert seconds to hours
        median_project_time_to_close = round(np.median(total_time_to_close) / 3600,2)  # C onvert seconds to hours

      #  project_data["average_time_to_close"] = average_project_time_to_close
        project_data["median_time_to_close"] = median_project_time_to_close
        project_data["fast_PR"] = fastPR
        project_data["slow_PR"] = slowPR
        
    

    return project_data

