import base64
import logging
from odoo import http
from odoo.http import request
import json
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)




class CarRentalContractController(http.Controller):
    @http.route('/api/available_cars', type='json', auth='public', methods=['POST'], csrf=False)
    def available_cars(self):
        # Access the raw request data
        raw_data = request.httprequest.data

        # Parse the JSON data
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON data provided.'}

        try:
            start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return {'error': 'Please provide both start_date and end_date in YYYY-MM-DD format.'}


        if not start_date or not end_date:
            return {'error': 'Please provide both start_date and end_date in YYYY-MM-DD format.'}

        # Validate date range
        if start_date >= end_date:
            return {'error': 'start_date must be earlier than end_date.'}

  

        # Get all vehicles that are reserved or rented during the given time frame
        rented_vehicle_ids = request.env['car.rental.contract'].sudo().search([
            ('state', 'in', ['reserved', 'running']),  # Exclude draft, done, and canceled
            ('rent_start_date', '<=', end_date),      # Overlapping contracts
            ('rent_end_date', '>=', start_date)
        ]).mapped('vehicle_id.id')

        # Get all vehicles excluding rented vehicles
        all_vehicles = request.env['fleet.vehicle'].sudo().search([('id', 'not in', rented_vehicle_ids)])

        def has_alert(vehicle):
            # Check Vidange Alert
            if vehicle.kilometrage_vidange <= vehicle.nbr_kilometres_alerte + vehicle.dernier_releve_kilometrique:
                return True

            # Check Assurance Alert
            if vehicle.date_echeance_assurance:
                assurance_alert_date = vehicle.date_echeance_assurance - timedelta(days=vehicle.nbr_jour_alerte_assurance)
                if start_date <= vehicle.date_echeance_assurance and end_date >= assurance_alert_date:
                    return True

            # Check Leasing Alert
            if vehicle.date_echeance_leasing:
                leasing_alert_date = vehicle.date_echeance_leasing - timedelta(days=vehicle.nbr_jours_alerte_leasing)
                if start_date <= vehicle.date_echeance_leasing and end_date >= leasing_alert_date:
                    return True

            # Check Visite Alert
            if vehicle.date_echeance_visite:
                visite_alert_date = vehicle.date_echeance_visite - timedelta(days=vehicle.nbr_jour_alerte_visite)
                if start_date <= vehicle.date_echeance_visite and end_date >= visite_alert_date:
                    return True

            # Check Vignette Alert
            if vehicle.date_echeance_vignette:
                vignette_alert_date = vehicle.date_echeance_vignette - timedelta(days=vehicle.nbr_jour_alerte_vignette)
                if start_date <= vehicle.date_echeance_vignette and end_date >= vignette_alert_date:
                    return True

            return False

        # Filter vehicles without alerts
        available_vehicles = all_vehicles.filtered(lambda v: not has_alert(v))

        # Format response data
        available_cars = [
            {
                'id': vehicle.id,
                'name': vehicle.name,
                'license_plate': vehicle.license_plate,
                'model': vehicle.model_id.name,
                'tarif': vehicle.tarif,
                'picture': vehicle.car_pic,
            }
            for vehicle in available_vehicles
        ]

        return {'available_cars': available_cars, 'status': '200'}
    
    @http.route('/api/contracts_by_email', type='json', auth='public', methods=['POST'], csrf=False)
    def contracts_by_email(self):
        # Access the raw request data
        raw_data = request.httprequest.data

        # Parse the JSON data
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON data provided.'}

        email = data.get('email')

        if not email:
            return {'error': 'Please provide an email in the request body.'}

        # Search for the res.partner (conducteur) with the given email
        conducteur = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)

        if not conducteur:
            return {'error': f'No conducteur found with the email: {email}'}

        # Fetch all contracts where the customer_id matches the conducteur's ID
        contracts = request.env['car.rental.contract'].sudo().search([
            ('customer_id', '=', conducteur.id)
        ])

        # Format response data
        contracts_data = [
            {
                'id': contract.id,
                'name': contract.name,
                'state': contract.state,
                'rent_start_date': contract.rent_start_date,
                'rent_end_date': contract.rent_end_date,
                'vehicle': contract.vehicle_id.name if contract.vehicle_id else None,
                'total_cost': contract.total_cost,
            }
            for contract in contracts
        ]

        return {
            'contracts': contracts_data,
        }
    
    @http.route('/api/payments_by_email', type='json', auth='public', methods=['POST'], csrf=False)
    def payments_by_email(self):
        # Access the raw request data
        raw_data = request.httprequest.data

        # Parse the JSON data
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON data provided.'}

        email = data.get('email')

        if not email:
            return {'error': 'Please provide an email in the request body.'}

        # Search for the res.partner (conducteur) with the given email
        conducteur = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)

        if not conducteur:
            return {'error': f'No conducteur found with the email: {email}'}

        # Fetch all payments where the customer_id matches the conducteur's ID
        payments = request.env['account.payment'].sudo().search([
            ('customer_id', '=', conducteur.id)
        ])

        # Format response data
        payments_data = [
            {
                'id': payment.id,
                'name': payment.name,
                'contract': payment.contract_id.name,
                'amount_notax': payment.no_tax,
                'amount_total': payment.total_amount,
                'date': payment.date,
                'journal': payment.journal_id.name,
            }
            for payment in payments
        ]

        return {
            
            'Payments': payments_data,
        }

    @http.route('/api/create_contract_user', type='json', auth='public', methods=['POST'], csrf=False)
    def create_contract_user(self):
        try :
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            email = data.get('email')
            car_id = data.get('car_id')
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            fuel_level = data.get("fuel_level")


            if not email or not car_id or not start_date or not end_date:
                return {'error': 'Please provide all fields .'}
            
                

            # Search for the res.partner (conducteur) with the given email
            conducteur = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            car= request.env['fleet.vehicle'].sudo().search([('id', '=', car_id)], limit=1)

            if not conducteur:
                return {'error': f'No conducteur found with the id: {email}'}
            if not car:
                return {'error': f'No car found with the car id: {car_id}'}
            
            if fuel_level == '1/4':
                fuel= ('1/4','1/4')

            # Create the rental contract
            contract_vals = {
                'vehicle_id': car.id,
                'customer_id': conducteur.id,
                'rent_start_date': start_date,
                'rent_end_date': end_date,
                'state': 'reserved',  # Default state
                'fuel_level': fuel_level,
                'acompte': 0
            }
            new_contract = request.env['car.rental.contract'].sudo().create(contract_vals)

            return {
                'message': 'Contract created successfully!',
                'contract_id': new_contract.id,
                'contract_name': new_contract.name,
            }

        except Exception as e:
            return {'error': str(e)}
    @http.route('/api/cancel_contract_user', type='json', auth='public', methods=['POST'], csrf=False)
    def cancel_contract_user(self):
        try :
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            email = data.get('email')
            contract_id = data.get('contract_id')
            


            if not email:
                return {'error': 'Please provide an email in the request body.'}
            if not contract_id:
                return {'error': 'Please provide an contract in the request body.'}
       
                

            # Search for the res.partner (conducteur) with the given email
            conducteur = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            contract= request.env['car.rental.contract'].sudo().search([('id', '=', contract_id)], limit=1)

            if not conducteur:
                return {'error': f'No conducteur found with the id: {email}'}
            if not contract:
                return {'error': f'No car found with the car id: {car_id}'}
            

            _logger.debug( contract.customer_id,conducteur.id)

            if contract.customer_id.id != conducteur.id :
                return {'error': f'No car found with the car id: {contract.customer_id,conducteur.id}'}



            # Create the rental contract
            update={"state": "cancel"}
            contract.write(update)

            return {
                'message': 'Contract annulé successfully!',
                
                'contract_name': contract.name,
                'contract_state': contract.state,
            }

        except Exception as e:
            return {'error': str(e)}
        


    @http.route('/api/login_user', type='json', auth='public', methods=['POST'], csrf=False)
    def login_user(self):
        try:
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {'error': 'Please provide both email and password in the request body.'}

            # Search for the res.partner (conducteur) with the given email
            conducteur = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)

            if not conducteur:
                return {'error': f'No conducteur found with the email: {email}'}

            # Validate the password
            if not check_password_hash(conducteur.password, password):
                return {'error': 'Invalid password provided. password'}

            # Limit the fields to be returned
            conducteur_data = conducteur.read([
            'email', 
            
            ])[0]
            if 'id' in conducteur_data:
                del conducteur_data['id']  # Remove the id field
            if 'password' in conducteur_data:
                del conducteur_data['password']  # Remove the id field

            return {
                'message': 'User found and login successfully!',
                'user_data': conducteur_data
            }
        except Exception as e:
            return {'error': str(e)}
        
    @http.route('/api/register_user', type='json', auth='public', methods=['POST'], csrf=False)
    def register_user(self):
        try:
            # Parse incoming data
            raw_data = request.httprequest.data

            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            # Extract and validate required fields
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return {'error': 'Email and password are required.'}

            # Check if the email already exists
            existing_user = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if existing_user:
                return {'error': f"A user with the email {email} already exists."}

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Update the data dictionary to replace password with hashed_password
            data['password'] = hashed_password

            # Extract and process binary fields
            binary_fields = ['profile_pic', 'identity_card_picture', 'drivers_license_picture']
            for binary_field in binary_fields:
                if binary_field in data and isinstance(data[binary_field], str):
                    data[binary_field] = data[binary_field].encode()  # Convert to binary

            # Set default value for `is_conducteur`
            data['is_conducteur'] = True

            # Create the new `res.partner` record with the data
            conducteur = request.env['res.partner'].sudo().create(data)

            # Return a success response
            return {
                'message': 'User registered successfully!',
                'user_id': conducteur.id,
                'user_data': {
                    'name': conducteur.name,
                    'email': conducteur.email,
                }
            }
        except Exception as e:
            return {'error': str(e)}

        
    @http.route('/api/create_payment_user', type='json', auth='public', methods=['POST'], csrf=False)
    def create_payment_user(self):
        try:
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            # Extract required fields
            contract_id = data.get('contract_id')
           # amount = data.get("amount")


            if not contract_id:
                return {
                    'error': 'Please provide contract_id '
                }
            
            

            # Ensure contract exists
            contract = request.env['car.rental.contract'].sudo().search([('id', '=', contract_id)], limit=1)
            if not contract.exists():
                return {'error': f'No contract found with ID {contract_id}.'}
            
            conducteur = request.env['res.partner'].sudo().search([('id', '=', contract.customer_id.id)], limit=1)

            total= contract.total_cost+ contract.total_cost * 0.19 + 1


            # Create the payment
            payment_vals = {
                'contract_id': contract_id,
                'amount': total,
                'acompte': contract.acompte,


                
            }

            payment = request.env['account.payment'].sudo().create(payment_vals)


            # Confirm payment

            return {
                'message': 'Payment created  successfully!',
                'payment_id': payment.id,
                'contract': contract.name,
            }
        
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'}

    """ @http.route('/api/create_payment_user_card', type='json', auth='public', methods=['POST'], csrf=False)
    def create_payment_user_card(self):
        try:
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            # Extract required fields
            contract_id = data.get('contract_id')
            journal_name = data.get('journal')  # Payment journal
            amount = data.get("amount")


            if not contract_id  or not journal_name or not amount:
                return {
                    'error': 'Please provide contract_id, and jjournal_name and amount.'
                }
            # Search for the journal by name
            journal = request.env['account.journal'].sudo().search([('name', '=', journal_name)], limit=1)
            if not journal:
                return {'error': f'No journal found with name "{journal_name}".'}
            

            # Ensure contract exists
            contract = request.env['car.rental.contract'].sudo().search([('id', '=', contract_id)], limit=1)
            if not contract.exists():
                return {'error': f'No contract found with ID {contract_id}.'}
            
            conducteur = request.env['res.partner'].sudo().search([('id', '=', contract.customer_id.id)], limit=1)


            # Create the payment
            payment_vals = {
                'name' : conducteur.name,
                'contract_id': contract_id,
                'journal_id': journal.id,
                'amount': amount,
                'acompte': contract.acompte,

                
            }

            payment = request.env['account.payment'].sudo().create(payment_vals)
            payment.action_confirm_payment()
            payment.state= "posted"

            # Confirm payment

            return {
                'message': 'Payment created and confirmed successfully!',
                'payment_id': payment.id,
                'contract': contract.name,
            }
        
        except Exception as e:
            return {'error': f'Unexpected error: {str(e)}'} """
        
    @http.route('/api/update_user', type='json', auth='public', methods=['POST'], csrf=False)
    def update_user(self):
        try:
            # Parse the JSON data from the request body
            try:
                raw_data = request.httprequest.data
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            # Ensure email is provided for user identification
            email = data.get('email')
            if not email:
                return {'error': 'Email is required to identify the user.'}

            # Search for the user
            user = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not user:
                return {'error': f"No user found with the email: {email}"}

            # Remove the email field to prevent overwriting it
            data.pop('email', None)

            # Prepare the update data
            update_data = {}
            for key, value in data.items():
                if key in ['profile_pic', 'identity_card_picture', 'drivers_license_picture', 'image_1920']:
                    # Handle binary fields (decode base64 string to binary)
                    try:
                        
                        update_data[key] = value if value else False

                    except Exception as e:
                        return {'error': f"Error decoding binary field {key}: {str(e)}"}
                elif key == 'country_id':
                    # Handle country field (convert name to ID)
                    country = request.env['res.country'].sudo().search([('name', '=', value)], limit=1)
                    if not country:
                        return {'error': f"Invalid country name: {value}"}
                    update_data[key] = country.id
                else:
                    # Add other fields directly
                    update_data[key] = value

            # Update the user
            user.write(update_data)

            # Return success response
            return {
                'message': 'User updated successfully!',
                'updated_fields': list(update_data.keys()),  # Return updated field names
            }

        except Exception as e:
            return {'error': str(e)}


        
    @http.route('/api/update_password', type='json', auth='public', methods=['POST'], csrf=False)
    def update_password(self):
        try:
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            email = data.get('email')  # Email to identify the user       
            old_password =data.get('oldPassword')
            new_password = data.get('newPassword')






            if not email or not old_password or not new_password:
                return {'error': 'Email, old password, and new password are required.'}

            # Find the user by email
            user = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not user:
                return {'error': 'User not found'}
            


            # Check if the old password matches
            if not check_password_hash(user.password, old_password):
                return {'error': 'Incorrect old password'}

            # Hash the new password

            # Update the user's password
            user.write({'password': new_password})

            # Return success response
            return {
                'message': 'Password updated successfully'}

        except Exception as e:
            _logger.error(f"Error while updating password: {e}")
            return {'error': 'An error occurred while updating the password.'}
        
    @http.route('/api/get_user', type='json', auth='public', methods=['POST'], csrf=False)
    def get_user(self):
        try:
            # Access the raw request data
            raw_data = request.httprequest.data

            # Parse the JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON data provided.'}

            email = data.get('email')

            if not email :
                return {'error': 'Please provide  email  in the request body.'}

            # Search for the res.partner (conducteur) with the given email
            conducteur = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)

            if not conducteur:
                return {'error': f'No conducteur found with the email: {email}'}

            
            # Limit the fields to be returned
            conducteur_data = conducteur.read([
            'name', 
            'email', 
            'mobile',
            'x_date_of_birth', 
            'x_place_of_birth', 
            'identity_card_picture', 
            'drivers_license_picture',  
            'driver_license_number', 
            'cin_number', 
            'x_cin_issue_date', 
            'x_license_issue_date', 
            'x_license_category', 
            'profile_pic',
            'image_1920',
            'street',
            'street2',
            'country_id',
            'zip',
            'city',
            'category_id'
            ])[0]
            if 'id' in conducteur_data:
                del conducteur_data['id']  # Remove the id field
            if 'password' in conducteur_data:
                del conducteur_data['password']  # Remove the id field

            return {
                'message': 'User found and returned successfully!',
                'user_data': conducteur_data
            }
        except Exception as e:
            return {'error': str(e)}
