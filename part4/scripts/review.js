document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();

  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  // Récupère et affiche dynamiquement le nom du lieu
  (async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`);
      if (response.ok) {
        const place = await response.json();
        const placeNameSpan = document.getElementById('place-name');
        if (placeNameSpan) {
          placeNameSpan.textContent = place.title;
        }
      } else {
        console.error('Error loading place:', response.status);
      }
    } catch (error) {
      console.error('Network error while loading place:', error);
    }
  })();

  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const reviewText = document.getElementById('review').value;
      const ratingValue = parseInt(document.getElementById('rating').value);

      const reviewData = {
        text: reviewText,
        rating: ratingValue,
        place_id: placeId
      };

      try {
        const response= await fetch('http://localhost:5000/api/v1/reviews/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(reviewData)
        });

        if (response.ok) {
          alert('Review submitted successfully!');
          reviewForm.reset(); // vide le formulaire
          window.location.href = `place.html?id=${placeId}`; // Renvoie le user vers la place pour voir sa review
        } else {
          const errorData = await response.json();
          console.error('Submission failed', errorData);
          alert('Failed to submit review: ' + (errorData.message || response.statusText));
        }
      } catch (error) {
        console.error('Error submitting review', error);
        alert('An error occurred while submitting your review.');
      }
    });
  }
});
