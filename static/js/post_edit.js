document.addEventListener('DOMContentLoaded', function () {
    // Get the edit post button by ID
    const editBtn = document.getElementById('edit-post-btn');

    if (editBtn) {
        // When edit button is clicked
        editBtn.addEventListener('click', function () {
            const slug = this.dataset.slug;

            // Fetch the edit form HTML from the server
            fetch(`/post/${slug}/edit/`)
                .then(res => res.text())
                .then(html => {
                    // Replace the post content area with the edit form HTML
                    document.getElementById('post-content').innerHTML = html;
                });
        });
    }

    // Listen for submit events on the whole document
    document.addEventListener('submit', function (e) {
        // Check if the submitted form is the edit post form
        if (e.target && e.target.id === 'editPostForm') {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);

            // Send form data via POST to the edit endpoint
            fetch(form.action || window.location.pathname + 'edit/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Add CSRF token header
                },
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // If edit successful, update post content with new content
                    document.getElementById('post-content').innerHTML = data.updated_content;

                    // If updated timestamp is returned, update it on page
                    if (data.updated_on) {
                        document.getElementById('post-updated-on').textContent = 'Updated on: ' + data.updated_on;
                    }
                }
            })
            .catch(err => console.error('Fetch error:', err));
        }
    });

    // Listen for clicks to cancel the edit
    document.addEventListener('click', function (e) {
        if (e.target && e.target.id === 'cancel-edit') {
            // Reload the page to cancel editing and revert changes
            location.reload();
        }
    });
});
