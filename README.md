## Purpose of application

An Inner source self assessment application based on the results from Alexanders Malm's thesis work 2023, deployed on GCP. IKEA-specific data and information have been deleted. The current values of the identidied outlier metrics are psuedo-randomly chosen.

A proof of concept for anInner source self assessment application based on the results from Alexanders Malm's thesis work 2023, initially deployed on GCP. IKEA-specific data and information have been deleted. The current values of the identidied outlier metrics are psuedo-randomly chosen. Based on the finding during the thesis work at IKEA https://lup.lub.lu.se/student-papers/search/publication/9120709.
>>>>>>> refs/remotes/origin/master

Developed after the thesis was finished, so the front-end is a bit sloppy but it serves the purpose. The app calculates a team's total metric scores as well as identifies repositores with characteristics that might indicate protential or problems for an inner sourced development. The outlier treshholds are based on the data gathered from the repositories of the 6 teams interviewed for the thesis.

Currently built for enterprise GitHub usage. 

Plug-n-play, enter team name as specified on GitHub, select repositories, and get the results. Repositories that are not a part of a team can not be used for the analysis.  


## Installation 

The app can easily be run locally by running Docker and creating an image of the dockerfile. To install and run the Docker image, use the following command:

```bash
docker run -p 8080:8080 -e API_TOKEN1=:GithubToken :imageName
```

To run on GCP, push the Docker image to GCP Artifact registry and deploy on Cloud run. Specifiy secret as the GitHub token and expose as env. 

**Improvement ideas** 

* For bigger teams it takes some time to gather the metrics time to close and GitHub Checks on merge - up to a couple of minutes. Threadpools using multiple tokens can  greatly speed up this process.
* If more metrics would be added, a new script accessing the correct GitHub api endpoint would need to be added, with smaller changes in app.py and resultscripts.js. 
* The limits for identified repositories can be changed. As mentioned above, the limits are based on the 6 interviewed team's data, and might need to be changed to better accomodate other teams.  

## Metrics used: 

- **Documentation Availability**: This metric assesses the availability of essential project documentation, inspired by the quantitative criteria of Engineering Baseline's ADR-EA-10 and OSPO’s recommended inner source documentation set. The total repository document set evaluated by this metric includes README files, License, Code owners, Contributing guidelines, and Pull_request_template. Additionally, the presence of links leading to further documentation contributes to the total score. Simple metric, the higher the better for inner source purposes. 
Simple metric, the higher the better. 

- **GitHub Check failrate on merge**: Measures informal test failure acceptance criteria of the teams by examining the rate of PRs with merged failed tests. It is derived by dividing the number of failed and cancelled jobs by the total number of jobs on merged PRs. Calculated for the last 90 days. A higher failrate might be acceptable within a closed development team who knows the inherent characteristics of their product and tests, an inner source project should aspire to maintain a low failure rate. An inner source project should aim for a low failrate while maintaining an effective and transparent test suite.

- **Time-to-close (h)**: Median time elapsed between the creation of a PR and its closure, either by merging or simply closed but not merged. Calculated for the last 90 days. A high time-to-close could imply potential challenges in team practices or engagement with GitHub processes. A very low time-to-close could signify a lack of thorough review process. A Transparent and efficient review process is crucial for an inner source project’s success, bad practices may deter contributions from outside the team.

- **Visibility**: This metric measures the level of engagement and interaction developers have with a repository, as indicated by the number of forks, stars, and watches a repository accumulates. A high number of forks could suggest the reusability of the code, as it shows that other teams are repurposing or testing the code for their own projects. Conversely, a high number of stars and watches can indicate active interest and monitoring of the repository's updates and activities, reflecting an environment of knowledge sharing. Simple metric, the higher the better for inner source purposes. 

  



