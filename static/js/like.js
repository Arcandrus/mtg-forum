// Run after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Find all forms with class 'like-form' (handles likes on posts)
    document.querySelectorAll('.like-form').forEach(form => {
        // Listen for form submit event
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent default form submission

            // Get post slug from form's data attribute
            const slug = form.dataset.slug;
            // Get CSRF token value from hidden input for security
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            // Get the like button inside the form to update its icon
            const button = form.querySelector('button');
            // Get the span element that shows the like count
            const countSpan = form.querySelector('.like-count');

            try {
                // Send AJAX POST request to like/unlike the post
                const response = await fetch(`/post/${slug}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,           // CSRF token header for Django
                        'X-Requested-With': 'XMLHttpRequest', // Identify AJAX request
                    },
                });

                if (response.ok) {
                    // Parse JSON data returned from the server
                    const data = await response.json();

                    // Find the <i> icon element inside the button
                    const icon = button.querySelector('i');
                    if (icon) {
                        // Toggle icon classes based on whether the post is liked
                        icon.classList.toggle('fa-solid', data.liked);   // solid star when liked
                        icon.classList.toggle('fa-regular', !data.liked); // regular star when not liked
                        icon.classList.toggle('blue', data.liked);        // add blue color when liked
                    }

                    // Update the like count text with proper pluralization
                    countSpan.textContent = `${data.total_likes} like${data.total_likes === 1 ? '' : 's'}`;
                } else {
                    // Alert user if server returned an error response
                    alert("Error submitting like.");
                }
            } catch (err) {
                // Log and alert if the fetch request fails (network or other error)
                console.error("Request failed", err);
                alert("An error occurred.");
            }
        });
    });
});
