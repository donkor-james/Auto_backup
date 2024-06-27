const path = require("path");
const { app, BrowserWindow } = require("electron");

const isMac = process.platform === "darwin";
const isDev = false;

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    title: "AutoBackup",
    width: isDev ? 800 : 580,
    height: 480,
    frame: false,
    autoHideMenuBar: true, // Set to true to hide the menu bar
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  // Use loadFile to load the HTML file
  mainWindow.loadFile(path.join(__dirname, "./renderer/index.html"));
  mainWindow;
  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  // Open dev tools if in dev environment
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }
}

app.allowRendererProcessReuse = true;

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (!isMac) {
    app.quit();
  }
});

// Move the close button event listener inside createWindow function
// app.on("ready", () => {
//   createWindow();

//   mainWindow.webContents.on("did-finish-load", () => {
//     const closeBtn = document.getElementById("close_btn");
//     closeBtn.addEventListener("click", () => {
//       let win = remote.BrowserWindow.getFocusedWindow();
//       win.close();
//       console.log("closed");
//     });
//   });
// });

console.log("consoled");
