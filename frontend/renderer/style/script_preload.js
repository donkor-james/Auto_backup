const { contextBridge, ipcRenderer, ipcMain } = require("electron");
const backup = document.getElementById("backup_path");
const what = document.getElementById("restore_path");

console.log(what);

fetch(
  "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\userData.json"
)
  .then((response) => response.json())
  .then((data) => {
    what.value = data.email;
    console.log(data.email);
  });

fetch("http://localhost:5000/api/user")
  .then((response) => response.json())
  .then((data) => {
    backup.value = data.user.email;
    console.log(JSON.stringify(data) + "yhhhh");
  });
ipcRenderer.on("sendData", (event, json) => {
  console.log(json);
});

ipcRenderer.on("gotUser", (event, json) => {
  const data = JSON.parse(json).user;
  const div = document.getElementById("div");
  console.log(div);
  console.log(whatt);
  whattodo.value = data.email;
  console.log(JSON.stringify(data.email));
});

// const data = JSON.parse(localStorage.getItem("data"));
// console.log(data + "in setting file");
// ipcRenderer.on("gotUser", (event, json) => {
//   const data = JSON.parse(json).user;
//   console.log(whatt);
//   whattodo.value = data.email;
//   console.log(JSON.stringify(data.email));
// });

// #!/usr/bin/env node

// const { contextBridge, ipcMain, ipcRenderer } = require("electron");

// let indexBridge = {
//   doRequest: async () => {
//     var result = await ipcRenderer.invoke("doRequest");
//   },

//   // apiRequestAxios: async () => {
//   //   var response = await ipcRenderer.invoke("apiRequestAxios");
//   //   var whattodo = document.getElementById("whattodo");
//   //   whattodo.innerText = JSON.parse(response + "yyy").activity;
//   // },
// };

// ipcRenderer.on("gotData", (event, json) => {
//   console.log(json);

//   var whattodo = document.getElementById("whattodo");
//   whattodo.innerText = JSON.parse(json).activity;
// });

// contextBridge.exposeInMainWorld("indexBrigde", indexBridge);
// list = ["A", "B", "C"];
// console.log(list[0]);
