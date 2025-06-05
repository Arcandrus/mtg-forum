// Wait for the DOM content to be fully loaded before running script
document.addEventListener('DOMContentLoaded', function () {
    // Select all forms with class 'favourite-form' (these handle favoriting posts)
    document.querySelectorAll('.favourite-form').forEach(form => {
        // Add submit event listener to each form
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent normal form submission (page reload)

            // Get post slug from data attribute on the form
            const slug = form.dataset.slug;
            // Get CSRF token value from the hidden input inside the form
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            // Get the button inside the form to update its icon/state later
            const button = form.querySelector('button');
            // Get the span element showing the favourite count (if needed)
            const countSpan = form.querySelector('.favourite-count');

            try {
                // Make a POST request to the server to toggle favourite status
                const response = await fetch(`/post/${slug}/favourite/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,         // Required for Django CSRF protection
                        'X-Requested-With': 'XMLHttpRequest', // Indicate AJAX request
                    },
                });

                if (response.ok) {
                    // Parse JSON response from server
                    const data = await response.json();

                    // Update button icon based on whether post is favourited
                    // Gold solid star if favourited, regular star if not
                    button.innerHTML = data.favourited 
                        ? '<i class="gold fa-solid fa-star"></i>' 
                        : '<i class="fa-regular fa-star"></i>';

                    // Optionally, update count if included in response
                    if (countSpan && data.favourite_count !== undefined) {
                        countSpan.textContent = data.favourite_count;
                    }

                } else {
                    // Log and alert on server errors
                    console.error("Server error");
                    alert("Could not update favourite.");
                }
            } catch (err) {
                // Log and alert on network or other AJAX errors
                console.error("AJAX error", err);
                alert("An error occurred.");
            }
        });
    });
});