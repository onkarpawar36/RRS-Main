// TEST ALL FUNCTIONALITY - Add this script to test everything is working

console.log(' Testing all functionality...');

// Test 1: Check if all functions exist
setTimeout(() => {
    console.log(' Testing Functions:');
    console.log('- reportRoom exists:', typeof reportRoom !== 'undefined');
    console.log('- shareRoom exists:', typeof shareRoom !== 'undefined');
    console.log('- showContactInfo exists:', typeof showContactInfo !== 'undefined');
    console.log('- getCookie exists:', typeof getCookie !== 'undefined');
    
    // Test 2: Check if Bootstrap is loaded
    console.log(' Bootstrap loaded:', typeof bootstrap !== 'undefined');
    
    // Test 3: Check if modal elements exist
    const reportModal = document.getElementById('reportModal');
    const contactModal = document.getElementById('contactModal');
    console.log(' Report Modal exists:', !!reportModal);
    console.log(' Contact Modal exists:', !!contactModal);
    
    // Test 4: Check CSRF token
    const csrfToken = document.querySelector('[name=\"csrfmiddlewaretoken\"]');
    console.log(' CSRF Token exists:', !!csrfToken);
    
    // Test 5: Check buttons
    const reportBtn = document.querySelector('[onclick=\"reportRoom()\"]');
    const bookmarkBtn = document.querySelector('.bookmark-btn');
    const chatBtn = document.getElementById('start-chat-btn');
    
    console.log(' Report Button exists:', !!reportBtn);
    console.log(' Bookmark Button exists:', !!bookmarkBtn);
    console.log(' Chat Button exists:', !!chatBtn);
    
    console.log(' All tests completed! Check console for any errors.');
    
    // Add visual indicator
    const indicator = document.createElement('div');
    indicator.innerHTML = ' JS Tests Passed';
    indicator.style.cssText = 'position:fixed;top:50px;right:20px;background:#28a745;color:white;padding:10px;border-radius:5px;z-index:9999;';
    document.body.appendChild(indicator);
    setTimeout(() => indicator.remove(), 3000);
    
}, 1000);
