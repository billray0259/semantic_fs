const { app, BrowserWindow, ipcMain } = require('electron')

const fs = require('fs-extra'); // import the fs-extra module
const path = require('path'); // import the path module

const createWindow = () => {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true,
        }
    })

    // Read file
    ipcMain.on('read-file', (event, filePath) => {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        event.sender.send('read-file-response', fileContent);
    });

    // Write file
    ipcMain.on('write-file', (event, filePath, fileContent) => {
        fs.writeFileSync(filePath, fileContent);
    });

    win.loadFile('index.html')
    win.webContents.openDevTools()

    const filePath = path.join(__dirname, 'my-file.txt'); // get the path to the file
    const fileContent = 'Hello World!'; // the content of the file
    fs.writeFileSync(filePath, fileContent); // write the file
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})