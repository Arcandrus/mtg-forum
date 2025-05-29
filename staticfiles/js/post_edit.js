document.addEventListener('DOMContentLoaded', function () {
    const editBtn = document.getElementById('edit-post-btn');

    if (editBtn) {
        editBtn.addEventListener('click', function () {
            const slug = this.dataset.slug;

            fetch(`/post/${slug}/edit/`)
                .then(res => res.text())
                .then(html => {
                    document.getElementById('post-content').innerHTML = html;
                });
        });
    }

document.addEventListener('submit', function (e) {
    if (e.target && e.target.id === 'editPostForm') {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);

        fetch(form.action || window.location.pathname + 'edit/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('post-content').innerHTML = data.updated_content;
                if (data.updated_on) {
                    document.getElementById('post-updated-on').textContent = 'Updated on: ' + data.updated_on;
                }
            }
        })
        .catch(err => console.error('Fetch error:', err));
    }
});

    document.addEventListener('click', function (e) {
        if (e.target && e.target.id === 'cancel-edit') {
            location.reload(); // basic cancel logic
        }
    });
});