from flask_restless.helpers import to_dict
        
def generate_tournament_class(db_handle):
    class Tournament(db_handle.Model):
        """Model object for a tournament"""
        # pylint: disable=no-init
        # pylint can't find SQLAlchemy's __init__() method for some reason
        tournament_id = db_handle.Column(db_handle.Integer, primary_key=True)        
        tournament_name = db_handle.Column(db_handle.String(1000))
        single_division = db_handle.Column(db_handle.Boolean)        
        start_date = db_handle.Column(db_handle.DateTime)
        end_date = db_handle.Column(db_handle.DateTime)
        divisions = db_handle.relationship('Division',lazy='joined')


        def to_dict_simple(self):
            tournament = to_dict(self)
            if self.single_division:
                if self.divisions[0].active:
                    tournament['active']=True
                else:
                    tournament['active']=False                    
            tournament['divisions']=[division.division_id for division in self.divisions]
            return tournament
    return Tournament
    
