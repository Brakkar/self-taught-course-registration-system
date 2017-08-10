from . import user
from flask import request, render_template
from src.user_services.authenticate_user_service import *


@user.route( '/logout', methods = [ 'GET', 'POST' ] )
def user_log_out_controller():
    """Trigger: User clicks on the log out button"""
    
    # Destroy session
    session = request.environ[ 'beaker.session' ]
    session.delete()
    
    # Redirect user to homepage
    message = 'You are now logged out'
    return render_template( 'home_view.html', message = message )
