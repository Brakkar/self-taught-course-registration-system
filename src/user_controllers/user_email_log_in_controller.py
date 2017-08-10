from . import user
from flask import request, render_template
from src.user_models.form_model import Form
from src.user_models.user_model import *
from src.user_services.authenticate_user_service import *


@user.route( '/email-login', methods = [ 'GET', 'POST' ] )
def user_email_log_in_controller():
    """Trigger: User clicks on the log in form button"""

    # User goes to the email login page
    if request.method == 'GET':
        return render_template( 'user_email_log_in_view.html' )
    
    # User enters his login information
    if request.method == 'POST':
    
        form = request.form

        # Systems validates the form data
        errors = Form( form ).validation_errors()  # Contains empty array, or array of error strings
        # Form data is invalid
        if errors:
            return render_template( 'user_email_log_in_view.html', error_message = errors )

        # System checks if provided email exists
        user = User().get_user_by_email( form.get('email') )
        # Email doesn’t exists in the database
        if not user:
            error_message = "This email doesn't exist in our database"
            return render_template( 'user_email_log_in_view.html', error_message = error_message )
        
        # System checks if passwords match
        match = password_match( user.password, form.get( 'password' ))
        # Password don’t match
        if not match:
            error_message = "The password doesn't match the one stored for that email address"
            return render_template( 'user_email_log_in_view.html', error_message = error_message )
        
        # System authenticates user
        authenticate_user( user )

        # System redirects user to his profile page
        message = 'You are now logged in the site'

        return render_template( 'user_profile_view.html', message = message )
