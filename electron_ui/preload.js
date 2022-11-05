const { contextBridge, ipcRenderer } = require('electron');


contextBridge.exposeInMainWorld("searchBridge", {
    launchFile: (filePath) => {
        return ipcRenderer.invoke('launch-file', filePath);
    },
    doesFileExist: (filePath) => {
        return ipcRenderer.invoke('does-file-exist', filePath);
    },
    search: (query, batch) => {
        return ipcRenderer.invoke('search', query, batch);
    }
});
