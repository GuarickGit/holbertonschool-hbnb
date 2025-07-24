console.log("🧠 place.js chargé");

async function fetchPlaceDetails(token, placeId) {
  if (!placeId) {
    console.error("Missing place ID");
    return;
  }

  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    console.log("fetchPlaceDetails lancé", placeId);
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
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
  placeDetailsSection.innerHTML = '';

  const infoDiv = document.createElement('div');
  infoDiv.className = 'place-info';

  console.log(place)
  infoDiv.innerHTML = `
    <h2>${place.title}</h2>
    <p><strong>Host:</strong> ${place.owner.first_name} ${place.owner.last_name}</p>
    <p><strong>Price per night:</strong> ${place.price} Gils</p>
    <p><strong>Description:</strong> ${place.description}</p>
  `;

  placeDetailsSection.appendChild(infoDiv);

  const amenitiesTitle = document.createElement('p');
  amenitiesTitle.innerHTML = '<strong>Amenities:</strong>';
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
    author.textContent = review.user_name;
    reviewCard.appendChild(author);

    const rating = document.createElement('p');
    const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
    rating.textContent = `Rating: ${stars}`;
    reviewCard.appendChild(rating);

    const text = document.createElement('p');
    text.textContent = review.text;
    reviewCard.appendChild(text);

    reviewSection.appendChild(reviewCard);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  const addReviewSection = document.getElementById('add-review');

  const reviewLink = document.querySelector('.add-review-button');
  if (reviewLink && placeId) {
    reviewLink.setAttribute('href', `add_review.html?id=${placeId}`);
  }

  console.log("DOM loaded", { token, placeId });

  if (addReviewSection) {
  addReviewSection.style.display = token ? 'block' : 'none';
}

  fetchPlaceDetails(token, placeId);

  checkAuthentication();
});
