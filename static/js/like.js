document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

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

                    // Toggle icon classes on the <i> inside the button
                    const icon = button.querySelector('i');
                    if (icon) {
                        icon.classList.toggle('fa-solid', data.liked);
                        icon.classList.toggle('fa-regular', !data.liked);
                        icon.classList.toggle('blue', data.liked);
                    }

                    // Update like count text
                    countSpan.textContent = `${data.total_likes} like${data.total_likes === 1 ? '' : 's'}`;
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
