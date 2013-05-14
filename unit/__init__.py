
# ##################################################
# import

import unittest

# ##################################################
# class Test

class Test( unittest.TestCase ):

    # ##################################################
    # checks

    def check_equal( self, name=None, computed=None, expected=None ):
        self.assertEqual( computed, expected, '{ name: %s, computed: %s, expected: %s, result: %s }' % ( name, computed, expected, ( computed == expected ) ) )

    def check_int( self, name=None, computed=None, expected=None ):
        self.check_equal( name=name, computed=int( computed ), expected=int( expected )  )

    def check_float( self, name=None, computed=None, expected=None ):
        self.check_equal( name=name, computed=float( computed ), expected=float( expected )  )
