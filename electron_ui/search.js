const {ipcRenderer} = require('electron');

const {fs} = require('fs-extra');

document.getElementById("search").addEventListener("click", search);


// POST /search/
//     {
//         "batchId": "1",
//         "query": "some text",
//         OPTIONAL:
//         "filepath": "pwd/",
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

const server = "http://24.34.20.62:55889/search/"

function search() {
    const query = document.getElementById("text-input").value;
    const batchId = document.getElementById("batch-id").value;
    // no filepath
    const data = {
        "batchId": batchId,
        "query": query,
    };
    
    // use jquery to send a post request to the server
    $.post(server, data, function(data, status) {
        console.log(data);
        console.log(status);
    });
    
    // ipcRenderer.send('read-file', filePath);

    // ipcRenderer.on('read-file-response', (event, fileContent) => {
    //     document.getElementById("title").innerHTML = fileContent;
    // });

    // ipcRenderer.send('write-file', filePath, textInput);
}