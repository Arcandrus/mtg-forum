// Reply function: handles setting the parent comment ID when a reply button is clicked
document.querySelectorAll('.reply-btn').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();

        const btn = e.currentTarget;
        const commentId = btn.dataset.commentId;  // Get the comment ID from data attribute
        const parentInput = document.querySelector('#id_parent'); // Hidden input to track parent comment ID

        if (commentId) {
            parentInput.value = commentId; // Set hidden input to the clicked comment's ID
        } else {
            parentInput.value = ''; // Clear if no comment ID found (should not happen usually)
        }

        const form = document.querySelector('form'); // The comment form
        form.querySelector('textarea[name="content"]').value = ''; // Clear textarea for new reply
        form.querySelector('textarea[name="content"]').focus();   // Focus on textarea to start typing
    });
});

// Collapsable reply thread: toggles showing/hiding replies under comments using Bootstrap collapse
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toggle-replies').forEach(button => {
        const targetSelector = button.getAttribute('data-bs-target'); // Selector for collapse target
        const target = document.querySelector(targetSelector); // Collapse container element

        if (!target) return; // If target doesn't exist, skip

        // Determine number of replies either from data attribute or by counting child elements
        const replyCount = button.getAttribute('data-reply-count') || target.children.length;

        // Create or get Bootstrap Collapse instance for the target, without toggling automatically
        const collapseInstance = bootstrap.Collapse.getOrCreateInstance(target, {
            toggle: false
        });

        // Function to update the button's label and aria-expanded attribute based on collapse state
        function updateButtonText() {
            if (target.classList.contains('show')) {
                button.textContent = `Hide Replies (${replyCount})`;
                button.setAttribute('aria-expanded', 'true');
            } else {
                button.textContent = `Show Replies (${replyCount})`;
                button.setAttribute('aria-expanded', 'false');
            }
        }

        // Listen to Bootstrap collapse show/hide events to update button text dynamically
        target.addEventListener('shown.bs.collapse', updateButtonText);
        target.addEventListener('hidden.bs.collapse', updateButtonText);

        // Initialize button text on page load
        updateButtonText();

        // Toggle collapse visibility when the button is clicked
        button.addEventListener('click', (e) => {
            collapseInstance.toggle();
            e.preventDefault(); // Prevent default link/button behavior
        });
    });
});

// Edit comment: loads an inline summernote form to allow users to edit the comment
document.addEventListener('DOMContentLoaded', function () {
    // When an edit-comment-btn is clicked
    document.addEventListener('click', function (e) {
        const editBtn = e.target.closest('.edit-comment-btn, .edit-reply-btn');
        if (editBtn) {
            console.log('Edit button clicked');
            const commentId = editBtn.getAttribute('data-comment-id');
            const displayDiv = document.getElementById(`comment-display-${commentId}`);

            if (!displayDiv) {
                console.error('Display div not found for comment id:', commentId);
                return;
            }

            // Remove any existing edit form before inserting a new one
            const existingForm = displayDiv.querySelector('form.comment-edit-form');
            if (existingForm) {
                existingForm.remove();
                // Also restore original content if any
                const originalContent = displayDiv.getAttribute('data-original-content');
                if (originalContent !== null) {
                    displayDiv.innerHTML = originalContent;
                }
            }

            // Save the current content before replacing it with the form
            displayDiv.setAttribute('data-original-content', displayDiv.innerHTML);

            fetch(`/comment/${commentId}/edit/`)
                .then(res => {
                    if (!res.ok) throw new Error('Failed to load edit form');
                    return res.text();
                })
                .then(html => {
                    displayDiv.innerHTML = html;
                })
                .catch(err => console.error('Fetch error loading edit form:', err));
        }
    });

    // When comment-edit-form is submitted
    document.addEventListener('submit', function (e) {
        const form = e.target;
        if (form.classList.contains('comment-edit-form')) {
            e.preventDefault();

            const formData = new FormData(form);
            const commentId = form.getAttribute('data-comment-id');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Replace with updated content (no form)
                        document.getElementById(`comment-display-${commentId}`).innerHTML = data.updated_content;
                    } else {
                        console.error('Form submission error:', data.errors);
                        // Optionally display errors inside the form
                    }
                })
                .catch(err => console.error('Fetch error submitting comment edit:', err));
        }
    });

    // Cancel edit button
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('cancel-comment-edit')) {
            e.preventDefault();

            const btn = e.target;
            const commentId = btn.getAttribute('data-comment-id');
            const displayDiv = document.getElementById(`comment-display-${commentId}`);

            if (!displayDiv) {
                console.error('Display div not found for comment id:', commentId);
                return;
            }

            // Restore original comment content saved on data attribute
            const originalContent = displayDiv.getAttribute('data-original-content');
            if (originalContent !== null) {
                displayDiv.innerHTML = originalContent;
            } else {
                // fallback: reload page if no saved content
                location.reload();
            }
        }
    });
});
