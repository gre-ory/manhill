
# ##################################################
# import


# ##################################################
# Class Object

class Object( object ):
    """ Generic object """

    # ##################################################
    # constructor
    
    def __init__( self, *args, **kwargs ):
        super( Object, self ).__init__()


# ##################################################
# Class Model

class Model( Object ):
    """ Generic model """

    # ##################################################
    # format
    
    def __repr__( self ):
        return '{ %s }' % ', '.join( [ '%s: %s' % ( key, value ) for key, value in self.__dict__.iteritems() ] )


# ##################################################
# Class Usecase

class Usecase( Object ):
    """ Generic usecase """

    # ##################################################
    # enter
    
    def __enter__( self, *args, **kwargs ):
        return self

    # ##################################################
    # execute
    
    def execute( self, *args, **kwargs ):
        return self

    # ##################################################
    # exit
    
    def __exit__( self, *args, **kwargs ):
        return self
