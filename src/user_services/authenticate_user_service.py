from beaker.middleware import SessionMiddleware
from flask import request


def authenticate_user( user ):
    """Create end populate user session"""
    
    # Get the session object from the environ
    session = request.environ[ 'beaker.session' ]
    
    # Set session data
    session[ 'username' ] = user.username
    session[ 'email' ] = user.email
    session[ 'user_group' ] = user.user_group or None
    session[ 'facebook_id' ] = user.facebook_id or None
    
    request.environ[ 'beaker.session' ].save()
