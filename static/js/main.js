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

function displayUploadedPreview(news) {
  var input = news.target;
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
      "{{ url_for('static', filename='img/home/homedetails/news/') }}" +
      currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(openhours) {
  var input = openhours.target;
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
      "{{ url_for('static', filename='img/home/homedetails/openhours/') }}" +
      currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(memberapply) {
  var input = memberapply.target;
  var preview = document.getElementById("preview");
  var currentDocument = document.getElementById("current_document").value;

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      preview.innerHTML =
        '<embed src="' +
        URL.createObjectURL(input.files[0]) +
        '" type="application/pdf" width="100%" height="500px" />';
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    var currentDocumentUrl =
      "{{ url_for('static', filename='pdf/membership/') }}" + currentDocument;
    preview.innerHTML =
      '<embed src="' +
      currentDocumentUrl +
      '" type="application/pdf" width="100%" height="500px" />';
  }
}

function displayUploadedPreview(funcen) {
  var input = funcen.target;
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
      "{{ url_for('static', filename='img/home/homedetails/function/') }}" +
      currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(cosponsor) {
  var input = cosponsor.target;
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
      "{{ url_for('static', filename='img/sponsors/') }}" + currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(clsponsor) {
  var input = clsponsor.target;
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
      "{{ url_for('static', filename='img/sponsors/') }}" + currentImage;
    preview.src = currentImageUrl;
  }
}

function displayUploadedPreview(pdfInput) {
  var input = pdfInput.target;
  var preview = document.getElementById("preview");
  var currentPdf = document.getElementById("current_pdf").value;

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      // For PDF, use a different method to display
      preview.innerHTML =
        "<embed src='" +
        e.target.result +
        "' width='100%' height='500px' type='application/pdf'>";
    };

    reader.readAsDataURL(input.files[0]);
  } else {
    var currentPdfUrl =
      "{{ url_for('static', filename='pdf/programme/') }}" + currentPdf;
    // For PDF, use a different method to display
    preview.innerHTML =
      "<embed src='" +
      currentPdfUrl +
      "' width='100%' height='500px' type='application/pdf'>";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Restore checkbox states
  document.querySelectorAll(".form-check-input").forEach(function (checkbox) {
    restoreCheckboxState(checkbox.id);
  });

  // Save checkbox state when it changes and toggle corresponding navbar dropdown item
  document.querySelectorAll(".form-check-input").forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      saveCheckboxState(this.id, this.checked);
      toggleNavbarDropdown(checkbox.id, this.checked);
    });
  });
});

// Save checkbox state to local storage
function saveCheckboxState(checkboxId, isChecked) {
  localStorage.setItem(checkboxId, isChecked);
}

// Restore checkbox state from local storage
function restoreCheckboxState(checkboxId) {
  var isChecked = localStorage.getItem(checkboxId);
  if (isChecked === "true") {
    document.getElementById(checkboxId).checked = true;
    toggleNavbarDropdown(checkboxId, true);
  }
}

// Toggle visibility of navbar dropdown item based on checkbox state
function toggleNavbarDropdown(checkboxId, isChecked) {
  var dropdownId = checkboxId; // Assume checkboxId is the same as dropdownId
  var dropdownItem = document.querySelector(
    "[data-dropdown-id='" + dropdownId + "']"
  );
  if (dropdownItem) {
    dropdownItem.style.display = isChecked ? "none" : "block";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  var dropdownItems = document.querySelectorAll(".dropdown-item");

  dropdownItems.forEach(function (item) {
    var itemId = item.id;

    // Restore checkbox state
    var isChecked = localStorage.getItem(itemId);
    if (isChecked === "true") {
      // If checkbox is checked, hide the corresponding navbar item
      item.style.display = "none";
    } else {
      // If checkbox is not checked, show the corresponding navbar item
      item.style.display = "block";
    }
  });
});

function togglePopupVisibility(popupId) {
  var popupContainer = document.getElementById("popupContainer" + popupId);
  var checkbox = document.getElementById(popupId);
  if (checkbox.checked) {
    popupContainer.style.display = "block"; // 显示弹窗
  } else {
    popupContainer.style.display = "none"; // 隐藏弹窗
  }
}
