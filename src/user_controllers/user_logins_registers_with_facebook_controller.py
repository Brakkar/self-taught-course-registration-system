from . import user
from flask import request, render_template
from src.user_models.user_model import *
from src.user_services.authenticate_user_service import *
from settings import *
import requests


@user.route( '/facebook-login-page', methods = [ 'GET', 'POST' ] )
def show_facebook_login_page():
    """Displays the Facebook login page"""
    
    if request.method == 'GET':
        return render_template( 'user_logins_registers_with_facebook_view.html', fb_app_id = parameters[ 'facebook_app_id' ] )


@user.route( '/facebook-login/<facebookprovidedtoken>' )
def user_logins_registers_with_facebook_controller( facebookprovidedtoken ):
    """Trigger: User clicks on the Facebook login button."""
    
    # System gets user information from Facebook
    fb_request = requests.get( 'https://graph.facebook.com/me/?fields=gender,first_name,last_name,name,email&access_token={}'.format( facebookprovidedtoken ) )
    request_status_code = fb_request.status_code
    
    # There is a problem establishing connection to Facebook:
    if request_status_code != 200:
        error_message = "There was a problem logging in with Facebook. Please try again later or contact us"
        return render_template( 'home_view.html', error_message = error_message )
    
    # Convert Json to Python
    user_facebook_record = fb_request.json()
    
    # System checks if Facebook user already exists in our database
    db_user = User().get_user_by_facebook_id( user_facebook_record.get( 'id' ) )
    # System authenticates Facebook user
    if db_user:
        authenticate_user( db_user )
        message = 'You are logged in the site'
        # System redirects user to his profile
        return render_template( 'user_profile_view.html', message = message )

    # Facebook User doesn’t exist in our database
    # System checks if non Facebook user email already exists in the database
    db_user = User().get_user_by_email( user_facebook_record.get( 'email' ) )
    # Email of non Facebook user already exists in the database
    if db_user:
        error_message = 'The email already exists in the database. You cannot register with this facebook account'
        return render_template( 'user_profile_view.html', message = error_message )
    
    # System creates user database entry
    new_user = User().create_fb_user( user_facebook_record )
    
    # System authenticates Facebook user
    authenticate_user( new_user )
    
    # Redirect to profile page
    message = 'You are now logged in the site'
    return render_template( 'user_profile_view.html', message = message )

