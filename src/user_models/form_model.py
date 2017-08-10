
class Form:
    """
    Email registration form model. Holds the form data and all operations performed on it.
    """
    
    def __init__( self, form ):
        self.form = form

    def validation_errors( self ):
        """ Checks if fields from the submitted form are valid."""
        
        error_bag = []  # Stays empty if there are no errors in the field.
        
        # user_name field validation conditions
        if 'user_name' in self.form:  # Check if form contains a user_name field
            if not self.form.get( 'user_name' ).isalnum():
                error_bag.append( 'User Name must not be empty and must consist of alpha numerical characters')

        # Email field validation conditions
        if 'email' in self.form:
            if not self.form.get( 'email' ):
                error_bag.append( 'Email must not be empty' )
    
        # More fields validations can be added, this is just for illustration purpose
    
        return error_bag
