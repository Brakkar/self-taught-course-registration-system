from settings import parameters

# This file holds the content of the email sent after user has registered with his email, so he can confirm it.


def registration_email_content( token, email ):
    site_url = parameters[ 'site_url' ]
    
    return "You just registered to our site. Please validate your email by clicking on " \
           "this link: {}/user/email_validation/{}/{}".format( site_url, token, email )


def registration_email_subject():
    return "Mysite.com: please confirm your email"
