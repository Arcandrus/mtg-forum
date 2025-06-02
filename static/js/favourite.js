document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.favourite-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const slug = form.dataset.slug;
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
            const button = form.querySelector('button');
            const countSpan = form.querySelector('.favourite-count');

            try {
                const response = await fetch(`/post/${slug}/favourite/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (response.ok) {
                    const data = await response.json();

                    button.innerHTML = data.favourited ? '<i class="gold fa-solid fa-star"></i>' : '<i black class="fa-regular fa-star"></i>';

                } else {
                    console.error("Server error");
                    alert("Could not update favourite.");
                }
            } catch (err) {
                console.error("AJAX error", err);
                alert("An error occurred.");
            }
        });
    });
});
