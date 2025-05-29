document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.messages li');
    if (messages.length) {
      setTimeout(() => {
        messages.forEach(msg => {
          msg.style.opacity = '0';
        });
      }, 2000);
      
      setTimeout(() => {
        const messagesContainer = document.querySelector('.messages');
        if (messagesContainer) {
          messagesContainer.remove();
        }
      }, 6000);
    }
  });