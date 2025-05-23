// Reply function
document.querySelectorAll('.reply-btn').forEach(button => {
  button.addEventListener('click', function(e) {
    e.preventDefault();
    console.log("Reply button clicked!");

    const commentId = e.target.dataset.commentId;
    console.log("commentId:", commentId);

    const parentInput = document.querySelector('#id_parent');
    console.log("Before setting:", parentInput.value);

    parentInput.value = commentId;

    console.log("After setting:", parentInput.value);

    form.querySelector('textarea[name="content"]').value = '';

    form.querySelector('textarea[name="content"]').focus();

    const commentModal = new bootstrap.Modal(document.getElementById('commentModal'));
    commentModal.show();
  });
});

// Collapsable reply thread
document.querySelectorAll('.toggle-replies').forEach(button => {
  const targetSelector = button.getAttribute('data-bs-target');
  const target = document.querySelector(targetSelector);
  if (!target) return;

  const replyCount = button.dataset.replyCount || target.children.length;

  target.addEventListener('show.bs.collapse', (event) => {
    // Only update button if event target matches
    if (event.target === target) {
      button.textContent = `Hide Replies (${replyCount})`;
    }
  });

  target.addEventListener('hide.bs.collapse', (event) => {
    if (event.target === target) {
      button.textContent = `Show Replies (${replyCount})`;
    }
  });

  // Initialize on load
  button.textContent = target.classList.contains('show') ? 
    `Hide Replies (${replyCount})` : 
    `Show Replies (${replyCount})`;
});