#!/usr/bin/env node

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
list = ["A", "B", "C"];
console.log(list[0]);
