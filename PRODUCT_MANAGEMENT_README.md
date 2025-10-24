# Product Management System

This system allows you to manage products, their variables, and options in your database through a modern tabbed table interface with popup modals.

## Features

- **Tabbed Category Interface**: Browse products by category using intuitive tabs
- **Product Table View**: Clean table layout showing all product information at a glance
- **Popup Modals**: Click on products to view and manage variables and options in popup windows
- **Product Categories**: Create and manage product categories
- **Products**: Add, edit, and delete products with base costs and multiplier costs
- **Product Variables**: Define variables for each product (e.g., size, material, quantity)
- **Variable Options**: Create specific options for variables (e.g., Small, Medium, Large for size)
- **Real-time Database**: All changes are saved to your database
- **Modern UI**: Clean, responsive interface with modals and notifications

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

If you haven't already set up your database, run:

```bash
python init_db.py
```

### 3. Initialize Sample Data (Optional)

To populate your database with sample data for testing:

```bash
python init_sample_data.py
```

This will create:
- 3 product categories (Signage, Printing, Digital)
- 3 sample products with variables and options
- Sample pricing structures

### 4. Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5001`

### 5. Access the Product Management Page

Navigate to `http://localhost:5001/products` in your web browser.

## How to Use

### Interface Overview

The new interface features:
- **Category Tabs**: Click on tabs to filter products by category
- **Product Table**: View all products in a clean table format
- **Click to View**: Click on any product name to open variables modal
- **Popup Modals**: Manage variables and options in dedicated popup windows

### Managing Product Categories

1. **Add a Category**: Click the "Add Category" button in the header
2. **View Categories**: All categories are displayed as tabs with product counts
3. **Filter by Category**: Click on a category tab to view only products in that category

### Managing Products

1. **Add a Product**: Click "Add Product" and fill in:
   - Product name
   - Category selection
   - Base cost (fixed cost)
   - Multiplier cost (cost per unit)

2. **Edit a Product**: Click the "Edit" button on any product row
3. **Delete a Product**: Click the "Delete" button on any product row
4. **View Variables**: Click on the product name to open the variables modal

### Managing Product Variables

1. **View Variables**: Click on any product name to open the variables modal
2. **Add a Variable**: Click "Add Variable" in the variables modal
3. **Variable Types**:
   - **Text**: Free text input
   - **Number**: Numeric input
   - **Select**: Dropdown with predefined options
   - **Boolean**: True/False selection

4. **Edit a Variable**: Click the "Edit" button next to any variable
5. **Delete a Variable**: Click the "Delete" button next to any variable
6. **View Options**: Click "View Options" to see variable options

### Managing Variable Options

1. **View Options**: Click "View Options" on any variable to open the options modal
2. **Add an Option**: Click "Add Option" in the options modal
3. **Option Pricing**: Each option can have its own base cost and multiplier cost
4. **Edit an Option**: Click the "Edit" button next to any option
5. **Delete an Option**: Click the "Delete" button next to any option

## Database Schema

### ProductCategory
- `product_category_id` (Primary Key)
- `name` (Text)

### Product
- `product_id` (Primary Key)
- `name` (Text)
- `base_cost` (Float)
- `multiplier_cost` (Float)
- `product_category_id` (Foreign Key)

### ProductVariable
- `product_variable_id` (Primary Key)
- `name` (Text)
- `base_cost` (Float)
- `multiplier_cost` (Float)
- `data_type` (Text: text, number, select, boolean)
- `product_id` (Foreign Key)

### VariableOption
- `variable_option_id` (Primary Key)
- `name` (Text)
- `base_cost` (Float)
- `multiplier_cost` (Float)
- `product_variable_id` (Foreign Key)

## API Endpoints

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create a new category
- `PUT /api/categories/{id}` - Update a category
- `DELETE /api/categories/{id}` - Delete a category

### Products
- `GET /api/products` - Get all products with variables and options
- `POST /api/products` - Create a new product
- `PUT /api/products/{id}` - Update a product
- `DELETE /api/products/{id}` - Delete a product

### Variables
- `POST /api/variables` - Create a new variable
- `PUT /api/variables/{id}` - Update a variable
- `DELETE /api/variables/{id}` - Delete a variable

### Options
- `POST /api/options` - Create a new option
- `PUT /api/options/{id}` - Update an option
- `DELETE /api/options/{id}` - Delete an option

## Cost Calculation

The system supports a flexible pricing model:

- **Base Cost**: Fixed cost that applies regardless of quantity
- **Multiplier Cost**: Cost per unit that scales with quantity

For example:
- Product base cost: $25.00
- Product multiplier cost: $0.15
- Variable base cost: $5.00
- Variable multiplier cost: $0.10
- Option base cost: $10.00
- Option multiplier cost: $0.05

Total cost for 10 units = $25.00 + (10 × $0.15) + $5.00 + (10 × $0.10) + $10.00 + (10 × $0.05) = $44.00

## User Interface Features

### Tabbed Navigation
- **All Categories Tab**: Shows all products across all categories
- **Category Tabs**: Individual tabs for each category with product counts
- **Active Tab Highlighting**: Clear visual indication of selected category

### Product Table
- **Product Name**: Clickable links that open variables modal
- **Category**: Shows which category the product belongs to
- **Base Cost**: Fixed cost display
- **Multiplier Cost**: Per-unit cost display
- **Variables Count**: Number of variables for each product
- **Actions**: Edit and delete buttons for each product

### Popup Modals
- **Variables Modal**: Shows all variables for a selected product
- **Options Modal**: Shows all options for a selected variable
- **Form Modals**: Add/edit forms for products, variables, and options
- **Responsive Design**: Modals work well on desktop and mobile

### Interactive Elements
- **Hover Effects**: Visual feedback on interactive elements
- **Confirmation Dialogs**: Safety confirmations for delete operations
- **Success/Error Notifications**: Real-time feedback for all operations
- **Form Validation**: Client-side validation for all inputs

## Troubleshooting

### Common Issues

1. **Server won't start**: Check if port 5001 is available
2. **Database errors**: Ensure your database is properly configured
3. **CORS errors**: The server includes CORS headers, but check browser console for issues
4. **Data not loading**: Check if the Flask server is running and accessible
5. **Modal not opening**: Ensure JavaScript is enabled and no console errors

### Error Messages

- **"Error loading data"**: Server is not running or database connection failed
- **"Failed to add/update/delete"**: Check database constraints and foreign key relationships
- **"Cannot delete category with existing products"**: Remove all products from a category before deleting it
- **"Modal not displaying"**: Check for JavaScript errors in browser console

## Development

### Adding New Features

1. **Backend**: Add new API endpoints in `app.py`
2. **Frontend**: Update `products.js` for new functionality
3. **Database**: Modify `models.py` for new data structures
4. **Styling**: Update `products.css` for new UI elements

### Styling

- Main styles: `styles.css`
- Product-specific styles: `products.css`
- Responsive design included
- Modern CSS with hover effects and transitions

### Testing

1. Start the server: `python app.py`
2. Open `http://localhost:5001/products`
3. Test all CRUD operations:
   - Add/edit/delete categories
   - Add/edit/delete products
   - Add/edit/delete variables
   - Add/edit/delete options
4. Test popup modals and navigation
5. Verify data persistence in database

## Security Notes

- This is a development setup with debug mode enabled
- For production, disable debug mode and add proper authentication
- Consider adding input validation and sanitization
- Implement proper error handling and logging
- Add CSRF protection for forms
- Consider rate limiting for API endpoints
