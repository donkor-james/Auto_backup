const path = require("path");
const { app, BrowserWindow, ipcMain } = require("electron");
const { net } = require("electron");
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...a));
const axios = require("axios");
const isMac = process.platform === "darwin";
const isDev = false;

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    title: "AutoBackup",
    width: isDev ? 800 : 780,
    height: 550,
    frame: false,
    autoHideMenuBar: true, // Set to true to hide the menu bar
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  // Use loadFile to load the HTML file
  mainWindow.loadFile(path.join(__dirname, "./renderer/settings.html"));
  // console.log(mainWindow);
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

ipcMain.handle("doRequestFetch", async () => {
  const response = await fetch("http://localhost:5000/api/files");
  body = response.json();
  return body;
});

ipcMain.handle("doRequestAxios", async () => {
  const response = await axios.get("http://localhost:5000/api/files");
  return response;
});

ipcMain.handle("doRequest", () => {
  const request = net.request("http://localhost:5000/api/files");
  request.on("response", (response) => {
    const data = [];
    response.on("data", (chunk) => {
      data.push(chunk);
      console.log(chunk);
    });

    response.on("end", () => {
      const json = Buffer.concat(data).toString();
      console.log(json[0][0]);
      mainWindow.webContents.send("gotData", json);
    });
  });

  request.end();
});

ipcMain.handle("getFolder", () => {
  const request = net.request("http://localhost:5000/api/folders");
  request.on("response", (response) => {
    const data = [];
    response.on("data", (chunk) => {
      data.push(chunk);
      console.log(chunk);
    });

    response.on("end", () => {
      const json = Buffer.concat(data).toString();
      console.log(json[0][0]);
      mainWindow.webContents.send("getFolder", json);
    });
  });

  request.end();
});

// ipcMain.handle("apiRequestAxios", async () => {
//   const response = await axios.get("http://localhost:5000/api/files");
//   return body;
// });
