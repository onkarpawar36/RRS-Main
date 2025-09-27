// Main JavaScript file for RentalHub

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initializeAnimations();
    
    // Initialize form validations
    initializeFormValidation();
    
    // Initialize image galleries
    initializeImageGalleries();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize search functionality
    initializeSearch();
});

// Animation Functions
function initializeAnimations() {
    // Fade in elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

// Form Validation
function initializeFormValidation() {
    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Add shake animation to invalid form
                form.classList.add('shake');
                setTimeout(() => form.classList.remove('shake'), 500);
            }
            
            form.classList.add('was-validated');
        });
    });

    // Real-time validation feedback
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
}

function validateField(field) {
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
}

// Image Gallery Functions
function initializeImageGalleries() {
    const galleries = document.querySelectorAll('.image-gallery');
    
    galleries.forEach(gallery => {
        const mainImg = gallery.querySelector('.gallery-main-img');
        const thumbnails = gallery.querySelectorAll('.gallery-thumbnail');
        
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                // Update main image
                mainImg.src = this.src;
                mainImg.alt = this.alt;
                
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // Add loading animation
                mainImg.style.opacity = '0.5';
                setTimeout(() => {
                    mainImg.style.opacity = '1';
                }, 200);
            });
        });
    });
}

// Tooltip Initialization
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href !== '#' && href !== '#!') {
                e.preventDefault();
                
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Search Functionality
function initializeSearch() {
    const searchInputs = document.querySelectorAll('.search-input input');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.toLowerCase().trim();
            
            searchTimeout = setTimeout(() => {
                performSearch(query, this);
            }, 300);
        });
    });
}

function performSearch(query, input) {
    const searchContainer = input.closest('.search-container');
    if (!searchContainer) return;
    
    const items = searchContainer.querySelectorAll('.searchable-item');
    let visibleCount = 0;
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        const isVisible = query === '' || text.includes(query);
        
        item.style.display = isVisible ? '' : 'none';
        if (isVisible) visibleCount++;
        
        // Add highlight effect
        if (query && isVisible) {
            item.classList.add('search-highlight');
        } else {
            item.classList.remove('search-highlight');
        }
    });
    
    // Show/hide no results message
    updateNoResultsMessage(searchContainer, visibleCount, query);
}

function updateNoResultsMessage(container, count, query) {
    let noResultsMsg = container.querySelector('.no-results-message');
    
    if (count === 0 && query) {
        if (!noResultsMsg) {
            noResultsMsg = document.createElement('div');
            noResultsMsg.className = 'no-results-message text-center text-muted py-4';
            noResultsMsg.innerHTML = `
                <i class="fas fa-search fa-2x mb-3"></i>
                <p>No results found for "${query}"</p>
            `;
            container.appendChild(noResultsMsg);
        }
        noResultsMsg.style.display = 'block';
    } else if (noResultsMsg) {
        noResultsMsg.style.display = 'none';
    }
}

// Image Upload Preview
function previewImage(input, previewContainer) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const img = previewContainer.querySelector('img') || document.createElement('img');
            img.src = e.target.result;
            img.className = 'img-thumbnail';
            img.style.maxWidth = '200px';
            img.style.maxHeight = '200px';
            
            if (!previewContainer.querySelector('img')) {
                previewContainer.appendChild(img);
            }
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Auto-resize textareas
function initializeAutoResize() {
    const textareas = document.querySelectorAll('textarea.auto-resize');
    
    textareas.forEach(textarea => {
        textarea.style.overflow = 'hidden';
        textarea.style.resize = 'none';
        
        function resize() {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        }
        
        textarea.addEventListener('input', resize);
        resize(); // Initial resize
    });
}

// Loading Spinner Functions
function showLoader(button) {
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    button.disabled = true;
}

function hideLoader(button) {
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Notification System
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Form Submission with Loading
function handleFormSubmit(form, button) {
    showLoader(button);
    
    // Simulate form submission delay
    setTimeout(() => {
        hideLoader(button);
    }, 2000);
}

// Price Formatter
function formatPrice(amount, currency = '₹') {
    return currency + amount.toLocaleString();
}

// Date Formatter
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Initialize Map (placeholder for future map integration)
function initializeMap(container, lat, lng) {
    // This would integrate with Google Maps or similar service
    console.log(`Map initialized at ${lat}, ${lng}`);
}

// AJAX Helper Functions
function ajaxGet(url, callback) {
    fetch(url)
        .then(response => response.json())
        .then(data => callback(null, data))
        .catch(error => callback(error, null));
}

function ajaxPost(url, data, callback) {
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => callback(null, data))
    .catch(error => callback(error, null));
}

// Get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Utility function to debounce function calls
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    .shake {
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .search-highlight {
        animation: highlight 0.3s ease-in-out;
    }
    
    @keyframes highlight {
        0% { background-color: transparent; }
        50% { background-color: rgba(255, 255, 0, 0.2); }
        100% { background-color: transparent; }
    }
`;
document.head.appendChild(style);