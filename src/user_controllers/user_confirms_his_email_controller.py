from . import user
from flask import request, render_template
from src.user_models.user_model import *
from flask import request


@user.route( '/email_validation/<emailconfirmationtoken>/<email>', methods = [ 'GET', 'POST' ] )
def user_confirms_his_email_controller( emailconfirmationtoken, email ):
    """Trigger: User clicks on the email confirmation link."""
    
    token = emailconfirmationtoken
    user = User()
    
    # System checks if there is a corresponding user to validate.
    user_with_token = user.get_user_by_registration_token( token )  # returns user instance or False
    
    # There is no user to validate
    if not user_with_token:
        error_message = "The user you are trying to validate either doesn't exist or is already validated"
        return render_template( 'home_view.html', error_message = error_message )

    # System checks if email from confirmation link, matches the email from db record
    if user_with_token.email != email:
        error_message = "The email from the confirmation link, doesn't match the one for the corresponding database record."
        return render_template( 'home_view.html', error_message = error_message )
    
    # System check if user is logged in
    session = request.environ[ 'beaker.session' ]
    logged_in = 'username' in session
    
    # System updates user session information
    if logged_in:
        session[ 'user_group' ] = 'registered'
    
    # System updates user database information
    user.update_user_group_to_registered( token )
    
    # System redirects user to his profile page
    message = "Your email was validated. Enjoy full access to this unique web site !!"
    
    return render_template( 'home_view.html', message = message )
