document.addEventListener('DOMContentLoaded', () => {
    // Select all list items inside the element with class 'messages'
    const messages = document.querySelectorAll('.messages li');
    
    if (messages.length) {
        // After 2 seconds, start fading out each message by setting opacity to 0
        setTimeout(() => {
            messages.forEach(msg => {
                msg.style.opacity = '0';
            });
        }, 2000);

        // After 6 seconds, remove the entire messages container from the DOM
        setTimeout(() => {
            const messagesContainer = document.querySelector('.messages');
            if (messagesContainer) {
                messagesContainer.remove();
            }
        }, 6000);
    }
});
