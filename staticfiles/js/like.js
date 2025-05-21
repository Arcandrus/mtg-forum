document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();  // Prevent page reload

            const slug = form.dataset.slug;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            const button = form.querySelector('button');
            const countSpan = form.querySelector('.like-count');

            try {
                const response = await fetch(`/post/${slug}/like/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (response.ok) {
                    const data = await response.json();

                    // Toggle button text
                    button.textContent = data.liked ? 'Unlike' : 'Like';

                    // Update like count
                    const likeText = `${data.total_likes} like${data.total_likes === 1 ? '' : 's'}`;
                    countSpan.textContent = likeText;
                } else {
                    alert("Error submitting like.");
                }
            } catch (err) {
                console.error("Request failed", err);
                alert("An error occurred.");
            }
        });
    });
});