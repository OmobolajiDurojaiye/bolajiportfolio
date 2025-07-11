"use strict";

const signupBtn = document.getElementById("signupBtn");
const loginBtn = document.getElementById("loginBtn");
const authContainer = document.getElementById("auth-container");

signupBtn.addEventListener("click", () => {
  authContainer.classList.add("right-panel-active");
});

loginBtn.addEventListener("click", () => {
  authContainer.classList.remove("right-panel-active");
});
