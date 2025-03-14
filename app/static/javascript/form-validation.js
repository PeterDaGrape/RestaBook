document.addEventListener('DOMContentLoaded', function() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    // validation styling 
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      input.addEventListener('blur', function() {
        validateField(this);
      });
      
      // check password strength
      if (input.type === 'password') {
        input.addEventListener('keyup', function() {
          checkPasswordStrength(this);
        });
      }
    });
    
    // submission validation
    form.addEventListener('submit', function(event) {
      let isValid = true;
      
      inputs.forEach(input => {
        if (!validateField(input)) {
          isValid = false;
        }
      });
      
      if (!isValid) {
        event.preventDefault();
        displayFormError("Please correct the errors in the form.");
      }
    });
  });
  
  // validate individual field
  function validateField(field) {
    // remove existing error messages
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
      existingError.remove();
    }
    
    // remove error styling
    field.classList.remove('error-input');
    
    // check if required field empty
    if (field.required && !field.value.trim()) {
      displayError(field, 'field is required');
      return false;
    }
    
    // email validation
    if (field.type === 'email' && field.value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(field.value)) {
        displayError(field, 'enter a valid email address');
        return false;
      }
    }
    
    // username validation
    if (field.name === 'username' && field.value) {
      const usernameRegex = /^[a-zA-Z0-9_]+$/;
      if (!usernameRegex.test(field.value)) {
        displayError(field, 'username can only contain letters, numbers, and underscores');
        return false;
      }
    }
    
    // password validation
    if (field.name === 'password' && field.value) {
      if (field.value.length < 8) {
        displayError(field, 'password must be at least 8 characters');
        return false;
      }
    }
    
    return true;
  }
  
  // display error for a specific field
  function displayError(field, message) {
    field.classList.add('error-input');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
  }
  
  // display general error
  function displayFormError(message) {
    const errorContainer = document.getElementById('form-errors') || createErrorContainer();
    errorContainer.textContent = message;
    errorContainer.style.display = 'block';
  }
  
  // create error container if it doesn't exist
  function createErrorContainer() {
    const container = document.createElement('div');
    container.id = 'form-errors';
    container.className = 'form-error-container';
    
    const form = document.querySelector('form');
    form.parentNode.insertBefore(container, form);
    
    return container;
  }
  
  // check password strength
  function checkPasswordStrength(passwordField) {
    // remove any existing strength indicator
    const existingIndicator = document.querySelector('.password-strength');
    if (existingIndicator) {
      existingIndicator.remove();
    }
    
    const password = passwordField.value;
    if (!password) return;
    
    // create strength indicator
    const strengthIndicator = document.createElement('div');
    strengthIndicator.className = 'password-strength';
    
    // calculate strength
    let strength = 0;
    if (password.length >= 8) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[a-z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    
    // set indicator text and class
    let strengthText = '';
    let strengthClass = '';
    
    switch (strength) {
      case 1:
        strengthText = 'Weak';
        strengthClass = 'weak';
        break;
      case 2:
      case 3:
        strengthText = 'Medium';
        strengthClass = 'medium';
        break;
      case 4:
      case 5:
        strengthText = 'Strong';
        strengthClass = 'strong';
        break;
    }
    
    strengthIndicator.textContent = `Password strength: ${strengthText}`;
    strengthIndicator.classList.add(strengthClass);
    
    passwordField.parentNode.appendChild(strengthIndicator);
  }
});