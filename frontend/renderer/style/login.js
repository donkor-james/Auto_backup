const { contextBridge, ipcRenderer, ipcMain } = require("electron");
const backup = document.getElementById("backup_path");
const restore = document.getElementById("restore_path");
const selectElement = document.getElementById("select");
const wrapper = document.getElementById("main_wrapper");
const wrapper2 = document.getElementById("main_wrapper2");
const registerBtn = document.getElementById("register_btn");
const loginBtn = document.getElementById("login_btn");
const passwd = document.getElementById("passwd");
const confirm_passwd = document.getElementById("confirm_passwd");
const username = document.getElementById("username");
const passwd_warning = document.getElementById("passwd_warning");
const passwd_warning2 = document.getElementById("passwd_warning2");
const user_warning = document.getElementById("user_warning");
const login_username = document.getElementById("login_username");
const login_password = document.getElementById("login_password");
const login_warning = document.getElementById("login_warning");
const save = document.getElementById("restore_btn");
const default_path = document.getElementById("radio");
const own_path = document.getElementById("radio1");
const own_path_value = document.getElementById("own_path_value");
const path_empty = document.getElementById("path_empty");
const usernameHome = document.getElementById("heading_details");
const total_data = document.getElementById("total_data");
const fs = require("fs");

function loginLink() {
  console.log("clicked on loginLink");
  window.location.href =
    "C:\\Users\\Donkor James\\Auto_backup2\\Auto_backup\\frontend\\renderer\\login.html";
  console.log(window.location.href);
  wrapper.style.display = "none";
}

// temporal
console.log("before fetch");
fetch("http://localhost:5000/api/getUser")
  .then((response) => response.json())
  .then((data) => {
    console.log(data.user);
    // console.log(usernameHome);
    usernameHome.innerHTML = data.user.name;
    backup.value = data.user.backup_schedule;
    restore.value = data.user.restore_path;

    total_data.innerHTML = data.user.total_data;
    console.log(JSON.stringify(data.user) + "yhhhh");
    if (!data.user.total_data) {
      total_data.innerHTML = "0 Bytes";
    }
  });
fetch("http://localhost:5000/api/folders")
  .then((response) => response.json())
  .then((data) => {
    let Desktop = document.getElementById("Desktop");
    let Documents = document.getElementById("Documents");
    let Downloads = document.getElementById("Downloads");
    let Pictures = document.getElementById("Pictures");
    let Videos = document.getElementById("Videos");
    let Others = document.getElementById("Others");

    const list = [
      "Desktop",
      "Documents",
      "Downloads",
      "Pictures",
      "Videos",
      "Others",
    ];
    const list2 = [Desktop, Documents, Downloads, Pictures, Videos, Others];
    // const data = JSON.parse(json).folders;
    folders = data.folders;
    console.log(folders.length, folders);
    if (folders.length != 0) {
      for (let files of data.folders) {
        for (let div of list) {
          if (files.name === div) {
            index = list.indexOf(div);
            list2[index].innerHTML = files.folder_size;
            console.log(files.folder_size);
          }
          // else if(list.indexOf()){

          // }
        }
        // for (let div of list) {
        //   if (files.name === div) {
        //     index = list.indexOf(div);
        //     list2[index].innerHTML = files.folder_size;
        //     console.log(files.folder_size);
        //   }
        // }
        console.log(files.folder_size);
        // whattodo.innerHTML = files.id;
        // console.log(JSON.stringify(files));
      }
    } else {
      for (let elements of list2) {
        console.log(elements);
        elements.innerHTML = "0 Bytes";
      }
    }
    // what.value = data.email
    console.log(JSON.stringify(data.folders) + "yhhhh");
  });
