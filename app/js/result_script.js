window.addEventListener('load', function () {
    let teamData = JSON.parse(sessionStorage.getItem('team'));
    renderToolbar();
    renderData('total', teamData);
});

function renderToolbar() {
    let toolbar = document.getElementById('toolbar');
    let options = ['visibility', 'checks', 'time_to_close', 'availability', 'total'];

    options.forEach(option => {
        let button = document.createElement('button');

        
        let displayText = option.replace(/_/g, ' ');
        displayText = displayText.charAt(0).toUpperCase() + displayText.slice(1);
        button.textContent = displayText;

        button.addEventListener('click', function() {
            handleOptionClick(option, JSON.parse(sessionStorage.getItem('team')));
        });
        toolbar.appendChild(button);
    });

    let infoButton = document.createElement('button');
    infoButton.textContent = 'More Info';
    infoButton.addEventListener('click', function() {
        window.location.href = '/static/metricInfo.html';
    });
    toolbar.appendChild(infoButton);
}

function handleOptionClick(option, teamData) {
    renderData(option, teamData);
}


function renderData(dictionaryName, data) {
    let main = document.getElementById('main');
    main.innerHTML = '';

    let cardElement = document.createElement("div");
    cardElement.className = "card";

    let dataElement = document.createElement("div");

    let displayText = dictionaryName.replace(/_/g, ' ');
    displayText = displayText.charAt(0).toUpperCase() + displayText.slice(1);


    dataElement.innerHTML = `<h2>${displayText}</h2>`;

    if(dictionaryName != "total"){

        for (let key in data[dictionaryName]) {
            if (typeof data[dictionaryName][key] !== 'object') {
                let formattedKey = key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '); 
                let value = data[dictionaryName][key];

                
                dataElement.innerHTML += `<h3>${formattedKey}</h3>`;
                if (value === 0 || value === null || value === '' || value === 'None' || value === undefined) {
                    dataElement.innerHTML += `No repos could be used to gather ${formattedKey} data<br>`;
                } else {
                    dataElement.innerHTML += `${formattedKey}: ${value}<br>`;
                }
            }
        }
        
    
        for (let key in data[dictionaryName]) {
            if (typeof data[dictionaryName][key] === 'object') {
                let formattedKey = key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '); 
                dataElement.innerHTML += ` <h3>Repos with ${formattedKey}</h3>`;
              
                if (Object.keys(data[dictionaryName][key]).length === 0) {
                    dataElement.innerHTML += `No repos with ${formattedKey} found`;
                } else {
                    
                    for (let innerKey in data[dictionaryName][key]) {
                        dataElement.innerHTML += `${innerKey}: ${data[dictionaryName][key][innerKey]}<br>`;
                    }
                }
            }
        }

    
    } else {
        dataElement.innerHTML = `
        <h2>Visibility score:</h2>
        Forks: ${data.visibility.forks} <br>
        Stars: ${data.visibility.stars} <br>
        Watchers: ${data.visibility.watchers} <br>
        <h2>Check data:</h2>
        Average failcheck ratio: ${(data.checks.average_failcheck_ratio * 100)}% <br>
        Average number of checks: ${data.checks.average_number_of_checks} <br>
        Merged PR: ${data.checks.total_merged_prs} <br>
        <h2>time-to-close:</h2>
        Median: ${(data.time_to_close.median_time_to_close)} h <br> 
        Total PRs: ${data.time_to_close.total_closed_PRs} <br>
        <h2>Doc. availability:</h2>
        Average score: ${data.availability.average_avail_score} <br>
        Number of repositories: ${data.Number_repos}
        `;
    }

    cardElement.appendChild(dataElement);
    main.appendChild(cardElement);
}
