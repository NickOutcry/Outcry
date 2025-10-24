// Workflow Management JavaScript

const API_BASE_URL = 'http://localhost:5001/api';

let jobs = [];
let stages = [];
let draggedJob = null;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Workflow page initialized');
    loadWorkflowData();
    initializeDragAndDrop();
    initializeModalEvents();
});

// Initialize modal event listeners
function initializeModalEvents() {
    // Close modal when clicking outside of it
    document.addEventListener('click', (e) => {
        const modal = document.getElementById('jobTasksModal');
        if (e.target === modal) {
            hideJobTasksModal();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            hideJobTasksModal();
        }
    });
}

// Load workflow data
async function loadWorkflowData() {
    try {
        console.log('Loading workflow data...');
        
        // Load jobs and stages in parallel
        const [jobsResponse, stagesResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/jobs`),
            fetch(`${API_BASE_URL}/stages`)
        ]);
        
        if (!jobsResponse.ok || !stagesResponse.ok) {
            throw new Error('Failed to load workflow data');
        }
        
        jobs = await jobsResponse.json();
        stages = await stagesResponse.json();
        
        console.log('Jobs loaded:', jobs.length);
        console.log('Stages loaded:', stages.length);
        
        renderWorkflow();
        
    } catch (error) {
        console.error('Error loading workflow data:', error);
        showNotification('Error loading workflow data', 'error');
    }
}

// Render the workflow
function renderWorkflow() {
    console.log('Rendering workflow...');
    
    const workflowStages = document.getElementById('workflowStages');
    
    // Clear existing content
    workflowStages.innerHTML = '';
    
    // Group jobs by stage
    const jobsByStage = {};
    stages.forEach(stage => {
        jobsByStage[stage.stage_id] = jobs.filter(job => job.stage_id === stage.stage_id);
    });
    
    // Create stage columns dynamically
    stages.forEach(stage => {
        const stageColumn = createStageColumn(stage);
        const stageJobs = jobsByStage[stage.stage_id] || [];
        renderStageColumn(stageColumn, stage, stageJobs);
        workflowStages.appendChild(stageColumn);
    });
}

// Create a stage column element
function createStageColumn(stage) {
    const stageColumn = document.createElement('div');
    stageColumn.className = 'stage-column';
    stageColumn.dataset.stageId = stage.stage_id;
    
    stageColumn.innerHTML = `
        <div class="stage-header">
            <h3>${stage.stage}</h3>
            <span class="stage-count">0</span>
        </div>
        <div class="stage-content">
            <div class="no-jobs">No jobs in this stage</div>
        </div>
    `;
    
    return stageColumn;
}

// Render a stage column
function renderStageColumn(stageColumn, stage, stageJobs) {
    const stageContent = stageColumn.querySelector('.stage-content');
    const stageCount = stageColumn.querySelector('.stage-count');
    
    // Update count
    stageCount.textContent = stageJobs.length;
    
    // Clear existing content
    stageContent.innerHTML = '';
    
    if (stageJobs.length === 0) {
        stageContent.innerHTML = '<div class="no-jobs">No jobs in this stage</div>';
        return;
    }
    
    // Render job cards
    stageJobs.forEach(job => {
        const jobCard = createJobCard(job);
        stageContent.appendChild(jobCard);
    });
}

// Create a job card
function createJobCard(job) {
    const jobCard = document.createElement('div');
    jobCard.className = 'job-card';
    jobCard.draggable = true;
    jobCard.dataset.jobId = job.job_id;
    
    // Format the title: job number - project (job reference)
    const title = `#${job.job_id} - ${job.project_name || 'No Project'} (${job.reference || 'No Reference'})`;
    
    // Format the due date
    const dueDate = job.stage_due_date ? new Date(job.stage_due_date).toLocaleDateString() : 'No due date set';
    
    jobCard.innerHTML = `
        <div class="job-title">${title}</div>
        <div class="job-due-date">${dueDate}</div>
    `;
    
    // Add click event to open job tasks modal
    jobCard.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        showJobTasksModal(job);
    });
    
    return jobCard;
}

// Move job to a different stage
async function moveJobToStage(jobId, stageId) {
    try {
        console.log(`Moving job ${jobId} to stage ${stageId}`);
        
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/stage`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                stage_id: stageId
            })
        });
        
        if (response.ok) {
            showNotification('Job stage updated successfully', 'success');
            
            // Update the job in our local data
            const job = jobs.find(j => j.job_id === jobId);
            if (job) {
                job.stage_id = stageId;
            }
            
            // Re-render the workflow
            renderWorkflow();
            
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update job stage', 'error');
        }
        
    } catch (error) {
        console.error('Error moving job to stage:', error);
        showNotification('Error updating job stage', 'error');
    }
}

// Initialize drag and drop functionality
function initializeDragAndDrop() {
    console.log('Initializing drag and drop...');
    
    // Add drag event listeners to job cards (using event delegation)
    document.addEventListener('dragstart', function(e) {
        if (e.target.classList.contains('job-card')) {
            draggedJob = e.target;
            e.target.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/html', e.target.outerHTML);
        }
    });
    
    document.addEventListener('dragend', function(e) {
        if (e.target.classList.contains('job-card')) {
            e.target.classList.remove('dragging');
            draggedJob = null;
        }
    });
    
    // Add drop event listeners to stage columns (using event delegation)
    document.addEventListener('dragover', function(e) {
        if (e.target.closest('.stage-column')) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            e.target.closest('.stage-column').classList.add('drag-over');
        }
    });
    
    document.addEventListener('dragleave', function(e) {
        if (e.target.closest('.stage-column')) {
            e.target.closest('.stage-column').classList.remove('drag-over');
        }
    });
    
    document.addEventListener('drop', function(e) {
        if (e.target.closest('.stage-column')) {
            e.preventDefault();
            const stageColumn = e.target.closest('.stage-column');
            stageColumn.classList.remove('drag-over');
            
            if (draggedJob) {
                const jobId = parseInt(draggedJob.dataset.jobId);
                const stageId = parseInt(stageColumn.dataset.stageId);
                
                if (jobId && stageId) {
                    moveJobToStage(jobId, stageId);
                }
            }
        }
    });
}

// Show job tasks modal
function showJobTasksModal(job) {
    const modal = document.getElementById('jobTasksModal');
    if (!modal) {
        console.error('Job tasks modal not found');
        return;
    }
    
    // Update modal title
    const title = `#${job.job_id} - ${job.project_name || 'No Project'} (${job.reference || 'No Reference'})`;
    const modalTitle = modal.querySelector('.modal-title');
    if (modalTitle) {
        modalTitle.textContent = title;
    }
    
    // Generate tabs for each stage
    const tabsContainer = modal.querySelector('.job-tabs');
    if (tabsContainer) {
        tabsContainer.innerHTML = stages.map(stage => `
            <button class="tab-button ${job.stage_id === stage.stage_id ? 'active' : ''}" 
                    onclick="switchJobTaskTab('${stage.stage}', ${job.job_id})">
                ${stage.stage}
            </button>
        `).join('');
    }
    
    // Generate tab content
    const tabContent = modal.querySelector('.tab-content');
    if (tabContent) {
        tabContent.innerHTML = stages.map(stage => `
            <div id="tab-${stage.stage}" class="tab-panel ${job.stage_id === stage.stage_id ? 'active' : ''}">
                <div class="stage-tasks">
                    <div class="stage-header">
                        <div class="stage-due-date-container">
                            <label class="stage-due-date-label">Stage due date:</label>
                            <div class="date-input-wrapper">
                                <input type="date" 
                                       class="stage-due-date-input" 
                                       value="${job.stage_due_date ? new Date(job.stage_due_date).toISOString().split('T')[0] : ''}"
                                       onchange="updateStageDueDate(${job.job_id}, ${stage.stage_id}, this.value)"
                                       onclick="this.showPicker && this.showPicker()"
                                       style="cursor: pointer;">
                                <span class="calendar-icon" style="cursor: pointer;" onclick="this.previousElementSibling.showPicker && this.previousElementSibling.showPicker()">📅</span>
                            </div>
                        </div>
                        ${job.stage_id === stage.stage_id ? 
                            `<button class="stage-complete-btn" onclick="markStageComplete(${job.job_id}, ${stage.stage_id})">
                                + stage complete
                            </button>` : 
                            '<div class="stage-complete-placeholder"></div>'
                        }
                    </div>
                    <div class="tasks-list">
                        ${generateItemsForStage(job, stage)}
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    // Store job ID in modal dataset for task creation
    modal.dataset.jobId = job.job_id;
    
    // Show the modal
    modal.style.display = 'flex';
    
    // Load tasks for all items after modal is shown
    loadTasksForAllItems(job, stages);
}

// Hide job tasks modal
function hideJobTasksModal() {
    const modal = document.getElementById('jobTasksModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Generate items for a specific stage
function generateItemsForStage(job, stage) {
    // Find the approved quote
    const approvedQuote = job.quotes ? job.quotes.find(q => q.quote_id === job.approved_quote) : null;
    
    if (!approvedQuote || !approvedQuote.items || approvedQuote.items.length === 0) {
        return '<p>No items available for this job.</p>';
    }
    
    return approvedQuote.items.map((item, index) => {
        const itemNumber = index + 1; // Sequential number starting from 1
        const uniqueItemId = `${item.item_id}-${stage.stage_id}`; // Make ID unique per stage
        return `
        <div class="item-box">
            <div class="item-header" onclick="toggleItemBox('${uniqueItemId}')">
                <div class="item-title">
                    <span class="item-name">${itemNumber} - ${item.reference || 'No Reference'} (${item.product_name})</span>
                    <span class="item-details">Qty: ${item.quantity}${item.length ? `, L: ${item.length}m` : ''}${item.height ? `, H: ${item.height}m` : ''}</span>
                </div>
                <div class="item-toggle">▼</div>
            </div>
            <div class="item-content" id="item-${uniqueItemId}">
                <div class="item-tasks">
                    <div class="tasks-loading">Loading tasks...</div>
                    <div class="task-item add-task-item" onclick="addNewTask(${item.item_id}, ${stage.stage_id})">
                        <div class="add-task-icon">+</div>
                        <span class="add-task-text">Add Task</span>
                    </div>
                </div>
            </div>
        </div>
        `;
    }).join('');
}

// Load tasks for all items in all stages
async function loadTasksForAllItems(job, stages) {
    try {
        // Find the approved quote
        const approvedQuote = job.quotes ? job.quotes.find(q => q.quote_id === job.approved_quote) : null;
        
        if (!approvedQuote || !approvedQuote.items || approvedQuote.items.length === 0) {
            return;
        }
        
        // Load tasks for each stage
        for (const stage of stages) {
            // Fetch tasks for this stage
            const response = await fetch(`${API_BASE_URL}/jobs/${job.job_id}/tasks?stage_id=${stage.stage_id}`);
            if (!response.ok) {
                console.error(`Failed to fetch tasks for stage ${stage.stage_id}`);
                continue;
            }
            
            const tasks = await response.json();
            
            // Load tasks for each item in this stage
            for (const item of approvedQuote.items) {
                const uniqueItemId = `${item.item_id}-${stage.stage_id}`;
                const itemContent = document.getElementById(`item-${uniqueItemId}`);
                
                if (itemContent) {
                    const tasksList = itemContent.querySelector('.item-tasks');
                    const loadingDiv = itemContent.querySelector('.tasks-loading');
                    
                    if (tasksList && loadingDiv) {
                        // Filter tasks for this specific item
                        const itemTasks = tasks.filter(task => task.item_id === item.item_id);
                        
                        // Generate HTML for tasks
                        const tasksHTML = itemTasks.map(task => {
                            const completedDate = task.time_completed ? new Date(task.time_completed).toLocaleString() : null;
                            return `
                            <div class="task-item">
                                <label class="task-checkbox">
                                    <input type="checkbox" id="task-${task.task_id}" 
                                           ${task.time_completed ? 'checked' : ''}
                                           onchange="updateTaskStatus(${task.task_id}, ${task.stage_id}, this.checked)">
                                    <span class="checkmark"></span>
                                    <span class="task-text">${task.task_name}</span>
                                    ${completedDate ? `<span class="task-timestamp">Completed: ${completedDate}</span>` : ''}
                                </label>
                            </div>
                            `;
                        }).join('');
                        
                        // Replace loading div with tasks
                        loadingDiv.outerHTML = tasksHTML;
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error loading tasks for all items:', error);
    }
}

// Generate tasks for a specific item and stage (kept for compatibility)
async function generateTasksForItem(item, stage) {
    try {
        // Get the current job ID from the modal
        const modal = document.getElementById('jobTasksModal');
        const jobId = modal.dataset.jobId;
        
        if (!jobId) {
            console.error('Job ID not found for task loading');
            return '';
        }
        
        // Fetch tasks for this job, stage, and item
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/tasks?stage_id=${stage.stage_id}`);
        if (!response.ok) {
            console.error('Failed to fetch tasks');
            return '';
        }
        
        const tasks = await response.json();
        
        // Filter tasks for this specific item
        const itemTasks = tasks.filter(task => task.item_id === item.item_id);
        
        // Generate HTML for tasks
        return itemTasks.map(task => {
            const completedDate = task.time_completed ? new Date(task.time_completed).toLocaleString() : null;
            return `
            <div class="task-item">
                <label class="task-checkbox">
                    <input type="checkbox" id="task-${task.task_id}" 
                           ${task.time_completed ? 'checked' : ''}
                           onchange="updateTaskStatus(${task.task_id}, ${task.stage_id}, this.checked)">
                    <span class="checkmark"></span>
                    <span class="task-text">${task.task_name}</span>
                    ${completedDate ? `<span class="task-timestamp">Completed: ${completedDate}</span>` : ''}
                </label>
            </div>
            `;
        }).join('');
        
    } catch (error) {
        console.error('Error loading tasks:', error);
        return '';
    }
}

// Add new task to an item
function addNewTask(itemId, stageId) {
    // Create unique ID for this item in this stage
    const uniqueItemId = `${itemId}-${stageId}`;
    
    // Find the item content for this item
    const itemContent = document.getElementById(`item-${uniqueItemId}`);
    if (itemContent) {
        const tasksList = itemContent.querySelector('.item-tasks');
        const addTaskItem = itemContent.querySelector('.add-task-item');
        
        // Check if input is already visible
        if (addTaskItem.querySelector('.task-input')) {
            return; // Already showing input
        }
        
        // Hide the add task item and show input
        addTaskItem.style.display = 'none';
        
        // Create input container
        const inputContainer = document.createElement('div');
        inputContainer.className = 'task-item task-input-container';
        inputContainer.innerHTML = `
            <div class="add-task-icon">+</div>
            <input type="text" class="task-input" placeholder="Enter task description..." autofocus>
            <div class="task-input-actions">
                <button class="task-save-btn" onclick="saveNewTask(${itemId}, ${stageId}, this)">Save</button>
                <button class="task-cancel-btn" onclick="cancelNewTask('${uniqueItemId}')">Cancel</button>
            </div>
        `;
        
        // Insert before the add task item
        tasksList.insertBefore(inputContainer, addTaskItem);
        
        // Focus the input
        const input = inputContainer.querySelector('.task-input');
        input.focus();
        
        // Handle Enter key
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                saveNewTask(itemId, stageId, inputContainer.querySelector('.task-save-btn'));
            }
        });
        
        // Handle Escape key
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                cancelNewTask(uniqueItemId);
            }
        });
    }
}

// Save new task
async function saveNewTask(itemId, stageId, button) {
    const inputContainer = button.closest('.task-input-container');
    const input = inputContainer.querySelector('.task-input');
    const taskText = input.value.trim();
    
    if (taskText) {
        try {
            // Get the current job ID from the modal
            const modal = document.getElementById('jobTasksModal');
            const jobId = modal.dataset.jobId;
            
            if (!jobId) {
                showNotification('Job ID not found', 'error');
                return;
            }
            
            // Create task via API
            const response = await fetch(`${API_BASE_URL}/tasks`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    task_name: taskText,
                    job_id: parseInt(jobId),
                    item_id: itemId,
                    stage_id: stageId
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                
                // Find the item content for this item
                const itemContent = document.getElementById(`item-${itemId}`);
                if (itemContent) {
                    const tasksList = itemContent.querySelector('.item-tasks');
                    const addTaskItem = itemContent.querySelector('.add-task-item');
                    
                    // Create new task element
                    const newTaskElement = document.createElement('div');
                    newTaskElement.className = 'task-item';
                    newTaskElement.innerHTML = `
                        <label class="task-checkbox">
                            <input type="checkbox" id="task-${result.task_id}" 
                                   onchange="updateTaskStatus(${result.task_id}, ${stageId}, this.checked)">
                            <span class="checkmark"></span>
                            <span class="task-text">${taskText}</span>
                        </label>
                    `;
                    
                    // Insert before the add task item
                    tasksList.insertBefore(newTaskElement, addTaskItem);
                    
                    showNotification('Task added successfully', 'success');
                }
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to create task', 'error');
                return;
            }
        } catch (error) {
            console.error('Error creating task:', error);
            showNotification('Error creating task', 'error');
            return;
        }
    }
    
    // Remove input container and show add task item
    inputContainer.remove();
    const addTaskItem = document.querySelector(`#item-${itemId} .add-task-item`);
    if (addTaskItem) {
        addTaskItem.style.display = 'flex';
    }
}

// Cancel new task
function cancelNewTask(uniqueItemId) {
    const inputContainer = document.querySelector(`#item-${uniqueItemId} .task-input-container`);
    if (inputContainer) {
        inputContainer.remove();
    }
    
    const addTaskItem = document.querySelector(`#item-${uniqueItemId} .add-task-item`);
    if (addTaskItem) {
        addTaskItem.style.display = 'flex';
    }
}

// Toggle item box expansion
function toggleItemBox(uniqueItemId) {
    const itemContent = document.getElementById(`item-${uniqueItemId}`);
    if (!itemContent) {
        console.error(`Item content not found for ID: item-${uniqueItemId}`);
        return;
    }
    
    const itemHeader = itemContent.previousElementSibling;
    const toggle = itemHeader.querySelector('.item-toggle');
    
    if (itemContent.style.display === 'none' || itemContent.style.display === '') {
        itemContent.style.display = 'block';
        toggle.textContent = '▲';
        itemHeader.classList.add('expanded');
    } else {
        itemContent.style.display = 'none';
        toggle.textContent = '▼';
        itemHeader.classList.remove('expanded');
    }
}

// Update task status
async function updateTaskStatus(taskId, stageId, completed) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                completed: completed
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            console.log(`Task ${taskId} status updated:`, result);
            
            // Update the task display to show/hide timestamp
            updateTaskDisplay(taskId, completed, result.time_completed);
            
            showNotification(`Task ${completed ? 'completed' : 'marked as incomplete'}`, 'success');
        } else {
            const error = await response.json();
            console.error('Failed to update task status:', error);
            showNotification(error.error || 'Failed to update task status', 'error');
        }
    } catch (error) {
        console.error('Error updating task status:', error);
        showNotification('Error updating task status', 'error');
    }
}

// Update task display to show/hide timestamp
function updateTaskDisplay(taskId, completed, timeCompleted) {
    const taskElement = document.getElementById(`task-${taskId}`);
    if (!taskElement) return;
    
    const taskText = taskElement.parentElement.querySelector('.task-text');
    if (!taskText) return;
    
    // Remove existing timestamp if any
    const existingTimestamp = taskText.parentElement.querySelector('.task-timestamp');
    if (existingTimestamp) {
        existingTimestamp.remove();
    }
    
    // Add timestamp if completed
    if (completed && timeCompleted) {
        const completedDate = new Date(timeCompleted).toLocaleString();
        const timestampSpan = document.createElement('span');
        timestampSpan.className = 'task-timestamp';
        timestampSpan.textContent = `Completed: ${completedDate}`;
        taskText.parentElement.appendChild(timestampSpan);
    }
}

// Update stage due date
async function updateStageDueDate(jobId, stageId, dueDate) {
    try {
        console.log(`Updating stage ${stageId} due date for job ${jobId} to ${dueDate}`);
        
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/stage-due-date`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                stage_id: stageId,
                due_date: dueDate 
            })
        });
        
        if (response.ok) {
            showNotification('Stage due date updated successfully', 'success');
            // Update local job data
            const job = jobs.find(j => j.job_id === jobId);
            if (job) {
                job.stage_due_date = dueDate;
            }
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update due date', 'error');
        }
    } catch (error) {
        console.error('Error updating stage due date:', error);
        showNotification('Error updating due date', 'error');
    }
}

// Open date picker
function openDatePicker(input) {
    if (input && input.showPicker) {
        input.showPicker();
    } else if (input) {
        input.focus();
        input.click();
    }
}

// Mark stage as complete
async function markStageComplete(jobId, stageId) {
    try {
        console.log(`Marking stage ${stageId} as complete for job ${jobId}`);
        
        // Find the current stage and get the next stage
        const currentStage = stages.find(s => s.stage_id === stageId);
        if (!currentStage) {
            showNotification('Current stage not found', 'error');
            return;
        }
        
        // Find the next stage in sequence
        const nextStage = stages.find(s => s.stage_order === currentStage.stage_order + 1);
        if (!nextStage) {
            showNotification('This is the final stage - no next stage available', 'info');
            return;
        }
        
        // Update the job stage
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/stage`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stage_id: nextStage.stage_id })
        });
        
        if (response.ok) {
            showNotification(`Stage completed! Moved to ${nextStage.stage}`, 'success');
            
            // Update local job data
            const job = jobs.find(j => j.job_id === jobId);
            if (job) {
                job.stage_id = nextStage.stage_id;
            }
            
            // Refresh the workflow data to update the display
            await loadWorkflowData();
            
            // If the modal is open, refresh it
            const modal = document.getElementById('jobTasksModal');
            if (modal && modal.style.display === 'flex') {
                showJobTasksModal(job);
            }
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to complete stage', 'error');
        }
    } catch (error) {
        console.error('Error completing stage:', error);
        showNotification('Error completing stage', 'error');
    }
}

// Switch between job task tabs
function switchJobTaskTab(stageName, jobId) {
    // Remove active class from all tabs and panels
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
    
    // Add active class to clicked tab
    const activeTab = document.querySelector(`button[onclick="switchJobTaskTab('${stageName}', ${jobId})"]`);
    if (activeTab) {
        activeTab.classList.add('active');
    }
    
    // Add active class to corresponding panel
    const activePanel = document.getElementById(`tab-${stageName}`);
    if (activePanel) {
        activePanel.classList.add('active');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Refresh workflow data
function refreshWorkflow() {
    console.log('Refreshing workflow data...');
    loadWorkflowData();
}
