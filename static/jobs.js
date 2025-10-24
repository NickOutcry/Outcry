// Jobs Management JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Global variables
let jobs = [];
let clients = [];
let projects = [];
let contacts = [];
let staff = [];
let jobStatuses = [];
let selectedJob = null;
let isEditing = false;

// DOM elements
const jobsTableBody = document.getElementById('jobsTableBody');

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadAllData().then(() => {
        populateDropdowns();
        
        // Check for URL parameters to auto-open job creation modal
        const urlParams = new URLSearchParams(window.location.search);
        const createJob = urlParams.get('createJob');
        const projectId = urlParams.get('projectId');
        const refresh = urlParams.get('refresh');
        
        if (createJob === 'true' && projectId) {
            // Auto-open job creation modal with project pre-selected
            setTimeout(() => {
                showAddJobModal();
                document.getElementById('jobProject').value = projectId;
            }, 500); // Small delay to ensure dropdowns are populated
        }
        
        // Clean up URL parameters after processing
        if (refresh || createJob || projectId) {
            // Remove URL parameters to clean up the URL
            const newUrl = window.location.pathname;
            window.history.replaceState({}, document.title, newUrl);
        }
    });
    setupEventListeners();
});

// Add page visibility change listener to refresh data when returning from quote page
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        // Page became visible, refresh data to show any new quotes
        loadAllData().then(() => {
            populateDropdowns();
        });
    }
});

// Load all data from API
async function loadAllData() {
    try {
        // Load all data in parallel
        const [jobsResponse, clientsResponse, projectsResponse, contactsResponse, staffResponse, statusesResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/jobs`),
            fetch(`${API_BASE_URL}/clients`),
            fetch(`${API_BASE_URL}/projects`),
            fetch(`${API_BASE_URL}/clients`), // We'll extract contacts from clients
            fetch(`${API_BASE_URL}/staff`),
            fetch(`${API_BASE_URL}/job-statuses`)
        ]);

        if (jobsResponse.ok) jobs = await jobsResponse.json();
        if (clientsResponse.ok) clients = await clientsResponse.json();
        if (projectsResponse.ok) projects = await projectsResponse.json();
        if (contactsResponse.ok) {
            // Extract contacts from clients
            contacts = [];
            const clientsData = await contactsResponse.json();
                    clientsData.forEach(client => {
            if (client.contacts) {
                contacts.push(...client.contacts);
            }
        });
        }
        if (staffResponse.ok) staff = await staffResponse.json();
        if (statusesResponse.ok) jobStatuses = await statusesResponse.json();

        renderJobsTable();
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification('Error loading data', 'error');
    }
}

// Render jobs table
function renderJobsTable() {
    const jobsHTML = jobs.map(job => {
        return `
            <tr class="job-row clickable" data-job-id="${job.job_id}" onclick="showJobDetails(${job.job_id})">
                <td class="job-number">#${job.job_id}</td>
                <td>${job.project_name || 'Unknown'}</td>
                <td>${job.reference}</td>
                <td>${job.client_name || 'Unknown'}</td>
                <td>
                    <span class="job-status ${getStatusClass(job.job_status || '')}">
                        ${job.job_status || 'Unknown'}
                    </span>
                </td>
                <td class="delete-cell">
                    <button class="delete-btn" onclick="deleteJob(${job.job_id}); event.stopPropagation()" title="Delete Job">×</button>
                </td>
            </tr>
        `;
    }).join('');
    
    jobsTableBody.innerHTML = jobsHTML;
}

// Get status CSS class
function getStatusClass(status) {
    const statusMap = {
        'Pending': 'pending',
        'In Progress': 'in-progress',
        'Completed': 'completed',
        'Cancelled': 'cancelled',
        'On Hold': 'on-hold',
        'Quote': 'quote',
        'Work Order': 'work-order',
        'Complete': 'complete',
        'Unsuccessful': 'unsuccessful'
    };
    return statusMap[status] || 'pending';
}

// Format date to dd-mm-yyyy
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'N/A';
    
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    
    return `${day}-${month}-${year}`;
}

// Show job details modal
function showJobDetails(jobId) {
    const job = jobs.find(j => j.job_id === jobId);
    if (!job) return;
    
    const detailsHTML = `
        <div class="job-details-tabs">
            <div class="tab-buttons">
                <button class="tab-button active" onclick="switchJobTab('project-info', ${job.job_id})">Job Information</button>
                <button class="tab-button" onclick="switchJobTab('quotes', ${job.job_id})">Quotes</button>
                <button class="tab-button" onclick="switchJobTab('billing', ${job.job_id})">Billing Details</button>
                <button class="tab-button" onclick="switchJobTab('status-history', ${job.job_id})">Job Status History</button>
            </div>
            
            <div class="tab-content">
                <div id="project-info-tab" class="tab-panel active">
                    <div class="job-details-header">
                        <button class="edit-toggle-btn" onclick="editJobFromDetails(${job.job_id})">+edit</button>
                    </div>
                    <div class="job-details-grid">
                        <div class="job-detail-item">
                            <div class="job-detail-label">Job Number</div>
                            <div class="job-detail-value">#${job.job_id}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Reference</div>
                            <div class="job-detail-value">${job.reference}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Client</div>
                            <div class="job-detail-value">${job.client_name || 'Unknown'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Project</div>
                            <div class="job-detail-value">${job.project_name || 'Unknown'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Contact</div>
                            <div class="job-detail-value">${job.contact_name || 'Unknown'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Project Manager</div>
                            <div class="job-detail-value">${job.staff_name || 'Unknown'}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Date Created</div>
                            <div class="job-detail-value">${formatDate(job.date_created)}</div>
                        </div>
                        <div class="job-detail-item">
                            <div class="job-detail-label">Current Status</div>
                            <div class="job-detail-value">
                                <div class="status-dropdown-container">
                                    <span class="job-status ${getStatusClass(job.job_status || '')}" id="currentStatusDisplay">
                                        ${job.job_status || 'Unknown'}
                                    </span>
                                    <button class="status-dropdown-btn" onclick="toggleStatusDropdown(${job.job_id})">
                                        <span class="dropdown-arrow">▼</span>
                                    </button>
                                    <div class="status-dropdown" id="statusDropdown_${job.job_id}" style="display: none;">
                                        ${jobStatuses && jobStatuses.length > 0 ? jobStatuses.map(status => `
                                            <div class="status-option ${status.job_status_id === job.job_status_id ? 'selected' : ''}" 
                                                 onclick="changeJobStatus(${job.job_id}, ${status.job_status_id}, '${status.job_status || 'Unknown'}')">
                                                <span class="job-status ${getStatusClass(status.job_status || 'Unknown')}">${status.job_status || 'Unknown'}</span>
                                            </div>
                                        `).join('') : '<div class="status-option">No statuses available</div>'}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="address-divider"></div>
                    
                    <div class="job-details-grid">
                        <div class="job-detail-item address-display">
                            <div class="job-detail-label">Job Address</div>
                            <div class="job-detail-value">
                                <div class="address-content">
                                    <div class="address-line1">${job.job_address || 'Not specified'}</div>
                                    <div class="address-line2">
                                        ${job.suburb || 'Not specified'}${job.suburb && job.state ? ', ' : ''}${job.state || ''}${job.postcode ? ' ' + job.postcode : ''}
                                    </div>
                                </div>
                                <button class="edit-address-btn" onclick="showEditAddressModal(${job.job_id})">+edit</button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="quotes-tab" class="tab-panel">
                    <div class="quotes-section">
                        <div class="quotes-header">
                            <button class="btn btn-primary" onclick="createQuote(${job.job_id})">
                                <span class="btn-icon">+</span>
                                New Quote
                            </button>
                        </div>
                        ${job.quotes && job.quotes.length > 0 ? `
                            <table class="quotes-table">
                                <thead>
                                    <tr>
                                        <th>Quote Number</th>
                                        <th>Date Created</th>
                                        <th>Cost (Excl. GST)</th>
                                        <th>Cost (Incl. GST)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${job.quotes.map(quote => `
                                        <tr class="quote-row clickable" onclick="editQuote(${quote.quote_id})">
                                            <td>${quote.quote_number || `#${quote.quote_id}`}</td>
                                            <td>${formatDate(quote.date_created) || 'N/A'}</td>
                                            <td>$${quote.cost_excl_gst ? quote.cost_excl_gst.toFixed(2) : '0.00'}</td>
                                            <td>$${quote.cost_incl_gst ? quote.cost_incl_gst.toFixed(2) : '0.00'}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        ` : 
                            '<p class="no-data">No quotes available for this job.</p>'
                        }
                    </div>
                </div>
                
                <div id="billing-tab" class="tab-panel">
                    <div class="job-details-section">
                        <h3>Billing Details</h3>
                        
                        <div class="billing-entity-selector">
                            <div class="billing-detail-item">
                                <div class="billing-detail-label">Billing Entity</div>
                                <select id="billingEntitySelect" class="billing-entity-dropdown" onchange="updateBillingDetails(${job.job_id})">
                                    <option value="">Select Billing Entity</option>
                                    ${job.billing_entities ? job.billing_entities.map(billing => `
                                        <option value="${billing.billing_id}" ${billing.billing_id === job.billing_entity ? 'selected' : ''}>
                                            ${billing.entity}
                                        </option>
                                    `).join('') : ''}
                                    <option value="create_new">+ Create New Entity</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="billing-details-display" id="billingDetailsDisplay" style="display: none;">
                            <div class="billing-entity-name" id="billingEntityName"></div>
                            <div class="billing-entity-address" id="billingEntityAddress"></div>
                        </div>
                        
                    </div>
                </div>
                
                <div id="status-history-tab" class="tab-panel">
                    <div class="job-details-section">
                        <h3>Status History</h3>
                        <div class="status-history">
                            ${job.status_history && job.status_history.length > 0 ? 
                                job.status_history.map(history => `
                                    <div class="status-history-item">
                                        <span class="status-history-status">${history.job_status || 'Unknown'}</span>
                                        <span class="status-history-date">${formatDate(history.date)}</span>
                                    </div>
                                `).join('') : 
                                '<p class="no-data">No status history available.</p>'
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    
    document.getElementById('jobDetailsContent').innerHTML = detailsHTML;
    document.getElementById('jobDetailsTitle').textContent = `#${job.job_id} - ${job.project_name || 'Unknown'} (${job.reference})`;
    document.getElementById('jobDetailsModal').style.display = 'block';
    
}

// Hide job details modal
function hideJobDetailsModal() {
    document.getElementById('jobDetailsModal').style.display = 'none';
}

// Switch job details tab
function switchJobTab(tabName, jobId) {
    console.log('Switching to tab:', tabName);
    
    // Remove active class from all tab buttons and panels
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabButtons.forEach(btn => btn.classList.remove('active'));
    tabPanels.forEach(panel => {
        panel.classList.remove('active');
        panel.style.display = 'none'; // Explicitly hide all panels
    });
    
    // Add active class to selected tab button and panel
    const activeButton = document.querySelector(`[onclick="switchJobTab('${tabName}', ${jobId})"]`);
    const activePanel = document.getElementById(`${tabName}-tab`);
    
    console.log('Active button found:', activeButton);
    console.log('Active panel found:', activePanel);
    
    if (activeButton) activeButton.classList.add('active');
    if (activePanel) {
        activePanel.classList.add('active');
        activePanel.style.display = 'block'; // Explicitly show the active panel
        console.log('Panel activated and displayed');
        
        // Fix quotes tab by rebuilding content
        if (tabName === 'quotes') {
            // Get the job data
            const job = jobs.find(j => j.job_id === jobId);
            if (job) {
                // Rebuild the quotes tab content
                const quotesContent = `
                    <div class="quotes-section">
                        <div class="quotes-header">
                            <button class="btn btn-primary" onclick="createQuote(${job.job_id})">
                                <span class="btn-icon">+</span>
                                New Quote
                            </button>
                        </div>
                        ${job.quotes && job.quotes.length > 0 ? `
                            <table class="quotes-table">
                                <thead>
                                    <tr>
                                        <th>Quote Number</th>
                                        <th>Date Created</th>
                                        <th>Cost (Excl. GST)</th>
                                        <th>Cost (Incl. GST)</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${job.quotes
                                        .sort((a, b) => {
                                            // Sort approved quote first, then by date created (newest first)
                                            if (job.approved_quote === a.quote_id) return -1;
                                            if (job.approved_quote === b.quote_id) return 1;
                                            return new Date(b.date_created) - new Date(a.date_created);
                                        })
                                        .map(quote => `
                                        <tr class="quote-row ${job.approved_quote === quote.quote_id ? 'approved-quote' : ''}">
                                            <td class="clickable" onclick="editQuote(${quote.quote_id})">${quote.quote_number || 'N/A'}</td>
                                            <td class="clickable" onclick="editQuote(${quote.quote_id})">${formatDate(quote.date_created) || 'N/A'}</td>
                                            <td class="clickable" onclick="editQuote(${quote.quote_id})">$${quote.cost_excl_gst ? quote.cost_excl_gst.toFixed(2) : '0.00'}</td>
                                            <td class="clickable" onclick="editQuote(${quote.quote_id})">$${quote.cost_incl_gst ? quote.cost_incl_gst.toFixed(2) : '0.00'}</td>
                                            <td>
                                                <button class="btn btn-sm btn-outline approve-btn" onclick="approveQuote(${job.job_id}, ${quote.quote_id}, event)" ${job.approved_quote === quote.quote_id ? 'disabled' : ''}>
                                                    ${job.approved_quote === quote.quote_id ? '✓ Approved' : '+ Approve'}
                                                </button>
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        ` : 
                            '<p class="no-data">No quotes available for this job.</p>'
                        }
                    </div>
                `;
                
                // Replace the entire panel content
                activePanel.innerHTML = quotesContent;
                console.log('Rebuilt quotes tab content');
            }
        }
    }
}

// Edit job from details modal
function editJobFromDetails(jobId) {
    // Close the details modal
    hideJobDetailsModal();
    
    // Open the edit modal
    editJob(jobId);
}

// Toggle status dropdown
function toggleStatusDropdown(jobId) {
    const dropdown = document.getElementById(`statusDropdown_${jobId}`);
    if (dropdown) {
        dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    }
}

// Change job status
async function changeJobStatus(jobId, newStatusId, newStatusName) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_status_id: newStatusId })
        });
        
        if (response.ok) {
            // Update the local job data
            const job = jobs.find(j => j.job_id === jobId);
            if (job) {
                // If changing from Work Order (ID 2) to Quote (ID 1), clear the approved quote
                if (job.job_status_id === 2 && newStatusId === 1) {
                    job.approved_quote = null;
                }
                
                job.job_status_id = newStatusId;
                job.job_status = newStatusName;
            }
            
            // Update the display
            const statusDisplay = document.getElementById('currentStatusDisplay');
            if (statusDisplay) {
                statusDisplay.textContent = newStatusName;
                statusDisplay.className = `job-status ${getStatusClass(newStatusName)}`;
            }
            
            // Hide the dropdown
            const dropdown = document.getElementById(`statusDropdown_${jobId}`);
            if (dropdown) {
                dropdown.style.display = 'none';
            }
            
            // Reload jobs to get updated data
            await loadAllData();
            renderJobsTable();
            
            showNotification('Job status updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update job status', 'error');
        }
    } catch (error) {
        console.error('Error updating job status:', error);
        showNotification('Error updating job status', 'error');
    }
}

// Show edit address modal
function showEditAddressModal(jobId) {
    const job = jobs.find(j => j.job_id === jobId);
    if (!job) return;
    
    // Populate the form with current address data
    document.getElementById('addressJobId').value = jobId;
    document.getElementById('editJobAddress').value = job.job_address || '';
    document.getElementById('editJobSuburb').value = job.suburb || '';
    document.getElementById('editJobState').value = job.state || '';
    document.getElementById('editJobPostcode').value = job.postcode || '';
    
    // Show the modal
    document.getElementById('editAddressModal').style.display = 'block';
}

// Hide edit address modal
function hideEditAddressModal() {
    document.getElementById('editAddressModal').style.display = 'none';
}

// Save address from modal
async function saveAddressFromModal() {
    const jobId = document.getElementById('addressJobId').value;
    const addressData = {
        job_address: document.getElementById('editJobAddress').value,
        suburb: document.getElementById('editJobSuburb').value,
        state: document.getElementById('editJobState').value,
        postcode: document.getElementById('editJobPostcode').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/address`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(addressData)
        });
        
        if (response.ok) {
            // Reload jobs to get updated data
            await loadAllData();
            renderJobsTable();
            
            // Hide the modal
            hideEditAddressModal();
            
            showNotification('Job address updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update job address', 'error');
        }
    } catch (error) {
        console.error('Error updating job address:', error);
        showNotification('Error updating job address', 'error');
    }
}

// Show add job modal
function showAddJobModal() {
    selectedJob = null;
    isEditing = false;
    
    // Reset form
    document.getElementById('jobForm').reset();
    document.getElementById('jobId').value = '';
    document.getElementById('jobModalTitle').textContent = 'Create New Job';
    document.getElementById('jobSubmitBtn').textContent = 'Create Job';
    
    // Populate dropdowns
    populateDropdowns();
    
    // Show modal
    document.getElementById('jobModal').style.display = 'block';
}

// Edit job
function editJob(jobId) {
    const job = jobs.find(j => j.job_id === jobId);
    if (!job) return;
    
    selectedJob = job;
    isEditing = true;
    
    // Update modal title and button
    document.getElementById('jobModalTitle').textContent = 'Edit Job';
    document.getElementById('jobSubmitBtn').textContent = 'Update Job';
    
    // Populate dropdowns first
    populateDropdowns();
    
    // Populate form fields AFTER dropdowns are populated
    document.getElementById('jobId').value = job.job_id;
    document.getElementById('jobReference').value = job.reference;
    document.getElementById('jobClient').value = job.client_id;
    document.getElementById('jobProject').value = job.project_id;
    document.getElementById('jobStaff').value = job.staff_id;
    
    // Update contacts for the selected client
    updateContacts();
    
    // Set the contact value after updating contacts
    document.getElementById('jobContact').value = job.contact_id;
    
    // Show modal
    document.getElementById('jobModal').style.display = 'block';
}

// Hide job modal
function hideJobModal() {
    document.getElementById('jobModal').style.display = 'none';
}

// Create quote
function createQuote(jobId) {
    const job = jobs.find(j => j.job_id === jobId);
    if (!job) return;
    
    // Navigate to quote page with job ID
    window.location.href = `/quote?jobId=${jobId}`;
}

// Edit quote
function editQuote(quoteId) {
    // Navigate to quote page with quote ID
    window.location.href = `/quote?quoteId=${quoteId}`;
}

// Hide quote modal
function hideQuoteModal() {
    document.getElementById('quoteModal').style.display = 'none';
}

// Populate dropdowns
function populateDropdowns() {
    // Populate clients
    const clientSelect = document.getElementById('jobClient');
    clientSelect.innerHTML = '<option value="">Select Client</option>' + 
        clients.map(client => `<option value="${client.client_id}">${client.name}</option>`).join('');
    
    // Populate projects
    const projectSelect = document.getElementById('jobProject');
    projectSelect.innerHTML = '<option value="">Select Project</option>' + 
        projects.map(project => `<option value="${project.project_id}">${project.name}</option>`).join('');
    
    // Populate contacts (only show "Select Contact" initially)
    const contactSelect = document.getElementById('jobContact');
    contactSelect.innerHTML = '<option value="">Select Contact</option>';
    
    // Populate staff
    const staffSelect = document.getElementById('jobStaff');
    staffSelect.innerHTML = '<option value="">Select Project Manager</option>' + 
        staff.map(staff => `<option value="${staff.staff_id}">${staff.first_name} ${staff.surname}</option>`).join('');
}

// Update contacts based on selected client
function updateContacts() {
    const clientId = parseInt(document.getElementById('jobClient').value);
    const contactSelect = document.getElementById('jobContact');
    
    if (clientId) {
        const clientContacts = contacts.filter(c => c.client_id === clientId);
        
        contactSelect.innerHTML = '<option value="">Select Contact</option>' + 
            clientContacts.map(contact => `<option value="${contact.contact_id}">${contact.first_name} ${contact.surname}</option>`).join('');
    } else {
        contactSelect.innerHTML = '<option value="">Select Contact</option>';
    }
}

// Delete job
async function deleteJob(jobId) {
    if (confirm('Are you sure you want to delete this job? This action cannot be undone.')) {
        try {
            const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Reload data
                await loadAllData();
                showNotification('Job deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete job', 'error');
            }
        } catch (error) {
            console.error('Error deleting job:', error);
            showNotification('Error deleting job', 'error');
        }
    }
}

// Submit job form function
async function submitJobForm() {
    const form = document.getElementById('jobForm');
    const formData = new FormData(form);
    const jobId = formData.get('job_id');
    
    // Get job status ID for "quote" status (for new jobs)
    const quoteStatus = jobStatuses.find(status => status.job_status && status.job_status.toLowerCase() === 'quote');
    const defaultStatusId = quoteStatus ? quoteStatus.job_status_id : 1; // Fallback to ID 1 if quote not found
    
    // For editing existing jobs, preserve the current status
    let jobStatusId;
    if (jobId) {
        // Editing existing job - preserve current status
        const currentJob = jobs.find(j => j.job_id === parseInt(jobId));
        jobStatusId = currentJob ? currentJob.job_status_id : defaultStatusId;
    } else {
        // Creating new job - use "quote" status
        jobStatusId = defaultStatusId;
    }
    
    const jobData = {
        reference: formData.get('reference'),
        client_id: parseInt(formData.get('client_id')),
        project_id: parseInt(formData.get('project_id')),
        contact_id: parseInt(formData.get('contact_id')),
        staff_id: parseInt(formData.get('staff_id')),
        job_status_id: jobStatusId,
        date_created: new Date().toISOString().split('T')[0]
    };
    
    try {
        if (jobId) {
            // Update existing job
            await updateJob(parseInt(jobId), jobData);
        } else {
            // Create new job
            await createJob(jobData);
        }
        
        hideJobModal();
    } catch (error) {
        console.error('Error handling job:', error);
        showNotification('Error handling job', 'error');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Job form submission (keeping for backward compatibility)
    document.getElementById('jobForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        await submitJobForm();
    });
    
    // Project creation form submission
    document.getElementById('createProjectForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        await createProjectFromJob();
    });
    
    // Client creation form submission
    document.getElementById('createClientForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        await createClientFromJob();
    });
    
    // Contact creation form submission
    document.getElementById('createContactForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        await createContactFromJob();
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
}

// Create new job
async function createJob(jobData) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jobData)
        });
        
        if (response.ok) {
            // Reload data
            await loadAllData();
            showNotification('Job created successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to create job', 'error');
        }
    } catch (error) {
        console.error('Error creating job:', error);
        showNotification('Error creating job', 'error');
    }
}

// Update existing job
async function updateJob(jobId, jobData) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jobData)
        });
        
        if (response.ok) {
            // Reload data
            await loadAllData();
            showNotification('Job updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update job', 'error');
        }
    } catch (error) {
        console.error('Error updating job:', error);
        showNotification('Error updating job', 'error');
    }
}


// Show create project modal
function showCreateProjectModal() {
    document.getElementById('createProjectForm').reset();
    document.getElementById('createProjectModal').style.display = 'block';
}

// Hide create project modal
function hideCreateProjectModal() {
    document.getElementById('createProjectModal').style.display = 'none';
}

// Create project from job modal
async function createProjectFromJob() {
    const formData = {
        name: document.getElementById('newProjectName').value,
        address: document.getElementById('newProjectAddress').value,
        suburb: document.getElementById('newProjectSuburb').value,
        state: document.getElementById('newProjectState').value,
        postcode: document.getElementById('newProjectPostcode').value ? parseInt(document.getElementById('newProjectPostcode').value) : null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const newProject = await response.json();
            
            // Add the new project to the projects array
            projects.push(newProject);
            
            // Update the project dropdown
            const projectSelect = document.getElementById('jobProject');
            const option = document.createElement('option');
            option.value = newProject.project_id;
            option.textContent = newProject.name;
            projectSelect.appendChild(option);
            
            // Select the new project
            projectSelect.value = newProject.project_id;
            
            showNotification('Project created successfully!', 'success');
            hideCreateProjectModal();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to create project', 'error');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        showNotification('Error creating project', 'error');
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

// Show create client modal
function showCreateClientModal() {
    document.getElementById('createClientForm').reset();
    document.getElementById('createClientModal').style.display = 'block';
}

// Hide create client modal
function hideCreateClientModal() {
    document.getElementById('createClientModal').style.display = 'none';
}

// Create client from job modal
async function createClientFromJob() {
    const formData = {
        name: document.getElementById('newClientName').value,
        address: document.getElementById('newClientAddress').value,
        suburb: document.getElementById('newClientSuburb').value,
        state: document.getElementById('newClientState').value,
        postcode: document.getElementById('newClientPostcode').value ? parseInt(document.getElementById('newClientPostcode').value) : null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/clients`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const newClient = await response.json();
            
            // Add the new client to the clients array
            clients.push(newClient);
            
            // Update the client dropdown
            const clientSelect = document.getElementById('jobClient');
            const option = document.createElement('option');
            option.value = newClient.client_id;
            option.textContent = newClient.name;
            clientSelect.appendChild(option);
            
            // Select the new client
            clientSelect.value = newClient.client_id;
            
            // Update contacts dropdown
            updateContacts();
            
            showNotification('Client created successfully!', 'success');
            hideCreateClientModal();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to create client', 'error');
        }
    } catch (error) {
        console.error('Error creating client:', error);
        showNotification('Error creating client', 'error');
    }
}

// Show create contact modal
function showCreateContactModal() {
    // Populate client dropdown in contact modal
    const contactClientSelect = document.getElementById('newContactClient');
    contactClientSelect.innerHTML = '<option value="">Select Client</option>';
    clients.forEach(client => {
        const option = document.createElement('option');
        option.value = client.client_id;
        option.textContent = client.name;
        contactClientSelect.appendChild(option);
    });
    
    document.getElementById('createContactForm').reset();
    document.getElementById('createContactModal').style.display = 'block';
}

// Hide create contact modal
function hideCreateContactModal() {
    document.getElementById('createContactModal').style.display = 'none';
}

// Create contact from job modal
async function createContactFromJob() {
    const formData = {
        client_id: parseInt(document.getElementById('newContactClient').value),
        first_name: document.getElementById('newContactFirstName').value,
        surname: document.getElementById('newContactSurname').value,
        email: document.getElementById('newContactEmail').value,
        phone: document.getElementById('newContactPhone').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/contacts`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            const newContact = await response.json();
            
            // Add the new contact to the contacts array
            contacts.push(newContact);
            
            // Update the contact dropdown if the client matches
            const selectedClientId = parseInt(document.getElementById('jobClient').value);
            if (selectedClientId === newContact.client_id) {
                const contactSelect = document.getElementById('jobContact');
                const option = document.createElement('option');
                option.value = newContact.contact_id;
                option.textContent = `${newContact.first_name} ${newContact.surname}`;
                contactSelect.appendChild(option);
                
                // Select the new contact
                contactSelect.value = newContact.contact_id;
            }
            
            showNotification('Contact created successfully!', 'success');
            hideCreateContactModal();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to create contact', 'error');
        }
    } catch (error) {
        console.error('Error creating contact:', error);
        showNotification('Error creating contact', 'error');
    }
}

// Update billing details when entity is selected
function updateBillingDetails(jobId) {
    const select = document.getElementById('billingEntitySelect');
    const selectedBillingId = select.value;
    const detailsDisplay = document.getElementById('billingDetailsDisplay');
    const entityName = document.getElementById('billingEntityName');
    const entityAddress = document.getElementById('billingEntityAddress');
    
    if (!selectedBillingId) {
        // Hide the details display if no entity is selected
        detailsDisplay.style.display = 'none';
        return;
    }
    
    // Handle create new entity option
    if (selectedBillingId === 'create_new') {
        // Hide the details display
        detailsDisplay.style.display = 'none';
        // Open the new billing entity modal
        showNewBillingEntityModal(jobId);
        // Reset the dropdown to no selection
        select.value = '';
        return;
    }
    
    // Find the selected billing entity from the job data
    const job = jobs.find(j => j.job_id === jobId);
    if (!job || !job.billing_entities) return;
    
    const selectedBilling = job.billing_entities.find(b => b.billing_id == selectedBillingId);
    if (!selectedBilling) return;
    
    // Display the billing entity details
    entityName.textContent = selectedBilling.entity;
    
    // Format the address: address, suburb, state postcode
    const addressParts = [
        selectedBilling.address,
        selectedBilling.suburb,
        selectedBilling.state,
        selectedBilling.postcode
    ].filter(Boolean);
    
    entityAddress.textContent = addressParts.join(', ');
    
    // Show the details display
    detailsDisplay.style.display = 'block';
    
    // Update the job's billing_entity in the database
    updateJobBillingEntity(jobId, selectedBillingId);
}

// Update job's billing entity in database
async function updateJobBillingEntity(jobId, billingEntityId) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/billing`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                billing_entity: billingEntityId ? parseInt(billingEntityId) : null
            })
        });
        
        if (response.ok) {
            console.log('Billing entity updated successfully');
        } else {
            console.error('Failed to update billing entity');
        }
    } catch (error) {
        console.error('Error updating billing entity:', error);
    }
}

// Show new billing entity modal
function showNewBillingEntityModal(jobId) {
    const modal = document.getElementById('createBillingEntityModal');
    modal.style.display = 'flex';
    
    // Store the job ID for later use
    modal.dataset.jobId = jobId;
    
    // Clear the form
    document.getElementById('createBillingEntityForm').reset();
}

// Hide new billing entity modal
function hideCreateBillingEntityModal() {
    const modal = document.getElementById('createBillingEntityModal');
    modal.style.display = 'none';
}

// Create new billing entity
async function createBillingEntity() {
    const modal = document.getElementById('createBillingEntityModal');
    const jobId = modal.dataset.jobId;
    
    const entity = document.getElementById('newBillingEntity').value.trim();
    const address = document.getElementById('newBillingAddress').value.trim();
    const suburb = document.getElementById('newBillingSuburb').value.trim();
    const state = document.getElementById('newBillingState').value;
    const postcode = document.getElementById('newBillingPostcode').value.trim();
    
    if (!entity) {
        showNotification('Entity name is required', 'error');
        return;
    }
    
    try {
        // Get the client ID from the job
        const job = jobs.find(j => j.job_id == jobId);
        if (!job) {
            showNotification('Job not found', 'error');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/billing`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                client_id: job.client_id,
                entity: entity,
                address: address || null,
                suburb: suburb || null,
                state: state || null,
                postcode: postcode ? parseInt(postcode) : null
            })
        });
        
        if (response.ok) {
            const newBillingEntity = await response.json();
            showNotification('Billing entity created successfully', 'success');
            
            // Close the modal
            hideCreateBillingEntityModal();
            
            // Update the current job's billing_entities array with the new entity
            const job = jobs.find(j => j.job_id == jobId);
            if (job) {
                if (!job.billing_entities) {
                    job.billing_entities = [];
                }
                job.billing_entities.push(newBillingEntity);
            }
            
            // Update the dropdown directly with the new billing entity
            const select = document.getElementById('billingEntitySelect');
            if (select) {
                // Create new option element
                const newOption = document.createElement('option');
                newOption.value = newBillingEntity.billing_id;
                newOption.textContent = newBillingEntity.entity;
                
                // Insert before the "Create New Entity" option
                const createNewOption = select.querySelector('option[value="create_new"]');
                if (createNewOption) {
                    select.insertBefore(newOption, createNewOption);
                } else {
                    select.appendChild(newOption);
                }
                
                // Select the newly created billing entity
                select.value = newBillingEntity.billing_id;
                updateBillingDetails(jobId);
            }
            
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to create billing entity', 'error');
        }
    } catch (error) {
        console.error('Error creating billing entity:', error);
        showNotification('Error creating billing entity', 'error');
    }
}

// Edit billing details
function editBillingDetails(jobId) {
    // For now, just show a notification that this feature is coming soon
    showNotification('Billing details editing will be available soon!', 'info');
    
    // TODO: Implement billing details editing modal
    // This would open a modal similar to the address editing modal
    // with fields for all the billing information
}

// Approve a quote for a job
async function approveQuote(jobId, quoteId, event) {
    // Prevent event bubbling to avoid triggering the row click
    event.stopPropagation();
    
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/approve-quote`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                approved_quote: quoteId
            })
        });
        
        if (response.ok) {
            showNotification('Quote approved successfully', 'success');
            
            // Update the job data in memory
            const job = jobs.find(j => j.job_id === jobId);
            if (job) {
                job.approved_quote = quoteId;
                job.job_status_id = 2; // Work Order status
                job.job_status = 'Work Order'; // Update status name for display
                job.stage_id = 1; // Pre-Production stage
            }
            
            // Re-render the jobs table to show updated status
            renderJobsTable();
            
            // Re-render the quotes tab to show updated approval status
            const jobDetailsModal = document.getElementById('jobDetailsModal');
            if (jobDetailsModal.style.display === 'block') {
                showJobDetails(jobId);
                setTimeout(() => {
                    switchJobTab('quotes', jobId);
                }, 100);
            }
            
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to approve quote', 'error');
        }
    } catch (error) {
        console.error('Error approving quote:', error);
        showNotification('Error approving quote', 'error');
    }
}

// Add event listener for billing entity form submission
document.addEventListener('DOMContentLoaded', function() {
    const billingEntityForm = document.getElementById('createBillingEntityForm');
    if (billingEntityForm) {
        billingEntityForm.addEventListener('submit', function(e) {
            e.preventDefault();
            createBillingEntity();
        });
    }
});

