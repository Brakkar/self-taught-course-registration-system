# Definition of Blueprint structure so it will  work with several routes files
from flask import Blueprint

user = Blueprint( 'user', __name__ )

# Must be at this level
from . import user_logins_registers_with_facebook_controller, user_confirms_his_email_controller, \
    user_email_log_in_controller, user_log_out_controller, user_registers_with_email_controller
