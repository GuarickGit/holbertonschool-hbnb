/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      console.log("Form submitted");

      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        if (response.ok) {
          const data = await response.json();
          const token = data.access_token;
          document.cookie = `token=${token}; path=/`;

          window.location.href = 'index.html';

        } else {
          alert('Login failed. Please check your credentials.');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });
  }
  const priceFilter = document.getElementById('price-filter');
    const options = [10, 50, 100, 'All'];

    options.forEach(value => {
      const option = document.createElement('option');
      option.textContent = value;

      if (value === 'All') {
        option.value = '';
        option.selected = true; // Force 'All' par défaut
      } else {
        option.value = value;
      }

      priceFilter.appendChild(option);
    })
  checkAuthentication();
});

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchPlaces(token) {
  console.log("fetchPlaces called");
    try {
    const response = await fetch('http://localhost:5000/api/v1/places/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
      console.log("Places received:", places);
    } else {
      console.error('Failed to fetch places', response.status);
    }
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
      const card = document.createElement('div');
      card.className = 'place-card';
      card.dataset.id = place.id;

      card.innerHTML = `
    <h3>${place.title}</h3>
    <p>Price per night: ${place.price} Gils</p>
    <button class="details-button" data-id="${place.id}">View Details</button>
  `;

    placesList.appendChild(card);
    });
}

document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;

  const cards = document.querySelectorAll('.place-card');

  cards.forEach(card => {
    const priceText = card.querySelector('p').textContent;
    const price = parseFloat(priceText.match(/\d+/)[0]);

    if (selectedPrice === "" || price <= parseFloat(selectedPrice)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
});


function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    const placeIdFromURL = params.get('id');
    return placeIdFromURL;
}

function checkAuthentication() {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        fetchPlaceDetails(token, placeId);
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchPlaceDetails(token, placeId) {
    if (!placeId) {
      console.error("Missing place ID");
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const place = await response.json();
        displayPlaceDetails(place);
      } else {
        console.error("Failed to fetch place details:", response.status);
      }
    } catch (error) {
      console.error("Error fetching place details:", error);
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    placeDetailsSection.innerHTML = ''; // clean pour réinjecter proprement

    const infoDiv = document.createElement('div');
    infoDiv.className = 'place-info';

    infoDiv.innerHTML = `
    <h2>${place.title}</h2>
    <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
    <p><strong>Price per night:</strong> ${place.price} Gils</p>
    <p><strong>Description:</strong> ${place.description}</p>
`;

    placeDetailsSection.appendChild(infoDiv);

    const amenitiesTitle = document.createElement('p');
    amenitiesTitle.textContent = 'Amenities';
    infoDiv.appendChild(amenitiesTitle);

    const amenitiesList = document.createElement('ul');
    infoDiv.appendChild(amenitiesList);

    place.amenities.forEach(amenity => {
      const li = document.createElement('li');
      li.textContent = amenity.name;
      amenitiesList.appendChild(li);
    });

    const reviewSection = document.createElement('section');
    reviewSection.id = 'reviews';

    const reviewsTitle = document.createElement('h2');
    reviewsTitle.textContent = 'Reviews';
    reviewSection.appendChild(reviewsTitle);

    placeDetailsSection.appendChild(reviewSection);

    place.reviews.forEach(review => {
      const reviewCard = document.createElement('div');
      reviewCard.className = 'review-card';

      const author = document.createElement('h3');
      author.textContent = review.user_id; // ATTENTION, TEMPORAIRE, ME SERT DE PLACEHOLDER
      reviewCard.appendChild(author);

      const rating = document.createElement('p');
      rating.textContent = `Rating: ${'★'.repeat(review.rating)}`;
      reviewCard.appendChild(rating);

      const text = document.createElement('p');
      text.textContent = review.text;
      reviewCard.appendChild(text);

      reviewSection.appendChild(reviewCard);
    })
}
