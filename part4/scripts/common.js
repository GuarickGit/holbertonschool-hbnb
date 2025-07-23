function checkAuthentication() {
  const pathname = window.location.pathname;
  const token = getCookie('token');

  const loginLink = document.getElementById('login-link');
  const logoutButton = document.getElementById('logout-button');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
    if (logoutButton) logoutButton.style.display = 'none';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    if (logoutButton) logoutButton.style.display = 'inline-block';
  }

  if (pathname.includes('index.html')) {
    fetchPlaces(token);
  } else if (pathname.includes('place.html')) {
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
      if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
      if (addReviewSection) addReviewSection.style.display = 'block';
    }
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

document.addEventListener("DOMContentLoaded", () => {
  const logoutButton = document.getElementById("logout-button");

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      // Supprimer le token
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

      // Redirection vers la page de login
      window.location.href = "login.html";
    });
  }
});

