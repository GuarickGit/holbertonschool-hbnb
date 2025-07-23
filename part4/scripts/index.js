async function fetchPlaces(token) {
  try {
    const headers = {
    'Content-Type': 'application/json'
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch('http://localhost:5000/api/v1/places/', {
    method: 'GET',
    headers: headers
  });

    if (response.ok) {
      const places = await response.json();
      displayPlaces(places);
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

document.addEventListener('DOMContentLoaded', () => {
  // LOGIN FORM (si sur cette page)
  const form = document.getElementById('login-form');

  if (form) {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

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

  // FILTRE PRIX
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    const options = [10, 50, 100, 'All'];

    options.forEach(value => {
      const option = document.createElement('option');
      option.textContent = value;

      if (value === 'All') {
        option.value = '';
        option.selected = true;
      } else {
        option.value = value;
      }

      priceFilter.appendChild(option);
    });

    priceFilter.addEventListener('change', (event) => {
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
  }

  // REDIRECTION BOUTON DETAILS
  const placesList = document.getElementById('places-list');
  if (placesList) {
    placesList.addEventListener('click', (event) => {
      const button = event.target.closest('.details-button');
      if (button) {
        const placeId = button.dataset.id;
        window.location.href = `place.html?id=${placeId}`;
      }
    });
  }

  // CHECK AUTH POUR CHARGER LES PLACES
  checkAuthentication();
});
