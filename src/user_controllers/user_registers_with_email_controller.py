from . import user
from flask import request, render_template
from src.user_models.form_model import Form
from src.user_models.user_model import *
from src.user_services.email_service import *
from src.user_utilities.user_utilities import *
from src.user_emails.registration_email import *


@user.route( '/email-registration', methods = [ 'GET', 'POST' ] )
def user_registers_with_email_controller():
    """Trigger: User clicks on the 'Submit' email registration form button."""
    
    # User goes to the registration page
    if request.method == 'GET':
        return render_template( 'user_registers_with_email_view.html' )
    
    # User enters his login information
    if request.method == 'POST':
        
        form = request.form
        token = token_string()
        
        # System checks if user entered values are valid.
        errors = Form(form).validation_errors()  # Contains empty array, or array of error strings
        # User has entered invalid information
        if errors:
            return render_template( 'user_registers_with_email_view.html', error_message = errors )

        # System creates User entry in the database
        user = User().create_user( form, token )  # Returns instance of new user or False
        
        # There is already a user with provided information into the database
        if not user:
            error_message = "Username or email already exists. Please choose other values"
            return render_template( 'user_registers_with_email_view.html', error_message = error_message )

        # System sends validation email to user provided email
        send_email( form.get('email'), registration_email_subject(), registration_email_content( token, form["email"] ) )
        
        # System redirects user to confirmation page
        message = 'Thanks for registering. You are now logged in the site. Please check your email to confirm it.'
        return render_template( 'confirmation_view.html', message = message )
    
    
    


