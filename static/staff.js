// API configuration
const API_BASE_URL = 'http://localhost:5001/api';

// Global variables
let staff = [];
let selectedStaff = null;
let isEditing = false;

// DOM elements
const staffGrid = document.getElementById('staffGrid');

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadStaff();
    setupEventListeners();
});

// Load staff from API
async function loadStaff() {
    try {
        const response = await fetch(`${API_BASE_URL}/staff`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        staff = await response.json();
        renderStaffGrid();
    } catch (error) {
        console.error('Error loading staff:', error);
        showNotification('Error loading staff data', 'error');
    }
}

// Render staff grid
function renderStaffGrid() {
    if (staff.length === 0) {
        staffGrid.innerHTML = `
            <div class="empty-state">
                <h3>No Staff Members</h3>
                <p>Get started by adding your first staff member.</p>
                <button class="btn btn-primary" onclick="showAddStaffModal()">
                    <span class="btn-icon">+</span>
                    Add First Staff Member
                </button>
            </div>
        `;
        return;
    }
    
    const staffHTML = staff.map(staffMember => {
        const fullAddress = [
            staffMember.address,
            staffMember.suburb,
            staffMember.state,
            staffMember.postcode
        ].filter(Boolean).join(', ');
        
        return `
            <div class="staff-card" data-staff-id="${staffMember.staff_id}">
                <div class="staff-card-header">
                    <h3 class="staff-name clickable" onclick="editStaff(${staffMember.staff_id})">${staffMember.first_name} ${staffMember.surname}</h3>
                    <div class="staff-actions">
                        <button class="delete-btn" onclick="deleteStaff(${staffMember.staff_id}); event.stopPropagation()" title="Delete Staff">×</button>
                    </div>
                </div>
                
                <div class="staff-info">
                    ${staffMember.phone ? `
                        <div class="staff-info-item">
                            <span class="staff-info-icon">📞</span>
                            <span class="staff-info-label">Phone:</span>
                            <span class="staff-info-value">${staffMember.phone}</span>
                        </div>
                    ` : ''}
                    
                    ${staffMember.dob ? `
                        <div class="staff-info-item">
                            <span class="staff-info-icon">🎂</span>
                            <span class="staff-info-label">DOB:</span>
                            <span class="staff-info-value">${formatDate(staffMember.dob)}</span>
                        </div>
                    ` : ''}
                    
                    ${staffMember.emergency_contact ? `
                        <div class="staff-info-item">
                            <span class="staff-info-icon">🚨</span>
                            <span class="staff-info-label">Emergency:</span>
                            <span class="staff-info-value">${staffMember.emergency_contact}</span>
                        </div>
                    ` : ''}
                </div>
                
                ${fullAddress ? `
                    <div class="staff-address">
                        <strong>Address:</strong><br>
                        ${fullAddress}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    staffGrid.innerHTML = staffHTML;
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-AU', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    });
}

// Show staff details modal
function showStaffDetails(staffId) {
    const staffMember = staff.find(s => s.staff_id === staffId);
    if (!staffMember) return;
    
    const fullAddress = [
        staffMember.address,
        staffMember.suburb,
        staffMember.state,
        staffMember.postcode
    ].filter(Boolean).join(', ');
    
    const detailsHTML = `
        <div class="staff-details-section">
            <h3>Personal Information</h3>
            <div class="staff-details-grid">
                <div class="staff-detail-item">
                    <div class="staff-detail-label">Full Name</div>
                    <div class="staff-detail-value">${staffMember.first_name} ${staffMember.surname}</div>
                </div>
                <div class="staff-detail-item">
                    <div class="staff-detail-label">Phone</div>
                    <div class="staff-detail-value ${!staffMember.phone ? 'empty' : ''}">${staffMember.phone || 'Not provided'}</div>
                </div>
                <div class="staff-detail-item">
                    <div class="staff-detail-label">Date of Birth</div>
                    <div class="staff-detail-value ${!staffMember.dob ? 'empty' : ''}">${staffMember.dob ? formatDate(staffMember.dob) : 'Not provided'}</div>
                </div>
                <div class="staff-detail-item">
                    <div class="staff-detail-label">Emergency Contact</div>
                    <div class="staff-detail-value ${!staffMember.emergency_contact ? 'empty' : ''}">${staffMember.emergency_contact || 'Not provided'}</div>
                </div>
                <div class="staff-detail-item">
                    <div class="staff-detail-label">Emergency Phone</div>
                    <div class="staff-detail-value ${!staffMember.emergency_contact_number ? 'empty' : ''}">${staffMember.emergency_contact_number || 'Not provided'}</div>
                </div>
                <div class="staff-detail-item">
                    <div class="staff-detail-label">Address</div>
                    <div class="staff-detail-value ${!fullAddress ? 'empty' : ''}">${fullAddress || 'Not provided'}</div>
                </div>
            </div>
        </div>
        
        <div class="staff-details-section">
            <h3>Assigned Jobs (${staffMember.assigned_jobs.length})</h3>
            ${staffMember.assigned_jobs.length > 0 ? `
                <div class="jobs-list">
                    ${staffMember.assigned_jobs.map(job => `
                        <div class="job-item">
                            <div class="job-info">
                                <div class="job-reference">${job.reference}</div>
                                <div class="job-details">
                                    ${job.client_name} - ${job.project_name}
                                </div>
                            </div>
                            <span class="job-status ${getStatusClass(job.status)}">
                                ${job.status}
                            </span>
                        </div>
                    `).join('')}
                </div>
            ` : `
                <p class="empty-state">No jobs assigned to this staff member.</p>
            `}
        </div>
    `;
    
    document.getElementById('staffDetailsContent').innerHTML = detailsHTML;
    document.getElementById('staffDetailsModal').style.display = 'block';
}

// Hide staff details modal
function hideStaffDetailsModal() {
    document.getElementById('staffDetailsModal').style.display = 'none';
}

// Get status CSS class
function getStatusClass(status) {
    const statusMap = {
        'Pending': 'pending',
        'In Progress': 'in-progress',
        'Completed': 'completed',
        'Cancelled': 'cancelled',
        'On Hold': 'on-hold'
    };
    return statusMap[status] || 'pending';
}

// Show add staff modal
function showAddStaffModal() {
    selectedStaff = null;
    isEditing = false;
    
    // Reset form
    document.getElementById('staffForm').reset();
    document.getElementById('staffId').value = '';
    document.getElementById('staffModalTitle').textContent = 'Add New Staff';
    document.getElementById('staffSubmitBtn').textContent = 'Add Staff';
    
    // Show modal
    document.getElementById('staffModal').style.display = 'block';
}

// Edit staff
function editStaff(staffId) {
    const staffMember = staff.find(s => s.staff_id === staffId);
    if (!staffMember) return;
    
    selectedStaff = staffMember;
    isEditing = true;
    
    // Populate form
    document.getElementById('staffId').value = staffMember.staff_id;
    document.getElementById('staffFirstName').value = staffMember.first_name;
    document.getElementById('staffSurname').value = staffMember.surname;
    document.getElementById('staffPhone').value = staffMember.phone || '';
    document.getElementById('staffAddress').value = staffMember.address || '';
    document.getElementById('staffSuburb').value = staffMember.suburb || '';
    document.getElementById('staffState').value = staffMember.state || '';
    document.getElementById('staffPostcode').value = staffMember.postcode || '';
    document.getElementById('staffDOB').value = staffMember.dob || '';
    document.getElementById('staffEmergencyContact').value = staffMember.emergency_contact || '';
    document.getElementById('staffEmergencyPhone').value = staffMember.emergency_contact_number || '';
    
    // Update modal title and button
    document.getElementById('staffModalTitle').textContent = 'Edit Staff';
    document.getElementById('staffSubmitBtn').textContent = 'Update Staff';
    
    // Show modal
    document.getElementById('staffModal').style.display = 'block';
}

// Hide staff modal
function hideStaffModal() {
    document.getElementById('staffModal').style.display = 'none';
}

// Delete staff
async function deleteStaff(staffId) {
    const staffMember = staff.find(s => s.staff_id === staffId);
    if (!staffMember) return;
    
    if (confirm(`Are you sure you want to delete ${staffMember.first_name} ${staffMember.surname}? This action cannot be undone.`)) {
        try {
            const response = await fetch(`${API_BASE_URL}/staff/${staffId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            await loadStaff(); // Reload staff data
            showNotification('Staff member deleted successfully!', 'success');
        } catch (error) {
            console.error('Error deleting staff:', error);
            showNotification(error.message, 'error');
        }
    }
}

// Setup event listeners
function setupEventListeners() {
    // Staff form submission
    document.getElementById('staffForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const staffId = formData.get('staff_id');
        
        const staffData = {
            first_name: formData.get('first_name'),
            surname: formData.get('surname'),
            phone: formData.get('phone') || null,
            address: formData.get('address') || null,
            suburb: formData.get('suburb') || null,
            state: formData.get('state') || null,
            postcode: parseInt(formData.get('postcode')) || null,
            dob: formData.get('dob') || null,
            emergency_contact: formData.get('emergency_contact') || null,
            emergency_contact_number: formData.get('emergency_contact_number') || null
        };
        
        try {
            if (staffId) {
                // Update existing staff
                await updateStaff(parseInt(staffId), staffData);
            } else {
                // Create new staff
                await createStaff(staffData);
            }
            
            hideStaffModal();
        } catch (error) {
            console.error('Error saving staff:', error);
            showNotification(error.message, 'error');
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
}

// Create new staff
async function createStaff(staffData) {
    try {
        const response = await fetch(`${API_BASE_URL}/staff`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(staffData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        await loadStaff(); // Reload staff data
        showNotification('Staff member added successfully!', 'success');
    } catch (error) {
        console.error('Error creating staff:', error);
        throw error;
    }
}

// Update existing staff
async function updateStaff(staffId, staffData) {
    try {
        const response = await fetch(`${API_BASE_URL}/staff/${staffId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(staffData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        await loadStaff(); // Reload staff data
        showNotification('Staff member updated successfully!', 'success');
    } catch (error) {
        console.error('Error updating staff:', error);
        throw error;
    }
}

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 1001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        ${type === 'success' ? 'background: #28a745;' : type === 'error' ? 'background: #dc3545;' : 'background: #17a2b8;'}
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

