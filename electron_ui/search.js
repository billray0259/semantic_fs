


// window.addEventListener('DOMContentLoaded', () => {

function addFileLinkToResult(resultElement, filePath) {
    const title = resultElement.querySelector('.card-title');
    title.addEventListener('click', () => {
        // console.log(result.filepath);
        // send file name to launch-file event
        searchBridge.launchFile(filePath);
    });
    // title underline on hover
    title.addEventListener('mouseover', () => {
        title.style.textDecoration = 'underline';
    });

    title.addEventListener('mouseout', () => {
        title.style.textDecoration = 'none';
    });

    // add primary-text class to title
    title.classList.add('primary-text');

    // add pointer cursor to title
    title.style.cursor = 'pointer';
}


// On the page there are two text fields and a button.
// Query id="query"
// Batch id="batch"
// Button id="search"

// POST /search/
//     {
//         "batchId": "1",
//         "query": "some text"
//     }
// Return value:
//     {
//         "status": "ok",
//         "data": [
//             {
//                 "filepath": "pwd/file1",
//                 "text": "some text",
//                 "similarity": 22.11,
//             },
//             {
//                 "filepath": "pwd/file2",
//                 "text": "some text2",
//                 "similarity": 15.11,
//             },
//         ]
//     }

// ['batch_4827', 'batch_1561', 'batch_7051', 'batch_2152', 'batch_3471', 'batch_7619', 'batch_1074', 'batch_1088', 'batch_1377', 'batch_5665', 'batch_7541', 'batch_8538', 'batch_4720', 'batch_1886', 'batch_3023', 'batch_4538', 'batch_6217', 'batch_123']


document.getElementById('search').addEventListener('click', () => {
    const query = document.getElementById('query').value;
    const batch = document.getElementById('batch').value;

    console.log(query);
    searchBridge.search(query, batch).then((response) => {
        console.log(response);
        const searchResults = JSON.parse(response).data;
        const template = document.getElementById('result-template');
        const templateClone = template.content.cloneNode(true);
        const resultItem = templateClone.querySelector('.row');

        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        // add the template back
        resultsDiv.appendChild(template);

        searchResults.forEach((result) => {
            const resultClone = resultItem.cloneNode(true);

            resultClone.querySelector('.card-title').innerText = result.filepath.split('/').pop();
            resultClone.querySelector('.card-subtitle').innerText = result.filepath;
            resultClone.querySelector('.card-text').innerText = result.text;
            resultsDiv.appendChild(resultClone);

            // ipcRenderer.send('does-file-exist', result.filepath);
            // ipcRenderer.on('does-file-exist', (event, arg) => {
            //     if (arg) {
            //         addFileLinkToResult(resultClone, result.filepath);
            //     }
            // });
            searchBridge.doesFileExist(result.filepath).then((exists) => {
                if (exists) {
                    addFileLinkToResult(resultClone, result.filepath);
                }
            });
        });
    });

    // console.log(`Query: ${query}`);
    
    // from the html:
    // <template id="result-template">
    //     <div class="row">
    //         <div class="col-md-12">
    //             <div class="card">
    //                 <div class="card-body">
    //                     <a id="card-title-link"><h5 class="card-title"></h5></a>
    //                     <h6 class="card-subtitle mb-2 text-muted"></h6>
    //                     <p class="card-text"></p>
    //                 </div>
    //             </div>
    //         </div>
    //     </div>
    // </template>
});
// });