// FIXED JAVASCRIPT SECTION FOR ROOM DETAIL PAGE

// Unified CSRF token function
function getCSRFToken() {
    // Try multiple methods to get CSRF token
    const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (tokenElement) {
        return tokenElement.value;
    }
    
    // Fallback to cookie method
    return getCookie('csrftoken');
}

// Bookmark functionality
document.addEventListener('DOMContentLoaded', function() {
    const bookmarkBtn = document.querySelector('.bookmark-btn');
    if (bookmarkBtn) {
        bookmarkBtn.addEventListener('click', function() {
            const roomId = this.dataset.roomId;
            const bookmarkText = this.querySelector('.bookmark-text');
            console.log('Bookmark button clicked for room ID:', roomId);

            fetch(\/room/\/bookmark/\, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Bookmark response data:', data);
                if (data.bookmarked) {
                    this.classList.add('bookmarked');
                    bookmarkText.textContent = 'Remove from Favorites';
                } else {
                    this.classList.remove('bookmarked');
                    bookmarkText.textContent = 'Add to Favorites';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

// Show contact info
function showContactInfo() {
    try {
        new bootstrap.Modal(document.getElementById('contactModal')).show();
    } catch (error) {
        console.error('Error showing contact modal:', error);
        alert('Error opening contact information.');
    }
}

// Share room
function shareRoom() {
    if (navigator.share) {
        navigator.share({
            title: '{{ room.title }}',
            text: 'Check out this room: {{ room.title }}',
            url: window.location.href
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Link copied to clipboard!');
        }).catch(() => {
            // Further fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = window.location.href;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('Link copied to clipboard!');
        });
    }
}

// Report room functionality - FIXED VERSION
function reportRoom() {
    console.log('Report button clicked');
    {% if user.is_authenticated %}
        try {
            const modal = new bootstrap.Modal(document.getElementById('reportModal'));
            modal.show();
            console.log('Report modal opened successfully');
        } catch (error) {
            console.error('Error opening report modal:', error);
            alert('Error opening report form. Please refresh the page and try again.');
        }
    {% else %}
        alert('Please log in to report this property.');
        window.location.href = \"{% url 'accounts:login' %}\";
    {% endif %}
}

// Handle report form submission - FIXED VERSION
document.addEventListener('DOMContentLoaded', function() {
    const reportForm = document.getElementById('reportForm');
    if (reportForm) {
        reportForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Report form submitted');
            
            const formData = new FormData();
            formData.append('reason', document.getElementById('reportReason').value);
            formData.append('description', document.getElementById('reportDescription').value);
            
            const submitButton = this.querySelector('button[type=\"submit\"]');
            const originalText = submitButton.innerHTML;
            
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class=\"fas fa-spinner fa-spin me-2\"></i>Submitting...';
            
            fetch(\/room/{{ room.id }}/report/\, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData
            })
            .then(response => {
                console.log('Report response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Report response data:', data);
                if (data.success) {
                    // Close modal and show success message
                    try {
                        bootstrap.Modal.getInstance(document.getElementById('reportModal')).hide();
                    } catch (e) {
                        document.getElementById('reportModal').style.display = 'none';
                    }
                    
                    // Show success alert
                    showAlert('success', 'Report Submitted! Thank you for your feedback. We\\'ll review this property.');
                    
                    // Reset form
                    this.reset();
                } else {
                    showAlert('error', data.error || 'An error occurred while submitting your report.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('error', 'An error occurred while submitting your report. Please try again.');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
            });
        });
    }
});

// Show alert function
function showAlert(type, message) {
    const alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
    const iconClass = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
    
    const alertDiv = document.createElement('div');
    alertDiv.className = \lert \ alert-dismissible fade show position-fixed\;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = \
        <i class=\"\ me-2\"></i>
        <strong>\</strong>
        <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\"></button>
    \;
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Chat functionality - ENHANCED VERSION
(function() {
    'use strict';

    function initChatButton() {
        const chatBtn = document.getElementById('start-chat-btn');
        if (!chatBtn) {
            console.log(' CHAT: Button not found');
            return;
        }

        // Clear any existing handlers completely
        chatBtn.replaceWith(chatBtn.cloneNode(true));
        const newChatBtn = document.getElementById('start-chat-btn');

        // Our clean click handler
        newChatBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            console.log(' CHAT: Processing chat request...');

            const roomId = this.dataset.roomId || window.location.pathname.split('/').filter(Boolean).pop();
            const ownerName = this.dataset.ownerName;

            console.log(' CHAT Details:', { roomId, ownerName });

            // Immediate visual feedback
            const originalText = this.innerHTML;
            this.innerHTML = '<i class=\"fas fa-rocket me-2\"></i>Opening Chat...';
            this.disabled = true;
            this.style.pointerEvents = 'none';

            // Navigate directly
            const chatUrl = \/chat/start/\/\;
            console.log(' CHAT: Redirecting to:', chatUrl);

            window.location.href = chatUrl;
        });

        console.log(' CHAT: Enhanced chat button ready!');
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatButton);
    } else {
        initChatButton();
    }

    // Also initialize after a short delay to override any late-loading scripts
    setTimeout(initChatButton, 1000);
})();

// Show all reviews
function showAllReviews() {
    alert('Show all reviews feature coming soon!');
}

// CSRF token helper (original version kept for compatibility)
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

// Thumbnail click functionality
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.thumbnail').forEach((thumb, index) => {
        thumb.addEventListener('click', function() {
            // Remove active class from all thumbnails
            document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
            // Add active class to clicked thumbnail
            this.classList.add('active');
        });
    });
});

console.log(' All JavaScript loaded successfully!');
