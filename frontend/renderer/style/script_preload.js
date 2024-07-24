const { contextBridge, ipcRenderer, ipcMain } = require("electron");
const backup = document.getElementById("backup_path");
const restore = document.getElementById("restore_path");

console.log(what);

// fetch(
//   "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\userData.json"
// )
//   .then((response) => response.json())
//   .then((data) => {
//     what.value = data.email;
//     console.log(data.email);
//   });

fetch("http://localhost:5000/api/test")
  .then((response) => response.json())
  .then((data) => {
    backup.value = data.user.backup_schedule;
    restore.value = data.user.restore_path;
    console.log(JSON.stringify(data.user.backup_schedule) + "yhhhh");
  });

fetch("http://localhost:5000/api/folders")
  .then((response) => response.json())
  .then((data) => {
    let Desktop = document.getElementById("Desktop");
    let Documents = document.getElementById("Documents");
    let Downloads = document.getElementById("Downloads");
    let Videos = document.getElementById("Videos");

    const list = ["Desktop", "Documents", "Downloads", "Videos"];
    const list2 = [Desktop, Documents, Downloads, Videos];
    // const data = JSON.parse(json).folders;
    console.log(data.folders);
    if (data.folders != null) {
      for (let files of data.folders) {
        for (let div of list) {
          if (files.name === div) {
            index = list.indexOf(div);
            list2[index].innerHTML = files.folder_size;
            console.log(files.folder_size);
          }
        }
        console.log(files.folder_size);
        // whattodo.innerHTML = files.id;
        // console.log(JSON.stringify(files));
      }
    } else {
      for (let elements in list2) {
        elements.innerHTML = "0 KB";
      }
    }
    // what.value = data.email
    console.log(JSON.stringify(data.folders) + "yhhhh");
  });
// ipcRenderer.on("sendData", (event, json) => {
//   console.log(json);
// });

// ipcRenderer.on("gotUser", (event, json) => {
//   const data = JSON.parse(json).user;
//   const div = document.getElementById("div");
//   console.log(div);
//   console.log(whatt);
//   whattodo.value = data.email;
//   console.log(JSON.stringify(data.email));
// });

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
