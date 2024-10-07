const body = document.querySelector("body"),
      nav = document.querySelector("nav"),
      modeToggle = document.querySelector(".dark-light"),
      sidebarOpen = document.querySelector(".sidebarOpen"),
      siderbarClose = document.querySelector(".siderbarClose");

let getMode = localStorage.getItem("mode");

if (getMode && getMode === "dark-mode") {
  body.classList.add("dark");
}

// JS code to toggle dark and light mode
modeToggle.addEventListener("click", () => {
  modeToggle.classList.toggle("active");
  body.classList.toggle("dark");

  // JS code to keep user selected mode even after page refresh or file reopen
  if (!body.classList.contains("dark")) {
    localStorage.setItem("mode", "light-mode");
  } else {
    localStorage.setItem("mode", "dark-mode");
  }
});


// JS code to toggle sidebar
sidebarOpen.addEventListener("click", () => {
  nav.classList.add("active");
});

body.addEventListener("click", (e) => {
  let clickedElm = e.target;
  if (!clickedElm.classList.contains("sidebarOpen") && !clickedElm.classList.contains("menu")) {
    nav.classList.remove("active");
  }
});

//  ==== Contact Form ====
function handleSubmit(event) {
  event.preventDefault();

  const successMessage = document.getElementById('successMessage');
  successMessage.style.display = 'block';
  
  setTimeout(() => {
      successMessage.style.display = 'none';
  }, 3000);

  document.getElementById('contactForm').reset();
}

//  ==== SendMail ====
function sendMail(){
  let params = {
    name : document.getElementById("name").value,
    email : document.getElementById("email").value,
    subject : document.getElementById("subject").value,
    msg : document.getElementById("msg").value,
  }

  emailjs.send("service_ycv2imy","template_rkyu3gq",params)
}