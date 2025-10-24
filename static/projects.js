// Projects Management JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Global variables
let projects = [];
let selectedProject = null;
let isEditing = false;

// Date formatting function
function formatDate(dateString) {
    if (!dateString) return null;
    
    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return null;
        
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        
        return `${day}-${month}-${year}`;
    } catch (error) {
        console.error('Error formatting date:', error);
        return null;
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadProjects();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Form submission
    document.getElementById('projectForm').addEventListener('submit', function(e) {
        e.preventDefault();
        if (isEditing) {
            updateProject();
        } else {
            createProject();
        }
    });
}

// Load projects from API
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        if (response.ok) {
            projects = await response.json();
            renderProjectsTable();
        } else {
            showNotification('Error loading projects', 'error');
        }
    } catch (error) {
        console.error('Error loading projects:', error);
        showNotification('Error loading projects', 'error');
    }
}

// Render projects table
function renderProjectsTable() {
    const tbody = document.getElementById('projectsTableBody');
    tbody.innerHTML = '';
    
    if (projects.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" style="text-align: center; padding: 2rem; color: #666;">
                    No projects found. Click "Add Project" to create your first project.
                </td>
            </tr>
        `;
        return;
    }
    
    projects.forEach(project => {
        const row = document.createElement('tr');
        row.onclick = () => showProjectDetails(project.project_id);
        
        row.innerHTML = `
            <td>#${project.project_id}</td>
            <td>${project.name}</td>
            <td>${project.address || 'N/A'}</td>
            <td>${project.suburb || 'N/A'}</td>
            <td>${project.state || 'N/A'}</td>
            <td>${project.postcode || 'N/A'}</td>
            <td>${formatDate(project.date_created) || 'N/A'}</td>
            <td class="delete-cell">
                <button class="delete-btn" onclick="deleteProject(${project.project_id}); event.stopPropagation()" title="Delete Project">×</button>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// Show project details modal
function showProjectDetails(projectId) {
    const project = projects.find(p => p.project_id === projectId);
    if (!project) return;
    
    const detailsHTML = `
        <div class="project-details-section">
            <div class="project-details-header">
                <h3>Project Information</h3>
                <button class="edit-toggle-btn" onclick="editProjectFromDetails(${project.project_id})">+edit</button>
            </div>
            <div class="project-details-grid">
                <div class="project-detail-item">
                    <div class="project-detail-label">Project ID</div>
                    <div class="project-detail-value">#${project.project_id}</div>
                </div>
                <div class="project-detail-item">
                    <div class="project-detail-label">Name</div>
                    <div class="project-detail-value">${project.name}</div>
                </div>
                <div class="project-detail-item">
                    <div class="project-detail-label">Address</div>
                    <div class="project-detail-value">${project.address || 'N/A'}</div>
                </div>
                <div class="project-detail-item">
                    <div class="project-detail-label">Suburb</div>
                    <div class="project-detail-value">${project.suburb || 'N/A'}</div>
                </div>
                <div class="project-detail-item">
                    <div class="project-detail-label">State</div>
                    <div class="project-detail-value">${project.state || 'N/A'}</div>
                </div>
                <div class="project-detail-item">
                    <div class="project-detail-label">Postcode</div>
                    <div class="project-detail-value">${project.postcode || 'N/A'}</div>
                </div>
                <div class="project-detail-item">
                    <div class="project-detail-label">Date Created</div>
                    <div class="project-detail-value">${formatDate(project.date_created) || 'N/A'}</div>
                </div>
            </div>
        </div>
        
        <div class="project-details-section">
            <h3>Jobs</h3>
            <div class="jobs-section">
                <p class="no-data">Jobs associated with this project will be displayed here.</p>
                <div class="jobs-actions">
                    <button class="btn btn-primary" onclick="createJobForProject(${project.project_id})">
                        <span class="btn-icon">+</span>
                        Create New Job
                    </button>
                </div>
            </div>
        </div>
        
        <div class="project-details-actions">
            <button class="btn btn-delete" onclick="deleteProjectFromDetails(${project.project_id})">Delete Project</button>
        </div>
    `;
    
    document.getElementById('projectDetailsContent').innerHTML = detailsHTML;
    document.getElementById('projectDetailsModal').style.display = 'block';
}

// Hide project details modal
function hideProjectDetailsModal() {
    document.getElementById('projectDetailsModal').style.display = 'none';
}

// Edit project from details modal
function editProjectFromDetails(projectId) {
    // Close the details modal
    hideProjectDetailsModal();
    
    // Open the edit modal
    editProject(projectId);
}

// Delete project from details modal
function deleteProjectFromDetails(projectId) {
    // Close the details modal first
    hideProjectDetailsModal();
    
    // Call the existing delete function
    deleteProject(projectId);
}

// Show add project modal
function showAddProjectModal() {
    selectedProject = null;
    isEditing = false;
    
    // Reset form
    document.getElementById('projectForm').reset();
    document.getElementById('projectId').value = '';
    document.getElementById('projectModalTitle').textContent = 'Create New Project';
    document.getElementById('projectSubmitBtn').textContent = 'Create Project';
    
    // Show modal
    document.getElementById('projectModal').style.display = 'block';
}

// Edit project
function editProject(projectId) {
    const project = projects.find(p => p.project_id === projectId);
    if (!project) return;
    
    selectedProject = project;
    isEditing = true;
    
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
    document.getElementById('projectModal').style.display = 'block';
}

// Hide project modal
function hideProjectModal() {
    document.getElementById('projectModal').style.display = 'none';
}

// Create project
async function createProject() {
    const formData = {
        name: document.getElementById('projectName').value,
        address: document.getElementById('projectAddress').value,
        suburb: document.getElementById('projectSuburb').value,
        state: document.getElementById('projectState').value,
        postcode: document.getElementById('projectPostcode').value ? parseInt(document.getElementById('projectPostcode').value) : null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showNotification('Project created successfully!', 'success');
            hideProjectModal();
            loadProjects();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to create project', 'error');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        showNotification('Error creating project', 'error');
    }
}

// Update project
async function updateProject() {
    const projectId = document.getElementById('projectId').value;
    const formData = {
        name: document.getElementById('projectName').value,
        address: document.getElementById('projectAddress').value,
        suburb: document.getElementById('projectSuburb').value,
        state: document.getElementById('projectState').value,
        postcode: document.getElementById('projectPostcode').value ? parseInt(document.getElementById('projectPostcode').value) : null
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showNotification('Project updated successfully!', 'success');
            hideProjectModal();
            loadProjects();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update project', 'error');
        }
    } catch (error) {
        console.error('Error updating project:', error);
        showNotification('Error updating project', 'error');
    }
}

// Delete project
async function deleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Project deleted successfully!', 'success');
            loadProjects();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to delete project', 'error');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        showNotification('Error deleting project', 'error');
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

// Create job for specific project
function createJobForProject(projectId) {
    // Close the project details modal
    hideProjectDetailsModal();
    
    // Navigate to the jobs page and open the job creation modal
    window.location.href = `/jobs?createJob=true&projectId=${projectId}`;
}
