// Quote Management JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// PDF Generation
function generateQuotePDF() {
    console.log('PDF generation started');
    
    // Check if we have a current quote ID
    if (!currentQuoteId) {
        alert('No quote selected. Please save the quote first.');
        return;
    }
    
    try {
        // Generate PDF using server-side endpoint
        const pdfUrl = `${API_BASE_URL}/quotes/${currentQuoteId}/pdf`;
        console.log('Generating PDF from:', pdfUrl);
        
        // Create a temporary link to download the PDF
        const link = document.createElement('a');
        link.href = pdfUrl;
        link.download = `quote_${currentQuoteId}.pdf`;
        link.target = '_blank';
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log('PDF download initiated');
        showNotification('PDF generated successfully', 'success');
        
    } catch (error) {
        console.error('Error generating PDF:', error);
        showNotification('Error generating PDF', 'error');
    }
}

// Global variables
let currentJobId = null;
let currentQuoteId = null;  // Track if we're editing an existing quote
let currentJob = null;
let categories = [];
let products = [];
let productVariables = {};
let items = [];

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Quote page initialized');
    
    // Load job data if jobId is provided
    const urlParams = new URLSearchParams(window.location.search);
    const jobId = urlParams.get('jobId');
    
    if (jobId) {
        currentJobId = parseInt(jobId);
        loadJobData();
    } else {
        showNotification('No job ID provided', 'error');
        setTimeout(() => goBack(), 2000);
    }
});

// Load job data
async function loadJobData() {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs`);
        if (response.ok) {
            const jobs = await response.json();
            currentJob = jobs.find(job => job.job_id == currentJobId);
            
            if (currentJob) {
                document.getElementById('jobNumber').textContent = `#${currentJob.job_id}`;
                document.getElementById('jobReference').textContent = currentJob.reference;
                document.getElementById('projectName').textContent = currentJob.project_name || 'Unknown Project';
                
                // Load quote number
                loadQuoteNumber();
                
                // Load categories and products
                await loadCategories();
                await loadProducts();
                
                showNotification('Job data loaded successfully', 'success');
            } else {
                showNotification('Job not found', 'error');
            }
        } else {
            showNotification('Error loading job data', 'error');
        }
    } catch (error) {
        console.error('Error loading job data:', error);
        showNotification('Error loading job data', 'error');
    }
}

// Load job data for existing quote (without loading quote number)
async function loadJobDataForExistingQuote() {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs`);
        if (response.ok) {
            const jobs = await response.json();
            currentJob = jobs.find(job => job.job_id == currentJobId);
            
            if (currentJob) {
                document.getElementById('jobNumber').textContent = `#${currentJob.job_id}`;
                document.getElementById('jobReference').textContent = currentJob.reference;
                document.getElementById('projectName').textContent = currentJob.project_name || 'Unknown Project';
                
                // Load categories and products
                await loadCategories();
                await loadProducts();
                
                showNotification('Job data loaded successfully', 'success');
            } else {
                showNotification('Job not found', 'error');
            }
        } else {
            showNotification('Error loading job data', 'error');
        }
    } catch (error) {
        console.error('Error loading job data:', error);
        showNotification('Error loading job data', 'error');
    }
}

// Load quote number for the current job
async function loadQuoteNumber(jobId) {
    try {
        const response = await fetch(`${API_BASE_URL}/quotes?job_id=${jobId}`);
        if (response.ok) {
            const quotes = await response.json();
            const nextQuoteNumber = quotes.length + 1;
            const quoteNumber = `${currentJobId}-${nextQuoteNumber.toString().padStart(3, '0')}`;
            document.getElementById('quoteNumber').textContent = quoteNumber;
        } else {
            console.error('Error loading quotes for quote number generation');
        }
    } catch (error) {
        console.error('Error loading quote number:', error);
    }
}

// Load product categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        if (response.ok) {
            categories = await response.json();
            console.log('Categories loaded:', categories.length);
        } else {
            console.error('Error loading categories');
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load products for a category
async function loadProducts(categoryId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (response.ok) {
            products = await response.json();
            console.log('Products loaded:', products.length);
        } else {
            console.error('Error loading products');
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Add new item
function addItem() {
    itemCounter++;
    const itemId = `item_${itemCounter}`;
    
    const itemsTableBody = document.getElementById('itemsTableBody');
    if (!itemsTableBody) {
        console.error('Items table body not found');
        return;
    }
    
    const newRow = document.createElement('tr');
    newRow.className = 'item-row';
    newRow.id = itemId;
    
    newRow.innerHTML = `
        <td><input type="text" class="item-reference" placeholder="Reference"></td>
        <td>
            <select class="product-select" onchange="loadProductVariables(this)">
                <option value="">Select Product</option>
                ${products.map(product => `<option value="${product.product_id}">${product.name}</option>`).join('')}
            </select>
        </td>
        <td><input type="number" class="quantity" value="1" min="1" onchange="calculateItemCost(this)"></td>
        <td><input type="number" class="length" step="0.01" onchange="calculateItemCost(this)"></td>
        <td><input type="number" class="width" step="0.01" onchange="calculateItemCost(this)"></td>
        <td><input type="number" class="height" step="0.01" onchange="calculateItemCost(this)"></td>
        <td class="item-cost">$0.00</td>
        <td><button type="button" class="btn btn-danger" onclick="removeItem(this)">Remove</button></td>
    `;
    
    itemsTableBody.appendChild(newRow);
    items.push({ id: itemId, row: newRow });
}

// Remove item
function removeItem(button) {
    const itemRow = button.closest('.item-row');
    itemRow.remove();
    
    // Remove from items array
    const itemId = itemRow.id;
    const itemIndex = items.findIndex(item => item.id === itemId);
    if (itemIndex > -1) {
        items.splice(itemIndex, 1);
    }
    
    // Recalculate totals
    calculateTotals();
}

// Calculate item cost
async function calculateItemCost(itemRow) {
    const quantity = parseFloat(itemRow.querySelector('.quantity').value) || 0;
    const length = parseFloat(itemRow.querySelector('.length').value) || 0;
    const width = parseFloat(itemRow.querySelector('.width').value) || 0;
    const height = parseFloat(itemRow.querySelector('.height').value) || 0;
    
    const productSelect = itemRow.querySelector('.product-select');
    const productId = productSelect.value;
    
    if (!productId) {
        itemRow.querySelector('.item-cost').textContent = '$0.00';
        calculateTotals();
        return;
    }
    
    const product = products.find(p => p.product_id == productId);
    if (!product) {
        itemRow.querySelector('.item-cost').textContent = '$0.00';
        calculateTotals();
        return;
    }
    
    // Get measure type
    const measureType = measureTypes.find(mt => mt.measure_type_id == product.measure_type_id);
    if (!measureType) {
        itemRow.querySelector('.item-cost').textContent = '$0.00';
        calculateTotals();
        return;
    }
    
    // Calculate cost based on measure type
    let cost = 0;
    
    if (measureType.measure_type === 'Linear') {
        // For linear products: base cost + (multiplier cost × length × quantity)
        cost = product.base_cost + (product.multiplier_cost * length * quantity);
    } else if (measureType.measure_type === 'Quantity Only') {
        // For quantity-only products: base cost + (multiplier cost × quantity)
        cost = product.base_cost + (product.multiplier_cost * quantity);
    } else if (measureType.measure_type === 'Area') {
        // For area products: base cost + (multiplier cost × width × height × quantity)
        cost = product.base_cost + (product.multiplier_cost * width * height * quantity);
    }
    
    // Apply product variables if any
    const variableSelects = itemRow.querySelectorAll('.variable-select');
    variableSelects.forEach(select => {
        const variableId = select.dataset.variableId;
        const selectedOption = select.value;
        
        if (selectedOption) {
            const variable = productVariables[productId]?.find(v => v.variable_id == variableId);
            if (variable) {
                const option = variable.options.find(o => o.option_id == selectedOption);
                if (option) {
                    cost += option.base_cost;
                    if (measureType.measure_type === 'Linear') {
                        cost += option.multiplier_cost * length * quantity;
                    } else if (measureType.measure_type === 'Quantity Only') {
                        cost += option.multiplier_cost * quantity;
                    } else if (measureType.measure_type === 'Area') {
                        cost += option.multiplier_cost * width * height * quantity;
                    }
                }
            }
        }
    });
    
    itemRow.querySelector('.item-cost').textContent = `$${cost.toFixed(2)}`;
    calculateTotals();
}

// Calculate totals
function calculateTotals() {
    let totalExclGST = 0;
    
    items.forEach(item => {
        const costText = item.row.querySelector('.item-cost').textContent;
        const cost = parseFloat(costText.replace('$', '')) || 0;
        totalExclGST += cost;
    });
    
    const totalInclGST = totalExclGST * 1.1; // 10% GST
    
    document.getElementById('totalExclGST').textContent = `$${totalExclGST.toFixed(2)}`;
    document.getElementById('totalInclGST').textContent = `$${totalInclGST.toFixed(2)}`;
}

// Save quote
async function saveQuote() {
    
    // Collect all items data
    const itemsData = [];
    items.forEach(item => {
        const row = item.row;
        const productSelect = row.querySelector('.product-select');
        const productId = productSelect.value;
        
        if (productId) {
            const itemData = {
                product_id: parseInt(productId),
                reference: row.querySelector('.item-reference').value,
                quantity: parseFloat(row.querySelector('.quantity').value) || 1,
                length: parseFloat(row.querySelector('.length').value) || null,
                width: parseFloat(row.querySelector('.width').value) || null,
                height: parseFloat(row.querySelector('.height').value) || null,
                cost_excl_gst: parseFloat(row.querySelector('.item-cost').textContent.replace('$', '')) || 0,
                cost_incl_gst: parseFloat(row.querySelector('.item-cost').textContent.replace('$', '')) * 1.1 || 0
            };
            itemsData.push(itemData);
        }
    });
    
    // Get totals
    const totalExclGST = parseFloat(document.getElementById('totalExclGST').textContent.replace('$', '').replace(',', '')) || 0;
    const totalInclGST = parseFloat(document.getElementById('totalInclGST').textContent.replace('$', '').replace(',', '')) || 0;
    
    // Prepare quote data
    const quoteData = {
        job_id: currentJobId,
        quote_number: document.getElementById('quoteNumber').textContent,
        cost_excl_gst: totalExclGST,
        cost_incl_gst: totalInclGST,
        items: itemsData
    };
    
    try {
        let response;
        if (currentQuoteId) {
            // Update existing quote
            response = await fetch(`${API_BASE_URL}/quotes/${currentQuoteId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(quoteData)
            });
        } else {
            // Create new quote
            response = await fetch(`${API_BASE_URL}/quotes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(quoteData)
            });
        }
        
        if (response.ok) {
            const result = await response.json();
            console.log('Quote saved:', result);
            
            showNotification('Quote saved successfully!', 'success');
            setTimeout(() => goBack(), 2000);
        } else {
            const error = await response.json();
            console.error('Error saving quote:', error);
            showNotification(error.error || 'Error saving quote', 'error');
        }
    } catch (error) {
        console.error('Error saving quote:', error);
        showNotification('Error saving quote', 'error');
    }
}

// Go back to jobs page
function goBack() {
    window.location.href = 'jobs.html';
}

// Global variables
let currentJobId = null;
let currentQuoteId = null;  // Track if we're editing an existing quote
let currentJob = null;
let categories = [];
let products = [];
let productVariables = {};
let items = [];
let itemCounter = 0;
let currentSelectedProduct = null;
let measureTypes = [];

// Helper function to safely set currentSelectedProduct with logging
function setCurrentSelectedProduct(product) {
    console.log('Setting currentSelectedProduct from:', currentSelectedProduct, 'to:', product);
    currentSelectedProduct = product;
}

// Load measure types
async function loadMeasureTypes() {
    try {
        const response = await fetch(`${API_BASE_URL}/measure-types`);
        if (response.ok) {
            measureTypes = await response.json();
            console.log('Measure types loaded:', measureTypes.length);
        } else {
            console.error('Error loading measure types');
        }
    } catch (error) {
        console.error('Error loading measure types:', error);
    }
}

// Load product variables
async function loadProductVariables(productSelect) {
    const productId = productSelect.value;
    if (!productId) {
        // Clear variables if no product selected
        const itemRow = productSelect.closest('.item-row');
        const variablesContainer = itemRow.querySelector('.variables-container');
        if (variablesContainer) {
            variablesContainer.remove();
        }
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/product-variables?product_id=${productId}`);
        if (response.ok) {
            const variables = await response.json();
            productVariables[productId] = variables;
            
            // Add variables to the item row
            const itemRow = productSelect.closest('.item-row');
            let variablesContainer = itemRow.querySelector('.variables-container');
            
            if (variablesContainer) {
                variablesContainer.remove();
            }
            
            if (variables.length > 0) {
                variablesContainer = document.createElement('div');
                variablesContainer.className = 'variables-container';
                variablesContainer.innerHTML = variables.map(variable => `
                    <div class="variable-group">
                        <label>${variable.variable_name}:</label>
                        <select class="variable-select" data-variable-id="${variable.variable_id}" onchange="calculateItemCost(this.closest('.item-row'))">
                            <option value="">Select ${variable.variable_name}</option>
                            ${variable.options.map(option => `<option value="${option.option_id}">${option.option_name}</option>`).join('')}
                        </select>
                    </div>
                `).join('');
                
                // Insert after the product select
                productSelect.parentNode.insertBefore(variablesContainer, productSelect.nextSibling);
            }
        } else {
            console.error('Error loading product variables');
        }
    } catch (error) {
        console.error('Error loading product variables:', error);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
    }
});

// Load job data
async function loadJobData() {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs`);
        if (response.ok) {
            const jobs = await response.json();
            currentJob = jobs.find(job => job.job_id == currentJobId);
            
            if (currentJob) {
                document.getElementById('jobNumber').textContent = `#${currentJob.job_id}`;
                document.getElementById('jobReference').textContent = currentJob.reference;
                document.getElementById('projectName').textContent = currentJob.project_name || 'Unknown';
                
                // Load existing quotes for this job to determine next quote number
                loadQuoteNumber(currentJob.job_id);
            } else {
                showNotification('Job not found', 'error');
                setTimeout(() => goBack(), 2000);
            }
        } else {
            showNotification('Error loading job data', 'error');
        }
    } catch (error) {
        console.error('Error loading job data:', error);
        showNotification('Error loading job data', 'error');
    }
}

// Load job data for existing quote (without loading quote number)
async function loadJobDataForExistingQuote() {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs`);
        if (response.ok) {
            const jobs = await response.json();
            currentJob = jobs.find(job => job.job_id == currentJobId);
            
            if (currentJob) {
                document.getElementById('jobNumber').textContent = `#${currentJob.job_id}`;
                document.getElementById('jobReference').textContent = currentJob.reference;
                document.getElementById('projectName').textContent = currentJob.project_name || 'Unknown';
                
                // Don't load quote number - we're editing an existing quote
            } else {
                showNotification('Job not found', 'error');
                setTimeout(() => goBack(), 2000);
            }
        } else {
            showNotification('Error loading job data', 'error');
        }
    } catch (error) {
        console.error('Error loading job data:', error);
        showNotification('Error loading job data', 'error');
    }
}

// Load quote number for the current job
async function loadQuoteNumber(jobId) {
    try {
        const response = await fetch(`${API_BASE_URL}/quotes?job_id=${jobId}`);
        if (response.ok) {
            const quotes = await response.json();
            const existingQuotes = quotes.filter(quote => quote.job_id == jobId);
            const nextQuoteNumber = existingQuotes.length + 1;
            const quoteNumber = `${jobId}-${nextQuoteNumber.toString().padStart(3, '0')}`;
            
            document.getElementById('quoteNumber').textContent = quoteNumber;
        } else {
            // If no quotes exist yet, show the first quote number
            const quoteNumber = `${jobId}-001`;
            document.getElementById('quoteNumber').textContent = quoteNumber;
        }
    } catch (error) {
        console.error('Error loading quote number:', error);
        // Fallback to first quote number
        const quoteNumber = `${jobId}-001`;
        document.getElementById('quoteNumber').textContent = quoteNumber;
    }
}

// Load existing quote data
async function loadExistingQuote(quoteId) {
    try {
        // Load the quote data
        const quoteResponse = await fetch(`${API_BASE_URL}/quotes/${quoteId}`);
        if (!quoteResponse.ok) {
            throw new Error('Quote not found');
        }
        
        const quote = await quoteResponse.json();
        currentJobId = quote.job_id;
        currentQuoteId = quote.quote_id;  // Set the current quote ID for editing
        
        
        // Load job data (but don't load quote number since we're editing an existing quote)
        await loadJobDataForExistingQuote();
        
        // Set the quote number display
        document.getElementById('quoteNumber').textContent = quote.quote_number;
        
        // Load categories and products
        await loadCategories();
        await loadAllProducts();
        
        // Load quote items
        await loadQuoteItems(quoteId);
        
    } catch (error) {
        console.error('Error loading existing quote:', error);
        showNotification('Error loading quote', 'error');
        setTimeout(() => goBack(), 2000);
    }
}

// Load quote items
async function loadQuoteItems(quoteId) {
    try {
        const response = await fetch(`${API_BASE_URL}/items?quote_id=${quoteId}`);
        if (response.ok) {
            const items = await response.json();
            
            // Clear existing items
            document.getElementById('itemsContainer').innerHTML = '';
            itemsData = [];
            
            // Add each item
            for (const item of items) {
                await addItemFromData(item);
            }
            
            updateTotals();
        }
    } catch (error) {
        console.error('Error loading quote items:', error);
    }
}

// Add item from existing data
async function addItemFromData(itemData) {
    itemCounter++;
    const itemId = `item_${itemCounter}`;
    
    // Clone the template
    const itemElement = itemTemplate.content.cloneNode(true);
    const itemRow = itemElement.querySelector('.item-row');
    itemRow.dataset.itemId = itemId;
    
    // Set item number and reference display
    itemRow.querySelector('.item-number').textContent = `${itemCounter} - `;
    itemRow.querySelector('.item-reference-display').textContent = itemData.reference || 'Enter reference';
    
    // Populate category dropdown
    const categorySelect = itemRow.querySelector('.product-category-select');
    categorySelect.innerHTML = '<option value="">Select Category</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.product_category_id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });
    
    // Add event listeners for cost calculation
    const quantityInput = itemRow.querySelector('.item-quantity');
    const lengthInput = itemRow.querySelector('.item-length');
    const widthInput = itemRow.querySelector('.item-width');
    
    [quantityInput, lengthInput, widthInput].forEach(input => {
        input.addEventListener('input', () => calculateItemCost(itemRow));
    });
    
    // Add event listener for cost excluding GST field only
    const costExclInput = itemRow.querySelector('.item-cost-excl');
    costExclInput.addEventListener('input', () => handleManualCostChange(itemRow, 'excl'));
    
    // Add to container
    itemsContainer.appendChild(itemElement);
    
    // Set the product data
    if (itemData.product_id) {
        // Find the product and set its category
        const product = products.find(p => p.product_id === itemData.product_id);
        if (product) {
            categorySelect.value = product.product_category_id;
            await updateProducts(categorySelect);
            
            const productSelect = itemRow.querySelector('.product-select');
            productSelect.value = itemData.product_id;
            await loadProductVariables(productSelect);
            
            // Load and set the variable options for this item
            await loadItemVariables(itemRow, itemData.item_id);
            
            // Update product name display
            const productNameDisplay = itemRow.querySelector('.item-product-name');
            if (productNameDisplay) {
                productNameDisplay.textContent = `(${product.name})`;
            }
        }
    }
    
    // Set the measurement values
    itemRow.querySelector('.item-length').value = itemData.length || '';
    itemRow.querySelector('.item-width').value = itemData.width || '';
    itemRow.querySelector('.item-quantity').value = itemData.quantity || 1;
    itemRow.querySelector('.item-notes').value = itemData.notes || '';
    itemRow.querySelector('.item-cost-excl').value = itemData.cost_excl_gst || '';
    
    // Update item footer cost display
    const costInclGST = parseFloat(itemData.cost_incl_gst) || 0;
    updateItemFooterCost(itemRow, costInclGST);
    
    // Add to items data array
    itemsData.push({
        item_id: itemData.item_id,
        product_id: itemData.product_id,
        reference: itemData.reference,
        length: itemData.length,
        width: itemData.width,
        quantity: itemData.quantity,
        notes: itemData.notes,
        cost_excl_gst: itemData.cost_excl_gst,
        cost_incl_gst: itemData.cost_incl_gst,
        variables: {}
    });
    
    // Ensure all measurement fields are visible for new items
    resetMeasurementFieldsVisibility(itemRow);
}

// Load product categories
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        if (response.ok) {
            categories = await response.json();
        } else {
            showNotification('Error loading categories', 'error');
        }
    } catch (error) {
        console.error('Error loading categories:', error);
        showNotification('Error loading categories', 'error');
    }
}

// Load all products
async function loadAllProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (response.ok) {
            products = await response.json();
            console.log('Loaded products:', products);
        } else {
            showNotification('Error loading products', 'error');
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Error loading products', 'error');
    }
}

// Load products for a category
async function loadProducts(categoryId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        if (response.ok) {
            const allProducts = await response.json();
            return allProducts.filter(product => product.product_category_id == categoryId);
        } else {
            showNotification('Error loading products', 'error');
            return [];
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showNotification('Error loading products', 'error');
        return [];
    }
}

// Load product variables
async function loadProductVariablesData(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}/variables`);
        if (response.ok) {
            return await response.json();
        } else {
            showNotification('Error loading product variables', 'error');
            return [];
        }
    } catch (error) {
        console.error('Error loading product variables:', error);
        showNotification('Error loading product variables', 'error');
        return [];
    }
}

// Add new item
function addItem() {
    itemCounter++;
    const itemId = `item_${itemCounter}`;
    
    // Clone the template
    const itemElement = itemTemplate.content.cloneNode(true);
    const itemRow = itemElement.querySelector('.item-row');
    itemRow.dataset.itemId = itemId;
    
    // Set item number and reference display
    itemRow.querySelector('.item-number').textContent = `${itemCounter} - `;
    itemRow.querySelector('.item-reference-display').textContent = 'Enter reference';
    
    // Populate category dropdown
    const categorySelect = itemRow.querySelector('.product-category-select');
    categorySelect.innerHTML = '<option value="">Select Category</option>';
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.product_category_id;
        option.textContent = category.name;
        categorySelect.appendChild(option);
    });
    
    // Add event listeners for cost calculation
    const quantityInput = itemRow.querySelector('.item-quantity');
    const lengthInput = itemRow.querySelector('.item-length');
    const widthInput = itemRow.querySelector('.item-width');
    
    [quantityInput, lengthInput, widthInput].forEach(input => {
        input.addEventListener('input', () => calculateItemCost(itemRow));
    });
    
    // Add event listener for cost excluding GST field only
    const costExclInput = itemRow.querySelector('.item-cost-excl');
    
    costExclInput.addEventListener('input', () => handleManualCostChange(itemRow, 'excl'));
    
    
    // Add to container
    itemsContainer.appendChild(itemElement);
    
    // Add to items array
    items.push({
        id: itemId,
        element: itemRow,
        data: {
            category_id: null,
            product_id: null,
            reference: '',
            variables: {},
            length: 0,
            width: 0,
            quantity: 1,
            notes: '',
            cost_excl_gst: 0,
            cost_incl_gst: 0
        }
    });
    
    // Ensure all measurement fields are visible for new items
    resetMeasurementFieldsVisibility(itemRow);
    
    updateTotals();
}

// Update products when category changes
async function updateProducts(categorySelect) {
    const itemRow = categorySelect.closest('.item-row');
    const productSelect = itemRow.querySelector('.product-select');
    const categoryId = categorySelect.value;
    
    // Clear product select
    productSelect.innerHTML = '<option value="">Select Product</option>';
    
    if (categoryId) {
        const products = await loadProducts(categoryId);
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.product_id;
            option.textContent = product.name;
            productSelect.appendChild(option);
        });
    }
    
    // Clear variables
    const variablesContainer = itemRow.querySelector('.variables-container');
    variablesContainer.innerHTML = '';
    itemRow.querySelector('.product-variables').style.display = 'none';
}

// Load product variables when product changes
async function loadProductVariables(productSelect) {
    const itemRow = productSelect.closest('.item-row');
    const productId = productSelect.value;
    const variablesContainer = itemRow.querySelector('.variables-container');
    const variablesSection = itemRow.querySelector('.product-variables');
    
    // Clear variables
    variablesContainer.innerHTML = '';
    variablesSection.style.display = 'none';
    
    if (productId) {
        // Store the currently selected product for the "New Variable" button
        setCurrentSelectedProduct(products.find(p => p.product_id == productId));
        console.log('Product selected:', productId, 'Found product:', currentSelectedProduct);
        
        // Update product name display
        const productNameDisplay = itemRow.querySelector('.item-product-name');
        if (productNameDisplay && currentSelectedProduct) {
            productNameDisplay.textContent = `(${currentSelectedProduct.name})`;
        }
        
        // Update measurement fields visibility based on measure type
        updateMeasurementFieldsVisibility(itemRow, currentSelectedProduct);
        
        const variables = await loadProductVariablesData(productId);
        
        if (variables.length > 0) {
            variables.forEach(variable => {
                const variableDiv = document.createElement('div');
                variableDiv.className = 'form-group';
                
                const label = document.createElement('label');
                label.textContent = variable.name;
                
                const select = document.createElement('select');
                select.className = 'variable-select';
                select.dataset.variableId = variable.product_variable_id;
                select.innerHTML = '<option value="">Select Option</option>';
                
                variable.options.forEach(option => {
                    const optionElement = document.createElement('option');
                    optionElement.value = option.variable_option_id;
                    optionElement.textContent = option.name;
                    select.appendChild(optionElement);
                });
                
                // Add change event listener for cost calculation
                select.addEventListener('change', () => calculateItemCost(itemRow));
                
                variableDiv.appendChild(label);
                variableDiv.appendChild(select);
                variablesContainer.appendChild(variableDiv);
            });
            
            variablesSection.style.display = 'block';
        }
    } else {
        console.log('No product selected, clearing currentSelectedProduct');
        setCurrentSelectedProduct(null);
        
        // Update product name display to show no product selected
        const productNameDisplay = itemRow.querySelector('.item-product-name');
        if (productNameDisplay) {
            productNameDisplay.textContent = '(No product selected)';
        }
        
        // Reset all measurement fields to visible when no product is selected
        resetMeasurementFieldsVisibility(itemRow);
    }
    
    calculateItemCost(itemRow);
}

// Update measurement fields visibility based on product measure type
function updateMeasurementFieldsVisibility(itemRow, product) {
    const lengthField = itemRow.querySelector('.item-length').closest('.form-group');
    const widthField = itemRow.querySelector('.item-width').closest('.form-group');
    const quantityField = itemRow.querySelector('.item-quantity').closest('.form-group');
    const lengthLabel = lengthField.querySelector('label');
    const widthLabel = widthField.querySelector('label');
    
    if (!product || !product.measure_type_id) {
        // Show all fields if no product or measure type
        lengthField.style.display = 'block';
        widthField.style.display = 'block';
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        lengthLabel.textContent = 'Height (m)';
        return;
    }
    
    // Hide all fields first
    lengthField.style.display = 'none';
    widthField.style.display = 'none';
    quantityField.style.display = 'none';
    
    // Show fields based on measure type
    if (product.measure_type_id === 1) {
        // Area (Width × Height × Quantity)
        widthField.style.display = 'block';
        lengthField.style.display = 'block';
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        lengthLabel.textContent = 'Height (m)';
    } else if (product.measure_type_id === 2) {
        // Linear (Length × Quantity)
        lengthField.style.display = 'block';
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        lengthLabel.textContent = 'Length (m)';
    } else if (product.measure_type_id === 3) {
        // Quantity Only
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        lengthLabel.textContent = 'Height (m)';
    }
}

// Reset measurement fields visibility (show all)
function resetMeasurementFieldsVisibility(itemRow) {
    const lengthField = itemRow.querySelector('.item-length').closest('.form-group');
    const widthField = itemRow.querySelector('.item-width').closest('.form-group');
    const quantityField = itemRow.querySelector('.item-quantity').closest('.form-group');
    const lengthLabel = lengthField.querySelector('label');
    const widthLabel = widthField.querySelector('label');
    
    lengthField.style.display = 'block';
    widthField.style.display = 'block';
    quantityField.style.display = 'block';
    widthLabel.textContent = 'Width (m)';
    lengthLabel.textContent = 'Height (m)';
}

// Handle manual cost changes
function handleManualCostChange(itemRow, type) {
    const costExclInput = itemRow.querySelector('.item-cost-excl');
    
    const costExcl = parseFloat(costExclInput.value) || 0;
    
    if (type === 'excl') {
        // When excluding GST is changed, calculate including GST
        const newCostIncl = costExcl * 1.1;
        
        // Update item footer cost display
        updateItemFooterCost(itemRow, newCostIncl);
    }
    
    updateTotals();
}

// Calculate item cost
async function calculateItemCost(itemRow) {
    const quantity = parseFloat(itemRow.querySelector('.item-quantity').value) || 0;
    const length = parseFloat(itemRow.querySelector('.item-length').value) || 0;
    const width = parseFloat(itemRow.querySelector('.item-width').value) || 0;
    
    // Get selected variable options
    const selectedOptions = [];
    itemRow.querySelectorAll('.variable-select').forEach(select => {
        if (select.value) {
            selectedOptions.push(parseInt(select.value));
        }
    });
    
    if (selectedOptions.length === 0) {
        // No variables selected, preserve manual costs or set to 0 if empty
        const costExclInput = itemRow.querySelector('.item-cost-excl');
        
        if (!costExclInput.value) {
            costExclInput.value = '0.00';
        }
        
        // Update item footer cost display
        const currentCostExcl = parseFloat(costExclInput.value) || 0;
        const currentCostIncl = currentCostExcl * 1.1;
        updateItemFooterCost(itemRow, currentCostIncl);
        
        updateTotals();
        return;
    }
    
    try {
        // Get cost data for selected options
        const costData = await getVariableOptionCosts(selectedOptions);
        
        // Get the selected product to determine measure type
        const productSelect = itemRow.querySelector('.product-select');
        const selectedProduct = products.find(p => p.product_id == productSelect.value);
        
        if (!selectedProduct) {
            console.error('No product selected for cost calculation');
            itemRow.querySelector('.item-cost-excl').value = '0.00';
            updateItemFooterCost(itemRow, 0);
            updateTotals();
            return;
        }
        
        // Calculate total cost using measure type-specific formula
        let totalCostExclGST = 0;
        
        costData.forEach(option => {
            let optionCost = 0;
            
            // Apply formula based on measure type
            if (selectedProduct.measure_type_id === 1) {
                // Area (Height × Width × Quantity)
                optionCost = option.base_cost + (option.multiplier_cost * length * width * quantity);
            } else if (selectedProduct.measure_type_id === 2) {
                // Linear (Length × Quantity)
                optionCost = option.base_cost + (option.multiplier_cost * length * quantity);
            } else if (selectedProduct.measure_type_id === 3) {
                // Quantity Only
                optionCost = option.base_cost + (option.multiplier_cost * quantity);
            } else {
                // Fallback to original formula if no measure type is set
                optionCost = option.base_cost + (option.multiplier_cost * length * width * quantity);
            }
            
            totalCostExclGST += optionCost;
        });
        
        // Calculate GST (10%)
        const totalCostInclGST = totalCostExclGST * 1.1;
        
        itemRow.querySelector('.item-cost-excl').value = totalCostExclGST.toFixed(2);
        
        // Update item footer cost display
        updateItemFooterCost(itemRow, totalCostInclGST);
        
        updateTotals();
    } catch (error) {
        console.error('Error calculating cost:', error);
        itemRow.querySelector('.item-cost-excl').value = '0.00';
        
        // Update item footer cost display
        updateItemFooterCost(itemRow, 0);
        
        updateTotals();
    }
}

// Load item variables and set selected options
async function loadItemVariables(itemRow, itemId) {
    try {
        const response = await fetch(`${API_BASE_URL}/item-variables?item_id=${itemId}`);
        if (response.ok) {
            const itemVariables = await response.json();
            
            // Add a small delay to ensure variable selects are created
            setTimeout(() => {
                // Set the selected options for each variable
                itemVariables.forEach(itemVar => {
                    const variableSelect = itemRow.querySelector(`.variable-select[data-variable-id="${itemVar.product_variable_id}"]`);
                    if (variableSelect && itemVar.variable_option_id) {
                        variableSelect.value = itemVar.variable_option_id;
                        console.log(`Set variable ${itemVar.product_variable_id} to option ${itemVar.variable_option_id}`);
                    }
                });
            }, 100);
        }
    } catch (error) {
        console.error('Error loading item variables:', error);
    }
}

// Update item footer cost display
function updateItemFooterCost(itemRow, costInclGST) {
    const costValueElement = itemRow.querySelector('.item-cost-value');
    if (costValueElement) {
        // Format number with comma separators for thousands
        const formattedCost = costInclGST.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        costValueElement.textContent = `$${formattedCost}`;
    }
}

// Toggle item collapse/expand
function toggleItemCollapse(button) {
    const itemRow = button.closest('.item-row');
    const itemContent = itemRow.querySelector('.item-content');
    const itemFooter = itemRow.querySelector('.item-footer');
    
    // Toggle collapsed class on button
    button.classList.toggle('collapsed');
    
    // Toggle collapsed class on content and footer
    itemContent.classList.toggle('collapsed');
    itemFooter.classList.toggle('collapsed');
}

// Get cost data for variable options
async function getVariableOptionCosts(optionIds) {
    try {
        const response = await fetch(`${API_BASE_URL}/variable-options/costs`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ option_ids: optionIds })
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Failed to fetch cost data');
        }
    } catch (error) {
        console.error('Error fetching cost data:', error);
        throw error;
    }
}

// Update totals
function updateTotals() {
    let totalExcl = 0;
    
    document.querySelectorAll('.item-row').forEach(itemRow => {
        const costExcl = parseFloat(itemRow.querySelector('.item-cost-excl').value) || 0;
        totalExcl += costExcl;
    });
    
    const totalIncl = totalExcl * 1.1;
    
    // Format numbers with comma separators for thousands
    const formattedExcl = totalExcl.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    const formattedIncl = totalIncl.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
    
    document.getElementById('totalExclGST').textContent = `$${formattedExcl}`;
    document.getElementById('totalInclGST').textContent = `$${formattedIncl}`;
    
    // Update PDF button visibility
    updatePDFButtonVisibility();
}

// Update PDF button visibility
function updatePDFButtonVisibility() {
    const pdfButton = document.getElementById('pdfButton');
    const itemRows = document.querySelectorAll('.item-row');
    
    if (itemRows.length > 0) {
        pdfButton.style.display = 'inline-flex';
    } else {
        pdfButton.style.display = 'none';
    }
}

// Remove item
function removeItem(button) {
    const itemRow = button.closest('.item-row');
    itemRow.remove();
    updateTotals();
}

// Save quote
async function saveQuote() {
    
    // Collect all items data
    const itemsData = [];
    document.querySelectorAll('.item-row').forEach(itemRow => {
        const categorySelect = itemRow.querySelector('.product-category-select');
        const productSelect = itemRow.querySelector('.product-select');
        const referenceDisplay = itemRow.querySelector('.item-reference-display');
        const reference = referenceDisplay.textContent === 'Enter reference' ? '' : referenceDisplay.textContent;
        const length = parseFloat(itemRow.querySelector('.item-length').value) || 0;
        const width = parseFloat(itemRow.querySelector('.item-width').value) || 0;
        const quantity = parseFloat(itemRow.querySelector('.item-quantity').value) || 1;
        const notes = itemRow.querySelector('.item-notes').value;
        const costExcl = parseFloat(itemRow.querySelector('.item-cost-excl').value) || 0;
        const costInclElement = itemRow.querySelector('.item-cost-value');
        const costIncl = costInclElement ? parseFloat(costInclElement.textContent.replace('$', '').replace(',', '')) || 0 : costExcl * 1.1;
        
        // Collect variable selections
        const variables = {};
        itemRow.querySelectorAll('.variable-select').forEach(select => {
            if (select.value) {
                variables[select.dataset.variableId] = select.value;
            }
        });
        
        if (productSelect.value) {
            itemsData.push({
                product_id: parseInt(productSelect.value),
                reference: reference,
                length: length,
                width: width,
                quantity: quantity,
                notes: notes,
                cost_excl_gst: costExcl,
                cost_incl_gst: costIncl,
                variables: variables
            });
        }
    });
    
    if (itemsData.length === 0) {
        showNotification('Please add at least one item to the quote', 'error');
        return;
    }
    
    try {
        let quote;
        
        
        if (currentQuoteId) {
            // Update existing quote
            const quoteData = {
                cost_excl_gst: parseFloat(document.getElementById('totalExclGST').textContent.replace('$', '').replace(',', '')),
                cost_incl_gst: parseFloat(document.getElementById('totalInclGST').textContent.replace('$', '').replace(',', ''))
            };
            
            const quoteResponse = await fetch(`${API_BASE_URL}/quotes/${currentQuoteId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(quoteData)
            });
            
            if (!quoteResponse.ok) {
                throw new Error('Failed to update quote');
            }
            
            quote = { quote_id: currentQuoteId };
        } else {
            // Create new quote
            const quoteData = {
                job_id: parseInt(currentJobId),
                date_created: new Date().toISOString().split('T')[0],
                cost_excl_gst: parseFloat(document.getElementById('totalExclGST').textContent.replace('$', '').replace(',', '')),
                cost_incl_gst: parseFloat(document.getElementById('totalInclGST').textContent.replace('$', '').replace(',', ''))
            };
            
            const quoteResponse = await fetch(`${API_BASE_URL}/quotes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(quoteData)
            });
            
            if (!quoteResponse.ok) {
                throw new Error('Failed to create quote');
            }
            
            quote = await quoteResponse.json();
        }
        
        // Handle items for the quote
        if (currentQuoteId) {
            // For existing quotes, we need to delete old items and create new ones
            // First, delete existing items
            const existingItemsResponse = await fetch(`${API_BASE_URL}/items?quote_id=${currentQuoteId}`);
            if (existingItemsResponse.ok) {
                const existingItems = await existingItemsResponse.json();
                for (const item of existingItems) {
                    await fetch(`${API_BASE_URL}/items/${item.item_id}`, {
                        method: 'DELETE'
                    });
                }
            }
        }
        
        // Create items for the quote
        for (const itemData of itemsData) {
            const itemResponse = await fetch(`${API_BASE_URL}/items`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    quote_id: quote.quote_id,
                    product_id: itemData.product_id,
                    reference: itemData.reference,
                    length: itemData.length,
                    width: itemData.width,
                    quantity: itemData.quantity,
                    notes: itemData.notes,
                    cost_excl_gst: itemData.cost_excl_gst,
                    cost_incl_gst: itemData.cost_incl_gst
                })
            });
            
            if (itemResponse.ok) {
                const item = await itemResponse.json();
                
                // Create item variables
                for (const [variableId, optionId] of Object.entries(itemData.variables)) {
                    await fetch(`${API_BASE_URL}/item-variables`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            item_id: item.item_id,
                            product_variable_id: parseInt(variableId),
                            variable_option_id: parseInt(optionId)
                        })
                    });
                }
            } else {
                throw new Error('Failed to create item');
            }
        }
        
        showNotification('Quote saved successfully!', 'success');
        setTimeout(() => goBack(), 2000);
    } catch (error) {
        console.error('Error saving quote:', error);
        showNotification('Error saving quote', 'error');
    }
}

// Edit item reference
function editItemReference(button) {
    const itemRow = button.closest('.item-row');
    const displaySection = itemRow.querySelector('.item-title-display');
    const editSection = itemRow.querySelector('.item-reference-edit');
    const referenceInput = itemRow.querySelector('.item-reference-input');
    const referenceDisplay = itemRow.querySelector('.item-reference-display');
    
    // Hide display section and show edit section
    displaySection.style.display = 'none';
    editSection.style.display = 'flex';
    
    // Set the current reference value in the input
    referenceInput.value = referenceDisplay.textContent === 'Enter reference' ? '' : referenceDisplay.textContent;
    referenceInput.focus();
}

// Save item reference
function saveItemReference(button) {
    const itemRow = button.closest('.item-row');
    const displaySection = itemRow.querySelector('.item-title-display');
    const editSection = itemRow.querySelector('.item-reference-edit');
    const referenceInput = itemRow.querySelector('.item-reference-input');
    const referenceDisplay = itemRow.querySelector('.item-reference-display');
    const itemId = itemRow.dataset.itemId;
    
    // Update the display with the new reference
    const newReference = referenceInput.value.trim() || 'Enter reference';
    referenceDisplay.textContent = newReference;
    
    // Update the item data
    const item = items.find(i => i.id === itemId);
    if (item) {
        item.data.reference = newReference === 'Enter reference' ? '' : newReference;
    }
    
    // Hide edit section and show display section
    editSection.style.display = 'none';
    displaySection.style.display = 'flex';
}

// Cancel editing item reference
function cancelEditReference(button) {
    const itemRow = button.closest('.item-row');
    const displaySection = itemRow.querySelector('.item-title-display');
    const editSection = itemRow.querySelector('.item-reference-edit');
    
    // Hide edit section and show display section
    editSection.style.display = 'none';
    displaySection.style.display = 'flex';
}

// Open product editor modal
function openProductEditor(button) {
    // Find the item row that contains this button
    const itemRow = button.closest('.item-row');
    const productSelect = itemRow.querySelector('.product-select');
    const productId = productSelect.value;
    
    console.log('openProductEditor called, productId:', productId);
    
    if (!productId) {
        showNotification('Please select a product first', 'error');
        return;
    }
    
    // Find the product in the products array
    const selectedProduct = products.find(p => p.product_id == productId);
    console.log('Found product:', selectedProduct);
    
    if (!selectedProduct) {
        showNotification('Product not found', 'error');
        return;
    }
    
    // Set the current selected product
    setCurrentSelectedProduct(selectedProduct);
    console.log('Product ID:', currentSelectedProduct.product_id);
    
    // Show the product modal as a popup for the selected product
    document.getElementById('productModal').style.display = 'block';
    
    // Initialize the product modal for editing the selected product
    editSelectedProduct();
}

// Initialize product modal
function initializeProductModal() {
    // Reset form
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('productModalTitle').textContent = 'Add New Product';
    document.getElementById('productSubmitBtn').textContent = 'Add Product';
    
    // Hide delete button
    document.getElementById('deleteProductBtn').style.display = 'none';
    
    // Load categories
    loadCategoriesForModal();
}

// Load categories for the product modal
async function loadCategoriesForModal() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        if (response.ok) {
            const categories = await response.json();
            const categoryDropdown = document.getElementById('categoryDropdown');
            categoryDropdown.innerHTML = '';
            
            categories.forEach(category => {
                const option = document.createElement('div');
                option.className = 'category-option';
                option.textContent = category.name;
                option.dataset.categoryId = category.product_category_id;
                option.onclick = () => selectCategory(category.product_category_id, category.name);
                categoryDropdown.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Select category
function selectCategory(categoryId, categoryName) {
    document.getElementById('productCategory').value = categoryId;
    document.getElementById('categoryDisplay').textContent = categoryName;
    document.getElementById('categoryDropdown').style.display = 'none';
}

// Toggle category dropdown
function toggleCategoryDropdown() {
    const dropdown = document.getElementById('categoryDropdown');
    dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
}

// Edit selected product
async function editSelectedProduct() {
    if (!currentSelectedProduct) return;
    
    const product = currentSelectedProduct;
    
    // Set modal title and button
    document.getElementById('productModalTitle').textContent = product.name;
    document.getElementById('productSubmitBtn').textContent = 'Update Product';
    document.getElementById('productId').value = product.product_id;
    
    // Show delete button for existing products
    document.getElementById('deleteProductBtn').style.display = 'block';
    
    // Set category display
    const categoryDisplay = document.getElementById('categoryDisplay');
    const productCategory = document.getElementById('productCategory');
    const selectedCategory = categories.find(cat => cat.product_category_id === product.product_category_id);
    categoryDisplay.textContent = selectedCategory ? selectedCategory.name : 'Select Category';
    productCategory.value = product.product_category_id;
    
    console.log('Setting category for product:', {
        productId: product.product_id,
        productCategoryId: product.product_category_id,
        selectedCategory: selectedCategory,
        categoryInputValue: productCategory.value
    });
    
    // Update selected state in dropdown
    const options = document.querySelectorAll('.category-option');
    options.forEach(option => {
        option.classList.remove('selected');
        if (option.dataset.categoryId == product.product_category_id) {
            option.classList.add('selected');
        }
    });
    
    // Load and populate product variables
    try {
        const variables = await loadProductVariablesData(product.product_id);
        populateProductVariablesList(variables);
    } catch (error) {
        console.error('Error loading product variables:', error);
        populateProductVariablesList([]);
    }
}

// Populate product variables list - Updated to match products page format
function populateProductVariablesList(variables) {
    const variablesContent = document.querySelector('.product-variables-content');
    variablesContent.innerHTML = '';
    
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
                <button type="button" class="variable-delete-btn" onclick="deleteVariable(${currentSelectedProduct.product_id}, ${variable.product_variable_id}); event.stopPropagation()">-delete</button>
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
                                    <button type="button" class="option-edit-btn" onclick="editOption(${option.variable_option_id})">+edit</button>
                                    <button type="button" class="option-delete-btn" onclick="deleteOption(${option.variable_option_id})">-delete</button>
                                </td>
                            </tr>
                        `).join('') : ''}
                    </tbody>
                </table>
                <button type="button" class="add-option-btn" onclick="showAddOptionModal(${variable.product_variable_id})">+ Add Option</button>
            </div>
        </div>
    `).join('');
    
    variablesContent.innerHTML = variablesHTML + `
        <div class="add-variable-container">
            <button type="button" class="add-variable-btn" onclick="addVariable()">+ Add Variable</button>
        </div>
    `;
}

// Hide product modal
function hideProductModal() {
    console.log('hideProductModal called');
    console.log('Current selected product before hiding:', currentSelectedProduct);
    document.getElementById('productModal').style.display = 'none';
    // Don't clear currentSelectedProduct here as it might be needed for adding variables
    // currentSelectedProduct = null;
}

// Clear product context (call this when truly done with product editing)
function clearProductContext() {
    console.log('Clearing product context');
    setCurrentSelectedProduct(null);
}

// Show add variable modal from the product modal context
function showAddVariableModalFromModal() {
    console.log('showAddVariableModalFromModal called');
    
    // Get the product from the modal context
    const productId = document.getElementById('productId').value;
    console.log('Product ID from modal:', productId);
    
    if (!productId) {
        console.error('No product ID found in modal');
        showNotification('No product selected. Please select a product first.', 'error');
        return;
    }
    
    // Find the product in the products array
    const product = products.find(p => p.product_id == productId);
    console.log('Found product from modal context:', product);
    
    if (!product) {
        console.error('Product not found in products array');
        showNotification('Product not found. Please try again.', 'error');
        return;
    }
    
    // Call the main function with the product
    showAddVariableModal(product);
}

// Show add variable modal
function showAddVariableModal(product = null) {
    console.log('showAddVariableModal called with product:', product);
    console.log('Current selected product:', currentSelectedProduct);
    console.log('Current selected product type:', typeof currentSelectedProduct);
    console.log('Current selected product keys:', currentSelectedProduct ? Object.keys(currentSelectedProduct) : 'null');
    console.log('Product parameter type:', typeof product);
    console.log('Product parameter keys:', product ? Object.keys(product) : 'null');
    
    // Use the passed product or fall back to currentSelectedProduct
    const productToUse = product || currentSelectedProduct;
    
    console.log('Product to use:', productToUse);
    console.log('Product to use type:', typeof productToUse);
    
    if (!productToUse) {
        console.error('No product available!');
        console.log('Available global variables:');
        console.log('- currentSelectedProduct:', currentSelectedProduct);
        console.log('- products array length:', products.length);
        console.log('- products:', products);
        showNotification('No product selected. Please select a product first.', 'error');
        return;
    }
    
    // Set the product context for the form submission
    setCurrentSelectedProduct(productToUse);
    
    document.getElementById('variableModalTitle').textContent = 'Add New Variable';
    document.getElementById('variableSubmitBtn').textContent = 'Add Variable';
    document.getElementById('variableForm').reset();
    document.getElementById('variableId').value = '';
    document.getElementById('variableModal').style.display = 'block';
    
    // Ensure event listener is attached
    const variableForm = document.getElementById('variableForm');
    if (variableForm) {
        // Remove any existing listeners to avoid duplicates
        variableForm.removeEventListener('submit', handleVariableFormSubmit);
        // Add the listener
        variableForm.addEventListener('submit', handleVariableFormSubmit);
        console.log('Event listener attached to variable form');
    } else {
        console.error('Variable form not found!');
    }
    
    console.log('Variable modal should be visible now');
}

// Hide variable modal
function hideVariableModal() {
    document.getElementById('variableModal').style.display = 'none';
}

// Edit variable
function editVariable(variableId) {
    const variable = currentSelectedProduct.variables.find(v => v.product_variable_id === variableId);
    if (!variable) return;
    
    document.getElementById('variableModalTitle').textContent = 'Edit Variable';
    document.getElementById('variableSubmitBtn').textContent = 'Update Variable';
    document.getElementById('variableId').value = variable.product_variable_id;
    document.getElementById('variableName').value = variable.name;
    document.getElementById('variableModal').style.display = 'block';
}

// Show add option modal
function showAddOptionModal(variableId) {
    document.getElementById('optionModalTitle').textContent = 'Add New Option';
    document.getElementById('optionSubmitBtn').textContent = 'Add Option';
    document.getElementById('optionForm').reset();
    document.getElementById('optionId').value = '';
    document.getElementById('optionVariableId').value = variableId;
    document.getElementById('optionModal').style.display = 'block';
}

// Hide option modal
function hideOptionModal() {
    document.getElementById('optionModal').style.display = 'none';
}

// Edit option
function editOption(optionId) {
    // Find the option in the current product's variables
    let option = null;
    let variableId = null;
    
    for (const variable of currentSelectedProduct.variables) {
        const foundOption = variable.options.find(o => o.variable_option_id === optionId);
        if (foundOption) {
            option = foundOption;
            variableId = variable.product_variable_id;
            break;
        }
    }
    
    if (!option) return;
    
    document.getElementById('optionModalTitle').textContent = 'Edit Option';
    document.getElementById('optionSubmitBtn').textContent = 'Update Option';
    document.getElementById('optionId').value = option.variable_option_id;
    document.getElementById('optionVariableId').value = variableId;
    document.getElementById('optionName').value = option.name;
    document.getElementById('optionBaseCost').value = option.base_cost;
    document.getElementById('optionMultiplierCost').value = option.multiplier_cost;
    document.getElementById('optionModal').style.display = 'block';
}

// Delete variable
async function deleteVariable(productId, variableId) {
    if (!confirm('Are you sure you want to delete this variable? This will also delete all its options.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/variables/${variableId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Variable deleted successfully', 'success');
            // Reload the product variables
            await editSelectedProduct();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to delete variable', 'error');
        }
    } catch (error) {
        console.error('Error deleting variable:', error);
        showNotification('Error deleting variable', 'error');
    }
}

// Delete option
async function deleteOption(optionId) {
    if (!confirm('Are you sure you want to delete this option?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/options/${optionId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Option deleted successfully', 'success');
            // Reload the product variables
            await editSelectedProduct();
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to delete option', 'error');
        }
    } catch (error) {
        console.error('Error deleting option:', error);
        showNotification('Error deleting option', 'error');
    }
}



// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        font-family: 'Futura Medium', 'Futura', 'Arial', sans-serif;
        font-weight: 500;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}
