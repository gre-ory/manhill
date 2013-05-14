
# ##################################################
# import

import unit

from manhill.match import *


# ##################################################
# class UnitTestMatch

class UnitTestMatch( unit.Test ):

    # ##################################################
    # checks

    def check_score( self, score, points=None, success=None, nb=None, *args, **kwargs ):
        self.check_float( name='points', computed=score.points, expected=points )
        self.check_float( name='success', computed=score.success, expected=success )
        self.check_float( name='nb', computed=score.nb, expected=nb )

    def check_player( self, player, *args, **kwargs ):
        self.check_score( player.score, *args, **kwargs )

    # ##################################################
    # test init

    def test_000_score_init( self ):
        score = Score()
        self.check_score( score, points=0, success=0, nb=0 )
        
    def test_001_player_init( self ):
        player = Player()
        self.check_player( player, points=0, success=0, nb=0 )
        
    # ##################################################
    # test elo
    
    def test_101_elo( self ):
        score = Elo.score_min
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .00315231 )
        self.check_int( 'score', new_score, score )

    def test_102_elo( self ):
        score = Elo.score_base - Elo.score_delta
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .09090909 )
        self.check_int( 'score', new_score, score )
        
    def test_103_elo( self ):
        score = Elo.score_base - ( Elo.score_delta / 2. )
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .24025307 )
        self.check_int( 'score', new_score, score )
        
    def test_104_elo( self ):
        score = Elo.score_base
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .5 )
        self.check_int( 'score', new_score, score )

    def test_105_elo( self ):
        score = Elo.score_base + ( Elo.score_delta / 2. )
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .75974693 )
        self.check_int( 'score', new_score, score )

    def test_106_elo( self ):
        score = Elo.score_base + Elo.score_delta
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .90909091 )
        self.check_int( 'score', new_score, score )

    def test_107_elo( self ):
        score = Elo.score_max
        success_rate = Elo.convert_score_to_success_rate( score )
        new_score = Elo.convert_success_rate_to_score( success_rate )
        
        self.check_float( 'success_rate', success_rate, .99999 )
        self.check_int( 'score', new_score, score )

    # ##################################################
    # test match

    def test_201_match_success( self ):
        player = Player()
        with Match( player ) as usecase:
            usecase.execute_success()
            self.check_player( usecase.player, points=0, success=1, nb=1 )

    def test_202_match_failure( self ):
        player = Player()
        with Match( player ) as usecase:
            usecase.execute_failure( score_gain=-10 )
            self.check_player( usecase.player, points=-10, success=0, nb=1 )

    def test_203_match_tie( self ):
        player = Player()
        with Match( player ) as usecase:
            usecase.execute_tie( score_gain=10 )
            self.check_player( usecase.player, points=10, success=.5, nb=1 )

    # ##################################################
    # test elo match

    def test_301_elo_match_success( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        with Elo( player ) as usecase:
            usecase.execute_success( competitor=competitor )
            self.check_player( usecase.player, points=1208, success=1, nb=11 )

    def test_302_elo_match_failure( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        with Elo( player ) as usecase:
            usecase.execute_failure( competitor=competitor )
            self.check_player( usecase.player, points=1176, success=0, nb=11 )

    def test_303_elo_match_tie( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        with Elo( player ) as usecase:
            usecase.execute_tie( competitor=competitor )
            self.check_player( usecase.player, points=1192, success=.5, nb=11 )

    def test_304_elo_match_success_against_immature( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=int( Elo.maturity_nb / 2. ) )
        with Elo( player ) as usecase:
            usecase.execute_success( competitor=competitor )
            self.check_player( usecase.player, points=1204, success=1, nb=11 )

    def test_305_elo_match_failure_against_immature( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=int( Elo.maturity_nb / 2. ) )
        with Elo( player ) as usecase:
            usecase.execute_failure( competitor=competitor )
            self.check_player( usecase.player, points=1188, success=0, nb=11 )

    def test_306_elo_match_tie_against_immature( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=int( Elo.maturity_nb / 2. ) )
        with Elo( player ) as usecase:
            usecase.execute_tie( competitor=competitor )
            self.check_player( usecase.player, points=1196, success=.5, nb=11 )

    def test_307_elo_match_success_against_mature( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=int( Elo.maturity_nb / 2. ) )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        with Elo( player ) as usecase:
            usecase.execute_success( competitor=competitor )
            self.check_player( usecase.player, points=1208, success=1, nb=6 )

    def test_308_elo_match_failure_against_mature( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=int( Elo.maturity_nb / 2. ) )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        with Elo( player ) as usecase:
            usecase.execute_failure( competitor=competitor )
            self.check_player( usecase.player, points=1176, success=0, nb=6 )

    def test_309_elo_match_tie_against_mature( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=int( Elo.maturity_nb / 2. ) )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        with Elo( player ) as usecase:
            usecase.execute_tie( competitor=competitor )
            self.check_player( usecase.player, points=1192, success=.5, nb=6 )

    def test_399_elo_match_tie_withou_with( self ):
        player = Player( points=Elo.score_base + ( Elo.score_delta / 2. ), nb=Elo.maturity_nb )
        competitor = Player( points=Elo.score_base , nb=Elo.maturity_nb )
        usecase = Elo( player )
        usecase.execute_tie( competitor=competitor )
        self.check_player( usecase.player, points=1192, success=.5, nb=11 )
        usecase.__enter__().execute_tie( competitor=competitor )
        self.check_player( usecase.player, points=1184, success=1., nb=12 )

    # ##################################################
    # test reversed elo match

    def test_401_reversed_elo_match_success( self ):
        player = Player( success=Elo.maturity_nb / 2, nb=Elo.maturity_nb )
        with ReverseElo( player ) as usecase:
            usecase.execute_success()
            self.check_player( usecase.player, points=1032, success=6, nb=11 )

    def test_402_reversed_elo_match_failure( self ):
        player = Player( success=Elo.maturity_nb / 2, nb=Elo.maturity_nb )
        with ReverseElo( player ) as usecase:
            usecase.execute_failure()
            self.check_player( usecase.player, points=968, success=5, nb=11 )

    def test_403_reversed_elo_match_tie( self ):
        player = Player( success=Elo.maturity_nb / 2, nb=Elo.maturity_nb )
        with ReverseElo( player ) as usecase:
            usecase.execute_tie()
            self.check_player( usecase.player, points=1000, success=5.5, nb=11 )

    def test_499_reversed_elo_match_without_with( self ):
        player = Player( success=Elo.maturity_nb / 2, nb=Elo.maturity_nb )
        usecase = ReverseElo( player )
        usecase.execute_tie()
        self.check_player( usecase.player, points=0, success=5.5, nb=11 )
        usecase.__enter__().execute_tie()
        self.check_player( usecase.player, points=1000, success=6, nb=12 )


# ##################################################
# main

if __name__ == '__main__':
    import unittest
    unittest.main()
