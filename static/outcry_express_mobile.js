// Outcry Express Mobile App JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Global variables
let bookings = [];
let pickupAutocomplete = null;
let dropoffAutocomplete = null;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initializeApp();
});

function initializeApp() {
    // Set up menu navigation
    setupMenuNavigation();
    
    // Load bookings from database
    loadBookings();
    
    // Load initial page
    loadPage('home');
}

function setupMenuNavigation() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const page = this.getAttribute('data-page');
            
            // Remove active class from all items and their icons
            menuItems.forEach(menuItem => {
                menuItem.classList.remove('active');
                const icon = menuItem.querySelector('.menu-icon');
                if (icon) {
                    icon.classList.remove('active');
                }
            });
            
            // Add active class to clicked item and its icon
            this.classList.add('active');
            const icon = this.querySelector('.menu-icon');
            if (icon) {
                icon.classList.add('active');
            }
            
            // Load the page
            loadPage(page);
            
            // Refresh bookings when switching to home or history
            if (page === 'home' || page === 'history') {
                refreshBookings();
            }
        });
    });
}

function loadPage(page) {
    const mainContent = document.querySelector('.main-content');
    
    // Clear existing content
    mainContent.innerHTML = '';
    
    switch(page) {
        case 'home':
            loadHomePage(mainContent);
            break;
        case 'history':
            loadHistoryPage(mainContent);
            break;
        case 'account':
            loadAccountPage(mainContent);
            break;
        default:
            loadHomePage(mainContent);
    }
}

// Load bookings from API
async function loadBookings() {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings`);
        if (response.ok) {
            bookings = await response.json();
        } else {
            console.error('Error loading bookings:', response.statusText);
            bookings = [];
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
        bookings = [];
    }
}

function loadHomePage(container) {
    // Filter incomplete bookings
    const incompleteBookings = bookings.filter(booking => !booking.completion);
    
    let bookingsHTML = '';
    if (incompleteBookings.length > 0) {
        incompleteBookings.forEach(booking => {
            const pickupDate = new Date(booking.pickup_date);
            const dropoffDate = new Date(booking.dropoff_date);
            const pickupTime = booking.pickup_time ? new Date(`2000-01-01T${booking.pickup_time}`).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) : '';
            const dropoffTime = booking.dropoff_time ? new Date(`2000-01-01T${booking.dropoff_time}`).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) : '';
            
            const dateTimeStr = formatBookingDateTime(pickupDate, pickupTime, dropoffDate, dropoffTime);
            const routeStr = formatBookingRoute(booking.pickup_address, booking.dropoff_address);
            
                     bookingsHTML += `
                         <div class="booking-item" onclick="viewBookingModal(${booking.booking_id})">
                             <div class="booking-info">
                                 <div class="booking-date-time">${dateTimeStr}</div>
                                 <hr class="booking-divider">
                                 <div class="booking-number-route">
                                     <span class="booking-number">#${booking.booking_id.toString().padStart(3, '0')}</span>
                                     <span class="booking-route">${routeStr}</span>
                                 </div>
                             </div>
                         </div>
                     `;
        });
    } else {
        bookingsHTML = `
            <div class="empty-state">
                <p>No active bookings</p>
                <p>All your bookings are complete or create a new one</p>
            </div>
        `;
    }
    
    container.innerHTML = `
        <div class="page-content">
            <div class="page-header">
                <img src="static/Outcry_Express_WhiteBG.svg" alt="Outcry Express" class="header-logo">
                <button class="new-booking-btn" onclick="createNewBooking()">+ New Booking</button>
            </div>
            <div class="bookings-list">
                ${bookingsHTML}
            </div>
        </div>
    `;
}

function loadHistoryPage(container) {
    // Filter complete bookings
    const completeBookings = bookings.filter(booking => booking.completion);
    
    let bookingsHTML = '';
    if (completeBookings.length > 0) {
        completeBookings.forEach(booking => {
            const pickupDate = new Date(booking.pickup_date);
            const dropoffDate = new Date(booking.dropoff_date);
            const pickupTime = booking.pickup_time ? new Date(`2000-01-01T${booking.pickup_time}`).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) : '';
            const dropoffTime = booking.dropoff_time ? new Date(`2000-01-01T${booking.dropoff_time}`).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) : '';
            
            const dateTimeStr = formatBookingDateTime(pickupDate, pickupTime, dropoffDate, dropoffTime);
            const routeStr = formatBookingRoute(booking.pickup_address, booking.dropoff_address);
            
                     bookingsHTML += `
                         <div class="booking-item history" onclick="viewBookingModal(${booking.booking_id})">
                             <div class="booking-info">
                                 <div class="booking-date-time">${dateTimeStr}</div>
                                 <hr class="booking-divider">
                                 <div class="booking-number-route">
                                     <span class="booking-number">#${booking.booking_id.toString().padStart(3, '0')}</span>
                                     <span class="booking-route">${routeStr}</span>
                                 </div>
                             </div>
                         </div>
                     `;
        });
    } else {
        bookingsHTML = `
            <div class="empty-state">
                <p>No completed bookings</p>
                <p>Your completed deliveries will appear here</p>
            </div>
        `;
    }
    
    container.innerHTML = `
        <div class="page-content">
            <div class="page-header">
                <img src="static/Outcry_Express_WhiteBG.svg" alt="Outcry Express" class="header-logo">
                <div class="search-container">
                    <input type="text" id="historySearch" class="search-input" placeholder="Search bookings...">
                    <button class="search-button" onclick="searchBookings()">🔍</button>
                </div>
            </div>
            <div class="bookings-list">
                ${bookingsHTML}
            </div>
        </div>
    `;
}

function loadAccountPage(container) {
    container.innerHTML = `
        <div class="page-content">
            <div class="page-header">
                <img src="static/Outcry_Express_WhiteBG.svg" alt="Outcry Express" class="header-logo">
            </div>
            <div class="account-actions">
                <button class="change-password-text-btn" onclick="changePassword()">
                    Change Password
                </button>
                <button class="logout-text-btn" onclick="logout()">
                    Logout
                </button>
            </div>
        </div>
    `;
}

function createNewBooking() {
    // Navigate to the new booking page
    window.location.href = '/outcry-express-new-booking';
}


// Helper function to format booking date and time
function formatBookingDateTime(pickupDate, pickupTime, dropoffDate, dropoffTime) {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    let dateStr = '';
    if (pickupDate.toDateString() === today.toDateString()) {
        dateStr = 'Today';
    } else if (pickupDate.toDateString() === yesterday.toDateString()) {
        dateStr = 'Yesterday';
    } else if (pickupDate.toDateString() === tomorrow.toDateString()) {
        dateStr = 'Tomorrow';
    } else {
        dateStr = pickupDate.toLocaleDateString('en-US', { 
            weekday: 'long', 
            month: 'short', 
            day: 'numeric' 
        });
    }
    
    const timeStr = pickupTime && dropoffTime ? `(${pickupTime} - ${dropoffTime})` : 
                   pickupTime ? `(${pickupTime})` : '';
    
    return `${dateStr} ${timeStr}`;
}

// Helper function to format booking route
function formatBookingRoute(pickupAddress, dropoffAddress) {
    const pickupSuburb = pickupAddress?.suburb || 'Unknown';
    const dropoffSuburb = dropoffAddress?.suburb || 'Unknown';
    return `${pickupSuburb} - ${dropoffSuburb}`;
}

function changePassword() {
    // This function will be called when the Change Password button is clicked
    alert('Change Password functionality will be implemented here');
    // Future: Open a modal or navigate to a change password form
}

function logout() {
    // This function will be called when the Logout button is clicked
    if (confirm('Are you sure you want to logout?')) {
        alert('Logout functionality will be implemented here');
        // Future: Clear session and redirect to login page
    }
}

function searchBookings() {
    const searchTerm = document.getElementById('historySearch').value.toLowerCase();
    const bookingItems = document.querySelectorAll('.booking-item.history');
    
    bookingItems.forEach(item => {
        const dateTime = item.querySelector('.booking-date-time').textContent.toLowerCase();
        const bookingNumber = item.querySelector('.booking-number').textContent.toLowerCase();
        const bookingRoute = item.querySelector('.booking-route').textContent.toLowerCase();
        
        const matches = dateTime.includes(searchTerm) || 
                       bookingNumber.includes(searchTerm) || 
                       bookingRoute.includes(searchTerm);
        
        item.style.display = matches ? 'flex' : 'none';
    });
}

// View booking modal function
function viewBookingModal(bookingId) {
    // Find the booking data
    const booking = bookings.find(b => b.booking_id === bookingId);
    if (!booking) {
        console.error('Booking not found:', bookingId);
        return;
    }
    
    // Format dates and times
    const pickupDate = new Date(booking.pickup_date);
    const dropoffDate = new Date(booking.dropoff_date);
    const pickupTime = booking.pickup_time ? new Date(`2000-01-01T${booking.pickup_time}`).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) : 'Not specified';
    const dropoffTime = booking.dropoff_time ? new Date(`2000-01-01T${booking.dropoff_time}`).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) : 'Not specified';
    
    // Format pickup and dropoff addresses
    const pickupAddress = booking.pickup_address ? booking.pickup_address.formatted_address : 'Not specified';
    const dropoffAddress = booking.dropoff_address ? booking.dropoff_address.formatted_address : 'Not specified';
    
    // Create and show the view booking modal
    const modal = document.createElement('div');
    modal.className = 'view-booking-modal-overlay';
    modal.innerHTML = `
        <div class="view-booking-modal">
            <div class="modal-header">
                <h2>Booking #${booking.booking_id.toString().padStart(3, '0')}</h2>
                <button class="close-modal-btn" onclick="closeViewBookingModal()">×</button>
            </div>
            <div class="modal-content">
                <div class="booking-details">
                    <div class="detail-section">
                        <h3>Pickup Details</h3>
                        <div class="detail-item">
                            <label>Date:</label>
                            <span>${pickupDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
                        </div>
                        <div class="detail-item">
                            <label>Time:</label>
                            <span>${pickupTime}</span>
                        </div>
                        <div class="detail-item">
                            <label>Address:</label>
                            <span>${pickupAddress}</span>
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h3>Dropoff Details</h3>
                        <div class="detail-item">
                            <label>Date:</label>
                            <span>${dropoffDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
                        </div>
                        <div class="detail-item">
                            <label>Time:</label>
                            <span>${dropoffTime}</span>
                        </div>
                        <div class="detail-item">
                            <label>Address:</label>
                            <span>${dropoffAddress}</span>
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h3>Additional Information</h3>
                        <div class="detail-item">
                            <label>Job Number:</label>
                            <span>${booking.job_number || 'Not specified'}</span>
                        </div>
                        <div class="detail-item">
                            <label>Notes:</label>
                            <span>${booking.notes || 'No notes'}</span>
                        </div>
                        <div class="detail-item">
                            <label>Status:</label>
                            <span class="status-badge ${booking.completion ? 'completed' : 'incomplete'}">${booking.completion ? 'Completed' : 'Incomplete'}</span>
                        </div>
                        <div class="detail-item">
                            <label>Created:</label>
                            <span>${new Date(booking.created).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' })}</span>
                        </div>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button type="button" class="close-btn" onclick="closeViewBookingModal()">Close</button>
                    ${!booking.completion ? `<button type="button" class="complete-btn" onclick="markBookingComplete(${booking.booking_id})">Mark Complete</button>` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

function closeViewBookingModal() {
    const modal = document.querySelector('.view-booking-modal-overlay');
    if (modal) {
        modal.remove();
    }
}

function markBookingComplete(bookingId) {
    // Update booking completion status
    fetch(`${API_BASE_URL}/bookings/${bookingId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            completion: true,
            dropoff_complete: true
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Booking marked complete:', data);
        alert('Booking marked as complete!');
        
        // Close modal and refresh bookings
        closeViewBookingModal();
        refreshBookings();
    })
    .catch(error => {
        console.error('Error marking booking complete:', error);
        alert('Error marking booking complete: ' + error.message);
    });
}

// Refresh bookings when switching pages
function refreshBookings() {
    loadBookings().then(() => {
        const currentPage = document.querySelector('.menu-item.active').getAttribute('data-page');
        loadPage(currentPage);
    });
}

