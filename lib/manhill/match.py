
# ##################################################
# import

import py
import math


# ##################################################
# Outcome

class Outcome( object ):
    """ Class to handle a outcome """
    
    success = 1.
    tie = .5
    failure = 0.


# ##################################################
# Score Model

class Score( py.Model ):
    """ Score Model """

    # ##################################################
    # attributes
    
    points = None
    success = None
    nb = None
    
    # ##################################################
    # constructor
    
    def __init__( self, points=None, success=None, nb=None, *args, **kwargs ):
        super( Score, self ).__init__( *args, **kwargs )
        self.points = points if points is not None else 0.
        self.success = success if success is not None else 0.
        self.nb = nb if nb is not None else 0.


# ##################################################
# Player Model

class Player( py.Model ):
    """ Player Model """

    # ##################################################
    # attributes
    
    score = None
    
    # ##################################################
    # constructor
    
    def __init__( self, score=None, *args, **kwargs ):
        super( Player, self ).__init__( *args, **kwargs )
        self.score = score if score is not None else Score( *args, **kwargs )


# ##################################################
# Match Usecase

class Match( py.Usecase ):
    """ Match Usecase """
    
    player = None
    
    # ##################################################
    # constructor
    
    def __init__( self, player=None, *args, **kwargs ):
        super( Match, self ).__init__( *args, **kwargs )
        self.player = player

    # ##################################################
    # enter        
    
    def __enter__( self, *args, **kwargs ):
        super( Match, self ).__enter__( *args, **kwargs )
        self.prepare_player()
        return self

    # ##################################################
    # exit        
    
    def __exit__( self, *args, **kwargs ):
        super( Match, self ).__exit__( *args, **kwargs )
        self.prepare_player()
        return self

    # ##################################################
    # prepare player        
    
    def prepare_player( self, *args, **kwargs ):
        self.player = self.player if self.player is not None else Player( *args, **kwargs )
        self.prepare_score( *args, **kwargs )

    # ##################################################
    # prepare score        
    
    def prepare_score( self, *args, **kwargs ):
        self.player.score = self.player.score if self.player.score is not None else Score( *args, **kwargs )
        self.player.score.success = max( min( self.player.score.success, self.player.score.nb ), 0 )
    
    # ##################################################
    # success
    
    def execute_success( self, *args, **kwargs ):
        return self.execute( outcome=Outcome.success, *args, **kwargs )

    # ##################################################
    # tie
    
    def execute_tie( self, *args, **kwargs ):
        return self.execute( outcome=Outcome.tie, *args, **kwargs )

    # ##################################################
    # failure
    
    def execute_failure( self, *args, **kwargs ):
        return self.execute( outcome=Outcome.failure, *args, **kwargs )

    # ##################################################
    # score gain

    def compute_score_gain( self, score_gain=None, *args, **kwargs ):
        return score_gain if score_gain is not None else 0.

    # ##################################################
    # execute
    
    def execute( self, outcome=None, score_gain=None, *args, **kwargs ):
        self.player.score.success += outcome if outcome is not None else Outcome.tie
        self.player.score.nb += 1
        self.player.score.points += self.compute_score_gain( outcome=outcome, score_gain=score_gain, *args, **kwargs )
        
        return super( Match, self ).execute( outcome=outcome, score_gain=score_gain, *args, **kwargs )                       


# ##################################################
# Elo usecase

class Elo( Match ):
    """ Elo Usecase """

    # ##################################################
    # constants

    maturity_nb = 10
    nomal_score_gain = 32
    expert_score_threshold = 2100
    expert_score_gain = 16
    success_rate_min = 0.00000001
    success_rate_max = 0.99999999
    success_rate_precision = 8
    score_min = 0
    score_base = 1000
    score_max = 3000
    score_delta = 400

    # ##################################################
    # helper

    @classmethod
    def cap_score( cls, score=None ):
        score = score if score is not None else cls.score_base
        return int( round( max( min( score, cls.score_max ), cls.score_min ) ) )

    @classmethod
    def cap_success_rate( cls, success_rate=None ):
        success_rate = success_rate if success_rate is not None else Outcome.tie
        return float( max( min( round( success_rate, cls.success_rate_precision ), cls.success_rate_max ), cls.success_rate_min ) )
    
    @classmethod
    def convert_score_to_success_rate( cls, score=None, score_ref=None ):
        score = cls.cap_score( score )
        score_ref = cls.cap_score( score_ref )
        success_rate = 1. / ( 1. + math.pow( 10., float( score_ref - score ) / float( cls.score_delta ) ) )
        success_rate = cls.cap_success_rate( success_rate )
        return success_rate

    @classmethod
    def convert_success_rate_to_score( cls, success_rate=None, score_ref=None ):
        success_rate = Elo.cap_success_rate( success_rate )
        score_ref = Elo.cap_score( score_ref )
        score = score_ref - ( float( Elo.score_delta ) * math.log10( float( 1 - success_rate ) / float( success_rate ) ) )
        score = Elo.cap_score( score )
        return score  

    # ##################################################
    # prepare player        
    
    def prepare_player( self, *args, **kwargs ):
        super( Elo, self ).prepare_player( points=Elo.score_base, *args, **kwargs )

    # ##################################################
    # gain

    def compute_score_gain( self, outcome=None, competitor=None, *args, **kwargs ):
        
        # compute base
        score_gain = self.nomal_score_gain if self.player.score.points < self.expert_score_threshold else self.expert_score_gain
        
        # filter by the maturity of the competitor
        score_gain *= float( min( competitor.score.nb, self.maturity_nb ) ) / float( self.maturity_nb )
        
        # filter by the outcome
        expected_outcome = self.convert_score_to_success_rate( score=self.player.score.points, score_ref=competitor.score.points ) 
        score_gain *= ( outcome - expected_outcome )
        
        # cap
        new_score = self.cap_score( self.player.score.points + score_gain )
        score_gain = ( new_score - self.player.score.points )
        
        return score_gain


# ##################################################
# ReverseElo usecase

class ReverseElo( Match ):
    """ ReverseElo Usecase """

    # ##################################################
    # prepare player
    
    def prepare_player( self, *args, **kwargs ):
        super( ReverseElo, self ).prepare_player( *args, **kwargs )
        self.update_score_from_success_rate()             

    # ##################################################
    # update score from success rate
    
    def update_score_from_success_rate( self ):
        
        # compute success rate
        success_rate = ( float( self.player.score.success ) /  float( self.player.score.nb ) ) if self.player.score.nb > 0 else Outcome.tie
        
        # compute score from success rate
        score = Elo.convert_success_rate_to_score( success_rate=success_rate, score_ref=Elo.score_base )
        
        # update player score
        self.player.score.points = Elo.cap_score( score )
        
        # print '{ points: %s, score: %s, success_rate: %s, success: %s, nb: %s }' % ( self.player.score.points, score, success_rate, self.player.score.success, self.player.score.nb )

