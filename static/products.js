// Global data storage
let categories = [];
let products = [];
let measureTypes = [];
let selectedCategory = null;
let currentProduct = null;
let currentVariable = null;

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// DOM elements
const categoryTabs = document.getElementById('categoryTabs');
const productsTableBody = document.getElementById('productsTableBody');

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    loadData();
    setupEventListeners();
});

// Load data from API
async function loadData() {
    try {
        await Promise.all([
            loadCategories(),
            loadProducts(),
            loadMeasureTypes()
        ]);
        renderCategoryTabs();
        renderProductsTable();
        populateCategoryDropdown(); // Populate dropdown after categories are loaded
        populateMeasureTypeDropdown(); // Populate measure type dropdown
    } catch (error) {
        console.error('Error loading data:', error);
        showNotification('Error loading data. Please check if the server is running.', 'error');
    }
}

// Load categories from API
async function loadCategories() {
    const response = await fetch(`${API_BASE_URL}/categories`);
    if (!response.ok) {
        throw new Error('Failed to load categories');
    }
    categories = await response.json();
}

// Load products from API
async function loadProducts() {
    const response = await fetch(`${API_BASE_URL}/products`);
    if (!response.ok) {
        throw new Error('Failed to load products');
    }
    products = await response.json();
}

// Load measure types from API
async function loadMeasureTypes() {
    const response = await fetch(`${API_BASE_URL}/measure-types`);
    if (!response.ok) {
        throw new Error('Failed to load measure types');
    }
    measureTypes = await response.json();
}

// Render category tabs
function renderCategoryTabs() {
    const allTabHTML = `
        <div class="category-tab ${!selectedCategory ? 'active' : ''}" onclick="selectCategory(null)">
            All Categories
        </div>
    `;
    
    const categoryTabsHTML = categories.map(category => {
        return `
            <div class="category-tab ${selectedCategory && selectedCategory.product_category_id === category.product_category_id ? 'active' : ''}" onclick="selectCategory(${category.product_category_id})">
                ${category.name}
            </div>
        `;
    }).join('');
    
    categoryTabs.innerHTML = allTabHTML + categoryTabsHTML;
}

// Render products table
function renderProductsTable() {
    const filteredProducts = selectedCategory 
        ? products.filter(p => p.product_category_id === selectedCategory.product_category_id)
        : products;
    
    if (filteredProducts.length === 0) {
        productsTableBody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 2rem; color: #666;">
                    No products found in this category.
                </td>
            </tr>
        `;
        return;
    }
    
    const productsHTML = filteredProducts.map(product => {
        const category = categories.find(c => c.product_category_id === product.product_category_id);
        return `
            <tr class="product-row" data-product-id="${product.product_id}">
                <td class="clickable" onclick="editProduct(${product.product_id})">
                    <div class="product-name">${product.name}</div>
                </td>
            </tr>
        `;
    }).join('');
    
    productsTableBody.innerHTML = productsHTML;
}

// Select category
function selectCategory(categoryId) {
    selectedCategory = categoryId ? categories.find(c => c.product_category_id === categoryId) : null;
    renderCategoryTabs();
    renderProductsTable();
}

// View product variables
function viewProductVariables(productId) {
    currentProduct = products.find(p => p.product_id === productId);
    if (!currentProduct) return;
    
    document.getElementById('variablesProductName').textContent = currentProduct.name;
    renderVariablesList();
    document.getElementById('variablesModal').style.display = 'block';
}

// Render variables list
function renderVariablesList() {
    if (!currentProduct) return;
    
    const variablesHTML = currentProduct.variables.map(variable => `
        <div class="variable-item">
            <div class="variable-header">
                <div class="variable-name clickable" onclick="editVariable(${variable.product_variable_id})">${variable.name}</div>
                <div class="variable-actions">
                    <button class="btn btn-sm btn-secondary" onclick="viewVariableOptions(${variable.product_variable_id})">
                        <span class="btn-icon">👁️</span>
                        View Options
                    </button>
                    <button class="delete-btn" onclick="deleteVariable(${currentProduct.product_id}, ${variable.product_variable_id}); event.stopPropagation()" title="Delete Variable">×</button>
                </div>
            </div>
            <div class="variable-details">
                <span>Base: $${variable.base_cost.toFixed(2)}</span>
                <span>Multiplier: $${variable.multiplier_cost.toFixed(2)}</span>
                <span class="variable-type">${variable.data_type}</span>
                <span>Options: ${variable.options.length}</span>
            </div>
        </div>
    `).join('');
    
    document.getElementById('variablesList').innerHTML = variablesHTML || '<p>No variables found for this product.</p>';
}

// View variable options
function viewVariableOptions(variableId) {
    if (!currentProduct) return;
    
    currentVariable = currentProduct.variables.find(v => v.product_variable_id === variableId);
    if (!currentVariable) return;
    
    document.getElementById('optionsVariableName').textContent = currentVariable.name;
    renderOptionsList();
    document.getElementById('optionsModal').style.display = 'block';
}

// Render options list
function renderOptionsList() {
    if (!currentVariable) return;
    
    const optionsHTML = currentVariable.options.map(option => `
        <div class="option-item">
            <div class="option-info clickable" onclick="editOption(${option.variable_option_id})">
                <div class="option-name">${option.name}</div>
                <div class="option-costs">
                    Base: $${option.base_cost.toFixed(2)} | Multiplier: $${option.multiplier_cost.toFixed(2)}
                </div>
            </div>
            <div class="option-actions">
                <button class="delete-btn" onclick="deleteOption(${option.variable_option_id}); event.stopPropagation()" title="Delete Option">×</button>
            </div>
        </div>
    `).join('');
    
    document.getElementById('optionsList').innerHTML = optionsHTML || '<p>No options found for this variable.</p>';
}

// Modal functions
function showAddCategoryModal() {
    document.getElementById('addCategoryModal').style.display = 'block';
}

function hideAddCategoryModal() {
    document.getElementById('addCategoryModal').style.display = 'none';
}

function showAddProductModal() {
    document.getElementById('productModalTitle').textContent = 'Add New Product';
    document.getElementById('productSubmitBtn').textContent = 'Add Product';
    document.getElementById('productId').value = '';
    document.getElementById('productForm').reset();
    
    // Hide delete button for new products
    document.getElementById('deleteProductBtn').style.display = 'none';
    
    // Reset category selection
    document.getElementById('productCategory').value = '';
    document.getElementById('categoryDisplay').textContent = 'Select Category';
    
    // Reset measure type selection
    document.getElementById('productMeasureType').value = '';
    document.getElementById('measureTypeDisplay').textContent = 'Select Measure Type';
    
    // Clear product variables list for new product
    document.getElementById('productVariablesList').innerHTML = '<p class="no-variables">No variables yet. Variables will be added after creating the product.</p>';
    
    document.getElementById('productModal').style.display = 'block';
}

function hideProductModal() {
    document.getElementById('productModal').style.display = 'none';
}

// Editable title functions
function toggleTitleEdit() {
    const titleElement = document.getElementById('productModalTitle');
    const inputElement = document.getElementById('productTitleInput');
    const editBtn = document.getElementById('editTitleBtn');
    
    // Hide the title and edit button, show the input
    titleElement.style.display = 'none';
    editBtn.style.display = 'none';
    inputElement.style.display = 'block';
    
    // Set the input value to the current title text
    inputElement.value = titleElement.textContent;
    
    // Focus and select the input text
    inputElement.focus();
    inputElement.select();
}

function saveTitleEdit() {
    const titleElement = document.getElementById('productModalTitle');
    const inputElement = document.getElementById('productTitleInput');
    const editBtn = document.getElementById('editTitleBtn');
    
    // Update the title text
    titleElement.textContent = inputElement.value;
    
    // Hide the input and show the title and edit button
    inputElement.style.display = 'none';
    titleElement.style.display = 'block';
    editBtn.style.display = 'block';
}

function handleTitleKeypress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        saveTitleEdit();
    } else if (event.key === 'Escape') {
        event.preventDefault();
        // Cancel editing and restore original title
        const titleElement = document.getElementById('productModalTitle');
        const inputElement = document.getElementById('productTitleInput');
        const editBtn = document.getElementById('editTitleBtn');
        
        inputElement.style.display = 'none';
        titleElement.style.display = 'block';
        editBtn.style.display = 'block';
    }
}

// Category dropdown functions
function toggleCategoryDropdown() {
    const dropdown = document.getElementById('categoryDropdown');
    const header = document.querySelector('.category-header');
    const container = document.querySelector('.category-container');
    
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
        header.classList.add('open');
        container.classList.add('dropdown-open');
    } else {
        dropdown.style.display = 'none';
        header.classList.remove('open');
        container.classList.remove('dropdown-open');
    }
}

function selectCategoryFromDropdown(categoryId, categoryName) {
    const categoryDisplay = document.getElementById('categoryDisplay');
    const productCategory = document.getElementById('productCategory');
    const dropdown = document.getElementById('categoryDropdown');
    const header = document.querySelector('.category-header');
    const container = document.querySelector('.category-container');
    
    // Update display and hidden input
    categoryDisplay.textContent = categoryName;
    productCategory.value = categoryId;
    
    // Close dropdown
    dropdown.style.display = 'none';
    header.classList.remove('open');
    container.classList.remove('dropdown-open');
    
    // Update selected state in dropdown options
    const options = dropdown.querySelectorAll('.category-dropdown-option');
    options.forEach(option => {
        option.classList.remove('selected');
        if (option.dataset.categoryId == categoryId) {
            option.classList.add('selected');
        }
    });
}

function populateCategoryDropdown() {
    const dropdown = document.getElementById('categoryDropdown');
    if (!dropdown) return;
    
    dropdown.innerHTML = '';
    
    categories.forEach(category => {
        const option = document.createElement('div');
        option.className = 'category-dropdown-option';
        option.textContent = category.name;
        option.dataset.categoryId = category.product_category_id;
        option.onclick = () => selectCategoryFromDropdown(category.product_category_id, category.name);
        dropdown.appendChild(option);
    });
}

// Measure type dropdown functions
function toggleMeasureTypeDropdown() {
    const dropdown = document.getElementById('measureTypeDropdown');
    const header = document.querySelector('.measure-type-header');
    const container = document.querySelector('.measure-type-container');
    
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';
        header.classList.add('open');
        container.classList.add('dropdown-open');
    } else {
        dropdown.style.display = 'none';
        header.classList.remove('open');
        container.classList.remove('dropdown-open');
    }
}

function selectMeasureTypeFromDropdown(measureTypeId, measureTypeName) {
    const measureTypeDisplay = document.getElementById('measureTypeDisplay');
    const productMeasureType = document.getElementById('productMeasureType');
    const dropdown = document.getElementById('measureTypeDropdown');
    const header = document.querySelector('.measure-type-header');
    const container = document.querySelector('.measure-type-container');
    
    // Update display and hidden input
    measureTypeDisplay.textContent = measureTypeName;
    productMeasureType.value = measureTypeId;
    
    // Close dropdown
    dropdown.style.display = 'none';
    header.classList.remove('open');
    container.classList.remove('dropdown-open');
    
    // Update selected state in dropdown options
    const options = dropdown.querySelectorAll('.measure-type-dropdown-option');
    options.forEach(option => {
        option.classList.remove('selected');
        if (option.dataset.measureTypeId == measureTypeId) {
            option.classList.add('selected');
        }
    });
}

function populateMeasureTypeDropdown() {
    const dropdown = document.getElementById('measureTypeDropdown');
    if (!dropdown) return;
    
    dropdown.innerHTML = '';
    
    measureTypes.forEach(measureType => {
        const option = document.createElement('div');
        option.className = 'measure-type-dropdown-option';
        option.textContent = measureType.measure_type;
        option.dataset.measureTypeId = measureType.measure_type_id;
        option.onclick = () => selectMeasureTypeFromDropdown(measureType.measure_type_id, measureType.measure_type);
        dropdown.appendChild(option);
    });
}

// Populate product variables list in the product modal
function populateProductVariablesList(variables) {
    const variablesContent = document.querySelector('#productVariablesList .product-variables-content');
    
    if (!variables || variables.length === 0) {
        variablesContent.innerHTML = `
            <p class="no-variables">No variables defined for this product.</p>
            <div class="add-variable-container">
                <button type="button" class="add-variable-btn" onclick="addVariable()">+ Add Variable</button>
            </div>
        `;
        return;
    }
    
    
    const variablesHTML = variables.map(variable => `
        <div class="product-variable-item">
            <div class="variable-header">
                <span class="variable-dropdown-arrow" id="arrow-${variable.product_variable_id}" onclick="toggleVariableOptions(${variable.product_variable_id})"></span>
                <span class="variable-name" onclick="toggleVariableOptions(${variable.product_variable_id})">${variable.name}</span>
                <button type="button" class="variable-delete-btn" onclick="deleteVariable(currentProduct.product_id, ${variable.product_variable_id}); event.stopPropagation()">-delete</button>
            </div>
            <div class="variable-options-container" id="options-${variable.product_variable_id}">
                <table class="variable-options-table">
                    <thead>
                        <tr>
                            <th>Option Name</th>
                            <th>Base Cost</th>
                            <th>Multiplier Cost</th>
                            <th></th>
                        </tr>
                    </thead>
                            <tbody>
                                ${variable.options ? variable.options.map(option => `
                                    <tr>
                                        <td>${option.name}</td>
                                        <td>$${option.base_cost ? option.base_cost.toFixed(2) : '0.00'}</td>
                                        <td>$${option.multiplier_cost ? option.multiplier_cost.toFixed(2) : '0.00'}</td>
                                        <td>
                                            <button type="button" class="option-edit-btn" onclick="editVariableOption(${option.variable_option_id})">+edit</button>
                                            <button type="button" class="option-delete-btn" onclick="deleteVariableOption(${option.variable_option_id})">-delete</button>
                                        </td>
                                    </tr>
                                `).join('') : ''}
                            </tbody>
                </table>
                <button type="button" class="add-option-btn" onclick="addVariableOption(${variable.product_variable_id})">+ add option</button>
            </div>
        </div>
    `).join('');
    
    variablesContent.innerHTML = variablesHTML + `
        <div class="add-variable-container">
            <button type="button" class="add-variable-btn" onclick="addVariable()">+ Add Variable</button>
        </div>
    `;
}

// Toggle variable options visibility
function toggleVariableOptions(variableId) {
    const optionsContainer = document.getElementById(`options-${variableId}`);
    const arrow = document.getElementById(`arrow-${variableId}`);
    
    if (optionsContainer.classList.contains('open')) {
        optionsContainer.classList.remove('open');
        arrow.classList.remove('open');
    } else {
        optionsContainer.classList.add('open');
        arrow.classList.add('open');
    }
}

// Edit variable option
function editVariableOption(optionId) {
    // Find the option row
    const optionRow = document.querySelector(`button[onclick="editVariableOption(${optionId})"]`).closest('tr');
    if (!optionRow) return;
    
    // Get current values
    const nameCell = optionRow.cells[0];
    const baseCostCell = optionRow.cells[1];
    const multiplierCostCell = optionRow.cells[2];
    const actionsCell = optionRow.cells[3];
    
    const currentName = nameCell.textContent.trim();
    const currentBaseCost = baseCostCell.textContent.replace('$', '').trim();
    const currentMultiplierCost = multiplierCostCell.textContent.replace('$', '').trim();
    
    // Replace cells with input fields
    nameCell.innerHTML = `<input type="text" id="edit-option-name-${optionId}" value="${currentName}" class="option-input">`;
    baseCostCell.innerHTML = `<input type="number" id="edit-option-base-cost-${optionId}" value="${currentBaseCost}" step="0.01" class="option-input">`;
    multiplierCostCell.innerHTML = `<input type="number" id="edit-option-multiplier-cost-${optionId}" value="${currentMultiplierCost}" step="0.01" class="option-input">`;
    actionsCell.innerHTML = `
        <button type="button" class="save-option-btn" onclick="saveEditedOption(${optionId})">Save</button>
        <button type="button" class="cancel-option-btn" onclick="cancelEditOption(${optionId})">Cancel</button>
    `;
    
    // Focus on the name input
    document.getElementById(`edit-option-name-${optionId}`).focus();
}

function saveEditedOption(optionId) {
    const name = document.getElementById(`edit-option-name-${optionId}`).value.trim();
    const baseCost = parseFloat(document.getElementById(`edit-option-base-cost-${optionId}`).value) || 0;
    const multiplierCost = parseFloat(document.getElementById(`edit-option-multiplier-cost-${optionId}`).value) || 0;
    
    if (!name) {
        alert('Please enter an option name');
        return;
    }
    
    // Store which variables are currently expanded
    const expandedVariables = [];
    document.querySelectorAll('.variable-options-container.open').forEach(container => {
        const variableId = container.id.replace('options-', '');
        expandedVariables.push(parseInt(variableId));
    });
    
    // Update the option via API
    fetch(`${API_BASE_URL}/options/${optionId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            base_cost: baseCost,
            multiplier_cost: multiplierCost
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error updating option: ' + data.error);
            return;
        }
        
        // Reload the product variables to show updated data
        const productId = currentProduct ? currentProduct.product_id : null;
        if (productId) {
            loadProductVariablesWithExpandedState(productId, expandedVariables);
        }
        
        showNotification('Option updated successfully!', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error updating option: ' + error.message);
    });
}

function cancelEditOption(optionId) {
    // Store which variables are currently expanded
    const expandedVariables = [];
    document.querySelectorAll('.variable-options-container.open').forEach(container => {
        const variableId = container.id.replace('options-', '');
        expandedVariables.push(parseInt(variableId));
    });
    
    // Reload the product variables to restore original values
    const productId = currentProduct ? currentProduct.product_id : null;
    if (productId) {
        loadProductVariablesWithExpandedState(productId, expandedVariables);
    }
}

// Add new variable
function addVariable() {
    const productId = currentProduct ? currentProduct.product_id : null;
    if (!productId) {
        alert('No product selected');
        return;
    }
    
    // Hide the add button
    const addButton = document.querySelector('.add-variable-btn');
    if (addButton) {
        addButton.style.display = 'none';
    }
    
    // Create inline form for adding new variable
    const addVariableContainer = document.querySelector('.add-variable-container');
    const formHTML = `
        <div class="add-variable-form" id="add-variable-form">
            <div class="variable-form-row">
                <input type="text" id="new-variable-name" placeholder="Variable Name" class="variable-input">
                <button type="button" class="save-variable-btn" onclick="saveVariable()">Save</button>
                <button type="button" class="cancel-variable-btn" onclick="cancelAddVariable()">Cancel</button>
            </div>
        </div>
    `;
    
    addVariableContainer.insertAdjacentHTML('beforeend', formHTML);
    
    // Focus on the input
    document.getElementById('new-variable-name').focus();
}

function saveVariable() {
    const productId = currentProduct ? currentProduct.product_id : null;
    if (!productId) {
        alert('No product selected');
        return;
    }
    
    const variableName = document.getElementById('new-variable-name').value.trim();
    if (!variableName) {
        alert('Please enter a variable name');
        return;
    }
    
    // Create the new variable via API
    fetch(`${API_BASE_URL}/variables`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: variableName,
            data_type: 'select',
            product_id: productId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error creating variable: ' + data.error);
            return;
        }
        
        // Remove the form
        cancelAddVariable();
        
        // Reload the product variables to show the new variable
        loadProductVariables(productId);
        
        showNotification('Variable added successfully!', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating variable: ' + error.message);
    });
}

function cancelAddVariable() {
    // Remove the form
    const form = document.getElementById('add-variable-form');
    if (form) {
        form.remove();
    }
    
    // Show the add button again
    const addButton = document.querySelector('.add-variable-btn');
    if (addButton) {
        addButton.style.display = 'block';
    }
}

// Delete product
function deleteProduct() {
    const productId = document.getElementById('productId').value;
    if (!productId) {
        alert('No product selected for deletion');
        return;
    }
    
    const productName = document.getElementById('productModalTitle').textContent;
    
    if (confirm(`Are you sure you want to delete "${productName}"? This action cannot be undone.`)) {
        fetch(`${API_BASE_URL}/products/${productId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete product');
            }
            return response.json();
        })
        .then(data => {
            showNotification('Product deleted successfully!', 'success');
            hideProductModal();
            loadProducts(); // Reload the products list
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting product: ' + error.message);
        });
    }
}

// Add new variable option
function addVariableOption(variableId) {
    // Create inline form for adding new option
    const optionsContainer = document.getElementById(`options-${variableId}`);
    const addButton = optionsContainer.querySelector('.add-option-btn');
    
    // Create form HTML
    const formHTML = `
        <div class="add-option-form" id="add-option-form-${variableId}">
            <table class="variable-options-table">
                <tbody>
                    <tr class="add-option-row">
                        <td><input type="text" id="option-name-${variableId}" placeholder="Option Name" class="option-input"></td>
                        <td><input type="number" id="option-base-cost-${variableId}" placeholder="Base Cost" step="0.01" class="option-input"></td>
                        <td><input type="number" id="option-multiplier-cost-${variableId}" placeholder="Multiplier Cost" step="0.01" class="option-input"></td>
                        <td>
                            <button type="button" class="save-option-btn" onclick="saveVariableOption(${variableId})">Save</button>
                            <button type="button" class="cancel-option-btn" onclick="cancelAddOption(${variableId})">Cancel</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
    
    // Insert form before the add button
    addButton.insertAdjacentHTML('beforebegin', formHTML);
    
    // Hide the add button
    addButton.style.display = 'none';
    
    // Focus on the name input
    document.getElementById(`option-name-${variableId}`).focus();
}

function saveVariableOption(variableId) {
    const name = document.getElementById(`option-name-${variableId}`).value.trim();
    const baseCost = parseFloat(document.getElementById(`option-base-cost-${variableId}`).value) || 0;
    const multiplierCost = parseFloat(document.getElementById(`option-multiplier-cost-${variableId}`).value) || 0;
    
    if (!name) {
        alert('Please enter an option name');
        return;
    }
    
    // Create the new option via API
    fetch(`${API_BASE_URL}/options`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            base_cost: baseCost,
            multiplier_cost: multiplierCost,
            product_variable_id: variableId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error creating option: ' + data.error);
            return;
        }
        
        // Remove the form
        cancelAddOption(variableId);
        
        // Reload the product variables to show the new option
        const productId = currentProduct ? currentProduct.product_id : null;
        if (productId) {
            loadProductVariables(productId);
        }
        
        showNotification('Option added successfully!', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error creating option: ' + error.message);
    });
}

function cancelAddOption(variableId) {
    // Remove the form
    const form = document.getElementById(`add-option-form-${variableId}`);
    if (form) {
        form.remove();
    }
    
    // Show the add button again
    const addButton = document.querySelector(`#options-${variableId} .add-option-btn`);
    if (addButton) {
        addButton.style.display = 'block';
    }
}

// Load product variables for a specific product
async function loadProductVariables(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}/variables`);
        if (!response.ok) {
            throw new Error('Failed to load product variables');
        }
        const variables = await response.json();
        
        // Update the current product's variables
        if (currentProduct) {
            currentProduct.variables = variables;
        }
        
        // Refresh the variables display
        populateProductVariablesList(variables);
    } catch (error) {
        console.error('Error loading product variables:', error);
        showNotification('Error loading product variables', 'error');
    }
}

// Load product variables and restore expanded state
async function loadProductVariablesWithExpandedState(productId, expandedVariables = []) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}/variables`);
        if (!response.ok) {
            throw new Error('Failed to load product variables');
        }
        const variables = await response.json();
        
        // Update the current product's variables
        if (currentProduct) {
            currentProduct.variables = variables;
        }
        
        
        // Refresh the variables display
        populateProductVariablesList(variables);
        
        // Restore expanded state
        setTimeout(() => {
            expandedVariables.forEach(variableId => {
                const optionsContainer = document.getElementById(`options-${variableId}`);
                const arrow = document.getElementById(`arrow-${variableId}`);
                if (optionsContainer && arrow) {
                    optionsContainer.classList.add('open');
                    arrow.classList.add('open');
                }
            });
        }, 100);
    } catch (error) {
        console.error('Error loading product variables:', error);
        showNotification('Error loading product variables', 'error');
    }
}

function editProduct(productId) {
    const product = products.find(p => p.product_id === productId);
    if (!product) return;
    
    // Set current product for add option functionality
    currentProduct = product;
    
    document.getElementById('productModalTitle').textContent = product.name;
    document.getElementById('productSubmitBtn').textContent = 'Update Product';
    document.getElementById('productId').value = product.product_id;
    
    // Show delete button for existing products
    document.getElementById('deleteProductBtn').style.display = 'block';
    
    // Set category display text and hidden input
    const categoryDisplay = document.getElementById('categoryDisplay');
    const productCategory = document.getElementById('productCategory');
    const selectedCategory = categories.find(cat => cat.product_category_id === product.product_category_id);
    categoryDisplay.textContent = selectedCategory ? selectedCategory.name : 'Select Category';
    productCategory.value = product.product_category_id;
    
    // Set measure type display text and hidden input
    const measureTypeDisplay = document.getElementById('measureTypeDisplay');
    const productMeasureType = document.getElementById('productMeasureType');
    const selectedMeasureType = measureTypes.find(mt => mt.measure_type_id === product.measure_type_id);
    measureTypeDisplay.textContent = selectedMeasureType ? selectedMeasureType.measure_type : 'Select Measure Type';
    productMeasureType.value = product.measure_type_id || '';
    
    // Populate product variables list
    populateProductVariablesList(product.variables || []);
    
    document.getElementById('productModal').style.display = 'block';
}

function hideVariablesModal() {
    document.getElementById('variablesModal').style.display = 'none';
    currentProduct = null;
}

function showAddVariableModal() {
    if (!currentProduct) return;
    
    document.getElementById('variableModalTitle').textContent = 'Add New Variable';
    document.getElementById('variableSubmitBtn').textContent = 'Add Variable';
    document.getElementById('variableId').value = '';
    document.getElementById('variableProductId').value = currentProduct.product_id;
    document.getElementById('variableForm').reset();
    
    document.getElementById('variableModal').style.display = 'block';
}

function hideVariableModal() {
    document.getElementById('variableModal').style.display = 'none';
}

function editVariable(variableId) {
    if (!currentProduct) return;
    
    const variable = currentProduct.variables.find(v => v.product_variable_id === variableId);
    if (!variable) return;
    
    document.getElementById('variableModalTitle').textContent = 'Edit Variable';
    document.getElementById('variableSubmitBtn').textContent = 'Update Variable';
    document.getElementById('variableId').value = variable.product_variable_id;
    document.getElementById('variableProductId').value = currentProduct.product_id;
    document.getElementById('variableName').value = variable.name;
    document.getElementById('variableBaseCost').value = variable.base_cost;
    document.getElementById('variableMultiplierCost').value = variable.multiplier_cost;
    document.getElementById('variableDataType').value = variable.data_type;
    
    document.getElementById('variableModal').style.display = 'block';
}

function hideOptionsModal() {
    document.getElementById('optionsModal').style.display = 'none';
    currentVariable = null;
}

function showAddOptionModal() {
    if (!currentVariable) return;
    
    document.getElementById('optionModalTitle').textContent = 'Add New Option';
    document.getElementById('optionSubmitBtn').textContent = 'Add Option';
    document.getElementById('optionId').value = '';
    document.getElementById('optionVariableId').value = currentVariable.product_variable_id;
    document.getElementById('optionForm').reset();
    
    document.getElementById('optionModal').style.display = 'block';
}

function hideOptionModal() {
    document.getElementById('optionModal').style.display = 'none';
}

function editOption(optionId) {
    if (!currentVariable) return;
    
    const option = currentVariable.options.find(o => o.variable_option_id === optionId);
    if (!option) return;
    
    document.getElementById('optionModalTitle').textContent = 'Edit Option';
    document.getElementById('optionSubmitBtn').textContent = 'Update Option';
    document.getElementById('optionId').value = option.variable_option_id;
    document.getElementById('optionVariableId').value = currentVariable.product_variable_id;
    document.getElementById('optionName').value = option.name;
    document.getElementById('optionBaseCost').value = option.base_cost;
    document.getElementById('optionMultiplierCost').value = option.multiplier_cost;
    
    document.getElementById('optionModal').style.display = 'block';
}

// Delete functions
async function deleteVariableOption(optionId) {
    if (confirm('Are you sure you want to delete this variable option? This action cannot be undone.')) {
        try {
            const response = await fetch(`${API_BASE_URL}/options/${optionId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Reload the product variables to refresh the display
                if (currentProduct) {
                    await loadProductVariablesWithExpandedState(currentProduct.product_id);
                }
                showNotification('Variable option deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete variable option', 'error');
            }
        } catch (error) {
            console.error('Error deleting variable option:', error);
            showNotification('Error deleting variable option', 'error');
        }
    }
}


async function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product? This will also delete all its variables and options.')) {
        try {
            const response = await fetch(`${API_BASE_URL}/products/${productId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                await loadProducts();
                renderCategoryTabs();
                renderProductsTable();
                showNotification('Product deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete product', 'error');
            }
        } catch (error) {
            console.error('Error deleting product:', error);
            showNotification('Error deleting product', 'error');
        }
    }
}

async function deleteVariable(productId, variableId) {
    if (confirm('Are you sure you want to delete this variable?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/variables/${variableId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                await loadProducts();
                renderVariablesList();
                showNotification('Variable deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete variable', 'error');
            }
        } catch (error) {
            console.error('Error deleting variable:', error);
            showNotification('Error deleting variable', 'error');
        }
    }
}

async function deleteOption(optionId) {
    if (confirm('Are you sure you want to delete this option?')) {
        try {
            const response = await fetch(`${API_BASE_URL}/options/${optionId}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                await loadProducts();
                renderOptionsList();
                showNotification('Option deleted successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to delete option', 'error');
            }
        } catch (error) {
            console.error('Error deleting option:', error);
            showNotification('Error deleting option', 'error');
        }
    }
}

// Setup event listeners
function setupEventListeners() {
    // Category form submission
    document.getElementById('addCategoryForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const categoryData = {
            name: formData.get('name')
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/categories`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(categoryData)
            });
            
            if (response.ok) {
                await loadCategories();
                renderCategoryTabs();
                populateCategoryDropdown(); // Repopulate dropdown with new category
                hideAddCategoryModal();
                this.reset();
                showNotification('Category added successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to add category', 'error');
            }
        } catch (error) {
            console.error('Error adding category:', error);
            showNotification('Error adding category', 'error');
        }
    });
    
    // Category dropdown will be populated after data is loaded
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const categoryContainer = document.querySelector('.category-container');
        if (categoryContainer && !categoryContainer.contains(event.target)) {
            const dropdown = document.getElementById('categoryDropdown');
            const header = document.querySelector('.category-header');
            if (dropdown && dropdown.style.display === 'block') {
                dropdown.style.display = 'none';
                header.classList.remove('open');
                categoryContainer.classList.remove('dropdown-open');
            }
        }
        
        const measureTypeContainer = document.querySelector('.measure-type-container');
        if (measureTypeContainer && !measureTypeContainer.contains(event.target)) {
            const dropdown = document.getElementById('measureTypeDropdown');
            const header = document.querySelector('.measure-type-header');
            if (dropdown && dropdown.style.display === 'block') {
                dropdown.style.display = 'none';
                header.classList.remove('open');
                measureTypeContainer.classList.remove('dropdown-open');
            }
        }
    });
    
    // Product form submission
    document.getElementById('productForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const productId = formData.get('product_id');
        const categoryId = document.getElementById('productCategory').value;
        if (!categoryId) {
            alert('Please select a category for the product');
            return;
        }
        
        const measureTypeId = document.getElementById('productMeasureType').value;
        const productData = {
            name: document.getElementById('productModalTitle').textContent,
            product_category_id: parseInt(categoryId),
            measure_type_id: measureTypeId ? parseInt(measureTypeId) : null
        };
        
        try {
            const url = productId ? `${API_BASE_URL}/products/${productId}` : `${API_BASE_URL}/products`;
            const method = productId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(productData)
            });
            
            if (response.ok) {
                await loadProducts();
                renderCategoryTabs();
                renderProductsTable();
                hideProductModal();
                this.reset();
                showNotification(productId ? 'Product updated successfully!' : 'Product added successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to save product', 'error');
            }
        } catch (error) {
            console.error('Error saving product:', error);
            showNotification('Error saving product', 'error');
        }
    });
    
    // Variable form submission
    document.getElementById('variableForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const variableId = formData.get('product_variable_id');
        const variableData = {
            name: formData.get('name'),
            base_cost: parseFloat(formData.get('base_cost')),
            multiplier_cost: parseFloat(formData.get('multiplier_cost')),
            data_type: formData.get('data_type'),
            product_id: parseInt(formData.get('product_id'))
        };
        
        try {
            const url = variableId ? `${API_BASE_URL}/variables/${variableId}` : `${API_BASE_URL}/variables`;
            const method = variableId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(variableData)
            });
            
            if (response.ok) {
                await loadProducts();
                renderVariablesList();
                hideVariableModal();
                this.reset();
                showNotification(variableId ? 'Variable updated successfully!' : 'Variable added successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to save variable', 'error');
            }
        } catch (error) {
            console.error('Error saving variable:', error);
            showNotification('Error saving variable', 'error');
        }
    });
    
    // Option form submission
    document.getElementById('optionForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const optionId = formData.get('variable_option_id');
        const optionData = {
            name: formData.get('name'),
            base_cost: parseFloat(formData.get('base_cost')),
            multiplier_cost: parseFloat(formData.get('multiplier_cost')),
            product_variable_id: parseInt(formData.get('product_variable_id'))
        };
        
        try {
            const url = optionId ? `${API_BASE_URL}/options/${optionId}` : `${API_BASE_URL}/options`;
            const method = optionId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(optionData)
            });
            
            if (response.ok) {
                await loadProducts();
                renderOptionsList();
                hideOptionModal();
                this.reset();
                showNotification(optionId ? 'Option updated successfully!' : 'Option added successfully!', 'success');
            } else {
                const error = await response.json();
                showNotification(error.error || 'Failed to save option', 'error');
            }
        } catch (error) {
            console.error('Error saving option:', error);
            showNotification('Error saving option', 'error');
        }
    });
    
    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
        }
    });
}

// Notification function
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    let backgroundColor;
    switch (type) {
        case 'success':
            backgroundColor = '#28a745';
            break;
        case 'error':
            backgroundColor = '#dc3545';
            break;
        default:
            backgroundColor = '#17a2b8';
    }
    
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
        background: ${backgroundColor};
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

