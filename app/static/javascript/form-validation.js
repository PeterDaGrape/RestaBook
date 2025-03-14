document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', (event) => {
      const inputs = form.querySelectorAll('input, select, textarea');
      let isValid = true;
  
      inputs.forEach(input => {
        if (!input.value.trim()) {
          isValid = false;
          input.classList.add('error');
        } else {
          input.classList.remove('error');
        }
      });
  
      if (!isValid) {
        event.preventDefault();
        alert("fill out all fields");
      }
    });
  });
  