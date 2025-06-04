// Reply function
document.querySelectorAll('.reply-btn').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();

        const btn = e.currentTarget;
        const commentId = btn.dataset.commentId;
        const parentInput = document.querySelector('#id_parent');

        if (commentId) {
            parentInput.value = commentId;
        } else {
            parentInput.value = ''; 
        }

        const form = document.querySelector('form');
        form.querySelector('textarea[name="content"]').value = '';
        form.querySelector('textarea[name="content"]').focus();

    });
});


// Collapsable reply thread
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toggle-replies').forEach(button => {
        const targetSelector = button.getAttribute('data-bs-target');
        const target = document.querySelector(targetSelector);

        if (!target) return;

        // Use data attribute or fallback to count children
        const replyCount = button.getAttribute('data-reply-count') || target.children.length;

        // Create a Bootstrap Collapse instance for this target (do NOT auto-toggle)
        const collapseInstance = bootstrap.Collapse.getOrCreateInstance(target, {
            toggle: false
        });

        // Update button text based on target state
        function updateButtonText() {
            if (target.classList.contains('show')) {
                button.textContent = `Hide Replies (${replyCount})`;
                button.setAttribute('aria-expanded', 'true');
            } else {
                button.textContent = `Show Replies (${replyCount})`;
                button.setAttribute('aria-expanded', 'false');
            }
        }

        // Listen only to this collapse's shown/hidden events
        target.addEventListener('shown.bs.collapse', updateButtonText);
        target.addEventListener('hidden.bs.collapse', updateButtonText);

        // Initialize text
        updateButtonText();

        // Toggle the collapse on button click
        button.addEventListener('click', (e) => {
            collapseInstance.toggle();
            e.preventDefault();
        });
    });
});


// Edit comments
document.addEventListener('DOMContentLoaded', () => {
    const editModal = document.getElementById('editCommentModal');
    const editForm = document.getElementById('editCommentForm');
    const editContent = document.getElementById('editCommentContent');
    const editParent = document.getElementById('editCommentParent'); // new hidden input

    let pendingContent = '';  // Store comment content temporarily
    let pendingCommentId = ''; // Store comment ID
    let pendingParentId = '';  // Store parent ID

    // Initialize Summernote when modal is shown
    $(editModal).on('shown.bs.modal', function () {
        $(editContent).summernote({
            height: 150,
            focus: true
        });

        // Now that it's initialized, set the content
        $(editContent).summernote('code', pendingContent);

        // Set form action
        editForm.action = `/comments/edit/${pendingCommentId}/`;

        // Set hidden parent input
        editParent.value = pendingParentId || '';
    });

    // Destroy Summernote when modal hidden
    $(editModal).on('hidden.bs.modal', function () {
        $(editContent).summernote('destroy');
        editForm.action = '';
        pendingContent = '';
        pendingCommentId = '';
        pendingParentId = '';
        editParent.value = '';
    });

    // Set pending data when edit button is clicked
    document.querySelectorAll('.edit-comment-btn').forEach(button => {
        button.addEventListener('click', () => {
            pendingCommentId = button.getAttribute('data-comment-id');
            pendingContent = button.getAttribute('data-content');
            pendingParentId = button.getAttribute('data-parent-id') || '';
        });
    });
});
