const URL = 'https://innersource-rcxwl5mx5a-ew.a.run.app'

function showLoader() {
    var loader = document.createElement('div');
    loader.className = 'loader';
    document.body.appendChild(loader);
  }

window.addEventListener('load', function () {
    const form = document.getElementById('text-form');
    const input = document.getElementById('user-input');
    const main = document.getElementById('main');
    const errorMessage = document.getElementById('error-message');

    const fetchingMessage = document.createElement('p');
    fetchingMessage.id = 'fetching-message';
    main.before(fetchingMessage);
    
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        main.innerHTML = '';
        errorMessage.innerHTML = '';

        const team = input.value;
        input.value = '';

        fetchingMessage.textContent = `Fetching ${team} repositories...`;
        form.style.display = 'none';

        axios.post(`${URL}/getTeam`, {
            key: team
        }, { withCredentials: true })  
        .then((response) => {
            return axios.post(`${URL}/getRepos`, {
                key: team,
                
            }, { withCredentials: true });
        })
        .then((response) => {
            fetchingMessage.textContent = `Found repositories for ${team}:`;

            const repos = response.data.repositories;

            const checkboxes = document.createElement('div');
            checkboxes.id = 'checkboxes';

            repos.forEach((repo) => {
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = repo;
                checkbox.id = repo;
                checkbox.checked = true; 

                const label = document.createElement('label');
                label.htmlFor = repo;
                label.textContent = repo;

                checkboxes.appendChild(checkbox);
                checkboxes.appendChild(label);
                checkboxes.appendChild(document.createElement('br'));
            });

            const submitButton = document.createElement('button');
            submitButton.textContent = 'Process selected repositories';
            submitButton.addEventListener('click', function () {
                const checkboxes = document.getElementById('checkboxes').getElementsByTagName('input');
                const selectedRepos = [];

                for (let i = 0; i < checkboxes.length; i++) {
                    if (checkboxes[i].checked) {
                        selectedRepos.push(checkboxes[i].value);
                    }
                }

                document.getElementById('checkboxes').style.display = 'none';
                fetchingMessage.textContent = 'Fetching repo data...';
                
                showLoader();
                axios.post(`${URL}/process`, {
                    key: team,
                    repositories: selectedRepos
                }, { withCredentials: true })
                .then((response) => {
                   
                    sessionStorage.setItem('team', JSON.stringify(response.data));
                    window.location.href = 'static/result_page.html';
                })
                .catch((error) => {
                    console.log('Error:', error);
                });
            });

            checkboxes.appendChild(submitButton);

            fetchingMessage.appendChild(checkboxes);
        })
        .catch((error) => {
            if (error.response) {
                if (error.response.status === 404) {
                    errorMessage.textContent = 'Team not found. Please try another team name.';
                } else {
                    errorMessage.textContent = 'There was an error: ' + error.response.status;
                }
            } else if (error.request) {
                errorMessage.textContent = 'Server is not responding. ';
            } else {
                errorMessage.textContent = 'An unexpected error occurred: ' + error.message;
            }
            console.log('Error:', error);
            form.style.display = 'block';
            fetchingMessage.textContent = '';
        });
    });
});