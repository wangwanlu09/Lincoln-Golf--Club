var currentUrl = window.location.href;

var breadcrumbLinks = document.querySelectorAll(".breadcrumb-item a");

breadcrumbLinks.forEach(function (link) {
  if (link.href === currentUrl) {
    link.classList.add("active");
  }
});
