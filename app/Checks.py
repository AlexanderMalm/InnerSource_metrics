import requests
from datetime import datetime, timedelta

def get_checks(api_token, repositories, days):
    headers = {'Authorization': f'token {api_token}', 'Accept': 'application/vnd.github+json'}
    output_data = {}
    average_checks_low = {}
    average_checks_high = {}
    failcheck_ratio_high = {}
    failcheck_ratio_low = {}

    project_total_ratios = 0
    project_num_prs = 0
    project_total_checks = 0
    days_ago = datetime.now() - timedelta(days)

    for repo in repositories:
        repo = repo.split('/')[-1]
        print(f"  Processing repo: {repo}\n")

        page = 1
        has_more_data = True
        
        total_ratios = 0
        num_prs = 0
        total_checks = 0

        while has_more_data:
            has_more_data = False

            pulls_url = f'https://api.github.com/repos//{repo}/pulls' #needs a correct endpoint
            
            params = {
                'state': 'closed',
                'sort': 'updated',
                'direction': 'desc',
                'per_page': 100,
                'page': page,
            }

            response = requests.get(pulls_url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch data from {pulls_url}. HTTP status code: {response.status_code}, Message: {response.json()}")
                break
            
            pulls = response.json()

            for pull in pulls:
                closed_at = datetime.strptime(pull['closed_at'], '%Y-%m-%dT%H:%M:%SZ')
                
                if closed_at < days_ago:
                    continue

                has_more_data = True  
                
                if pull['merged_at'] is not None:
                    num_prs += 1
                    
                    commit_sha = pull['head']['sha']

                    check_runs_url = f'https://api.github.com/repos/ingka-group-digital/{repo}/commits/{commit_sha}/check-runs?per_page=100'
                    response = requests.get(check_runs_url, headers=headers)
                    check_runs = response.json()['check_runs']

                    passed_checks = 0
                    failed_checks = 0
                    cancelled_checks = 0

                    for check_run in check_runs:
                        if check_run['conclusion'] == 'success':
                            passed_checks += 1
                        elif check_run['conclusion'] == 'failure':
                            failed_checks += 1
                        elif check_run['conclusion'] == 'cancelled':
                            cancelled_checks += 1

                    total_checks += passed_checks + failed_checks + cancelled_checks

                    if passed_checks + failed_checks + cancelled_checks > 0:
                        ratio = (failed_checks + cancelled_checks) / (total_checks)
                        total_ratios += ratio
                        

            page += 1

        project_total_ratios += total_ratios
        project_num_prs += num_prs
        project_total_checks += total_checks

        if num_prs > 0:
            average_checks = total_checks / num_prs
            if average_checks < 5:
                average_checks_low[repo] = round(average_checks,1)
            if average_checks > 15:
                average_checks_high[repo] = round(average_checks, 1)

            failcheck_ratio = total_ratios / num_prs
            if failcheck_ratio < 0.003:
                failcheck_ratio_low[repo] = round(failcheck_ratio, 2)
            if failcheck_ratio > 0.04:
                failcheck_ratio_high[repo] = round(failcheck_ratio, 2)

        else:
            print(f"No merged PRs found in the last {days} days.")
     
   

    output_data["average_failcheck_ratio"] = round(project_total_ratios / project_num_prs, 2) if project_num_prs > 0 else 0
    output_data["average_number_of_checks"] = round(project_total_checks / project_num_prs,1) if project_num_prs > 0 else 0
    output_data["total_merged_prs"] = project_num_prs
    output_data["average_checks_low"] = average_checks_low
    output_data["average_checks_high"] = average_checks_high
    output_data["failcheck_ratio_low"] = failcheck_ratio_low
    output_data["failcheck_ratio_high"] = failcheck_ratio_high

    #output_data["average_failcheck_ratio"] = round(output_data["average_failcheck_ratio"], 2)
    #output_data["average_number_of_checks"] = round(output_data["average_number_of_checks"], 1)
    return output_data
