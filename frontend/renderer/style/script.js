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

const temp_user = {};

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
    let Pictures = document.getElementById("Pictures");
    let Videos = document.getElementById("Videos");
    let Others = document.getElementById("Others");

    const list = ["Desktop", "Documents", "Downloads", "Videos", "Others"];
    const list2 = [Desktop, Documents, Downloads, Pictures, Videos, Others];
    // const data = JSON.parse(json).folders;
    folders = data.folders;
    console.log(folders.length, folders);
    if (folders.length < 0) {
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
        console.log(JSON.stringify(files));
      }
    } else {
      for (let elements of list2) {
        console.log(elements);
        elements.innerHTML = "0 KB";
      }
    }
    // what.value = data.email
    console.log(JSON.stringify(data.folders) + "yhhhh", selectElement);
  });

fetch("http://localhost:5000/api/getUser")
  .then((response) => response.json())
  .then((data) => {
    user = data.user;

    // options = selectElement.options;
    // console.log(options);
    const options = selectElement.options;
    console.log(user);
    for (let option of options) {
      // option.innerHTML = "Yes";
      // console.log(option.value, user.backup_schedule, option.selected);
      if (option.value === user.backup_schedule) {
        option.selected = true;
      }
    }
    // temp_user.name = user.name;
    // // temp_user.backedup_at = user.backedup_at;
    // temp_user.backup_schedule = user.backup_schedule;
    // temp_user.restore_path = user.restore_path;
    // temp_user.total_data = user.total_data;

    console.log(user, temp_user);
    // console.log(typeof user, user);
    if (user.restore_path && user.restore_path === "Default_Path") {
      // for (let files of data.folders) {
      //   for (let div of list) {
      //     if (files.name === div) {
      //       index = list.indexOf(div);
      //       list2[index].innerHTML = files.folder_size;
      //       console.log(files.folder_size);
      //     }
      //   }

      // console.log(user);
      default_path.checked = true;
      console.log(default_path.checked);
    } else if (user.restore_path) {
      own_path.checked = true;
      path_empty.value = user.restore_path;
    }

    // console.log(user);
    // if (user.backup_schedule) {

    // } else {
    //   return;
    // }
    // what.value = data.email
    console.log(JSON.stringify(data.user) + "yhhhh", selectElement);
  });
fetch("http://localhost:5000/api/getUser")
  .then((response) => response.json())
  .then((data) => {
    // console.log(user);
    // console.log(typeof user, user);

    user = data.user;
    console.log(user);
    // Array.prototype.forEach.call(selectElement.options, function (option) {
    //   console.log(option.text, user.re);
    //   if (option.text === user.backup_schedule) {
    //     console.log(option);
    //     option.selected = true;
    //   }
    // });

    console.log(user);
    if (user.restore_path && user.restore_path === "Default_Path") {
      // for (let files of data.folders) {
      //   for (let div of list) {
      //     if (files.name === div) {
      //       index = list.indexOf(div);
      //       list2[index].innerHTML = files.folder_size;
      //       console.log(files.folder_size);
      //     }
      //   }

      // console.log(user);
      default_path.checked = true;
      console.log(default_path.checked);
    } else if (user.restore_path) {
      own_path.checked = true;
      // console.log(user.restore_path, path_empty);
      own_path_value.value = user.restore_path;
    }
    console.log(JSON.stringify(data.folders) + "yhhhh", selectElement);
  });

console.log(temp_user);

const options = selectElement.options;
console.log(options[0]);
for (let option of options) {
  // option.innerHTML = "Yes";
  console.log(temp_user);
  if (option.value === temp_user.backup_schedule) {
    option.value = temp_user.backup_schedule;
  }
}
// options.forEach((element) => {
//   console.log(element);
// });

function doRequest() {
  indexBridge.doRequest();
  console.log("it worked");
}

function postDataForRequest() {
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  postData.backup_schedule = selectedOption.value;
  console.log(selectElement);
  ipcRenderer.send("postDataForRequest", postData);
}

// console.log(default_path);
// console.log(default_path);

function restoreData() {
  if (default_path.checked) {
    console.log(default_path.value);
    postRestore.restore_path = default_path.value;
    path_empty.style.display = "none";
    console.log(path_empty.style.display);

    ipcRenderer.send("postDataForRequest", postRestore);
  } else if (own_path.checked) {
    // path_empty.style.display = "flex";
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
