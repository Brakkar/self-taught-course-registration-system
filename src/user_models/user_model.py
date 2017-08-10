from peewee import *
from src.user_utilities.user_utilities import *
from settings import *

db = MySQLDatabase( parameters[ 'mysql_settings' ][ 'db' ],
                    host = parameters[ 'mysql_settings' ][ 'host' ],
                    port = parameters[ 'mysql_settings' ][ 'port' ],
                    user = parameters[ 'mysql_settings' ][ 'user' ],
                    passwd = parameters[ 'mysql_settings' ][ 'passwd' ] )


class User( Model ):
    """
    user model. Holds the model data and all operations performed on it.
    """
    
    # Model properties
    username = CharField( unique = True )
    email = CharField( unique = True )
    password = CharField( null = True )
    facebook_id = CharField( unique = True, null = True )
    user_group = CharField( default = 'unconfirmed' )
    registration_confirmation_token = CharField( null = True )
    
    
    class Meta:
        database = db  # This model uses the "user.db" database.
    
    
    def initialize_db( self ):
        db.connect()
        db.create_tables( [ User ], safe = True )
    
    def create_user( self, form, token ):
        """Create user in the database. Those users have registered with email.
        If user is correctly created, we return user instance."""
        
        try:
            self.initialize_db()
            user_instance = User.create( username = form.get( 'user_name' ),
                                         email = form.get( 'email' ),
                                         password = encrypt_string( form.get( 'password' ) ),
                                         registration_confirmation_token = token )
            user_instance.save()
            
            return user_instance
        except IntegrityError as e:
            # If there is a duplicate username or email, an exception is raised. We return False
            print( str( e ) )
            return False
        except Exception as e:
            # Global exception cacther, we just print the issue. On production, this should be logged.
            print( str( e ) )
        finally:
            db.close()
    
    def create_fb_user( self, user_facebook_record ):
        """Create facebook user entry in the database. Those users have registered by clicking on FB button.
        If user is correctly created, we return user instance."""
    
        try:
            self.initialize_db()
            
            # If user is correctly created, we return user instance.
            user_instance = User.create( username = user_facebook_record.get( 'first_name' ) + ' ' + user_facebook_record.get( 'last_name' ),
                                         email = user_facebook_record.get( 'email' ),
                                         facebook_id = user_facebook_record.get( 'id' ) )
            user_instance.save()
            
            return user_instance
        except IntegrityError as e:
            return False
        except Exception as e:
            print( str( e ) )
        finally:
            db.close()
    
    def get_user( self, username ):
        """Returns a single user based on username field."""
    
        try:
            self.initialize_db()
    
            return User.select().where( User.username == username ).get()
        except DoesNotExist as e:
            return False
        except Exception as e:
            print( str( e ) )
        finally:
            db.close()
    
    def get_user_by_email( self, email ):
        """Returns a single user based on email field."""
    
        try:
            self.initialize_db()
    
            return User.select().where( User.email == email ).get()
        except DoesNotExist as e:
            return False
        except Exception as e:
            print( str( e ) )
        finally:
            db.close()
    
    def get_user_by_registration_token( self, token ):
        """Returns a single user based on registration token field."""
    
        try:
            self.initialize_db()
    
            return User.select().where( User.registration_confirmation_token == token ).get()
        except DoesNotExist as e:
            return False
        except Exception as e:
            print( str( e ) )
        finally:
            db.close()
    
    def update_user_group_to_registered( self, token ):
        """Updates the user_group field and empties registration_confirmation_token field after user has confirmed his email address."""
    
        try:
            self.initialize_db()
            
            query = User.update( user_group = 'registered', registration_confirmation_token = None ).where( User.registration_confirmation_token == token )
            query.execute()
            
        except Exception as e:
            print( str( e ) )
        finally:
            db.close()

    def get_user_by_facebook_id( self, fb_id ):
        """Returns a single user based on facebook_id field."""
    
        try:
            self.initialize_db()
            return User.select().where( User.facebook_id == fb_id ).get()
        except DoesNotExist as e:
            return False
        except Exception as e:
            print( str( e ) )
        finally:
            db.close()
