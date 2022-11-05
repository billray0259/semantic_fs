const { app, net, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

const { ipcMain } = require('electron');

function createWindow () {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });

    ipcMain.handle('does-file-exist', (event, filePath) => {
        return new Promise((resolve, reject) => {
            fs.access(filePath, fs.constants.F_OK, (err) => {
                if (err) {
                    resolve(false);
                } else {
                    resolve(true);
                }
            });
        });
    });

    ipcMain.handle('launch-file', (event, filePath) => {
        console.log("launch-file event received");
        console.log(filePath);
    });

    const searchEndpoint = 'http://24.34.20.62:55889/search/';
    ipcMain.handle('search', (event, query, batch) => { // returns a promise and use net.request
        return new Promise((resolve, reject) => {
            const request = net.request({
                method: 'POST',
                url: searchEndpoint,
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            request.on('response', (response) => {
                let data = '';
                response.on('data', (chunk) => {
                    data += chunk;
                });
                response.on('end', () => {
                    resolve(data);
                });
            });

            request.write(JSON.stringify({
                batchId: batch,
                query: query
            }));
            request.end();
        }
    )});


    //     const xhr = new XMLHttpRequest(); // why does this throw "ReferenceError: XMLHttpRequest is not defined"? answer: because it's not a node module
    //     xhr.open('POST', searchEndpoint, true);
    //     xhr.setRequestHeader('Content-Type', 'application/json');
    //     xhr.send(JSON.stringify({
    //         "batchId": batch,
    //         "query": query
    //     }));
    //     return new Promise((resolve, reject) => {
    //         xhr.onload = function() {
    //             if (xhr.status === 200) {
    //                 resolve(xhr.response);
    //             } else {
    //                 reject(xhr.status);
    //             }
    //         };
    //     });
    // });

    win.loadFile('search.html');

    // open dev tools
    win.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
