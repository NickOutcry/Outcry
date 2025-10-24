// Client Management JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Global variables
let clients = [];
let selectedClient = null;
let isEditing = false;
let originalData = null;

// DOM elements
const clientList = document.getElementById('clientList');
const clientDetailsSection = document.getElementById('clientDetailsSection');
const addClientModal = document.getElementById('addClientModal');
const addClientForm = document.getElementById('addClientForm');

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadClients();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Add client form submission
    addClientForm.addEventListener('submit', handleAddClient);
    
    // Close modal when clicking outside
    addClientModal.addEventListener('click', function(e) {
        if (e.target === addClientModal) {
            closeAddClientModal();
        }
    });
    
    // Project form submission
    const projectForm = document.getElementById('projectForm');
    if (projectForm) {
        projectForm.addEventListener('submit', handleProjectSubmit);
    }
    
    // Close project modal when clicking outside
    const projectModal = document.getElementById('projectModal');
    if (projectModal) {
        projectModal.addEventListener('click', function(e) {
            if (e.target === projectModal) {
                hideProjectModal();
            }
        });
    }
}

// Load clients from API
async function loadClients() {
    try {
        const response = await fetch(`${API_BASE_URL}/clients`);
        if (response.ok) {
            clients = await response.json();
            renderClientList();
        } else {
            console.error('Failed to load clients');
            showNotification('Error loading clients', 'error');
        }
    } catch (error) {
        console.error('Error loading clients:', error);
        showNotification('Error loading clients', 'error');
    }
}

// Render client list
function renderClientList() {
    clientList.innerHTML = '';
    
    clients.forEach(client => {
        const clientItem = document.createElement('div');
        clientItem.className = 'client-item';
        clientItem.dataset.clientId = client.client_id;
        
        clientItem.innerHTML = `
            <div class="client-name">${client.name}</div>
        `;
        
        clientItem.addEventListener('click', () => selectClient(client.client_id));
        clientList.appendChild(clientItem);
    });
}

// Select a client
function selectClient(clientId) {
    // Remove active class from all items
    document.querySelectorAll('.client-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Add active class to selected item
    const selectedItem = document.querySelector(`[data-client-id="${clientId}"]`);
    if (selectedItem) {
        selectedItem.classList.add('active');
    }
    
    // Get client data
    selectedClient = clients.find(client => client.client_id === clientId);
    if (selectedClient) {
        showClientDetails(selectedClient);
    }
}

// Load projects for a client
async function loadClientProjects(clientId) {
    try {
        const response = await fetch(`${API_BASE_URL}/clients/${clientId}/projects`);
        if (response.ok) {
            const projects = await response.json();
            return projects;
        } else {
            console.error('Failed to load client projects');
            return [];
        }
    } catch (error) {
        console.error('Error loading client projects:', error);
        return [];
    }
}

// Show client details
async function showClientDetails(client) {
    // Load projects for this client
    const projects = await loadClientProjects(client.client_id);
    client.projects = projects;
    const detailsHTML = `
        <div class="client-details active">
            <div class="details-header">
                <h3 class="details-title">${client.name}</h3>
                <button class="edit-toggle" onclick="toggleEdit()">
                    ${isEditing ? 'Cancel' : 'Edit'}
                </button>
            </div>
            
            <form id="clientDetailsForm">
                <div class="form-group">
                    <label for="editName">Client Name</label>
                    <input type="text" id="editName" name="name" value="${client.name}" ${!isEditing ? 'readonly' : ''}>
                </div>
                
                <div class="form-group">
                    <label for="editAddress">Address</label>
                    <input type="text" id="editAddress" name="address" value="${client.address || ''}" ${!isEditing ? 'readonly' : ''}>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="editSuburb">Suburb</label>
                        <input type="text" id="editSuburb" name="suburb" value="${client.suburb || ''}" ${!isEditing ? 'readonly' : ''}>
                    </div>
                    <div class="form-group">
                        <label for="editState">State</label>
                        <select id="editState" name="state" ${!isEditing ? 'disabled' : ''}>
                            <option value="">Select State</option>
                            <option value="NSW" ${client.state === 'NSW' ? 'selected' : ''}>NSW</option>
                            <option value="VIC" ${client.state === 'VIC' ? 'selected' : ''}>VIC</option>
                            <option value="QLD" ${client.state === 'QLD' ? 'selected' : ''}>QLD</option>
                            <option value="WA" ${client.state === 'WA' ? 'selected' : ''}>WA</option>
                            <option value="SA" ${client.state === 'SA' ? 'selected' : ''}>SA</option>
                            <option value="TAS" ${client.state === 'TAS' ? 'selected' : ''}>TAS</option>
                            <option value="ACT" ${client.state === 'ACT' ? 'selected' : ''}>ACT</option>
                            <option value="NT" ${client.state === 'NT' ? 'selected' : ''}>NT</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="editPostcode">Postcode</label>
                    <input type="number" id="editPostcode" name="postcode" value="${client.postcode || ''}" min="1000" max="9999" ${!isEditing ? 'readonly' : ''}>
                </div>
            </form>
            
            <!-- Contacts Section -->
            <div class="section-divider">
                <h4>Contacts</h4>
                <button class="btn btn-sm btn-primary" onclick="addContact()">+ Add Contact</button>
            </div>
            
            <div class="contacts-list">
                ${client.contacts && client.contacts.length > 0 ? 
                    client.contacts.map(contact => `
                        <div class="contact-item">
                            <div class="contact-info clickable" onclick="editContact(${contact.contact_id})">
                                <div class="contact-name">${contact.first_name} ${contact.surname}</div>
                                <div class="contact-details">
                                    <span>${contact.email || ''}</span>
                                    <span>${contact.phone || ''}</span>
                                </div>
                            </div>
                            <div class="contact-actions">
                                <button class="delete-btn" onclick="deleteContact(${contact.contact_id}); event.stopPropagation()" title="Delete Contact">×</button>
                            </div>
                        </div>
                    `).join('') : 
                    '<p class="no-data">No contacts added yet.</p>'
                }
            </div>
            
            <!-- Billing Section -->
            <div class="section-divider">
                <h4>Billing</h4>
                <button class="btn btn-sm btn-primary" onclick="addBilling()">+ Add Billing</button>
            </div>
            
            <div class="billing-list">
                ${client.billing && client.billing.length > 0 ? 
                    client.billing.map(bill => `
                        <div class="billing-item">
                            <div class="billing-info clickable" onclick="editBilling(${bill.billing_id})">
                                <div class="billing-entity">${bill.entity}</div>
                                <div class="billing-address">
                                    ${bill.address || ''}, ${bill.suburb || ''} ${bill.state || ''} ${bill.postcode || ''}
                                </div>
                            </div>
                            <div class="billing-actions">
                                <button class="delete-btn" onclick="deleteBilling(${bill.billing_id}); event.stopPropagation()" title="Delete Billing">×</button>
                            </div>
                        </div>
                    `).join('') : 
                    '<p class="no-data">No billing information added yet.</p>'
                }
            </div>
            
            <!-- Projects Section -->
            <div class="section-divider">
                <h4>Projects</h4>
                <button class="btn btn-sm btn-primary" onclick="addProject()">+ Add Project</button>
            </div>
            
            <div class="projects-list">
                ${client.projects && client.projects.length > 0 ? 
                    client.projects.map(project => `
                        <div class="project-item">
                            <div class="project-info clickable" onclick="editProject(${project.project_id})">
                                <div class="project-name">${project.name}</div>
                                <div class="project-address">
                                    ${project.address || ''}, ${project.suburb || ''} ${project.state || ''} ${project.postcode || ''}
                                </div>
                            </div>
                            <div class="project-actions">
                                <button class="delete-btn" onclick="deleteProject(${project.project_id}); event.stopPropagation()" title="Delete Project">×</button>
                            </div>
                        </div>
                    `).join('') : 
                    '<p class="no-data">No projects added yet.</p>'
                }
            </div>
            
            ${isEditing ? `
                <div class="details-actions">
                    <button type="button" class="btn btn-secondary" onclick="discardChanges()">Discard</button>
                    <button type="button" class="btn btn-success" onclick="saveChanges()">Save Changes</button>
                </div>
            ` : `
                <div class="details-actions">
                    <button type="button" class="btn btn-danger" onclick="deleteClient()">Delete Client</button>
                </div>
            `}
        </div>
    `;
    
    clientDetailsSection.innerHTML = detailsHTML;
    
    // Store original data for comparison
    if (!originalData) {
        originalData = { ...client };
    }
}

// Toggle edit mode
function toggleEdit() {
    isEditing = !isEditing;
    
    if (isEditing) {
        // Store original data when entering edit mode
        originalData = { ...selectedClient };
    } else {
        // Cancel editing - restore original data
        discardChanges();
    }
    
    // Re-render details with new edit state
    showClientDetails(selectedClient);
}

// Save changes
async function saveChanges() {
    const form = document.getElementById('clientDetailsForm');
    const formData = new FormData(form);
    
    const clientData = {
        name: formData.get('name'),
        address: formData.get('address'),
        suburb: formData.get('suburb'),
        state: formData.get('state'),
        postcode: parseInt(formData.get('postcode')) || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/clients/${selectedClient.client_id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(clientData)
        });
        
        if (response.ok) {
            // Reload clients to get updated data
            await loadClients();
            
            // Re-select the updated client
            selectClient(selectedClient.client_id);
            
            // Exit edit mode
            isEditing = false;
            originalData = null;
            
            showNotification('Client updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update client', 'error');
        }
    } catch (error) {
        console.error('Error updating client:', error);
        showNotification('Error updating client', 'error');
    }
}

// Discard changes
function discardChanges() {
    isEditing = false;
    selectedClient = { ...originalData };
    originalData = null;
    showClientDetails(selectedClient);
}

// Delete client
async function deleteClient() {
    if (!selectedClient) return;
    
    // Show confirmation dialog
    if (confirm(`Are you sure you want to delete "${selectedClient.name}"? This action cannot be undone.`)) {
        try {
            const response = await fetch(`${API_BASE_URL}/clients/${selectedClient.client_id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Reload clients
                await loadClients();
                
                // Clear selection
                selectedClient = null;
                isEditing = false;
                originalData = null;
                
                // Show placeholder in details section
                clientDetailsSection.innerHTML = `
                    <div class="details-placeholder">
                        <p>Select a client to view details</p>
                    </div>
                `;
                
                showNotification('Client deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete client', 'error');
            }
        } catch (error) {
            console.error('Error deleting client:', error);
            showNotification('Error deleting client', 'error');
        }
    }
}

// Modal functions
function showAddClientModal() {
    addClientModal.classList.add('active');
    addClientForm.reset();
}

function closeAddClientModal() {
    addClientModal.classList.remove('active');
}

// Handle add client form submission
async function handleAddClient(e) {
    e.preventDefault();
    
    const formData = new FormData(addClientForm);
    
    const clientData = {
        name: formData.get('name'),
        address: formData.get('address'),
        suburb: formData.get('suburb'),
        state: formData.get('state'),
        postcode: parseInt(formData.get('postcode')) || null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/clients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(clientData)
        });
        
        if (response.ok) {
            const newClient = await response.json();
            
            // Reload clients
            await loadClients();
            
            // Close modal
            closeAddClientModal();
            
            showNotification('Client added successfully!', 'success');
            
            // Select the new client
            selectClient(newClient.client_id);
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to add client', 'error');
        }
    } catch (error) {
        console.error('Error adding client:', error);
        showNotification('Error adding client', 'error');
    }
}

// Contact and Billing Functions
function addContact() {
    // Reset form and set up for adding
    document.getElementById('contactForm').reset();
    document.getElementById('contactId').value = '';
    document.getElementById('contactModalTitle').textContent = 'Add New Contact';
    document.getElementById('contactSubmitBtn').textContent = 'Add Contact';
    
    // Hide delete button for new contacts
    document.getElementById('deleteContactBtn').style.display = 'none';
    
    // Show modal
    document.getElementById('contactModal').style.display = 'block';
}

function editContact(contactId) {
    // Find the contact
    const contact = selectedClient.contacts.find(c => c.contact_id === contactId);
    if (!contact) return;
    
    // Populate form with contact data
    document.getElementById('contactId').value = contact.contact_id;
    document.getElementById('contactFirstName').value = contact.first_name;
    document.getElementById('contactSurname').value = contact.surname;
    document.getElementById('contactEmail').value = contact.email || '';
    document.getElementById('contactPhone').value = contact.phone || '';
    
    // Update modal title and button
    document.getElementById('contactModalTitle').textContent = 'Edit Contact';
    document.getElementById('contactSubmitBtn').textContent = 'Update Contact';
    
    // Show delete button for existing contacts
    document.getElementById('deleteContactBtn').style.display = 'block';
    document.getElementById('deleteContactBtn').setAttribute('data-contact-id', contactId);
    
    // Show modal
    document.getElementById('contactModal').style.display = 'block';
}

function hideContactModal() {
    document.getElementById('contactModal').style.display = 'none';
}

async function deleteContact(contactId) {
    if (confirm('Are you sure you want to delete this contact?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/contacts/${contactId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Reload clients to get updated data
                await loadClients();
                
                // Re-select the current client
                if (selectedClient) {
                    selectClient(selectedClient.client_id);
                }
                
                showNotification('Contact deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete contact', 'error');
            }
        } catch (error) {
            console.error('Error deleting contact:', error);
            showNotification('Error deleting contact', 'error');
        }
    }
}

function addBilling() {
    // Reset form and set up for adding
    document.getElementById('billingForm').reset();
    document.getElementById('billingId').value = '';
    document.getElementById('billingModalTitle').textContent = 'Add New Billing';
    document.getElementById('billingSubmitBtn').textContent = 'Add Billing';
    
    // Hide delete button for new billing
    document.getElementById('deleteBillingBtn').style.display = 'none';
    
    // Show modal
    document.getElementById('billingModal').style.display = 'block';
}

function editBilling(billingId) {
    // Find the billing
    const billing = selectedClient.billing.find(b => b.billing_id === billingId);
    if (!billing) return;
    
    // Populate form with billing data
    document.getElementById('billingId').value = billing.billing_id;
    document.getElementById('billingEntity').value = billing.entity;
    document.getElementById('billingAddress').value = billing.address || '';
    document.getElementById('billingSuburb').value = billing.suburb || '';
    document.getElementById('billingState').value = billing.state || '';
    document.getElementById('billingPostcode').value = billing.postcode || '';
    
    // Update modal title and button
    document.getElementById('billingModalTitle').textContent = 'Edit Billing';
    document.getElementById('billingSubmitBtn').textContent = 'Update Billing';
    
    // Show delete button for existing billing
    document.getElementById('deleteBillingBtn').style.display = 'block';
    document.getElementById('deleteBillingBtn').setAttribute('data-billing-id', billingId);
    
    // Show modal
    document.getElementById('billingModal').style.display = 'block';
}

function hideBillingModal() {
    document.getElementById('billingModal').style.display = 'none';
}

async function deleteBilling(billingId) {
    if (confirm('Are you sure you want to delete this billing information?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/billing/${billingId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Reload clients to get updated data
                await loadClients();
                
                // Re-select the current client
                if (selectedClient) {
                    selectClient(selectedClient.client_id);
                }
                
                showNotification('Billing information deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete billing', 'error');
            }
        } catch (error) {
            console.error('Error deleting billing:', error);
            showNotification('Error deleting billing', 'error');
        }
    }
}

// Form submission handlers
document.addEventListener('DOMContentLoaded', function() {
    // Contact form submission
    document.getElementById('contactForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const contactId = formData.get('contactId');
        const contactData = {
            first_name: formData.get('first_name'),
            surname: formData.get('surname'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            client_id: selectedClient.client_id
        };
        
        try {
            if (contactId) {
                // Update existing contact
                await updateContact(parseInt(contactId), contactData);
            } else {
                // Add new contact
                await addNewContact(contactData);
            }
            
            hideContactModal();
        } catch (error) {
            console.error('Error handling contact:', error);
            showNotification('Error handling contact', 'error');
        }
    });
    
    // Billing form submission
    document.getElementById('billingForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const billingId = formData.get('billingId');
        const billingData = {
            entity: formData.get('entity'),
            address: formData.get('address'),
            suburb: formData.get('suburb'),
            state: formData.get('state'),
            postcode: parseInt(formData.get('postcode')) || null,
            client_id: selectedClient.client_id
        };
        
        try {
            if (billingId) {
                // Update existing billing
                await updateBilling(parseInt(billingId), billingData);
            } else {
                // Add new billing
                await addNewBilling(billingData);
            }
            
            hideBillingModal();
        } catch (error) {
            console.error('Error handling billing:', error);
            showNotification('Error handling billing', 'error');
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
});

async function addNewContact(contactData) {
    try {
        const response = await fetch(`${API_BASE_URL}/contacts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(contactData)
        });
        
        if (response.ok) {
            // Reload clients to get updated data
            await loadClients();
            
            // Re-select the current client
            if (selectedClient) {
                selectClient(selectedClient.client_id);
            }
            
            showNotification('Contact added successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to add contact', 'error');
        }
    } catch (error) {
        console.error('Error adding contact:', error);
        showNotification('Error adding contact', 'error');
    }
}

async function updateContact(contactId, contactData) {
    try {
        const response = await fetch(`${API_BASE_URL}/contacts/${contactId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(contactData)
        });
        
        if (response.ok) {
            // Reload clients to get updated data
            await loadClients();
            
            // Re-select the current client
            if (selectedClient) {
                selectClient(selectedClient.client_id);
            }
            
            showNotification('Contact updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update contact', 'error');
        }
    } catch (error) {
        console.error('Error updating contact:', error);
        showNotification('Error updating contact', 'error');
    }
}

async function addNewBilling(billingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/billing`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(billingData)
        });
        
        if (response.ok) {
            // Reload clients to get updated data
            await loadClients();
            
            // Re-select the current client
            if (selectedClient) {
                selectClient(selectedClient.client_id);
            }
            
            showNotification('Billing information added successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to add billing', 'error');
        }
    } catch (error) {
        console.error('Error adding billing:', error);
        showNotification('Error adding billing', 'error');
    }
}

async function updateBilling(billingId, billingData) {
    try {
        const response = await fetch(`${API_BASE_URL}/billing/${billingId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(billingData)
        });
        
        if (response.ok) {
            // Reload clients to get updated data
            await loadClients();
            
            // Re-select the current client
            if (selectedClient) {
                selectClient(selectedClient.client_id);
            }
            
            showNotification('Billing information updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update billing', 'error');
        }
    } catch (error) {
        console.error('Error updating billing:', error);
        showNotification('Error updating billing', 'error');
    }
}

// Notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
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
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Project functions
function addProject() {
    if (!selectedClient) return;
    
    // Reset form
    document.getElementById('projectForm').reset();
    document.getElementById('projectId').value = '';
    document.getElementById('projectModalTitle').textContent = 'Add New Project';
    document.getElementById('projectSubmitBtn').textContent = 'Add Project';
    
    // Show modal
    document.getElementById('projectModal').classList.add('active');
}

function editProject(projectId) {
    if (!selectedClient || !selectedClient.projects) return;
    
    const project = selectedClient.projects.find(p => p.project_id === projectId);
    if (!project) return;
    
    // Populate form
    document.getElementById('projectId').value = project.project_id;
    document.getElementById('projectName').value = project.name;
    document.getElementById('projectAddress').value = project.address || '';
    document.getElementById('projectSuburb').value = project.suburb || '';
    document.getElementById('projectState').value = project.state || '';
    document.getElementById('projectPostcode').value = project.postcode || '';
    
    // Update modal title and button
    document.getElementById('projectModalTitle').textContent = 'Edit Project';
    document.getElementById('projectSubmitBtn').textContent = 'Update Project';
    
    // Show modal
    document.getElementById('projectModal').classList.add('active');
}

function hideProjectModal() {
    document.getElementById('projectModal').classList.remove('active');
}

async function handleProjectSubmit(e) {
    e.preventDefault();
    
    if (!selectedClient) return;
    
    const form = document.getElementById('projectForm');
    const formData = new FormData(form);
    const projectId = formData.get('projectId');
    
    const projectData = {
        name: formData.get('name'),
        address: formData.get('address'),
        suburb: formData.get('suburb'),
        state: formData.get('state'),
        postcode: parseInt(formData.get('postcode')) || null
    };
    
    try {
        let response;
        if (projectId) {
            // Update existing project
            response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(projectData)
            });
        } else {
            // Create new project
            response = await fetch(`${API_BASE_URL}/projects`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(projectData)
            });
        }
        
        if (response.ok) {
            // Hide modal
            hideProjectModal();
            
            // Reload client details to show updated projects
            if (selectedClient) {
                await showClientDetails(selectedClient);
            }
            
            showNotification(projectId ? 'Project updated successfully!' : 'Project added successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to save project', 'error');
        }
    } catch (error) {
        console.error('Error saving project:', error);
        showNotification('Error saving project', 'error');
    }
}

async function deleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            // Reload client details to show updated projects
            if (selectedClient) {
                await showClientDetails(selectedClient);
            }
            
            showNotification('Project deleted successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to delete project', 'error');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        showNotification('Error deleting project', 'error');
    }
}

// Delete functions for modals
function deleteContactFromModal() {
    const contactId = document.getElementById('deleteContactBtn').getAttribute('data-contact-id');
    if (contactId && confirm('Are you sure you want to delete this contact? This action cannot be undone.')) {
        deleteContact(contactId);
        hideContactModal();
    }
}

function deleteBillingFromModal() {
    const billingId = document.getElementById('deleteBillingBtn').getAttribute('data-billing-id');
    if (billingId && confirm('Are you sure you want to delete this billing information? This action cannot be undone.')) {
        deleteBilling(billingId);
        hideBillingModal();
    }
}
