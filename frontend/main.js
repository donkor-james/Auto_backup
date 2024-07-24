const path = require("path");
const { app, BrowserWindow, ipcMain, ipcRenderer } = require("electron");
const { net } = require("electron");
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...a));
const axios = require("axios");
const http = require("http");
const fs = require("fs");
const { error } = require("console");
const isMac = process.platform === "darwin";
const isDev = false;
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    title: "AutoBackup",
    width: isDev ? 800 : 780,
    height: 550,
    frame: false,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, "./renderer/settings.html"));
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

ipcMain.on("postDataForRequest", (event, postData) => {
  console.log(postData);
  const postDataString = JSON.stringify(postData);
  const options = {
    hostname: "localhost",
    port: 5000,
    path: "/api/test",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(postDataString),
    },
  };

  const req = http.request(options, (res) => {
    let data = "";

    res.on("data", (chunk) => {
      data += chunk;
      console.log(chunk);
    });

    res.on("end", () => {
      if (fs.existsSync("userData.json")) {
        fs.readFile("userData.json", "utf8", (err, userData) => {
          if (err) {
            console.log(err);
            return;
          }
          const existData = JSON.parse(userData);

          existData.id = JSON.parse(data).user.id;
          existData.email = JSON.parse(data).user.email;

          const updated_data = existData;

          fs.writeFile("userData.json", JSON.stringify(updated_data), (err) => {
            if (err) {
              console.log(err);
              return;
            }
            console.log("Data updated successfully");
          });
        });
      } else {
        console.log(data);
        console.log(typeof data);
        fs.writeFile("userData.json", data, (err) => {
          console.log(err);
        });
      }
      console.log(JSON.parse(data).user.email + "yhg");
      mainWindow.webContents.send("gotUser", data);
    });
    // const user = JSON.parse(data);
    console.log("hsggdjh");
    // mainWindow.webContents.se;
  });

  req.on("error", (error) => {
    console.error(error);
  });

  req.write(postDataString);
  req.end();
});

ipcMain.on("sendData", (event, data) => {
  console.log("fuck youu");
  // ipcRenderer.send("sendData2", data);
});

// ipcMain.handle("apiRequestAxios", async () => {
//   const response = await axios.get("http://localhost:5000/api/files");
//   return body;
// });
