// New Booking Page JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Global variables for Google Maps
let pickupAutocomplete = null;
let dropoffAutocomplete = null;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the page
    initializePage();
});

function initializePage() {
    // Initialize Google Places Autocomplete after a short delay
    setTimeout(() => {
        initializeAutocomplete();
    }, 100);
}

function goBack() {
    // Navigate back to the mobile app
    window.location.href = '/outcry-express-mobile';
}

// Handle date selection changes
function handleDateChange() {
    const dateSelect = document.getElementById('bookingDate');
    const customDateInput = document.getElementById('customDate');
    const pickupTimeGroup = document.getElementById('pickupTimeGroup');
    const dropoffTimeGroup = document.getElementById('dropoffTimeGroup');
    
    // Show/hide custom date input
    if (dateSelect.value === 'custom') {
        customDateInput.style.display = 'block';
        customDateInput.required = true;
    } else {
        customDateInput.style.display = 'none';
        customDateInput.required = false;
    }
    
    // Show/hide time fields based on date selection
    if (dateSelect.value && dateSelect.value !== 'anytime') {
        pickupTimeGroup.style.display = 'block';
        dropoffTimeGroup.style.display = 'block';
    } else {
        pickupTimeGroup.style.display = 'none';
        dropoffTimeGroup.style.display = 'none';
    }
}

function submitBooking(event) {
    event.preventDefault();
    
    // Show loading state
    const form = event.target;
    const submitBtn = form.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    
    form.classList.add('loading');
    submitBtn.textContent = 'Creating...';
    submitBtn.disabled = true;
    
    // Get form data
    const formData = new FormData(form);
    const bookingDate = formData.get('bookingDate');
    const customDate = formData.get('customDate');
    
    // Determine the actual date
    let actualDate;
    if (bookingDate === 'today') {
        actualDate = new Date().toISOString().split('T')[0];
    } else if (bookingDate === 'tomorrow') {
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        actualDate = tomorrow.toISOString().split('T')[0];
    } else if (bookingDate === 'custom') {
        actualDate = customDate;
    } else if (bookingDate === 'anytime') {
        actualDate = null;
    }
    
    const bookingData = {
        pickup_date: actualDate,
        pickup_time: formData.get('pickupTime') || null,
        pickupAddress: formData.get('pickupAddress'),
        dropoff_date: actualDate,
        dropoff_time: formData.get('dropoffTime') || null,
        dropoffAddress: formData.get('dropoffAddress'),
        job_number: formData.get('jobNumber') || null,
        notes: formData.get('notes') || null
    };
    
    // Send data to backend
    createBookingInDatabase(bookingData)
        .then(() => {
            // Show success message
            showMessage('Booking created successfully!', 'success');
            
            // Redirect back to mobile app after a short delay
            setTimeout(() => {
                window.location.href = '/outcry-express-mobile';
            }, 1500);
        })
        .catch((error) => {
            // Show error message
            showMessage('Error creating booking: ' + error.message, 'error');
            
            // Reset form state
            form.classList.remove('loading');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        });
}

// Create booking in database
async function createBookingInDatabase(bookingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/bookings`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookingData)
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log('Booking created:', result);
            return result;
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Error creating booking:', error);
        throw error;
    }
}

function showMessage(text, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    
    // Insert message at the top of the form
    const form = document.getElementById('bookingForm');
    form.insertBefore(message, form.firstChild);
    
    // Auto-remove success messages after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            message.remove();
        }, 3000);
    }
}

// Google Maps initialization
function initGoogleMaps() {
    console.log('Google Maps API loaded');
    initializeAutocomplete();
}

// Initialize Google Places Autocomplete
function initializeAutocomplete() {
    // Check if Google Maps API is available
    if (!window.google || !window.google.maps || !window.google.maps.places) {
        console.log('Google Maps API not available - using standard input fields');
        return;
    }
    
    // Initialize pickup address autocomplete
    const pickupInput = document.getElementById('pickupAddress');
    if (pickupInput) {
        pickupAutocomplete = new google.maps.places.Autocomplete(pickupInput, {
            types: ['address'],
            componentRestrictions: { country: 'au' } // Restrict to Australia
        });
        
        pickupAutocomplete.addListener('place_changed', function() {
            const place = pickupAutocomplete.getPlace();
            if (place.formatted_address) {
                pickupInput.value = place.formatted_address;
                console.log('Pickup address selected:', place.formatted_address);
            }
        });
    }
    
    // Initialize dropoff address autocomplete
    const dropoffInput = document.getElementById('dropoffAddress');
    if (dropoffInput) {
        dropoffAutocomplete = new google.maps.places.Autocomplete(dropoffInput, {
            types: ['address'],
            componentRestrictions: { country: 'au' } // Restrict to Australia
        });
        
        dropoffAutocomplete.addListener('place_changed', function() {
            const place = dropoffAutocomplete.getPlace();
            if (place.formatted_address) {
                dropoffInput.value = place.formatted_address;
                console.log('Dropoff address selected:', place.formatted_address);
            }
        });
    }
}

// Handle form validation
function validateForm() {
    const bookingDate = document.getElementById('bookingDate').value;
    const customDate = document.getElementById('customDate').value;
    const pickupAddress = document.getElementById('pickupAddress').value;
    const dropoffAddress = document.getElementById('dropoffAddress').value;
    
    if (!bookingDate || !pickupAddress || !dropoffAddress) {
        showMessage('Please fill in all required fields', 'error');
        return false;
    }
    
    // If custom date is selected, validate it
    if (bookingDate === 'custom') {
        if (!customDate) {
            showMessage('Please select a custom date', 'error');
            return false;
        }
        
        // Check if custom date is not in the past
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const customDateObj = new Date(customDate);
        
        if (customDateObj < today) {
            showMessage('Custom date cannot be in the past', 'error');
            return false;
        }
    }
    
    return true;
}

// Add form validation on submit
document.getElementById('bookingForm').addEventListener('submit', function(event) {
    if (!validateForm()) {
        event.preventDefault();
        return false;
    }
});
