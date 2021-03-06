from flask_restless.helpers import to_dict

def generate_division_class(db_handle,relationship=None,fk=None):    
    class Division(db_handle.Model):
        """Model object for a division in a tournament"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        #metadivision_id = db_handle.Column(db_handle.Integer, db_handle.ForeignKey(
        #    'metadivision.metadivision_id'
        #))
        
        division_id = db_handle.Column(db_handle.Integer, primary_key=True)
        active = db_handle.Column(db_handle.Boolean,default=False)
        team_tournament = db_handle.Column(db_handle.Boolean)
        scoring_type = db_handle.Column(db_handle.String(100))
        division_name = db_handle.Column(db_handle.String(100))
        number_of_scores_per_entry = db_handle.Column(db_handle.Integer)
        number_of_relevant_scores = db_handle.Column(db_handle.Integer)
        use_stripe = db_handle.Column(db_handle.Boolean)
        stripe_sku = db_handle.Column(db_handle.String(100))
        discount_stripe_sku = db_handle.Column(db_handle.String(100))
        
        local_price = db_handle.Column(db_handle.Integer)
        ifpa_range_start = db_handle.Column(db_handle.Integer,default=0)
        ifpa_range_end = db_handle.Column(db_handle.Integer)
        ppo_a_ifpa_range_end = db_handle.Column(db_handle.Integer)                
        
        
        finals_player_selection_type = db_handle.Column(db_handle.String(100))
        finals_num_qualifiers = db_handle.Column(db_handle.Integer)
        finals_num_qualifiers_ppo_a = db_handle.Column(db_handle.Integer)
        finals_num_qualifiers_ppo_b = db_handle.Column(db_handle.Integer)
        finals_challonge_name_ppo_a = db_handle.Column(db_handle.String(100))
        finals_challonge_name_ppo_b = db_handle.Column(db_handle.String(100))        
        finals_num_players_per_group = db_handle.Column(db_handle.Integer)
        finals_num_games_per_match = db_handle.Column(db_handle.Integer)
        queuing = db_handle.Column(db_handle.Boolean,default=False)
        discount_ticket_count = db_handle.Column(db_handle.Integer)
        discount_ticket_price = db_handle.Column(db_handle.Integer)
        min_num_tickets_to_purchase = db_handle.Column(db_handle.Integer,default=1)

        division_is_limited_herb = db_handle.Column(db_handle.Boolean,default=False)
        
        meta_division_id = db_handle.Column(db_handle.Integer,
                                         db_handle.ForeignKey(
                                             'meta_division.meta_division_id'))
        
        tournament_id = db_handle.Column(db_handle.Integer,
                                         db_handle.ForeignKey(
                                             'tournament.tournament_id'
                                         ))
        tournament = db_handle.relationship(
            'Tournament',
            foreign_keys=[tournament_id]
        )
        
        
        def to_dict_simple(self):
            division = to_dict(self)
            division['tournament_name'] = self.get_tournament_name(self.tournament)
            division['single_division'] = self.tournament.single_division
            return division

        def get_tournament_name(self, tournament):
            if tournament.single_division:
                return tournament.tournament_name
            return tournament.tournament_name+", "+self.division_name

        def get_self_tournament_name(self):
            if self.tournament.single_division:
                return self.tournament.tournament_name
            return self.tournament.tournament_name+", "+self.division_name
        
        
        
    return Division
