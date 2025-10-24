from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from database import engine, SessionLocal
from models import Product, ProductCategory, ProductVariable, VariableOption, Quote, Client, Contact, Billing, Job, Project, JobStatus, JobStatusHistory, Staff, Item, ItemVariable, ItemVariableOption, MeasureType, Address, Booking, Attachment
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database session
def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

# Routes for serving HTML pages
@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/products')
def products():
    return render_template_string(open('products.html').read())

@app.route('/clients')
def clients():
    return render_template_string(open('clients.html').read())

@app.route('/jobs')
def jobs():
    return render_template_string(open('jobs.html').read())

@app.route('/staff')
def staff():
    return render_template_string(open('staff.html').read())

@app.route('/quote')
def quote():
    return render_template_string(open('quote.html').read())

@app.route('/projects')
def projects():
    return render_template_string(open('projects.html').read())

@app.route('/workflow')
def workflow():
    return render_template_string(open('workflow.html').read())

@app.route('/outcry-express-mobile')
def outcry_express_mobile():
    return render_template_string(open('outcry_express_mobile.html').read())

@app.route('/outcry-express-new-booking')
def outcry_express_new_booking():
    return render_template_string(open('outcry_express_new_booking.html').read())

@app.route('/outcry-express-login')
def outcry_express_login():
    return render_template_string(open('outcry_express_login.html').read())




# API Routes for Product Categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    db = get_db()
    try:
        categories = db.query(ProductCategory).all()
        return jsonify([{
            'product_category_id': cat.product_category_id,
            'name': cat.name
        } for cat in categories])
    finally:
        db.close()

@app.route('/api/categories', methods=['POST'])
def create_category():
    db = get_db()
    try:
        data = request.json
        new_category = ProductCategory(name=data['name'])
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return jsonify({
            'product_category_id': new_category.product_category_id,
            'name': new_category.name
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    db = get_db()
    try:
        category = db.query(ProductCategory).filter(ProductCategory.product_category_id == category_id).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        data = request.json
        category.name = data['name']
        db.commit()
        
        return jsonify({
            'product_category_id': category.product_category_id,
            'name': category.name
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    db = get_db()
    try:
        category = db.query(ProductCategory).filter(ProductCategory.product_category_id == category_id).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if category has products
        if category.products:
            return jsonify({'error': 'Cannot delete category with existing products'}), 400
        
        db.delete(category)
        db.commit()
        return jsonify({'message': 'Category deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Measure Types
@app.route('/api/measure-types', methods=['GET'])
def get_measure_types():
    db = get_db()
    try:
        measure_types = db.query(MeasureType).all()
        return jsonify([{
            'measure_type_id': mt.measure_type_id,
            'measure_type': mt.measure_type
        } for mt in measure_types])
    finally:
        db.close()

# API Routes for Products
@app.route('/api/products', methods=['GET'])
def get_products():
    db = get_db()
    try:
        products = db.query(Product).all()
        result = []
        for product in products:
            product_data = {
                'product_id': product.product_id,
                'name': product.name,
                'base_cost': 0.0,  # Default value since column doesn't exist
                'multiplier_cost': 0.0,  # Default value since column doesn't exist
                'product_category_id': product.product_category_id,
                'category_name': product.category.name if product.category else None,
                'measure_type_id': product.measure_type_id,
                'measure_type_name': product.measure_type.measure_type if product.measure_type else None,
                'variables': []
            }
            
            for variable in product.variables:
                variable_data = {
                    'product_variable_id': variable.product_variable_id,
                    'name': variable.name,
                    'base_cost': 0.0,  # Default value since column doesn't exist
                    'multiplier_cost': 0.0,  # Default value since column doesn't exist
                    'data_type': variable.data_type,
                    'options': []
                }
                
                for option in variable.options:
                    option_data = {
                        'variable_option_id': option.variable_option_id,
                        'name': option.name,
                        'base_cost': float(option.base_cost),
                        'multiplier_cost': float(option.multiplier_cost)
                    }
                    variable_data['options'].append(option_data)
                
                product_data['variables'].append(variable_data)
            
            result.append(product_data)
        
        return jsonify(result)
    finally:
        db.close()

@app.route('/api/products', methods=['POST'])
def create_product():
    db = get_db()
    try:
        data = request.json
        new_product = Product(
            name=data['name'],
            product_category_id=data['product_category_id'],
            measure_type_id=data.get('measure_type_id')
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return jsonify({
            'product_id': new_product.product_id,
            'name': new_product.name,
            'base_cost': 0.0,  # Default value since column doesn't exist
            'multiplier_cost': 0.0,  # Default value since column doesn't exist
            'product_category_id': new_product.product_category_id,
            'measure_type_id': new_product.measure_type_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    db = get_db()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.json
        product.name = data['name']
        product.product_category_id = data['product_category_id']
        product.measure_type_id = data.get('measure_type_id')
        
        db.commit()
        
        return jsonify({
            'product_id': product.product_id,
            'name': product.name,
            'base_cost': 0.0,  # Default value since column doesn't exist
            'multiplier_cost': 0.0,  # Default value since column doesn't exist
            'product_category_id': product.product_category_id,
            'measure_type_id': product.measure_type_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    db = get_db()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # First, delete all variable options for this product's variables
        variables = db.query(ProductVariable).filter(ProductVariable.product_id == product_id).all()
        for variable in variables:
            # Delete all options for this variable
            db.query(VariableOption).filter(VariableOption.product_variable_id == variable.product_variable_id).delete()
        
        # Then delete all variables for this product
        db.query(ProductVariable).filter(ProductVariable.product_id == product_id).delete()
        
        # Finally delete the product
        db.delete(product)
        db.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Product Variables
@app.route('/api/variables', methods=['POST'])
def create_variable():
    db = get_db()
    try:
        data = request.json
        new_variable = ProductVariable(
            name=data['name'],
            data_type=data['data_type'],
            product_id=data['product_id']
        )
        db.add(new_variable)
        db.commit()
        db.refresh(new_variable)
        
        return jsonify({
            'product_variable_id': new_variable.product_variable_id,
            'name': new_variable.name,
            'base_cost': 0.0,  # Default value since column doesn't exist
            'multiplier_cost': 0.0,  # Default value since column doesn't exist
            'data_type': new_variable.data_type,
            'product_id': new_variable.product_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/variables/<int:variable_id>', methods=['DELETE'])
def delete_variable(variable_id):
    db = get_db()
    try:
        variable = db.query(ProductVariable).filter(ProductVariable.product_variable_id == variable_id).first()
        if not variable:
            return jsonify({'error': 'Variable not found'}), 404
        
        # First delete all options for this variable
        db.query(VariableOption).filter(VariableOption.product_variable_id == variable_id).delete()
        
        # Then delete the variable
        db.delete(variable)
        db.commit()
        return jsonify({'message': 'Variable deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/variables/<int:variable_id>', methods=['PUT'])
def update_variable(variable_id):
    db = get_db()
    try:
        variable = db.query(ProductVariable).filter(ProductVariable.product_variable_id == variable_id).first()
        if not variable:
            return jsonify({'error': 'Variable not found'}), 404
        
        data = request.json
        variable.name = data['name']
        variable.data_type = data['data_type']
        
        db.commit()
        
        return jsonify({
            'product_variable_id': variable.product_variable_id,
            'name': variable.name,
            'base_cost': 0.0,  # Default value since column doesn't exist
            'multiplier_cost': 0.0,  # Default value since column doesn't exist
            'data_type': variable.data_type,
            'product_id': variable.product_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Variable Options
@app.route('/api/options', methods=['POST'])
def create_option():
    db = get_db()
    try:
        data = request.json
        new_option = VariableOption(
            name=data['name'],
            base_cost=data['base_cost'],
            multiplier_cost=data['multiplier_cost'],
            product_variable_id=data['product_variable_id']
        )
        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        
        return jsonify({
            'variable_option_id': new_option.variable_option_id,
            'name': new_option.name,
            'base_cost': float(new_option.base_cost),
            'multiplier_cost': float(new_option.multiplier_cost),
            'product_variable_id': new_option.product_variable_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/options/<int:option_id>', methods=['PUT'])
def update_option(option_id):
    db = get_db()
    try:
        option = db.query(VariableOption).filter(VariableOption.variable_option_id == option_id).first()
        if not option:
            return jsonify({'error': 'Option not found'}), 404
        
        data = request.json
        option.name = data['name']
        option.base_cost = data['base_cost']
        option.multiplier_cost = data['multiplier_cost']
        
        db.commit()
        
        return jsonify({
            'variable_option_id': option.variable_option_id,
            'name': option.name,
            'base_cost': float(option.base_cost),
            'multiplier_cost': float(option.multiplier_cost),
            'product_variable_id': option.product_variable_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/options/<int:option_id>', methods=['DELETE'])
def delete_option(option_id):
    db = get_db()
    try:
        option = db.query(VariableOption).filter(VariableOption.variable_option_id == option_id).first()
        if not option:
            return jsonify({'error': 'Option not found'}), 404
        
        db.delete(option)
        db.commit()
        return jsonify({'message': 'Option deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Clients
@app.route('/api/clients', methods=['GET'])
def get_clients():
    db = get_db()
    try:
        clients = db.query(Client).all()
        result = []
        for client in clients:
            client_data = {
                'client_id': client.client_id,
                'name': client.name,
                'address': client.address,
                'suburb': client.suburb,
                'state': client.state,
                'postcode': client.postcode,
                'contacts': [],
                'billing': []
            }
            
            # Add contacts
            for contact in client.contacts:
                contact_data = {
                    'contact_id': contact.contact_id,
                    'first_name': contact.first_name,
                    'surname': contact.surname,
                    'email': contact.email,
                    'phone': contact.phone,
                    'client_id': contact.client_id
                }
                client_data['contacts'].append(contact_data)
            
            # Add billing
            for bill in client.billing:
                billing_data = {
                    'billing_id': bill.billing_id,
                    'entity': bill.entity,
                    'address': bill.address,
                    'suburb': bill.suburb,
                    'state': bill.state,
                    'postcode': bill.postcode
                }
                client_data['billing'].append(billing_data)
            
            result.append(client_data)
        
        return jsonify(result)
    finally:
        db.close()

@app.route('/api/clients', methods=['POST'])
def create_client():
    db = get_db()
    try:
        data = request.json
        new_client = Client(
            name=data['name'],
            address=data.get('address'),
            suburb=data.get('suburb'),
            state=data.get('state'),
            postcode=data.get('postcode')
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        
        return jsonify({
            'client_id': new_client.client_id,
            'name': new_client.name,
            'address': new_client.address,
            'suburb': new_client.suburb,
            'state': new_client.state,
            'postcode': new_client.postcode
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    db = get_db()
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        data = request.json
        client.name = data.get('name', client.name)
        client.address = data.get('address', client.address)
        client.suburb = data.get('suburb', client.suburb)
        client.state = data.get('state', client.state)
        client.postcode = data.get('postcode', client.postcode)
        
        db.commit()
        
        return jsonify({
            'client_id': client.client_id,
            'name': client.name,
            'address': client.address,
            'suburb': client.suburb,
            'state': client.state,
            'postcode': client.postcode
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    db = get_db()
    try:
        client = db.query(Client).filter(Client.client_id == client_id).first()
        if not client:
            return jsonify({'error': 'Client not found'}), 404
        
        db.delete(client)
        db.commit()
        return jsonify({'message': 'Client deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Contacts
@app.route('/api/contacts', methods=['POST'])
def create_contact():
    db = get_db()
    try:
        data = request.json
        new_contact = Contact(
            first_name=data['first_name'],
            surname=data['surname'],
            email=data.get('email'),
            phone=data.get('phone'),
            client_id=data['client_id']
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        
        return jsonify({
            'contact_id': new_contact.contact_id,
            'first_name': new_contact.first_name,
            'surname': new_contact.surname,
            'email': new_contact.email,
            'phone': new_contact.phone,
            'client_id': new_contact.client_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    db = get_db()
    try:
        contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        data = request.json
        contact.first_name = data.get('first_name', contact.first_name)
        contact.surname = data.get('surname', contact.surname)
        contact.email = data.get('email', contact.email)
        contact.phone = data.get('phone', contact.phone)
        
        db.commit()
        
        return jsonify({
            'contact_id': contact.contact_id,
            'first_name': contact.first_name,
            'surname': contact.surname,
            'email': contact.email,
            'phone': contact.phone,
            'client_id': contact.client_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    db = get_db()
    try:
        contact = db.query(Contact).filter(Contact.contact_id == contact_id).first()
        if not contact:
            return jsonify({'error': 'Contact not found'}), 404
        
        db.delete(contact)
        db.commit()
        return jsonify({'message': 'Contact deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Billing
@app.route('/api/billing', methods=['POST'])
def create_billing():
    db = get_db()
    try:
        data = request.json
        new_billing = Billing(
            entity=data['entity'],
            address=data.get('address'),
            suburb=data.get('suburb'),
            state=data.get('state'),
            postcode=data.get('postcode'),
            client_id=data['client_id']
        )
        db.add(new_billing)
        db.commit()
        db.refresh(new_billing)
        
        return jsonify({
            'billing_id': new_billing.billing_id,
            'entity': new_billing.entity,
            'address': new_billing.address,
            'suburb': new_billing.suburb,
            'state': new_billing.state,
            'postcode': new_billing.postcode,
            'client_id': new_billing.client_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/billing/<int:billing_id>', methods=['PUT'])
def update_billing(billing_id):
    db = get_db()
    try:
        billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
        if not billing:
            return jsonify({'error': 'Billing not found'}), 404
        
        data = request.json
        billing.entity = data.get('entity', billing.entity)
        billing.address = data.get('address', billing.address)
        billing.suburb = data.get('suburb', billing.suburb)
        billing.state = data.get('state', billing.state)
        billing.postcode = data.get('postcode', billing.postcode)
        
        db.commit()
        
        return jsonify({
            'billing_id': billing.billing_id,
            'entity': billing.entity,
            'address': billing.address,
            'suburb': billing.suburb,
            'state': billing.state,
            'postcode': billing.postcode,
            'client_id': billing.client_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/billing/<int:billing_id>', methods=['DELETE'])
def delete_billing(billing_id):
    db = get_db()
    try:
        billing = db.query(Billing).filter(Billing.billing_id == billing_id).first()
        if not billing:
            return jsonify({'error': 'Billing not found'}), 404
        
        db.delete(billing)
        db.commit()
        return jsonify({'message': 'Billing deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/clients/<int:client_id>/billing-entities', methods=['GET'])
def get_client_billing_entities(client_id):
    db = get_db()
    try:
        billing_entities = db.query(Billing).filter(Billing.client_id == client_id).all()
        result = []
        for billing in billing_entities:
            billing_data = {
                'billing_id': billing.billing_id,
                'entity': billing.entity,
                'address': billing.address,
                'suburb': billing.suburb,
                'state': billing.state,
                'postcode': billing.postcode
            }
            result.append(billing_data)
        return jsonify(result)
    finally:
        db.close()

# API Routes for Jobs
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    db = get_db()
    try:
        jobs = db.query(Job).all()
        result = []
        for job in jobs:
            # Get related data
            client = db.query(Client).filter(Client.client_id == job.client_id).first()
            project = db.query(Project).filter(Project.project_id == job.project_id).first()
            contact = db.query(Contact).filter(Contact.contact_id == job.contact_id).first()
            staff = db.query(Staff).filter(Staff.staff_id == job.staff_id).first()
            job_status = db.query(JobStatus).filter(JobStatus.job_status_id == job.job_status_id).first()
            
            # Get billing information
            billing = None
            if job.billing_entity:
                billing = db.query(Billing).filter(Billing.billing_id == job.billing_entity).first()
            
            # Get all billing entities for this client
            client_billing_entities = db.query(Billing).filter(Billing.client_id == job.client_id).all()
            
            # Get stage due date for this job
            stage_due_date = None
            if job.stage_id:
                from models import ThroughputStageDate
                stage_date = db.query(ThroughputStageDate).filter(
                    ThroughputStageDate.job_id == job.job_id,
                    ThroughputStageDate.status_id == job.stage_id
                ).first()
                stage_due_date = stage_date.due_date.isoformat() if stage_date and stage_date.due_date else None
            
            job_data = {
                            'job_id': job.job_id,
                            'reference': job.reference,
                            'client_id': job.client_id,
                            'project_id': job.project_id,
                            'contact_id': job.contact_id,
                            'staff_id': job.staff_id,
                            'billing_entity': job.billing_entity,
                            'po': job.po,
                            'date_created': job.date_created.isoformat() if job.date_created else None,
                            'job_status_id': job.job_status_id,
                            'job_address': job.job_address,
                            'suburb': job.suburb,
                            'state': job.state,
                            'postcode': job.postcode,
                            'approved_quote': job.approved_quote,
                            'stage_id': job.stage_id,
                            'stage_due_date': stage_due_date,
                            'client_name': client.name if client else None,
                            'project_name': project.name if project else None,
                            'contact_name': f"{contact.first_name} {contact.surname}" if contact else None,
                            'staff_name': f"{staff.first_name} {staff.surname}" if staff else None,
                            'staff_first_name': staff.first_name if staff else None,
                            'staff_surname': staff.surname if staff else None,
                            'staff_email': staff.email if staff else None,
                            'staff_phone': staff.phone if staff else None,
                            'billing_entity_name': billing.entity if billing else None,
                            'billing_address': billing.address if billing else None,
                            'billing_suburb': billing.suburb if billing else None,
                            'billing_state': billing.state if billing else None,
                            'billing_postcode': billing.postcode if billing else None,
                            'billing_contact_name': None,  # Not available in current Billing model
                            'billing_email': None,  # Not available in current Billing model
                            'billing_phone': None,  # Not available in current Billing model
                            'payment_terms': None,  # Not available in current Billing model
                            'invoice_frequency': None,  # Not available in current Billing model
                            'tax_id': None,  # Not available in current Billing model
                            'billing_entities': [
                                {
                                    'billing_id': b.billing_id,
                                    'entity': b.entity,
                                    'address': b.address,
                                    'suburb': b.suburb,
                                    'state': b.state,
                                    'postcode': b.postcode
                                } for b in client_billing_entities
                            ],
                            'job_status': job_status.job_status if job_status else None,
                            'status_history': [],
                            'quotes': []
                        }
            
            # Add status history
            status_history = db.query(JobStatusHistory).filter(JobStatusHistory.job_id == job.job_id).all()
            for history in status_history:
                history_status = db.query(JobStatus).filter(JobStatus.job_status_id == history.job_status_id).first()
                history_data = {
                    'history_id': history.job_status_history_id,
                    'job_status': history_status.job_status if history_status else None,
                    'date': history.date.isoformat() if history.date else None
                }
                job_data['status_history'].append(history_data)
            
            # Add quotes for this job
            quotes = db.query(Quote).filter(Quote.job_id == job.job_id).all()
            for quote in quotes:
                quote_data = {
                    'quote_id': quote.quote_id,
                    'quote_number': quote.quote_number,
                    'date_created': quote.date_created.isoformat() if quote.date_created else None,
                    'cost_excl_gst': float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
                    'cost_incl_gst': float(quote.cost_incl_gst) if quote.cost_incl_gst else None,
                    'items': []
                }
                
                # Add items for this quote
                items = db.query(Item).filter(Item.quote_id == quote.quote_id).all()
                for item in items:
                    # Get product information
                    product = db.query(Product).filter(Product.product_id == item.product_id).first()
                    item_data = {
                        'item_id': item.item_id,
                        'product_id': item.product_id,
                        'product_name': product.name if product else 'Unknown Product',
                        'reference': item.reference,
                        'notes': item.notes,
                        'quantity': float(item.quantity),
                        'length': float(item.length) if item.length else None,
                        'height': float(item.height) if item.height else None,
                        'cost_excl_gst': float(item.cost_excl_gst) if item.cost_excl_gst else None,
                        'cost_incl_gst': float(item.cost_incl_gst) if item.cost_incl_gst else None
                    }
                    quote_data['items'].append(item_data)
                
                job_data['quotes'].append(quote_data)
            
            result.append(job_data)
        
        return jsonify(result)
    finally:
        db.close()

@app.route('/api/jobs', methods=['POST'])
def create_job():
    db = get_db()
    try:
        data = request.json
        new_job = Job(
            reference=data['reference'],
            project_id=data['project_id'],
            client_id=data['client_id'],
            billing_entity=data.get('billing_entity'),
            po=data.get('po'),
            date_created=data.get('date_created'),
            contact_id=data['contact_id'],
            staff_id=data['staff_id'],
            job_status_id=data['job_status_id']
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        
        # Create initial status history
        initial_history = JobStatusHistory(
            job_id=new_job.job_id,
            job_status_id=new_job.job_status_id,
            date=new_job.date_created or datetime.utcnow().date()
        )
        db.add(initial_history)
        db.commit()
        
        return jsonify({
            'job_id': new_job.job_id,
            'reference': new_job.reference,
            'project_id': new_job.project_id,
            'client_id': new_job.client_id,
            'billing_entity': new_job.billing_entity,
            'po': new_job.po,
            'date_created': new_job.date_created.isoformat() if new_job.date_created else None,
            'contact_id': new_job.contact_id,
            'staff_id': new_job.staff_id,
            'job_status_id': new_job.job_status_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    db = get_db()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        data = request.json
        old_status = job.job_status_id
        
        job.reference = data.get('reference', job.reference)
        job.project_id = data.get('project_id', job.project_id)
        job.client_id = data.get('client_id', job.client_id)
        job.billing_entity = data.get('billing_entity', job.billing_entity)
        job.po = data.get('po', job.po)
        job.contact_id = data.get('contact_id', job.contact_id)
        job.staff_id = data.get('staff_id', job.staff_id)
        job.job_status_id = data.get('job_status_id', job.job_status_id)
        
        # Add status history if status changed
        if old_status != job.job_status_id:
            new_history = JobStatusHistory(
                job_id=job.job_id,
                job_status_id=job.job_status_id,
                date=datetime.utcnow().date()
            )
            db.add(new_history)
        
        db.commit()
        
        return jsonify({
            'job_id': job.job_id,
            'reference': job.reference,
            'project_id': job.project_id,
            'client_id': job.client_id,
            'billing_entity': job.billing_entity,
            'po': job.po,
            'date_created': job.date_created.isoformat() if job.date_created else None,
            'contact_id': job.contact_id,
            'staff_id': job.staff_id,
            'job_status_id': job.job_status_id
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db = get_db()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        db.delete(job)
        db.commit()
        return jsonify({'message': 'Job deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Staff
@app.route('/api/staff', methods=['GET'])
def get_staff():
    db = get_db()
    try:
        staff_members = db.query(Staff).all()
        result = []
        for staff_member in staff_members:
            # Get assigned jobs for this staff member
            assigned_jobs = db.query(Job).filter(Job.staff_id == staff_member.staff_id).all()
            jobs_data = []
            for job in assigned_jobs:
                client = db.query(Client).filter(Client.client_id == job.client_id).first()
                project = db.query(Project).filter(Project.project_id == job.project_id).first()
                job_status = db.query(JobStatus).filter(JobStatus.job_status_id == job.job_status_id).first()
                
                job_data = {
                    'job_id': job.job_id,
                    'reference': job.reference,
                    'client_name': client.name if client else None,
                    'project_name': project.name if project else None,
                    'status': job_status.job_status if job_status else None
                }
                jobs_data.append(job_data)
            
            staff_data = {
                'staff_id': staff_member.staff_id,
                'first_name': staff_member.first_name,
                'surname': staff_member.surname,
                'phone': staff_member.phone,
                'address': staff_member.address,
                'suburb': staff_member.suburb,
                'state': staff_member.state,
                'postcode': staff_member.postcode,
                'dob': staff_member.dob.isoformat() if staff_member.dob else None,
                'emergency_contact': staff_member.emergency_contact,
                'emergency_contact_number': staff_member.emergency_contact_number,
                'assigned_jobs': jobs_data
            }
            result.append(staff_data)
        return jsonify(result)
    finally:
        db.close()

@app.route('/api/staff', methods=['POST'])
def create_staff():
    db = get_db()
    try:
        data = request.get_json()
        
        new_staff = Staff(
            first_name=data['first_name'],
            surname=data['surname'],
            phone=data.get('phone'),
            address=data.get('address'),
            suburb=data.get('suburb'),
            state=data.get('state'),
            postcode=data.get('postcode'),
            dob=datetime.strptime(data['dob'], '%Y-%m-%d').date() if data.get('dob') else None,
            emergency_contact=data.get('emergency_contact'),
            emergency_contact_number=data.get('emergency_contact_number')
        )
        
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)
        
        return jsonify({
            'staff_id': new_staff.staff_id,
            'message': 'Staff member created successfully'
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/staff/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    db = get_db()
    try:
        staff_member = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        if not staff_member:
            return jsonify({'error': 'Staff member not found'}), 404
        
        data = request.get_json()
        
        staff_member.first_name = data['first_name']
        staff_member.surname = data['surname']
        staff_member.phone = data.get('phone')
        staff_member.address = data.get('address')
        staff_member.suburb = data.get('suburb')
        staff_member.state = data.get('state')
        staff_member.postcode = data.get('postcode')
        staff_member.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date() if data.get('dob') else None
        staff_member.emergency_contact = data.get('emergency_contact')
        staff_member.emergency_contact_number = data.get('emergency_contact_number')
        
        db.commit()
        
        return jsonify({'message': 'Staff member updated successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/staff/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    db = get_db()
    try:
        staff_member = db.query(Staff).filter(Staff.staff_id == staff_id).first()
        if not staff_member:
            return jsonify({'error': 'Staff member not found'}), 404
        
        # Check if staff member has assigned jobs
        assigned_jobs = db.query(Job).filter(Job.staff_id == staff_id).count()
        if assigned_jobs > 0:
            return jsonify({'error': f'Cannot delete staff member. They have {assigned_jobs} assigned job(s).'}), 400
        
        db.delete(staff_member)
        db.commit()
        
        return jsonify({'message': 'Staff member deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    db = get_db()
    try:
        projects = db.query(Project).all()
        result = []
        for project in projects:
            project_data = {
                'project_id': project.project_id,
                'name': project.name,
                'address': project.address,
                'suburb': project.suburb,
                'state': project.state,
                'postcode': project.postcode,
                'date_created': project.date_created.isoformat() if project.date_created else None
            }
            result.append(project_data)
        return jsonify(result)
    finally:
        db.close()

@app.route('/api/projects', methods=['POST'])
def create_project():
    db = get_db()
    try:
        data = request.json
        new_project = Project(
            name=data['name'],
            address=data.get('address'),
            suburb=data.get('suburb'),
            state=data.get('state'),
            postcode=data.get('postcode')
        )
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        
        return jsonify({
            'project_id': new_project.project_id,
            'name': new_project.name,
            'address': new_project.address,
            'suburb': new_project.suburb,
            'state': new_project.state,
            'postcode': new_project.postcode,
            'date_created': new_project.date_created.isoformat() if new_project.date_created else None
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    db = get_db()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        data = request.json
        project.name = data['name']
        project.address = data.get('address')
        project.suburb = data.get('suburb')
        project.state = data.get('state')
        project.postcode = data.get('postcode')
        
        db.commit()
        
        return jsonify({
            'project_id': project.project_id,
            'name': project.name,
            'address': project.address,
            'suburb': project.suburb,
            'state': project.state,
            'postcode': project.postcode,
            'date_created': project.date_created.isoformat() if project.date_created else None
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    db = get_db()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        db.delete(project)
        db.commit()
        
        return jsonify({'message': 'Project deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/clients/<int:client_id>/projects', methods=['GET'])
def get_client_projects(client_id):
    db = get_db()
    try:
        # Get all projects that have jobs associated with this client
        projects = db.query(Project).join(Job).filter(Job.client_id == client_id).distinct().all()
        result = []
        for project in projects:
            project_data = {
                'project_id': project.project_id,
                'name': project.name,
                'address': project.address,
                'suburb': project.suburb,
                'state': project.state,
                'postcode': project.postcode,
                'date_created': project.date_created.isoformat() if project.date_created else None
            }
            result.append(project_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Job Statuses
@app.route('/api/job-statuses', methods=['GET'])
def get_job_statuses():
    db = get_db()
    try:
        statuses = db.query(JobStatus).all()
        result = []
        for status in statuses:
            status_data = {
                'job_status_id': status.job_status_id,
                'job_status': status.job_status
            }
            result.append(status_data)
        return jsonify(result)
    finally:
        db.close()



# API Routes for Items
@app.route('/api/items', methods=['POST'])
def create_item():
    db = get_db()
    try:
        data = request.json
        new_item = Item(
            quote_id=data['quote_id'],
            product_id=data['product_id'],
            reference=data.get('reference', ''),
            length=data.get('length'),
            height=data.get('height'),
            quantity=data['quantity'],
            notes=data.get('notes'),
            cost_excl_gst=data.get('cost_excl_gst'),
            cost_incl_gst=data.get('cost_incl_gst')
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        return jsonify({
            'item_id': new_item.item_id,
            'quote_id': new_item.quote_id,
            'product_id': new_item.product_id,
            'reference': new_item.reference,
            'length': float(new_item.length) if new_item.length else None,
            'height': float(new_item.height) if new_item.height else None,
            'quantity': float(new_item.quantity),
            'notes': new_item.notes,
            'cost_excl_gst': float(new_item.cost_excl_gst) if new_item.cost_excl_gst else None,
            'cost_incl_gst': float(new_item.cost_incl_gst) if new_item.cost_incl_gst else None
        }), 201
    except Exception as e:
        db.rollback()
        print(f"Error creating item: {str(e)}")
        print(f"Request data: {request.json}")
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Item Variables
@app.route('/api/item-variables', methods=['GET'])
def get_item_variables():
    db = get_db()
    try:
        item_id = request.args.get('item_id', type=int)
        
        if item_id:
            # Get item variables for a specific item
            item_variables = db.query(ItemVariable).filter(ItemVariable.item_id == item_id).all()
        else:
            # Get all item variables
            item_variables = db.query(ItemVariable).all()
        
        result = []
        for item_var in item_variables:
            item_var_data = {
                'item_variable_id': item_var.item_variable_id,
                'item_id': item_var.item_id,
                'product_variable_id': item_var.product_variable_id,
                'variable_option_id': None
            }
            
            # Get the selected option for this item variable
            item_var_option = db.query(ItemVariableOption).filter(
                ItemVariableOption.item_variable_id == item_var.item_variable_id
            ).first()
            
            if item_var_option:
                item_var_data['variable_option_id'] = item_var_option.variable_option_id
            
            result.append(item_var_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/item-variables', methods=['POST'])
def create_item_variable():
    db = get_db()
    try:
        data = request.json
        new_item_variable = ItemVariable(
            item_id=data['item_id'],
            product_variable_id=data['product_variable_id']
        )
        db.add(new_item_variable)
        db.commit()
        db.refresh(new_item_variable)
        
        # Create item variable option if provided
        if 'variable_option_id' in data:
            from models import ItemVariableOption
            new_item_variable_option = ItemVariableOption(
                item_variable_id=new_item_variable.item_variable_id,
                variable_option_id=data['variable_option_id']
            )
            db.add(new_item_variable_option)
            db.commit()
        
        return jsonify({
            'item_variable_id': new_item_variable.item_variable_id,
            'item_id': new_item_variable.item_id,
            'product_variable_id': new_item_variable.product_variable_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# API Routes for Product Variables (for quote page)
@app.route('/api/products/<int:product_id>/variables', methods=['GET'])
def get_product_variables(product_id):
    db = get_db()
    try:
        variables = db.query(ProductVariable).filter(ProductVariable.product_id == product_id).all()
        result = []
        for variable in variables:
            variable_data = {
                'product_variable_id': variable.product_variable_id,
                'name': variable.name,
                'options': []
            }
            
            # Get options for this variable
            options = db.query(VariableOption).filter(VariableOption.product_variable_id == variable.product_variable_id).all()
            for option in options:
                option_data = {
                    'variable_option_id': option.variable_option_id,
                    'name': option.name,
                    'base_cost': float(option.base_cost) if option.base_cost else 0.0,
                    'multiplier_cost': float(option.multiplier_cost) if option.multiplier_cost else 0.0
                }
                variable_data['options'].append(option_data)
            
            result.append(variable_data)
        
        return jsonify(result)
    finally:
        db.close()

# API Routes for Variable Option Costs
@app.route('/api/variable-options/costs', methods=['POST'])
def get_variable_option_costs():
    db = get_db()
    try:
        data = request.json
        option_ids = data.get('option_ids', [])
        
        if not option_ids:
            return jsonify([])
        
        options = db.query(VariableOption).filter(VariableOption.variable_option_id.in_(option_ids)).all()
        result = []
        
        for option in options:
            option_data = {
                'variable_option_id': option.variable_option_id,
                'base_cost': float(option.base_cost),
                'multiplier_cost': float(option.multiplier_cost)
            }
            result.append(option_data)
        
        return jsonify(result)
    finally:
        db.close()

# API Routes for Quotes
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    db = get_db()
    try:
        job_id = request.args.get('job_id', type=int)
        
        if job_id:
            # Get quotes for a specific job using the new job_id field
            quotes = db.query(Quote).filter(Quote.job_id == job_id).all()
        else:
            # Get all quotes
            quotes = db.query(Quote).all()
        
        result = []
        for quote in quotes:
            quote_data = {
                'quote_id': quote.quote_id,
                'quote_number': quote.quote_number,
                'job_id': quote.job_id,
                'date_created': quote.date_created.isoformat() if quote.date_created else None,
                'cost_excl_gst': float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
                'cost_incl_gst': float(quote.cost_incl_gst) if quote.cost_incl_gst else None
            }
            result.append(quote_data)
        
        return jsonify(result)
    finally:
        db.close()

@app.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    db = get_db()
    try:
        quote = db.query(Quote).filter(Quote.quote_id == quote_id).first()
        if not quote:
            return jsonify({'error': 'Quote not found'}), 404
        
        # Get items for this quote
        items = db.query(Item).filter(Item.quote_id == quote_id).all()
        items_data = []
        
        for item in items:
            item_data = {
                'item_id': item.item_id,
                'product_id': item.product_id,
                'reference': item.reference,
                'notes': item.notes,
                'quantity': float(item.quantity),
                'length': float(item.length) if item.length else None,
                'height': float(item.height) if item.height else None,
                'cost_excl_gst': float(item.cost_excl_gst) if item.cost_excl_gst else None,
                'cost_incl_gst': float(item.cost_incl_gst) if item.cost_incl_gst else None
            }
            
            # Get product details
            product = db.query(Product).filter(Product.product_id == item.product_id).first()
            if product:
                item_data['product'] = {
                    'product_id': product.product_id,
                    'name': product.name,
                    'product_category_id': product.product_category_id
                }
            
            items_data.append(item_data)
        
        quote_data = {
            'quote_id': quote.quote_id,
            'quote_number': quote.quote_number,
            'job_id': quote.job_id,
            'date_created': quote.date_created.isoformat() if quote.date_created else None,
            'cost_excl_gst': float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
            'cost_incl_gst': float(quote.cost_incl_gst) if quote.cost_incl_gst else None,
            'items': items_data
        }
        
        return jsonify(quote_data)
    finally:
        db.close()

@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    db = get_db()
    try:
        quote = db.query(Quote).filter(Quote.quote_id == quote_id).first()
        if not quote:
            return jsonify({'error': 'Quote not found'}), 404
        
        data = request.json
        quote.cost_excl_gst = data.get('cost_excl_gst', quote.cost_excl_gst)
        quote.cost_incl_gst = data.get('cost_incl_gst', quote.cost_incl_gst)
        
        db.commit()
        
        return jsonify({
            'quote_id': quote.quote_id,
            'quote_number': quote.quote_number,
            'job_id': quote.job_id,
            'date_created': quote.date_created.isoformat() if quote.date_created else None,
            'cost_excl_gst': float(quote.cost_excl_gst) if quote.cost_excl_gst else None,
            'cost_incl_gst': float(quote.cost_incl_gst) if quote.cost_incl_gst else None
        })
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/items', methods=['GET'])
def get_items():
    db = get_db()
    try:
        quote_id = request.args.get('quote_id', type=int)
        
        if quote_id:
            # Get items for a specific quote
            items = db.query(Item).filter(Item.quote_id == quote_id).all()
        else:
            # Get all items
            items = db.query(Item).all()
        
        items_data = []
        for item in items:
            item_data = {
                'item_id': item.item_id,
                'quote_id': item.quote_id,
                'product_id': item.product_id,
                'reference': item.reference,
                'notes': item.notes,
                'quantity': float(item.quantity),
                'length': float(item.length) if item.length else None,
                'height': float(item.height) if item.height else None,
                'cost_excl_gst': float(item.cost_excl_gst) if item.cost_excl_gst else None,
                'cost_incl_gst': float(item.cost_incl_gst) if item.cost_incl_gst else None
            }
            items_data.append(item_data)
        
        return jsonify(items_data)
    finally:
        db.close()

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    db = get_db()
    try:
        item = db.query(Item).filter(Item.item_id == item_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        db.delete(item)
        db.commit()
        
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

def generate_quote_number(job_id, db):
    """Generate the next quote number for a given job."""
    # Count existing quotes for this job
    existing_quotes = db.query(Quote).filter(Quote.job_id == job_id).count()
    
    # Generate the next quote number (001, 002, 003, etc.)
    next_quote_number = existing_quotes + 1
    
    # Format as job_id-quote_number (e.g., "156-001")
    quote_number = f"{job_id}-{next_quote_number:03d}"
    
    return quote_number

@app.route('/api/quotes', methods=['POST'])
def create_quote():
    db = get_db()
    try:
        data = request.json
        job_id = data.get('job_id')
        
        if not job_id:
            return jsonify({'error': 'job_id is required'}), 400
        
        # Generate quote number
        quote_number = generate_quote_number(job_id, db)
        
        new_quote = Quote(
            quote_number=quote_number,
            job_id=job_id,
            date_created=data.get('date_created', datetime.now().date()),
            cost_excl_gst=data.get('cost_excl_gst', 0.0),
            cost_incl_gst=data.get('cost_incl_gst', 0.0)
        )
        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)
        
        return jsonify({
            'quote_id': new_quote.quote_id,
            'quote_number': new_quote.quote_number,
            'job_id': new_quote.job_id,
            'date_created': new_quote.date_created.isoformat() if new_quote.date_created else None,
            'cost_excl_gst': float(new_quote.cost_excl_gst) if new_quote.cost_excl_gst else None,
            'cost_incl_gst': float(new_quote.cost_incl_gst) if new_quote.cost_incl_gst else None
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Update job status
@app.route('/api/jobs/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    db = get_db()
    try:
        data = request.get_json()
        new_status_id = data.get('job_status_id')
        
        if not new_status_id:
            return jsonify({'error': 'Job status ID is required'}), 400
        
        # Update the job status
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # If changing from Work Order (ID 2) to Quote (ID 1), clear the approved quote
        if job.job_status_id == 2 and new_status_id == 1:
            job.approved_quote = None
        
        job.job_status_id = new_status_id
        
        # Add to status history
        from datetime import datetime
        new_history = JobStatusHistory(
            job_id=job_id,
            job_status_id=new_status_id,
            date=datetime.now()
        )
        db.add(new_history)
        
        db.commit()
        
        return jsonify({'message': 'Job status updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Update job address
@app.route('/api/jobs/<int:job_id>/address', methods=['PUT'])
def update_job_address(job_id):
    db = get_db()
    try:
        data = request.get_json()
        
        # Update the job address fields
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        job.job_address = data.get('job_address')
        job.suburb = data.get('suburb')
        job.state = data.get('state')
        job.postcode = data.get('postcode')
        
        db.commit()
        
        return jsonify({'message': 'Job address updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Update job billing entity
@app.route('/api/jobs/<int:job_id>/billing', methods=['PUT'])
def update_job_billing_entity(job_id):
    db = get_db()
    try:
        data = request.get_json()
        
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        job.billing_entity = data.get('billing_entity')
        
        db.commit()
        
        return jsonify({'message': 'Job billing entity updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/billing', methods=['POST'])
def create_billing_entity():
    db = get_db()
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('client_id'):
            return jsonify({'error': 'Client ID is required'}), 400
        if not data.get('entity'):
            return jsonify({'error': 'Entity name is required'}), 400
        
        # Create new billing entity
        billing_entity = Billing(
            client_id=data['client_id'],
            entity=data['entity'],
            address=data.get('address'),
            suburb=data.get('suburb'),
            state=data.get('state'),
            postcode=data.get('postcode')
        )
        
        db.add(billing_entity)
        db.commit()
        
        return jsonify({
            'billing_id': billing_entity.billing_id,
            'entity': billing_entity.entity,
            'address': billing_entity.address,
            'suburb': billing_entity.suburb,
            'state': billing_entity.state,
            'postcode': billing_entity.postcode
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/jobs/<int:job_id>/approve-quote', methods=['PUT'])
def approve_quote(job_id):
    db = get_db()
    try:
        data = request.get_json()
        approved_quote_id = data.get('approved_quote')
        
        # Find the job
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # If approving a quote, verify it belongs to this job
        if approved_quote_id:
            quote = db.query(Quote).filter(
                Quote.quote_id == approved_quote_id,
                Quote.job_id == job_id
            ).first()
            if not quote:
                return jsonify({'error': 'Quote not found or does not belong to this job'}), 400
        
        # Update the approved quote
        job.approved_quote = approved_quote_id
        
        # If approving a quote, change job status to "Work Order" (ID 2) and stage to "Pre-Production" (ID 1)
        if approved_quote_id:
            job.job_status_id = 2  # Work Order status
            job.stage_id = 1  # Pre-Production stage
        
        db.commit()
        
        return jsonify({'message': 'Quote approval updated successfully'}), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

# Workflow API endpoints
@app.route('/api/stages', methods=['GET'])
def get_stages():
    db = get_db()
    try:
        from models import ThroughputStage
        stages = db.query(ThroughputStage).order_by(ThroughputStage.stage_order).all()
        
        result = []
        for stage in stages:
            stage_data = {
                'stage_id': stage.stage_id,
                'stage': stage.stage,
                'stage_order': stage.stage_order
            }
            result.append(stage_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/jobs/<int:job_id>/stage', methods=['PUT'])
def update_job_stage(job_id):
    db = get_db()
    try:
        data = request.get_json()
        stage_id = data.get('stage_id')
        
        # Find the job
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        # If setting a stage, verify it exists
        if stage_id:
            from models import ThroughputStage
            stage = db.query(ThroughputStage).filter(ThroughputStage.stage_id == stage_id).first()
            if not stage:
                return jsonify({'error': 'Stage not found'}), 400
        
        # Update the job stage
        job.stage_id = stage_id
        db.commit()
        
        return jsonify({'message': 'Job stage updated successfully'}), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/jobs/<int:job_id>/stage-due-date', methods=['PUT'])
def update_stage_due_date(job_id):
    db = get_db()
    try:
        data = request.get_json()
        stage_id = data.get('stage_id')
        due_date = data.get('due_date')
        
        if not stage_id or not due_date:
            return jsonify({'error': 'Stage ID and due date are required'}), 400
        
        # Convert date string to date object
        from datetime import datetime
        due_date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
        
        # Check if stage date already exists
        from models import ThroughputStageDate
        stage_date = db.query(ThroughputStageDate).filter(
            ThroughputStageDate.job_id == job_id,
            ThroughputStageDate.status_id == stage_id
        ).first()
        
        if stage_date:
            # Update existing record
            stage_date.due_date = due_date_obj
        else:
            # Create new record
            new_stage_date = ThroughputStageDate(
                job_id=job_id,
                status_id=stage_id,
                due_date=due_date_obj
            )
            db.add(new_stage_date)
        
        db.commit()
        
        return jsonify({'message': 'Stage due date updated successfully'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/tasks', methods=['POST'])
def create_task():
    db = get_db()
    try:
        data = request.get_json()
        task_name = data.get('task_name')
        job_id = data.get('job_id')
        item_id = data.get('item_id')
        stage_id = data.get('stage_id')
        
        if not all([task_name, job_id, stage_id]):
            return jsonify({'error': 'Task name, job ID, and stage ID are required'}), 400
        
        # Get the next task order for this job and stage
        from models import ThroughputTask, ThroughputStatus
        max_order = db.query(ThroughputTask.task_order).filter(
            ThroughputTask.job_number == job_id,
            ThroughputTask.stage_id == stage_id
        ).order_by(ThroughputTask.task_order.desc()).first()
        
        next_order = (max_order[0] + 1) if max_order else 1
        
        # Get the default status (assuming status_id 1 is "Not Started" or similar)
        default_status = db.query(ThroughputStatus).first()
        if not default_status:
            return jsonify({'error': 'No status found'}), 400
        
        # Create new task
        new_task = ThroughputTask(
            task_name=task_name,
            job_number=job_id,
            item_id=item_id,
            stage_id=stage_id,
            status_id=default_status.status_id,
            task_order=next_order
        )
        
        db.add(new_task)
        db.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task_id': new_task.task_id
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/jobs/<int:job_id>/tasks', methods=['GET'])
def get_job_tasks(job_id):
    db = get_db()
    try:
        from models import ThroughputTask, ThroughputStatus
        stage_id = request.args.get('stage_id')
        
        # Build query
        query = db.query(ThroughputTask).filter(ThroughputTask.job_number == job_id)
        if stage_id:
            query = query.filter(ThroughputTask.stage_id == stage_id)
        
        tasks = query.order_by(ThroughputTask.task_order).all()
        
        # Get status information
        statuses = db.query(ThroughputStatus).all()
        status_map = {s.status_id: s.status for s in statuses}
        
        tasks_data = []
        for task in tasks:
            task_data = {
                'task_id': task.task_id,
                'task_name': task.task_name,
                'job_number': task.job_number,
                'item_id': task.item_id,
                'stage_id': task.stage_id,
                'status_id': task.status_id,
                'status': status_map.get(task.status_id, 'Unknown'),
                'task_order': task.task_order,
                'time_completed': task.time_completed.isoformat() if task.time_completed else None
            }
            tasks_data.append(task_data)
        
        return jsonify(tasks_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    db = get_db()
    try:
        from models import ThroughputTask
        from datetime import datetime
        
        data = request.get_json()
        completed = data.get('completed', False)
        
        # Find the task
        task = db.query(ThroughputTask).filter(ThroughputTask.task_id == task_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        if completed:
            # Mark as completed (status_id = 2)
            task.status_id = 2
            task.time_completed = datetime.now()
        else:
            # Mark as not completed (status_id = 1)
            task.status_id = 1
            task.time_completed = None
        
        db.commit()
        
        return jsonify({
            'message': 'Task status updated successfully',
            'task_id': task.task_id,
            'status_id': task.status_id,
            'time_completed': task.time_completed.isoformat() if task.time_completed else None
        }), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()


# Delivery API Endpoints
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    db = get_db()
    try:
        bookings = db.query(Booking).all()
        result = []
        for booking in bookings:
            booking_data = {
                'booking_id': booking.booking_id,
                'pickup_date': booking.pickup_date.isoformat() if booking.pickup_date else None,
                'pickup_time': booking.pickup_time.isoformat() if booking.pickup_time else None,
                'dropoff_date': booking.dropoff_date.isoformat() if booking.dropoff_date else None,
                'dropoff_time': booking.dropoff_time.isoformat() if booking.dropoff_time else None,
                'notes': booking.notes,
                'job_number': booking.job_number,
                'completion': booking.completion,
                'created': booking.created.isoformat() if booking.created else None,
                'pickup_complete': booking.pickup_complete.isoformat() if booking.pickup_complete else None,
                'dropoff_complete': booking.dropoff_complete.isoformat() if booking.dropoff_complete else None,
                'creator_id': booking.creator_id
            }
            
            # Add pickup address info
            if booking.pickup_address:
                booking_data['pickup_address'] = {
                    'address_id': booking.pickup_address.address_id,
                    'formatted_address': booking.pickup_address.formatted_address,
                    'suburb': booking.pickup_address.suburb
                }
            
            # Add dropoff address info
            if booking.dropoff_address:
                booking_data['dropoff_address'] = {
                    'address_id': booking.dropoff_address.address_id,
                    'formatted_address': booking.dropoff_address.formatted_address,
                    'suburb': booking.dropoff_address.suburb
                }
            
            result.append(booking_data)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()


@app.route('/api/bookings', methods=['POST'])
def create_booking():
    db = get_db()
    try:
        data = request.get_json()
        print(f"Received booking data: {data}")  # Debug log
        
        # Validate required fields
        if not data.get('pickup_date'):
            return jsonify({'error': 'Pickup date is required'}), 400
        if not data.get('dropoff_date'):
            return jsonify({'error': 'Dropoff date is required'}), 400
        
        # Create pickup address if provided
        pickup_address_id = None
        if data.get('pickupAddress'):
            # Extract suburb from pickup address (assuming format: "123 Street, Suburb")
            pickup_address_parts = data['pickupAddress'].split(',')
            pickup_suburb = pickup_address_parts[-1].strip() if len(pickup_address_parts) > 1 else ''
            
            pickup_address = Address(
                formatted_address=data['pickupAddress'],
                suburb=pickup_suburb,
                state='NSW',  # Default state
                postcode='',  # Default postcode
                country='Australia'
            )
            db.add(pickup_address)
            db.flush()  # Get the ID
            pickup_address_id = pickup_address.address_id
        
        # Create dropoff address if provided
        dropoff_address_id = None
        if data.get('dropoffAddress'):
            # Extract suburb from dropoff address (assuming format: "123 Street, Suburb")
            dropoff_address_parts = data['dropoffAddress'].split(',')
            dropoff_suburb = dropoff_address_parts[-1].strip() if len(dropoff_address_parts) > 1 else ''
            
            dropoff_address = Address(
                formatted_address=data['dropoffAddress'],
                suburb=dropoff_suburb,
                state='NSW',  # Default state
                postcode='',  # Default postcode
                country='Australia'
            )
            db.add(dropoff_address)
            db.flush()  # Get the ID
            dropoff_address_id = dropoff_address.address_id
        
        # Parse dates
        pickup_date = datetime.strptime(data['pickup_date'], '%Y-%m-%d').date()
        dropoff_date = datetime.strptime(data['dropoff_date'], '%Y-%m-%d').date()
        
        # Parse times if provided
        pickup_time = None
        if data.get('pickup_time'):
            pickup_time = datetime.strptime(data['pickup_time'], '%H:%M').time()
        
        dropoff_time = None
        if data.get('dropoff_time'):
            dropoff_time = datetime.strptime(data['dropoff_time'], '%H:%M').time()
        
        # Create booking
        booking = Booking(
            pickup_address_id=pickup_address_id,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            dropoff_address_id=dropoff_address_id,
            dropoff_date=dropoff_date,
            dropoff_time=dropoff_time,
            creator_id=data.get('creator_id', 1),  # Default to staff ID 1
            notes=data.get('notes'),
            job_number=data.get('job_number'),
            completion=False
        )
        
        db.add(booking)
        db.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking_id': booking.booking_id
        }), 201
        
    except Exception as e:
        db.rollback()
        print(f"Error creating booking: {str(e)}")  # Debug log
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()


@app.route('/api/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    db = get_db()
    try:
        booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        data = request.get_json()
        
        # Update completion status
        if 'completion' in data:
            booking.completion = data['completion']
        
        # Update pickup completion
        if 'pickup_complete' in data:
            booking.pickup_complete = datetime.now() if data['pickup_complete'] else None
        
        # Update dropoff completion
        if 'dropoff_complete' in data:
            booking.dropoff_complete = datetime.now() if data['dropoff_complete'] else None
        
        db.commit()
        
        return jsonify({
            'message': 'Booking updated successfully',
            'booking_id': booking.booking_id
        }), 200
        
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
                                                                