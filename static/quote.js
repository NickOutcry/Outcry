// Quote Management JavaScript

// API Base URL
const API_BASE_URL = 'http://localhost:5001/api';

// Add footer with terms and conditions to PDF
function addFooter(doc, pageNumber, totalPages) {
    const pageHeight = doc.internal.pageSize.height;
    const footerStartY = pageHeight - 50; // Start footer 50 units from bottom
    
    // Draw a line above the footer
    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.5);
    doc.line(20, footerStartY - 5, 190, footerStartY - 5);
    
    // Terms and Conditions
    doc.setFontSize(8);
    doc.setFont('helvetica', 'bold');
    doc.text('Terms and Conditions', 20, footerStartY);
    
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(7);
    let footerY = footerStartY + 4;
    
    // Add each term
    const terms = [
        '• This quote is valid for 30 days from the date of issue',
        '• Payment terms: 50% deposit required to commence work, balance on completion',
        '• All work is guaranteed for 12 months against manufacturing defects',
        '• Client approval required before production commences',
        '• Delivery times are estimates and may vary depending on materials and complexity'
    ];
    
    terms.forEach(term => {
        doc.text(term, 20, footerY);
        footerY += 3;
    });
    
    // Add page number
    doc.setFontSize(8);
    doc.text(`Page ${pageNumber} of ${totalPages}`, 190, pageHeight - 10, { align: 'right' });
    
    // Add thank you message
    doc.setFontSize(7);
    doc.text('Thank you for choosing Outcry for your signage needs', 105, pageHeight - 5, { align: 'center' });
}

// PDF Generation
async function generateQuotePDF() {
    console.log('PDF generation started');
    
    // Check if jsPDF is loaded
    if (typeof window.jspdf === 'undefined') {
        console.error('jsPDF library not loaded');
        alert('PDF library not loaded. Please refresh the page and try again.');
        return;
    }
    
    // Get quote data
    const quoteNumber = document.getElementById('quoteNumber').textContent;
    const jobNumber = document.getElementById('jobNumber').textContent;
    const jobReference = document.getElementById('jobReference').textContent;
    const projectName = document.getElementById('projectName').textContent;
    const clientName = currentJob ? currentJob.client_name : 'Unknown Client';
    const quoteDate = new Date().toLocaleDateString('en-AU');
    
    console.log('Quote data:', { quoteNumber, jobNumber, jobReference, projectName, clientName, quoteDate });
    
    try {
        // Create filename
        const fileName = `Quote_${quoteNumber.replace('#', '')}_${new Date().toISOString().split('T')[0]}.pdf`;
        
        // Create new PDF document
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        console.log('PDF document created');
        
        // Set font to Helvetica
        doc.setFont('helvetica');
        
        // Add Outcry header image
        try {
            // Add the header image in the top left corner with correct proportions
            // Original image: 2882 x 842 pixels (aspect ratio ~3.42:1)
            // Set height to 25 and calculate width to maintain aspect ratio
            const imageHeight = 25;
            const imageWidth = imageHeight * (2882 / 842); // ~85.5
            doc.addImage('/static/outcry_header.png', 'PNG', 20, 10, imageWidth, imageHeight);
        } catch (error) {
            console.log('Could not load header image, using text fallback');
            // Fallback to text if image fails to load
            doc.setFontSize(20);
            doc.setFont('helvetica', 'bold');
            doc.text('OUTCRY', 20, 25);
        }
        
        // Add staff information and quote details on the right side (top)
        let yPos = 10; // Moved up from 15 to eliminate space
        
        // Get staff information from currentJob
        const staffFirstName = currentJob && currentJob.staff_first_name ? currentJob.staff_first_name : '';
        const staffSurname = currentJob && currentJob.staff_surname ? currentJob.staff_surname : '';
        const staffEmail = currentJob && currentJob.staff_email ? currentJob.staff_email : 'staff@outcry.com.au';
        const staffPhone = currentJob && currentJob.staff_phone ? currentJob.staff_phone : '(02) 1234 5678';
        
        // Combine first name and surname
        const staffFullName = `${staffFirstName} ${staffSurname}`.trim() || 'Staff Name';
        
        // Staff information
        doc.setFontSize(11);
        doc.setFont('helvetica', 'normal');
        doc.text(staffFullName, 190, yPos, { align: 'right' });
        yPos += 5; // Reduced from 8 to 5 (37.5% reduction)
        doc.text(staffEmail, 190, yPos, { align: 'right' });
        yPos += 5; // Reduced from 8 to 5 (37.5% reduction)
        doc.text(staffPhone, 190, yPos, { align: 'right' });
        yPos += 7; // Reduced from 12 to 7 (42% reduction)
        
        // Quotation title
        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text('Quotation', 190, yPos, { align: 'right' });
        yPos += 5; // Reduced from 8 to 5 (37.5% reduction)
        
        // ABN
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.text('ABN: 77 252 335 264', 190, yPos, { align: 'right' });
        yPos += 7; // Reduced from 12 to 7 (42% reduction)
        
        // Quote Number
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        doc.text(`Quote Number: ${quoteNumber}`, 190, yPos, { align: 'right' });
        yPos += 5; // Reduced from 8 to 5 (37.5% reduction)
        
        // Quote Date
        doc.text(quoteDate, 190, yPos, { align: 'right' });
        
        // Add client billing information and job details (left-justified)
        // Position billing info to sit lower than the date (which ends around yPos)
        let yPosition = yPos + 5; // Position billing info 5pt below the date
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        
        // Get billing information from currentJob
        const billingEntity = currentJob && currentJob.billing_entity_name ? currentJob.billing_entity_name : 'Billing Entity';
        const billingAddress = currentJob && currentJob.billing_address ? currentJob.billing_address : 'Billing Address';
        const billingSuburb = currentJob && currentJob.billing_suburb ? currentJob.billing_suburb : '';
        const billingState = currentJob && currentJob.billing_state ? currentJob.billing_state : '';
        const billingPostcode = currentJob && currentJob.billing_postcode ? currentJob.billing_postcode : '';
        
        // Client billing information
        doc.text(billingEntity, 20, yPosition);
        yPosition += 5; // Reduced from 8 to 5 (37.5% reduction)
        doc.text(billingAddress, 20, yPosition);
        yPosition += 5; // Reduced from 8 to 5 (37.5% reduction)
        
        // Combine suburb, state, and postcode
        const billingLocation = `${billingSuburb}${billingSuburb && billingState ? ', ' : ''}${billingState}${billingState && billingPostcode ? ' ' : ''}${billingPostcode}`.trim();
        if (billingLocation) {
            doc.text(billingLocation, 20, yPosition);
            yPosition += 7; // Reduced from 12 to 7 (42% reduction)
        } else {
            yPosition += 2; // Reduced from 4 to 2 (50% reduction)
        }
        
        // Job details
        doc.text(`${jobNumber} - ${projectName} (${jobReference})`, 20, yPosition);
        yPosition += 12; // Reduced from 20 to 12 (40% reduction)
        
        // Add items table
        const itemsContainer = document.getElementById('itemsContainer');
        console.log('Items container found:', itemsContainer);
        
        if (itemsContainer) {
            const itemRows = itemsContainer.querySelectorAll('.item-row');
            console.log('Number of item rows found:', itemRows.length);
            
            if (itemRows.length > 0) {
                // Table headers with background color
                // Draw background rectangle
                doc.setFillColor(245, 183, 164); // #f5b7a4
                doc.rect(20, yPosition - 5, 170, 7, 'F'); // x, y, width, height, 'F' for filled
                
                doc.setFontSize(11); // Increased from 10 by 10%
                doc.setFont('helvetica', 'bold');
                doc.setTextColor(0, 0, 0); // Black text
                doc.text('Item', 25, yPosition); // Inset from 20 to 25
                doc.text('Quantity', 150, yPosition, { align: 'right' }); // Right-aligned
                doc.text('Price (Excl GST)', 185, yPosition, { align: 'right' }); // Right-aligned
                
                yPosition += 5.5; // Increased by 10% from 5
                
                // Table rows
                doc.setFont('helvetica', 'normal');
                doc.setFontSize(10); // Increased from 9 by 10%
                
                let itemNumber = 1;
                for (let i = 0; i < itemRows.length; i++) {
                    const itemRow = itemRows[i];
                    console.log('Processing item row:', itemRow);
                    
                    // Get item data from the row
                    const itemRef = itemRow.querySelector('.item-reference-display')?.textContent.trim() || 'No Reference';
                    const productSelect = itemRow.querySelector('.product-select');
                    const productName = productSelect?.selectedOptions[0]?.textContent || 'No Product';
                    const qty = itemRow.querySelector('.quantity-input')?.value || '0';
                    const width = itemRow.querySelector('.item-length')?.value || '0';  // Frontend "Width" maps to database "length"
                    const height = itemRow.querySelector('.item-height')?.value || '0';  // Frontend "Height" maps to database "height"
                    const costElement = itemRow.querySelector('.item-cost-value');
                    const cost = costElement?.textContent.trim() || '$0.00';
                    
                    // Check for variable options in the frontend
                    const variableSelects = itemRow.querySelectorAll('.variable-select');
                    console.log('Variable selects found:', variableSelects.length);
                    const selectedVariables = [];
                    variableSelects.forEach(select => {
                        if (select.value) {
                            const optionText = select.selectedOptions[0]?.textContent;
                            selectedVariables.push(optionText);
                            console.log('Selected variable:', optionText);
                        }
                    });
                    
                    console.log('Item data:', { itemRef, productName, qty, width, height, cost });
                    console.log('Selected variables in frontend:', selectedVariables);
                    
                    // Get the real database item ID from itemsData array
                    const realItemId = itemsData[i]?.item_id;
                    console.log('Real Item ID from itemsData:', realItemId);
                    console.log('itemsData array:', itemsData);
                    console.log('itemsData[i]:', itemsData[i]);
                    
                    // Check if we need a new page (leave room for footer)
                    if (yPosition > 220) {
                        doc.addPage();
                        yPosition = 40;
                        
                        // Re-add table headers on new page with background color
                        doc.setFillColor(245, 183, 164); // #f5b7a4
                        doc.rect(20, yPosition - 5, 170, 7, 'F'); // x, y, width, height, 'F' for filled
                        
                        doc.setFontSize(11); // Increased from 10 by 10%
                        doc.setFont('helvetica', 'bold');
                        doc.setTextColor(0, 0, 0); // Black text
                        doc.text('Item', 25, yPosition); // Inset from 20 to 25
                        doc.text('Quantity', 150, yPosition, { align: 'right' }); // Right-aligned
                        doc.text('Price (Excl GST)', 185, yPosition, { align: 'right' }); // Right-aligned
                        
                        yPosition += 8.8; // Increased by 10% from 8
                        doc.setFont('helvetica', 'normal');
                        doc.setFontSize(10); // Increased from 9 by 10%
                    }
                    
                    // Format item description
                    const itemDescription = `${itemNumber}. ${itemRef} - ${productName} (${width} x ${height})`;
                    
                    // Store the starting Y position for this row
                    const rowStartY = yPosition;
                    
                    // Add item description (inset)
                    doc.text(itemDescription, 25, yPosition); // Inset from 20 to 25
                    yPosition += 4.4; // Increased by 10% from 4
                    
                    // Add variable options if available
                    let variablesAdded = false;
                    
                    if (realItemId) {
                        console.log('Fetching variables for item ID:', realItemId);
                        try {
                            const response = await fetch(`${API_BASE_URL}/item-variables?item_id=${realItemId}`);
                            console.log('API response status:', response.status);
                            if (response.ok) {
                                const itemVariables = await response.json();
                                console.log('Item variables response:', itemVariables);
                                console.log('Number of variables:', itemVariables.length);
                                
                                if (itemVariables.length > 0) {
                                    for (const itemVar of itemVariables) {
                                        console.log('Processing variable:', itemVar);
                                        if (itemVar.variable_name) {
                                            console.log('Adding variable:', itemVar.variable_name);
                                            doc.text(`• ${itemVar.variable_name}`, 30, yPosition); // Inset more from 25 to 30
                                            yPosition += 3.3; // Increased by 10% from 3
                                            variablesAdded = true;
                                        }
                                    }
                                } else {
                                    console.log('No variables found in database for this item');
                                }
                            } else {
                                console.log('API response not ok:', response.status, response.statusText);
                            }
                        } catch (error) {
                            console.log('Error loading item variables:', error);
                        }
                    } else {
                        console.log('No real item ID found, skipping database variables');
                    }
                    
                    // Fallback: Use frontend variable options if database doesn't have them
                    if (!variablesAdded && selectedVariables.length > 0) {
                        console.log('Using frontend variable options as fallback');
                        for (const variable of selectedVariables) {
                            console.log('Adding frontend variable:', variable);
                            doc.text(`• ${variable}`, 30, yPosition); // Inset more from 25 to 30
                            yPosition += 3.3; // Increased by 10% from 3
                        }
                    }
                    
                    // Add quantity and price aligned to the top of the row (rowStartY), right-aligned
                    doc.text(qty, 150, rowStartY, { align: 'right' }); // Right-aligned at x=150
                    doc.text(cost, 185, rowStartY, { align: 'right' }); // Right-aligned at x=185
                    
                    // Move to next row position
                    yPosition += 5.5; // Increased by 10% from 5
                    
                    itemNumber++;
                }
                
                yPosition += 6; // Reduced from 10 to 6 (40% reduction)
            } else {
                console.log('No item rows found');
                // Add a message if no items
                doc.setFontSize(10);
                doc.setFont('helvetica', 'normal');
                doc.text('No items found in this quote.', 20, yPosition);
                yPosition += 10;
            }
        } else {
            console.log('Items container not found');
            // Add a message if container not found
            doc.setFontSize(10);
            doc.setFont('helvetica', 'normal');
            doc.text('Items container not found.', 20, yPosition);
            yPosition += 10;
        }
        
        // Add totals integrated into the table (columns B and C)
        const totalExclGSTElement = document.getElementById('totalExclGST');
        const totalInclGSTElement = document.getElementById('totalInclGST');
        
        if (totalExclGSTElement && totalInclGSTElement) {
            // Check if we need a new page for totals (leave room for footer)
            if (yPosition > 210) {
                doc.addPage();
                yPosition = 40;
            }
            
            const totalExclGST = totalExclGSTElement.textContent;
            const totalInclGST = totalInclGSTElement.textContent;
            
            // Calculate GST from the totals
            const totalExclValue = parseFloat(totalExclGST.replace('$', '').replace(',', ''));
            const totalInclValue = parseFloat(totalInclGST.replace('$', '').replace(',', ''));
            const totalGST = totalInclValue - totalExclValue;
            
            yPosition += 6.6; // Increased by 10% from 6
            
            // Add border separating items from totals
            doc.setDrawColor(0, 0, 0); // Black
            doc.setLineWidth(0.15); // Reduced by 70% from 0.5 (0.5 * 0.3 = 0.15)
            doc.line(20, yPosition - 3, 190, yPosition - 3); // Horizontal line across table
            
            yPosition += 3; // Space after border
            
            // Subtotal row - labels in column B, values in column C (unbolded)
            doc.setFontSize(11); // Increased by 10%
            doc.setFont('helvetica', 'normal'); // Changed from bold to normal
            doc.text('Subtotal (Excl. GST)', 150, yPosition, { align: 'right' }); // Column B
            doc.text(`$${totalExclValue.toFixed(2)}`, 185, yPosition, { align: 'right' }); // Column C
            
            yPosition += 5.5; // Increased by 10% from 5
            
            // GST row (unbolded)
            doc.text('GST (10%)', 150, yPosition, { align: 'right' }); // Column B
            doc.text(`$${totalGST.toFixed(2)}`, 185, yPosition, { align: 'right' }); // Column C
            
            yPosition += 5.5; // Increased by 10% from 5
            
            // Total row with grey background
            // Draw grey background rectangle only for columns B and C
            doc.setFillColor(220, 220, 220); // Light grey
            doc.rect(129, yPosition - 5, 61, 8, 'F'); // x, y, width, height - covers columns B and C only (129 to 190)
            
            doc.setFontSize(12); // Increased by 10% (was 12, now ~13)
            doc.setFont('helvetica', 'bold'); // Total stays bold
            doc.text('Total (Incl. GST)', 150, yPosition, { align: 'right' }); // Column B
            doc.text(`$${totalInclValue.toFixed(2)}`, 185, yPosition, { align: 'right' }); // Column C
        }
        
        // Add footer to all pages
        const pageCount = doc.internal.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            addFooter(doc, i, pageCount);
        }
        
        // Save the PDF
        doc.save(fileName);
        console.log('PDF saved:', fileName);
        
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Error generating PDF: ' + error.message);
    }
}

// Generate HTML content for PDF
function generateQuoteHTML(quoteNumber, jobNumber, jobReference, projectName, clientName, quoteDate) {
    // Get items data
    const itemsTable = document.getElementById('itemsTable');
    const items = [];
    
    if (itemsTable) {
        const rows = itemsTable.querySelectorAll('tbody tr');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 7) {
                items.push({
                    item: cells[0].textContent.trim(),
                    reference: cells[1].textContent.trim(),
                    product: cells[2].textContent.trim(),
                    quantity: cells[3].textContent.trim(),
                    length: cells[4].textContent.trim(),
                    width: cells[5].textContent.trim(),
                    cost: cells[6].textContent.trim()
                });
            }
        });
    }
    
    // Get totals
    const totalExclGSTElement = document.getElementById('totalExclGST');
    const totalInclGSTElement = document.getElementById('totalInclGST');
    
    const totalExclGST = totalExclGSTElement ? totalExclGSTElement.textContent : '$0.00';
    const totalInclGST = totalInclGSTElement ? totalInclGSTElement.textContent : '$0.00';
    
    // Calculate GST
    const totalExclValue = parseFloat(totalExclGST.replace('$', '').replace(',', ''));
    const totalInclValue = parseFloat(totalInclGST.replace('$', '').replace(',', ''));
    const totalGST = totalInclValue - totalExclValue;
    
    // Generate items table rows
    const itemsRows = items.map(item => `
        <tr>
            <td class="col-item">${item.item}</td>
            <td class="col-reference">${item.reference}</td>
            <td class="col-description">${item.product}</td>
            <td class="col-quantity">${item.quantity}</td>
            <td class="col-length">${item.length}</td>
            <td class="col-width">${item.width}</td>
            <td class="col-unit-price">${item.cost}</td>
            <td class="col-total">${item.cost}</td>
        </tr>
    `).join('');
    
    return `
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Quote ${quoteNumber}</title>
        <style>
            /* Quote PDF Styling - Based on Outcry_Quote_Template.docx */
            @page {
                size: A4;
                margin: 2cm 1.5cm;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Arial', sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #333;
                background: white;
            }
            
            /* Header Section */
            .quote-header {
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #2c5aa0;
                padding-bottom: 20px;
            }
            
            .company-name {
                font-size: 24pt;
                font-weight: bold;
                color: #2c5aa0;
                margin-bottom: 5px;
                letter-spacing: 1px;
            }
            
            .company-tagline {
                font-size: 12pt;
                color: #666;
                font-style: italic;
                margin-bottom: 10px;
            }
            
            .company-details {
                font-size: 10pt;
                color: #555;
                line-height: 1.3;
            }
            
            /* Quote Title */
            .quote-title {
                text-align: center;
                font-size: 20pt;
                font-weight: bold;
                color: #2c5aa0;
                margin: 30px 0 20px 0;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            /* Quote Information Section */
            .quote-info {
                display: table;
                width: 100%;
                margin-bottom: 25px;
            }
            
            .quote-info-left,
            .quote-info-right {
                display: table-cell;
                width: 50%;
                vertical-align: top;
            }
            
            .quote-info-right {
                text-align: right;
            }
            
            .info-group {
                margin-bottom: 15px;
            }
            
            .info-label {
                font-weight: bold;
                color: #2c5aa0;
                font-size: 10pt;
                margin-bottom: 3px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .info-value {
                font-size: 11pt;
                color: #333;
                margin-bottom: 8px;
            }
            
            /* Client Information */
            .client-section {
                margin-bottom: 25px;
                padding: 15px;
                background-color: #f8f9fa;
                border-left: 4px solid #2c5aa0;
            }
            
            .client-title {
                font-size: 14pt;
                font-weight: bold;
                color: #2c5aa0;
                margin-bottom: 10px;
                text-transform: uppercase;
            }
            
            .client-details {
                font-size: 11pt;
                line-height: 1.4;
            }
            
            /* Items Table */
            .items-section {
                margin-bottom: 30px;
            }
            
            .items-title {
                font-size: 14pt;
                font-weight: bold;
                color: #2c5aa0;
                margin-bottom: 15px;
                text-transform: uppercase;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5px;
            }
            
            .items-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                font-size: 10pt;
            }
            
            .items-table th {
                background-color: #2c5aa0;
                color: white;
                font-weight: bold;
                padding: 12px 8px;
                text-align: left;
                text-transform: uppercase;
                font-size: 9pt;
                letter-spacing: 0.5px;
            }
            
            .items-table td {
                padding: 10px 8px;
                border-bottom: 1px solid #ddd;
                vertical-align: top;
            }
            
            .items-table tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            
            /* Table column widths */
            .col-item { width: 8%; }
            .col-reference { width: 12%; }
            .col-description { width: 35%; }
            .col-quantity { width: 8%; text-align: center; }
            .col-length { width: 8%; text-align: center; }
            .col-width { width: 8%; text-align: center; }
            .col-unit-price { width: 10%; text-align: right; }
            .col-total { width: 11%; text-align: right; }
            
            /* Totals Section */
            .totals-section {
                margin-top: 20px;
                margin-left: auto;
                width: 300px;
            }
            
            .totals-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 11pt;
            }
            
            .totals-table td {
                padding: 8px 12px;
                border-bottom: 1px solid #ddd;
            }
            
            .totals-table .total-label {
                font-weight: bold;
                color: #2c5aa0;
                text-align: right;
                width: 60%;
            }
            
            .totals-table .total-value {
                text-align: right;
                font-weight: bold;
                width: 40%;
            }
            
            .totals-table .final-total {
                background-color: #2c5aa0;
                color: white;
                font-size: 12pt;
                font-weight: bold;
            }
            
            .totals-table .final-total .total-label,
            .totals-table .final-total .total-value {
                color: white;
            }
            
            /* Notes Section */
            .notes-section {
                margin-top: 30px;
                padding: 15px;
                background-color: #f8f9fa;
                border-left: 4px solid #2c5aa0;
            }
            
            .notes-title {
                font-size: 12pt;
                font-weight: bold;
                color: #2c5aa0;
                margin-bottom: 10px;
                text-transform: uppercase;
            }
            
            .notes-content {
                font-size: 10pt;
                line-height: 1.4;
                color: #555;
            }
            
            /* Terms and Conditions */
            .terms-section {
                margin-top: 25px;
                font-size: 9pt;
                color: #666;
                line-height: 1.3;
            }
            
            .terms-title {
                font-weight: bold;
                color: #2c5aa0;
                margin-bottom: 8px;
                text-transform: uppercase;
            }
            
            /* Footer */
            .quote-footer {
                margin-top: 40px;
                text-align: center;
                font-size: 9pt;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 15px;
            }
            
            .footer-text {
                margin-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <!-- Header Section -->
        <div class="quote-header">
            <div class="company-name">OUTCRY</div>
            <div class="company-tagline">Professional Signage Solutions</div>
            <div class="company-details">
                123 Business Street, City, State 12345<br>
                Phone: (02) 1234 5678 | Email: info@outcry.com.au
            </div>
        </div>
        
        <!-- Quote Title -->
        <div class="quote-title">Quote</div>
        
        <!-- Quote Information -->
        <div class="quote-info">
            <div class="quote-info-left">
                <div class="info-group">
                    <div class="info-label">Quote Number</div>
                    <div class="info-value">${quoteNumber}</div>
                </div>
                <div class="info-group">
                    <div class="info-label">Job Number</div>
                    <div class="info-value">${jobNumber}</div>
                </div>
                <div class="info-group">
                    <div class="info-label">Project</div>
                    <div class="info-value">${projectName}</div>
                </div>
                <div class="info-group">
                    <div class="info-label">Reference</div>
                    <div class="info-value">${jobReference}</div>
                </div>
            </div>
            <div class="quote-info-right">
                <div class="info-group">
                    <div class="info-label">Date</div>
                    <div class="info-value">${quoteDate}</div>
                </div>
                <div class="info-group">
                    <div class="info-label">Valid Until</div>
                    <div class="info-value">${new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toLocaleDateString('en-AU')}</div>
                </div>
            </div>
        </div>
        
        <!-- Client Information -->
        <div class="client-section">
            <div class="client-title">Client Information</div>
            <div class="client-details">
                <strong>${clientName}</strong><br>
                ${currentJob && currentJob.client_address ? currentJob.client_address + '<br>' : ''}
                ${currentJob && currentJob.client_suburb ? currentJob.client_suburb + ', ' : ''}
                ${currentJob && currentJob.client_state ? currentJob.client_state + ' ' : ''}
                ${currentJob && currentJob.client_postcode ? currentJob.client_postcode : ''}
            </div>
        </div>
        
        <!-- Items Section -->
        <div class="items-section">
            <div class="items-title">Quote Items</div>
            <table class="items-table">
                <thead>
                    <tr>
                        <th class="col-item">Item</th>
                        <th class="col-reference">Reference</th>
                        <th class="col-description">Description</th>
                        <th class="col-quantity">Qty</th>
                        <th class="col-length">Length</th>
                        <th class="col-width">Width</th>
                        <th class="col-unit-price">Unit Price</th>
                        <th class="col-total">Total</th>
                    </tr>
                </thead>
                <tbody>
                    ${itemsRows}
                </tbody>
            </table>
        </div>
        
        <!-- Totals Section -->
        <div class="totals-section">
            <table class="totals-table">
                <tr>
                    <td class="total-label">Subtotal (Excl. GST):</td>
                    <td class="total-value">${totalExclGST}</td>
                </tr>
                <tr>
                    <td class="total-label">GST (10%):</td>
                    <td class="total-value">$${totalGST.toFixed(2)}</td>
                </tr>
                <tr class="final-total">
                    <td class="total-label">Total (Incl. GST):</td>
                    <td class="total-value">${totalInclGST}</td>
                </tr>
            </table>
        </div>
        
        <!-- Notes Section -->
        <div class="notes-section">
            <div class="notes-title">Notes</div>
            <div class="notes-content">
                • All prices are in Australian Dollars (AUD)<br>
                • GST is included where applicable<br>
                • Installation and delivery charges may apply<br>
                • Materials and specifications subject to client approval
            </div>
        </div>
        
        <!-- Terms and Conditions -->
        <div class="terms-section">
            <div class="terms-title">Terms and Conditions</div>
            <div>
                • This quote is valid for 30 days from the date of issue<br>
                • Payment terms: 50% deposit required to commence work, balance on completion<br>
                • All work is guaranteed for 12 months against manufacturing defects<br>
                • Client approval required before production commences<br>
                • Delivery times are estimates and may vary depending on materials and complexity
            </div>
        </div>
        
        <!-- Footer -->
        <div class="quote-footer">
            <div class="footer-text">Thank you for choosing Outcry for your signage needs</div>
            <div class="footer-text">For any questions regarding this quote, please contact us on (02) 1234 5678</div>
        </div>
    </body>
    </html>
    `;
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

// Helper function to safely set currentSelectedProduct with logging
function setCurrentSelectedProduct(product) {
    console.log('Setting currentSelectedProduct from:', currentSelectedProduct, 'to:', product);
    currentSelectedProduct = product;
    console.log('currentSelectedProduct is now:', currentSelectedProduct);
}

// DOM elements
const itemsContainer = document.getElementById('itemsContainer');
const itemTemplate = document.getElementById('itemTemplate');

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Get job ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    currentJobId = urlParams.get('jobId');
    const quoteId = urlParams.get('quoteId');
    
    if (currentJobId) {
        // Creating a new quote for a job
        loadJobData();
        loadCategories();
        loadAllProducts();
    } else if (quoteId) {
        // Loading an existing quote
        loadExistingQuote(quoteId);
    } else {
        showNotification('No job ID or quote ID provided', 'error');
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
                try {
                    await addItemFromData(item);
                } catch (itemError) {
                    console.error(`Error loading item ${item.item_id}:`, itemError);
                    // Continue loading other items even if one fails
                }
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
    const widthInput = itemRow.querySelector('.item-length');  // Frontend "Width" maps to database "length"
    const heightInput = itemRow.querySelector('.item-height');  // Frontend "Height" maps to database "height"
    
    [quantityInput, widthInput, heightInput].forEach(input => {
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
    itemRow.querySelector('.item-length').value = itemData.length || '';  // Frontend "Width" field gets database "length" value
    itemRow.querySelector('.item-height').value = itemData.height || '';
    itemRow.querySelector('.item-quantity').value = itemData.quantity || 1;
    itemRow.querySelector('.item-notes').value = itemData.notes || '';
    itemRow.querySelector('.item-cost-excl').value = itemData.cost_excl_gst || '';
    
    // Update item footer cost display
    const costExclGST = parseFloat(itemData.cost_excl_gst) || 0;
    updateItemFooterCost(itemRow, costExclGST);
    
    // Add to items data array
    itemsData.push({
        item_id: itemData.item_id,
        product_id: itemData.product_id,
        reference: itemData.reference,
        length: itemData.length,
        height: itemData.height,
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
    const widthInput = itemRow.querySelector('.item-length');  // Frontend "Width" maps to database "length"
    const heightInput = itemRow.querySelector('.item-height');  // Frontend "Height" maps to database "height"
    
    [quantityInput, widthInput, heightInput].forEach(input => {
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
    const widthField = itemRow.querySelector('.item-length').closest('.form-group');  // Frontend "Width" field
    const heightField = itemRow.querySelector('.item-height').closest('.form-group');  // Frontend "Height" field
    const quantityField = itemRow.querySelector('.item-quantity').closest('.form-group');
    const widthLabel = widthField.querySelector('label');
    const heightLabel = heightField.querySelector('label');
    
    if (!product || !product.measure_type_id) {
        // Show all fields if no product or measure type
        widthField.style.display = 'block';
        heightField.style.display = 'block';
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        heightLabel.textContent = 'Height (m)';
        return;
    }
    
    // Hide all fields first
    widthField.style.display = 'none';
    heightField.style.display = 'none';
    quantityField.style.display = 'none';
    
    // Show fields based on measure type
    if (product.measure_type_id === 1) {
        // Area (Width × Height × Quantity)
        widthField.style.display = 'block';
        heightField.style.display = 'block';
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        heightLabel.textContent = 'Height (m)';
    } else if (product.measure_type_id === 2) {
        // Linear (Length × Quantity)
        widthField.style.display = 'block';
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Length (m)';
        heightLabel.textContent = 'Height (m)';
    } else if (product.measure_type_id === 3) {
        // Quantity Only
        quantityField.style.display = 'block';
        widthLabel.textContent = 'Width (m)';
        heightLabel.textContent = 'Height (m)';
    }
}

// Reset measurement fields visibility (show all)
function resetMeasurementFieldsVisibility(itemRow) {
    const widthField = itemRow.querySelector('.item-length').closest('.form-group');  // Frontend "Width" field
    const heightField = itemRow.querySelector('.item-height').closest('.form-group');  // Frontend "Height" field
    const quantityField = itemRow.querySelector('.item-quantity').closest('.form-group');
    const widthLabel = widthField.querySelector('label');
    const heightLabel = heightField.querySelector('label');
    
    heightField.style.display = 'block';
    widthField.style.display = 'block';
    quantityField.style.display = 'block';
    widthLabel.textContent = 'Width (m)';
    heightLabel.textContent = 'Height (m)';
}

// Handle manual cost changes
function handleManualCostChange(itemRow, type) {
    const costExclInput = itemRow.querySelector('.item-cost-excl');
    
    const costExcl = parseFloat(costExclInput.value) || 0;
    
    if (type === 'excl') {
        // When excluding GST is changed, update item footer cost display
        
        // Update item footer cost display
        updateItemFooterCost(itemRow, costExcl);
    }
    
    updateTotals();
}

// Calculate item cost
async function calculateItemCost(itemRow) {
    const quantity = parseFloat(itemRow.querySelector('.item-quantity').value) || 0;
    const width = parseFloat(itemRow.querySelector('.item-length').value) || 0;  // Frontend "Width" field
    const height = parseFloat(itemRow.querySelector('.item-height').value) || 0;  // Frontend "Height" field
    
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
        updateItemFooterCost(itemRow, currentCostExcl);
        
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
                // Area (Width × Height × Quantity)
                optionCost = option.base_cost + (option.multiplier_cost * width * height * quantity);
            } else if (selectedProduct.measure_type_id === 2) {
                // Linear (Width × Quantity)
                optionCost = option.base_cost + (option.multiplier_cost * width * quantity);
            } else if (selectedProduct.measure_type_id === 3) {
                // Quantity Only
                optionCost = option.base_cost + (option.multiplier_cost * quantity);
            } else {
                // Fallback to original formula if no measure type is set (Area formula)
                optionCost = option.base_cost + (option.multiplier_cost * width * height * quantity);
            }
            
            totalCostExclGST += optionCost;
        });
        
        // Calculate GST (10%)
        const totalCostInclGST = totalCostExclGST * 1.1;
        
        itemRow.querySelector('.item-cost-excl').value = totalCostExclGST.toFixed(2);
        
        // Update item footer cost display
        updateItemFooterCost(itemRow, totalCostExclGST);
        
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
function updateItemFooterCost(itemRow, costExclGST) {
    const costValueElement = itemRow.querySelector('.item-cost-value');
    if (costValueElement) {
        // Format number with comma separators for thousands
        const formattedCost = costExclGST.toLocaleString('en-US', {
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
        const length = parseFloat(itemRow.querySelector('.item-length').value) || 0;  // Frontend "Width" field maps to database "length"
        const height = parseFloat(itemRow.querySelector('.item-height').value) || 0;  // Frontend "Height" field maps to database "height"
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
                height: height,  // Frontend "Height" field maps to database "height"
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
    
    // Validate all items have required data
    for (let i = 0; i < itemsData.length; i++) {
        if (!itemsData[i].product_id) {
            showNotification(`Item ${i + 1} is missing a product selection`, 'error');
            return;
        }
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
        
        // Create all new items first (before deleting old ones)
        const createdItems = [];
        for (const itemData of itemsData) {
            const itemResponse = await fetch(`${API_BASE_URL}/items`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    quote_id: quote.quote_id,
                    product_id: itemData.product_id,
                    reference: itemData.reference,
                    length: itemData.length,
                    height: itemData.height,
                    quantity: itemData.quantity,
                    notes: itemData.notes,
                    cost_excl_gst: itemData.cost_excl_gst,
                    cost_incl_gst: itemData.cost_incl_gst
                })
            });
            
            if (itemResponse.ok) {
                const item = await itemResponse.json();
                createdItems.push({ item: item, variables: itemData.variables });
                
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
                // If creating a new item fails, delete all items we just created and abort
                for (const created of createdItems) {
                    await fetch(`${API_BASE_URL}/items/${created.item.item_id}`, { method: 'DELETE' });
                }
                throw new Error('Failed to create item');
            }
        }
        
        // Only delete old items after all new items are successfully created
        if (currentQuoteId) {
            const existingItemsResponse = await fetch(`${API_BASE_URL}/items?quote_id=${currentQuoteId}`);
            if (existingItemsResponse.ok) {
                const existingItems = await existingItemsResponse.json();
                // Don't delete items we just created
                const newItemIds = createdItems.map(ci => ci.item.item_id);
                for (const item of existingItems) {
                    if (!newItemIds.includes(item.item_id)) {
                        await fetch(`${API_BASE_URL}/items/${item.item_id}`, {
                            method: 'DELETE'
                        });
                    }
                }
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
