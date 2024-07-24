const { contextBridge, ipcRenderer } = require("electron");
const fs = require("fs");
let postData = {
  // name: "",
  backup_schedule: "",
  // backedup_at: null,
  // total_data: ""
};

let postRestore = {
  restore_path: "",
};
const selectElement = document.getElementById("select");
const save = document.getElementById("restore_btn");
const default_path = document.getElementById("radio");
const own_path = document.getElementById("radio1");
const own_path_value = document.getElementById("own_path_value");
const path_empty = document.getElementById("path_empty");

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
// fetch("http://localhost:5000/api/test")
//   .then((response) => response.json())
//   .then((data) => {
//     // what.value = data.email
//     console.log(JSON.stringify(data) + "yhhhh");
//   });

function doRequest() {
  indexBridge.doRequest();
  console.log("it worked");
}

// function getFolder() {
//   indexBridge.getFolder();
// }

function postDataForRequest() {
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  postData.email = selectedOption.value;
  ipcRenderer.send("postDataForRequest", postData);
}

function restoreData() {
  if (default_path.checked) {
    console.log(default_path.value);
    postRestore.restore_path = default_path.value;
    ipcRenderer.send("postDataForRequest", postRestore);
  } else if (own_path.checked) {
    if (own_path_value.value === "") {
      path_empty.innerHTML = "Field cannot be empty";
      console.log("empty");
    } else {
      if (fs.existsSync(own_path_value.value)) {
        postRestore.restore_path = own_path_value.value;
        // console.log("empty", own_path_value.value);
        ipcRenderer.send("postDataForRequest", postRestore);
      } else {
        path_empty.innerHTML = "Path does not exist";
      }
    }
  }
}

let indexBridge = {
  doRequest: async () => {
    var result = await ipcRenderer.invoke("doRequest");
  },

  getFolder: async () => {
    fetch("http://localhost:5000/api/folders")
      .then((response) => response.json())
      .then((data) => {
        // what.value = data.email
        console.log(JSON.stringify(data.folders) + "yhhhh");
      });
    var result = await ipcRenderer.invoke("getFolder");
  },
};

ipcRenderer.on("gotData", (event, json) => {
  let whattodo = document.getElementById("whattodo");
  const whatt = document.getElementById("schedule");

  const data = JSON.parse(json).files;
  for (let files of data) {
    whattodo.innerHTML = files.id;
    console.log(JSON.stringify(files));
  }
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

  console.log(data);
});

// ipcRenderer.on("gotUser", (event, json) => {
//   const data = JSON.parse(json).user;
//   const div = document.getElementById("div");
//   // ipcRenderer.send("data", data);
//   // console.log(Desktop);
//   // console.log(whatt);
//   // whattodo.value = data.email;
//   console.log(JSON.stringify(data.email));
//   // ipcRenderer.send("sendData", data);
// });

// ipcRenderer.send("postDataForRequest", backup_interval);

contextBridge.exposeInMainWorld("indexBridge", indexBridge);
