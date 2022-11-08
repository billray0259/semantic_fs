const { contextBridge, ipcRenderer } = require('electron');


contextBridge.exposeInMainWorld("bridge", {
    launchFile: (filePath) => {
        return ipcRenderer.invoke('launch-file', filePath);
    },
    doesFileExist: (filePath) => {
        return ipcRenderer.invoke('does-file-exist', filePath);
    },
    search: (query, batch) => {
        return ipcRenderer.invoke('search', query, batch);
    },
    openFileDialog: () => {
        return ipcRenderer.invoke('open-file-dialog');
    },
    uploadFiles: (filePath, batchName) => {
        return ipcRenderer.invoke('upload-files', filePath, batchName);
    },
    // expose upload file callback that notifies renderer after every file upload
    fileUploaded: (callback) => {
        ipcRenderer.on('file-uploaded', (event, arg) => {
            callback(arg);
        });
    }
});
