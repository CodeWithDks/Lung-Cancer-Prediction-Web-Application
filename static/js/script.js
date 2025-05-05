document.addEventListener('DOMContentLoaded', function() {
    // Form validation and submission handling
    const predictionForm = document.getElementById('prediction-form');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(event) {
            // Prevent the default form submission
            event.preventDefault();
            
            // Validate the form
            if (validateForm()) {
                // If validation passes, submit the form
                this.submit();
            }
        });
    }
    
    // Initialize collapsible sections in history cards
    initializeCollapsibleSections();
    
    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add form reset confirmation
    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to reset the form?')) {
                e.preventDefault();
            }
        });
    }
});

// Form validation
function validateForm() {
    let isValid = true;
    
    // Get all required inputs
    const requiredInputs = document.querySelectorAll('[required]');
    
    // Check each required input
    requiredInputs.forEach(input => {
        if (!input.value) {
            isValid = false;
            showError(input, 'This field is required');
        } else {
            clearError(input);
        }
    });
    
    // Validate age specifically
    const ageInput = document.getElementById('AGE');
    if (ageInput) {
        const age = parseInt(ageInput.value);
        if (isNaN(age) || age < 0 || age > 120) {
            isValid = false;
            showError(ageInput, 'Age must be between 0 and 120');
        }
    }
    
    return isValid;
}

// Show error message
function showError(input, message) {
    // Clear any existing error
    clearError(input);
    
    // Create error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'error-text';
    errorElement.textContent = message;
    errorElement.style.color = 'red';
    errorElement.style.fontSize = '0.85rem';
    errorElement.style.marginTop = '5px';
    
    // Insert the error message after the input
    input.parentNode.appendChild(errorElement);
    
    // Highlight the input
    input.style.borderColor = 'red';
}

// Clear error message
function clearError(input) {
    // Remove any existing error message
    const parent = input.parentNode;
    const errorElement = parent.querySelector('.error-text');
    if (errorElement) {
        parent.removeChild(errorElement);
    }
    
    // Reset input style
    input.style.borderColor = '';
}

// Initialize collapsible sections
function initializeCollapsibleSections() {
    const historyCards = document.querySelectorAll('.history-card');
    
    historyCards.forEach(card => {
        const header = card.querySelector('.history-header');
        const details = card.querySelector('.history-details');
        
        if (header && details) {
            // Initially hide details
            details.style.display = 'none';
            
            // Add click handler to header
            header.addEventListener('click', function() {
                // Toggle details visibility
                if (details.style.display === 'none') {
                    details.style.display = 'block';
                    header.classList.add('active');
                } else {
                    details.style.display = 'none';
                    header.classList.remove('active');
                }
            });
            
            // Add cursor style to indicate it's clickable
            header.style.cursor = 'pointer';
        }
    });
}

// Function to enable API mode for developers
function enableApiMode() {
    console.log('API Mode enabled');
    
    // Add API documentation link
    const container = document.querySelector('.container');
    
    if (container) {
        const apiInfo = document.createElement('div');
        apiInfo.className = 'api-info';
        apiInfo.innerHTML = `
            <h3>API Endpoints</h3>
            <ul>
                <li><code>POST /predict</code> - Make a prediction (send JSON data)</li>
                <li><code>GET /api/predictions</code> - Get prediction history</li>
                <li><code>GET /api/prediction/:id</code> - Get a specific prediction</li>
            </ul>
        `;
        
        // Add style to apiInfo
        apiInfo.style.backgroundColor = '#f8f9fa';
        apiInfo.style.padding = '15px';
        apiInfo.style.borderRadius = '8px';
        apiInfo.style.marginTop = '20px';
        
        // Check if apiInfo already exists
        const existingApiInfo = document.querySelector('.api-info');
        if (!existingApiInfo) {
            // Append to container
            container.appendChild(apiInfo);
        }
    }
    
    // Return API info for reference
    return {
        endpoints: {
            predict: '/predict',
            getAllPredictions: '/api/predictions',
            getPrediction: '/api/prediction/:id'
        },
        contentType: 'application/json',
        sampleRequest: {
            GENDER: 1,
            AGE: 65,
            SMOKING: 2,
            YELLOW_FINGERS: 2,
            ANXIETY: 1,
            PEER_PRESSURE: 2,
            "CHRONIC DISEASE": 1,
            FATIGUE: 2,
            ALLERGY: 1,
            WHEEZING: 2,
            "ALCOHOL CONSUMING": 2,
            COUGHING: 2,
            "SHORTNESS OF BREATH": 2,
            "SWALLOWING DIFFICULTY": 2,
            "CHEST PAIN": 2
        }
    };
}