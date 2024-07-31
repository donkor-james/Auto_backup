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
const fs = require("fs");

const registeredUser = {
  name: "",
  password: "",
  isFirstTime: true,
};

const setupData = {
  backup_schedule: "",
  restore_path: "",
  isFirstTime: "",
};

default_path.checked = true;

// wrapper2.style.display = "none";

function loginLink() {
  window.location.href =
    "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\frontend\\renderer\\login.html";

  wrapper.style.display = "none";
}

// function postUser(data, requestMethod) {
//   fetch("http://localhost:5000/api/test/1", {
//     method: requestMethod,
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify(data),
//   })
//     .then((response) => {
//       response.json();
//     })
//     .then((data) => {
//       console.log(data);
//     });
// }

function login() {
  registeredUser.name = login_username.value;
  registeredUser.password = login_password.value;
  console.log(registeredUser);
  fetch("http://localhost:5000/api/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(registeredUser),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      valid = data.valid;
      console.log(valid);
      if (valid.isValid) {
        if (valid.isFirstTime) {
          window.location.href =
            "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\frontend\\renderer\\setup.html";
        } else {
          window.location.href =
            "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\frontend\\renderer\\settings.html";
        }
      } else {
        login_warning.innerText = "Wrong username or password";
      }
      console.log(registeredUser);
    });
}

function signUp() {
  window.location.href =
    "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\frontend\\renderer\\index.html";
}

function submit() {
  console.log(passwd.value.length);
  if (passwd.value.length < 8 || username.value.length === 0) {
    if (passwd.value.length < 8) {
      console.log("less than 8");
      passwd_warning.innerText = "password should be 8 character long or more ";
    } else {
      passwd_warning.innerText = "";
    }
    if (username.value.length === 0) {
      console.log("ccvf");
      user_warning.innerText = "name cannot be empty";
    } else {
      console.log("cf");
      user_warning.innerText = "";
    }
  } else {
    user_warning.innerText = "";
    passwd_warning.innerText = "";

    registeredUser.name = username.value;
    registeredUser.password = passwd.value;
    registeredUser.isFirstTime = true;
    console.log(registeredUser);

    if (confirm_passwd.value === passwd.value) {
      fetch("http://localhost:5000/api/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(registeredUser),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          loginLink();
        });

      // loginLink();
    } else {
      passwd_warning2.innerText = "password does not match";
    }
    // username.value = "";
    // passwd.value = "";

    // wrapper.style.display = "none";
    // wrapper2.style.display = "flex";
  }
}

function submitSetup() {
  // const options = selectElement.options;
  const selectedOption = selectElement.options[selectElement.selectedIndex];
  setupData.backup_schedule = selectedOption.value;

  setupData.isFirstTime = false;
  if (default_path.checked) {
    console.log(default_path.value);
    setupData.restore_path = default_path.value;
    path_empty.style.display = "none";
    console.log(path_empty.style.display);

    console.log(setupData);
    fetch("http://localhost:5000/api/updateUser", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(setupData),
    })
      .then((response) => {
        response.json();
      })
      .then((data) => {
        console.log(data, "this is updated user after setup");
        window.location.href =
          "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\frontend\\renderer\\settings.html";
      });
    // ipcRenderer.send("postDataForRequest", registeredUser);
  } else if (own_path.checked) {
    if (own_path_value.value === "") {
      path_empty.innerHTML = "Field cannot be empty";
      console.log("empty");
    } else {
      if (fs.existsSync(own_path_value.value)) {
        setupData.restore_path = own_path_value.value;
        console.log(setupData, own_path_value.value);
        fetch("http://localhost:5000/api/updateUser", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(setupData),
        })
          .then((response) => {
            response.json();
          })
          .then((data) => {
            console.log(data);
            window.location.href =
              "C:\\Users\\Donkor James\\Desktop\\Auto_backup2\\Auto_backup\\frontend\\renderer\\settings.html";
          });
      } else {
        path_empty.innerHTML = "Path does not exist";
      }
    }
  }

  // console.log(registeredUser);
}

// console.log(what);
console.log(wrapper);

// temporal
console.log("before fetch");
fetch("http://localhost:5000/api/getUser")
  .then((response) => response.json())
  .then((data) => {
    console.log(data.user);
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
    console.log(folders.length);
    if (folders.length != 0) {
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
      for (let elements of list2) {
        console.log(elements);
        elements.innerHTML = "0 KB";
      }
    }
    // what.value = data.email
    console.log(JSON.stringify(data.folders) + "yhhhh");
  });

// };

// ipcRenderer.on("gotData", (event, json) => {
//   console.log(json);

//   var whattodo = document.getElementById("whattodo");
//   whattodo.innerText = JSON.parse(json).activity;
// });

// contextBridge.exposeInMainWorld("indexBrigde", indexBridge);
// list = ["A", "B", "C"];
// console.log(list[0]);
