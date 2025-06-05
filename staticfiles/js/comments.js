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

// Edit comments functionality: handles loading comment content into a modal form with Summernote editor
document.addEventListener('DOMContentLoaded', () => {
    const editModal = document.getElementById('editCommentModal'); // Modal element for editing
    const editForm = document.getElementById('editCommentForm'); // Form inside the modal
    const editContent = document.getElementById('editCommentContent'); // Textarea for comment content in modal
    const editParent = document.getElementById('editCommentParent'); // Hidden input for parent comment ID in modal

    // Variables to temporarily store current comment data to edit
    let pendingContent = '';  
    let pendingCommentId = ''; 
    let pendingParentId = '';  

    // Initialize Summernote editor when modal is shown
    $(editModal).on('shown.bs.modal', function () {
        $(editContent).summernote({
            height: 150, // Set editor height
            focus: true  // Automatically focus the editor
        });

        // Set the editor content to the comment text stored in pendingContent
        $(editContent).summernote('code', pendingContent);

        // Set the form's action URL dynamically to submit the edited comment
        editForm.action = `/comments/edit/${pendingCommentId}/`;

        // Set the hidden parent ID input value in the form
        editParent.value = pendingParentId || '';
    });

    // Clean up Summernote editor and reset form when modal is hidden
    $(editModal).on('hidden.bs.modal', function () {
        $(editContent).summernote('destroy'); // Destroy the Summernote editor instance
        editForm.action = '';                  // Reset form action
        pendingContent = '';                   // Clear temporary variables
        pendingCommentId = '';
        pendingParentId = '';
        editParent.value = '';                 // Clear hidden parent input
    });

    // Set pending comment data (content, comment ID, parent ID) when an edit button is clicked
    document.querySelectorAll('.edit-comment-btn').forEach(button => {
        button.addEventListener('click', () => {
            pendingCommentId = button.getAttribute('data-comment-id'); // Get comment ID
            pendingContent = button.getAttribute('data-content');      // Get comment content
            pendingParentId = button.getAttribute('data-parent-id') || ''; // Get parent ID, or empty
        });
    });
});
