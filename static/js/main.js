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
window.onload = function () {
  displayUploadedPreview();
};

function displayUploadedPreview(course) {
  var input = course.target;
  var preview = document.getElementById("preview");
  var currentImage = document.getElementById("current_image").value;

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      preview.src = e.target.result;
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    var currentImageUrl =
      "{{ url_for('static', filename='img/golf/course/') }}" + currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(scorecard) {
  var input = scorecard.target;
  var preview = document.getElementById("preview");
  var currentImage = document.getElementById("current_image").value;

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      preview.src = e.target.result;
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    var currentImageUrl =
      "{{ url_for('static', filename='img/golf/scorecard/') }}" + currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(home) {
  var input = home.target;
  var preview = document.getElementById("preview");
  var currentImage = document.getElementById("current_image").value;

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      preview.src = e.target.result;
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    var currentImageUrl =
      "{{ url_for('static', filename='img/home/home_module/') }}" +
      currentImage;
    preview.src = currentImageUrl;
  }
}
