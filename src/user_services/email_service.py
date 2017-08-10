from smtplib import SMTP
from email.mime.text import MIMEText
from settings import *


def send_email( to, subject, content ):
    """Function responsible for sending email message with the SMTP protocol."""

    smtp = SMTP()
    text_subtype = 'plain'
    smtp.set_debuglevel( False )
    smtp.connect( parameters['email_settings']['server_host'], parameters[ 'email_settings' ][ 'server_port' ] )
    smtp.login( parameters[ 'email_settings' ][ 'server_login' ], parameters[ 'email_settings' ][ 'server_pass' ] )
    from_addr = parameters[ 'email_settings' ][ 'from_adr' ]

    msg = MIMEText( content, text_subtype )
    msg[ "Subject" ] = subject
    msg[ 'From' ] = from_addr

    try:
        smtp.sendmail( from_addr, to, str( msg ) )
        print( "Email Sent " )
    except Exception as e:
        print( e )

    finally:
        smtp.quit()
        print( "Smtp has quit" )





