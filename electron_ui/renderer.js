
// window.addEventListener('DOMContentLoaded', () => {

function addFileLinkToResult(resultElement, filePath) {
    const title = resultElement.querySelector('.card-title');
    title.addEventListener('click', () => {
        // console.log(result.filepath);
        // send file name to launch-file event
        bridge.launchFile(filePath);
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


// id=upload-collapse expands when id=upload is clicked
const uploadButton = document.getElementById('upload');
const uploadCollapse = document.getElementById('upload-collapse');
uploadButton.addEventListener('click', () => {
    uploadCollapse.classList.toggle('show');
});

// when id=select-files is clicked, get file path from ipc open-file-dialog and update text of id=selected-file-path
const selectFilesButton = document.getElementById('select-files');
const selectedFilePath = document.getElementById('selected-file-path');
selectFilesButton.addEventListener('click', () => {
    bridge.openFileDialog().then((filePath) => {
        selectedFilePath.innerText = filePath;
    });
});

// when id=submit-upload is clicked, get file path from id=selected-file-path and text from id=batch-name
// call ipc upload-files with file path and batch name
const submitUploadButton = document.getElementById('submit-upload');
submitUploadButton.addEventListener('click', () => {
    const filePath = selectedFilePath.innerText;
    const batchName = document.getElementById('batch-name').value;
    bridge.uploadFiles(filePath, batchName);
});





document.getElementById('search').addEventListener('click', () => {
    const query = document.getElementById('query').value;
    const batch = document.getElementById('batch').value;

    console.log(query);
    bridge.search(query, batch).then((response) => {
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
            bridge.doesFileExist(result.filepath).then((exists) => {
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