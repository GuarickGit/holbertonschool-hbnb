document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;

  // ------------------------------
  // Page de login
  // ------------------------------
  if (path.includes('/login')) {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        await loginUser(email, password);
      });
    }

    async function loginUser(email, password) {
      const response = await fetch('api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = '/index';
      } else {
        alert('Login failed: ' + response.statusText);
      }
    }
  }

  // on continue avec les blocs suivants
  // ------------------------------
  // Page index.html
  // ------------------------------
  if (path.includes('/index') || path === '/' || path === '/index.html') {

    // Fonction pour lire les cookies (commune à d'autres pages)
    function getCookie(name) {
      const cookies = document.cookie;
      const cookieArray = cookies.split(';');

      for (let i = 0; i < cookieArray.length; i++) {
        const cookie = cookieArray[i].trim();
        const [cookieName, cookieValue] = cookie.split('=');

        if (cookieName === name) {
          return cookieValue;
        }
      }

      return null;
    }

    function checkAuthentication({ fetchPlaces = false } = {}) {
      const token = getCookie('token');
      const loginLink = document.getElementById('login-link');

      if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
      }

      if (token && fetchPlaces) {
        fetchPlacesFromAPI(token); // renomme ta fonction fetchPlaces → fetchPlacesFromAPI
      }

      return token;
    }


    async function fetchPlacesFromAPI(token) {
      const response = await fetch('/api/v1/places', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        console.error('Erreur lors de la récupération des places');
        return;
      }

      const data = await response.json();
      displayPlaces(data);
    }


    function displayPlaces(places) {
      const placesList = document.getElementById('places-list');
      if (!placesList) return;

      placesList.innerHTML = '';

      const imageMap = {
        1: "Charmante-maison-à-Evron.jpg"
      };

      places.forEach(place => {
        const imageName = imageMap[place.id] || 'default.jpg';

        const placeElement = document.createElement('div');
        placeElement.classList.add('place');
        placeElement.innerHTML = `
          <img src="/static/images/${imageName}" alt="Image de ${place.title}">
          <h2>${place.title}</h2>
          <p>${place.description}</p>
          <p>Prix par nuit: ${place.price} €</p>
          <button class="view-details" data-id="${place.id}">Voir détails</button>
        `;

        const button = placeElement.querySelector('.view-details');
        button.addEventListener('click', () => {
          window.location.href = `/place?id=${place.id}`;
        });
        placesList.appendChild(placeElement);
      });
    }

    // ------------------------------
    // Filtrage par prix
    // ------------------------------
    const priceFilterElement = document.getElementById('price-filter');

    if (priceFilterElement) {
      // Ajoute dynamiquement les options
      const options = ['All', 10, 50, 100];
      options.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        priceFilterElement.appendChild(option);
      });

      // Applique le filtre lors du changement
      priceFilterElement.addEventListener('change', (event) => {
        const selectPrice = event.target.value;
        const places = document.querySelectorAll('.place');

        places.forEach(place => {
          const priceText = place.querySelector('p:last-of-type').textContent;
          const price = parseInt(priceText.replace(/\D/g, ''), 10);

          if (selectPrice === 'All' || price <= parseInt(selectPrice)) {
            place.style.display = 'block';
          } else {
            place.style.display = 'none';
          }
        });
      });
    }

    // Lance la vérification d'authentification au chargement
    checkAuthentication({ fetchPlaces: true });
  }

  // ------------------------------
  // Page place.html (détails d’un lieu)
  // ------------------------------
  if (path.includes('/place')) {

    function getCookie(name) {
      const cookies = document.cookie;
      const cookieArray = cookies.split(';');

      for (let i = 0; i < cookieArray.length; i++) {
        const cookie = cookieArray[i].trim();
        const [cookieName, cookieValue] = cookie.split('=');

        if (cookieName === name) {
          return cookieValue;
        }
      }

      return null;

    }

    function getPlaceIdFromURL() {
      const params = new URLSearchParams(window.location.search);
      return params.get('id');
    }

    function checkAuthenticationForPlaceDetails() {
      const addReviewSection = document.getElementById('add-review');
      const placeId = getPlaceIdFromURL();

      if (!placeId) {
        console.warn('Aucun ID de logement dans l’URL.');
        return;
      }

      const token = getCookie('token');

      const loginLink = document.getElementById('login-link');
      if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
      }

      if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
      }

      if (token) {
        fetchPlaceDetails(token, placeId);
      } else {
        fetchPlaceDetails(null, placeId);
      }
    }

    async function fetchPlaceDetails(token, placeId) {
      try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          console.error('Erreur lors de la récupération des détails du logement');
          return;
        }

        const place = await response.json();
        displayPlaceDetails(Array.isArray(place) ? place[0] : place);
      } catch (error) {
        console.error('Erreur fetchPlaceDetails :', error);
      }
    }

    function displayPlaceDetails(place) {
      console.log('Place reçu dans displayPlaceDetails :', place);
      console.log('Type de price :', typeof place.price, place.price);

      const container = document.getElementById('place-details');
      if (!container) return;

      container.innerHTML = '';

      const title = document.createElement('h2');
      title.innerHTML = `${place.title}`;

      const description = document.createElement('p');
      description.textContent = place.description;

      const price = document.createElement('p');
      price.textContent = `Prix: ${place.price} €`;

      const amenities = document.createElement('ul');
      amenities.innerHTML = '<strong>Équipements :</strong>';
      if (place.amenities && place.amenities.length > 0) {
        place.amenities.forEach(am => {
          const item = document.createElement('li');
          item.textContent = am;
          amenities.appendChild(item);
        });
      } else {
        const noAm = document.createElement('li');
        noAm.textContent = 'Aucun équipement';
        amenities.appendChild(noAm);
      }

      const reviews = document.createElement('div');
      reviews.innerHTML = '<h3>Avis :</h3>';
      if (place.reviews && place.reviews.length > 0) {
        place.reviews.forEach(review => {
          const div = document.createElement('div');
          div.classList.add('review');
          const authorName = review.user ? review.user.first_name : "Utilisateur inconnu";
          div.innerHTML = `
            <strong>${authorName}</strong> <br>
            <em>Note : ${review.rating}/5</em>
            <p>${review.text}</p>
          `;
          reviews.appendChild(div);
        });
      } else {
        reviews.innerHTML += '<p>Aucun avis pour le moment.</p>';
      }

      container.appendChild(title);
      container.appendChild(description);
      container.appendChild(price);
      container.appendChild(amenities);
      container.appendChild(reviews);
    }

    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const token = getCookie('token');
        const placeId = getPlaceIdFromURL();

        const rating = parseInt(document.getElementById('rating').value);
        const text = document.getElementById('review-text').value;

        try {
          const response = await fetch(`/api/v1/reviews/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ rating, text, place_id: placeId })
          });

          const data = await response.json();
          console.log(data.user);

          if (response.ok) {
            alert('Avis ajouté !');
            location.reload();
          } else {
            alert('Erreur lors de l’ajout de l’avis.');
          }
        } catch (error) {
          console.error('Erreur lors de l’envoi du commentaire :', error);
        }
      });
    }
    checkAuthenticationForPlaceDetails();
  }
});
