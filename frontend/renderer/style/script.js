const { contextBridge, ipcMain, ipcRenderer } = require("electron");

function doRequest() {
  indexBridge.doRequest();
}

function getFolder() {
  indexBridge.getFolder();
}

// Bridge code

let indexBridge = {
  doRequest: async () => {
    var result = await ipcRenderer.invoke("doRequest");
  },

  getFolder: async () => {
    var result = await ipcRenderer.invoke("getFolder");
  },
};

ipcRenderer.on("gotData", (event, json) => {
  // const jsonString = {
  //   files: [
  //     {
  //       file_path: "Documents\\token.txt",
  //       Id: 1,
  //     },
  //     {
  //       file_path: "Desktop\\file.txt",
  //       Id: 2,
  //     },
  //   ],
  // };
  let whattodo = document.getElementById("whattodo");
  const data = JSON.parse(json).files;
  for (let files of data) {
    whattodo.innerHTML = files.id;
    console.log(JSON.stringify(files));
  }
  // console.log(data);
});

ipcRenderer.on("getFolder", (event, json) => {
  // const jsonString = {
  //   files: [
  //     {
  //       file_path: "Documents\\token.txt",
  //       Id: 1,
  //     },
  //     {
  //       file_path: "Desktop\\file.txt",
  //       Id: 2,
  //     },
  //   ],
  // };
  let Desktop = document.getElementById("Desktop");
  let Documents = document.getElementById("Documents");
  let Downloads = document.getElementById("Downloads");
  let Videos = document.getElementById("Videos");

  const list = ["Desktop", "Documents", "Downloads", "Videos"];
  const list2 = [Desktop, Documents, Downloads, Videos];
  const data = JSON.parse(json).files;
  for (let files of data) {
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
  // console.log(data);
});

contextBridge.exposeInMainWorld("indexBridge", indexBridge);
