from flask import Flask, render_template, request
from src.user_controllers.user_registers_with_email_controller import user
from beaker.middleware import SessionMiddleware
from settings import *


app = Flask( __name__, template_folder = "src/user_views" )

# Custom modules
app.register_blueprint( user, url_prefix = '/user' )

app.secret_key = 'A*************'


@app.route( '/' )
def hello_world():
    return render_template( 'home_view.html' )


if __name__ == '__main__':
    app.wsgi_app = SessionMiddleware( app.wsgi_app, parameters["session_opts"] )
    app.run()
