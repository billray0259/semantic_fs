const { app, net, dialog, BrowserWindow } = require('electron');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const { ipcMain } = require('electron');

function createWindow () {
    const win = new BrowserWindow({
        width: 1600,
        height: 1200,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });

    // ipc search: seaches te endpoint for the query and batch, returns promise with results

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

    // ipc does-file-exist: checks if the file exists, returns promise with boolean

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

    // ipc launch-file: launches the file in native program, returns promise with boolean

    ipcMain.handle('launch-file', (event, filePath) => {
        return new Promise((resolve, reject) => {
            const command = `start "" "${filePath}"`;
            exec(command, (err, stdout, stderr) => {
                if (err) {
                    resolve(false);
                } else {
                    resolve(true);
                }
            });
        });
    });

    // ipc open-file-dialog: opens a file dialog, returns promise with file path

    ipcMain.handle('open-file-dialog', (event) => {
        return new Promise((resolve, reject) => {
            const result = dialog.showOpenDialogSync(win, {
                // select one file, multiple files, or directories
                properties: ['openFile', 'openDirectory']
            });
            if (result) {
                resolve(result);
            } else {
                resolve(null);
            }
        });
    });

    // ipc upload-files: given file path and batch name
    // if file path is a directory, recursively process all files in directory
    // if file path is a file, process the file
    // to process a file, check if the file is a .txt or .pdf
    // extract the text from the file and upload it to the endpoint
    // wait for the response before processing the next file
    // after every file upload, send a message to ipc file-uploaded with the file name and the percentage of files uploaded

    const uploadEndpoint = 'http://24.34.20.62:55889/data_upload/';
    ipcMain.handle('upload-files', (event, filePath, batchName) => {
        return new Promise((resolve, reject) => {
            const files = [];
            var filesUploadedCount = 0;

            const processFile = (filePath) => {
                const fileName = path.basename(filePath);
                const fileExtension = path.extname(filePath);
                if (fileExtension === '.txt' || fileExtension === '.pdf') {
                    fs.readFile(filePath, 'utf8', (err, data) => {
                        if (err) {
                            console.log(err);
                        } else {
                            // POST /data_upload/
                            // {
                            //     "data": [
                            //         {
                            //             "file": "pwd/file1",
                            //             "text": "some text",
                            //         },
                            //         {
                            //             "file": "pwd/file2",
                            //             "text": "some text2",
                            //         },
                            //     ],
                            //     "batchId": "batch1"
                            // }
                            const request = net.request({
                                method: 'POST',
                                url: uploadEndpoint,
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
                                    filesUploadedCount++;
                                    const percentage = filesUploadedCount / files.length;
                                    event.sender.send('file-uploaded', fileName, percentage);
                                    if (filesUploadedCount === files.length) {
                                        resolve(true);
                                    }
                                });
                            });

                            request.write(JSON.stringify({
                                data: [
                                    {
                                        file: filePath,
                                        text: data
                                    }
                                ]
                            }));
                            request.end();
                        }
                    });
                } else {
                    filesUploadedCount++;
                    const percentage = filesUploadedCount / files.length;
                    event.sender.send('file-uploaded', fileName, percentage);
                    if (filesUploadedCount === files.length) {
                        resolve(true);
                    }
                }
            };

            const processDirectory = (dirPath) => {
                fs.readdir(dirPath, (err, files) => {
                    if (err) {
                        console.log(err);
                    } else {
                        files.forEach((file) => {
                            const filePath = path.join(dirPath, file);
                            fs.stat(filePath, (err, stats) => {
                                if (err) {
                                    console.log(err);
                                } else {
                                    if (stats.isDirectory()) {
                                        processDirectory(filePath);
                                    } else {
                                        processFile(filePath);
                                    }
                                }
                            });
                        });
                    }
                });
            };

            fs.stat(filePath, (err, stats) => {
                if (err) {
                    console.log(err);
                } else {
                    if (stats.isDirectory()) {
                        processDirectory(filePath);
                    } else {
                        processFile(filePath);
                    }
                }
            });
        });
    });









    win.loadFile('page.html');

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
