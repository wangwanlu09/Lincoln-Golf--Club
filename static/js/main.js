document.addEventListener("DOMContentLoaded", function () {
  var navbar = document.querySelector(".navbar");
  var threshold = 100;
  window.addEventListener("scroll", function () {
    if (window.scrollY > threshold) {
      navbar.classList.add("navbar-scrolled");
    } else {
      navbar.classList.remove("navbar-scrolled");
    }
  });
});

function scrollToElement(elementId) {
  var element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
}

function redirectToPage(url) {
  window.location.href = url;
}
