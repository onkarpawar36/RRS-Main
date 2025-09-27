// TEST REPORT FUNCTIONALITY
console.log('Testing report functionality...');

// Test if Bootstrap is loaded
if (typeof bootstrap !== 'undefined') {
    console.log(' Bootstrap is loaded');
} else {
    console.error(' Bootstrap not found');
}

// Test CSRF token
function testCSRFToken() {
    const token1 = document.querySelector('[name=csrfmiddlewaretoken]');
    console.log('CSRF Token Element:', token1);
    
    if (token1) {
        console.log(' CSRF token found:', token1.value.substring(0, 10) + '...');
    } else {
        console.error(' CSRF token not found');
    }
}

// Test report modal
function testReportModal() {
    const modal = document.getElementById('reportModal');
    console.log('Report Modal Element:', modal);
    
    if (modal) {
        console.log(' Report modal found');
        try {
            const bootstrapModal = new bootstrap.Modal(modal);
            console.log(' Bootstrap modal created successfully');
            bootstrapModal.show();
            console.log(' Modal shown successfully');
            setTimeout(() => {
                bootstrapModal.hide();
                console.log(' Modal hidden successfully');
            }, 2000);
        } catch (error) {
            console.error(' Error with Bootstrap modal:', error);
        }
    } else {
        console.error(' Report modal not found');
    }
}

// Run tests when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, running tests...');
    testCSRFToken();
    
    // Add test button to page
    const testButton = document.createElement('button');
    testButton.textContent = 'TEST REPORT MODAL';
    testButton.className = 'btn btn-danger';
    testButton.style.position = 'fixed';
    testButton.style.top = '10px';
    testButton.style.right = '10px';
    testButton.style.zIndex = '9999';
    testButton.onclick = testReportModal;
    document.body.appendChild(testButton);
    
    console.log(' Test button added to page');
});
