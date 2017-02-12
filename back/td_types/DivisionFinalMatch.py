from flask_restless.helpers import to_dict

def generate_division_final_match_class(db_handle,relationship=None,fk=None):    
    class DivisionFinalMatch(db_handle.Model):        
        division_final_match_id = db_handle.Column(db_handle.Integer, primary_key=True)
        division_final_round_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_final_round.division_final_round_id'))
        tiebreaker_division_machine_id = db_handle.Column(db_handle.Integer,db_handle.ForeignKey('division_machine.division_machine_id'))
        
        completed = db_handle.Column(db_handle.Boolean,default=False)
        has_tiebreaker = db_handle.Column(db_handle.Boolean,default=False)
        
        number_of_games = db_handle.Column(db_handle.Integer)
        finals_match_player_results = db_handle.relationship('FinalsMatchPlayerResult')
        finals_match_game_results = db_handle.relationship('FinalsMatchGameResult')
 
        
        def to_dict_simple(self):
            export_dict = to_dict(self)
            if len(self.finals_match_player_results) > 0:
                export_dict['finals_match_player_results'] = []
                for result in self.finals_match_player_results:
                    export_dict['finals_match_player_results'].append(result.to_dict_simple())
            if len(self.finals_match_game_results) > 0:
                export_dict['finals_match_game_results'] = []
                for result in self.finals_match_game_results:
                    export_dict['finals_match_game_results'].append(result.to_dict_simple())                    
            return export_dict
        
    return DivisionFinalMatch