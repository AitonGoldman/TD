from sqlalchemy_utils import create_database, database_exists
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine.reflection import Inspector
from td_types import ImportedTables
from machine_list import machines
from machine_list_test import test_machines
def load_machines_from_json(app,test=False):    
    machines_to_load = machines
    if test:
        machines_to_load = test_machines
    for machine in machines_to_load:
        new_machine = app.tables.Machine(
            machine_name=machine['machine_name']
        )
        if 'abbreviation' in machine:
            new_machine.abbreviation = machine['abbreviation']

        app.tables.db_handle.session.add(new_machine)
        app.tables.db_handle.session.commit()
        pass
        
    
def create_db_and_tables(app, db_name, db_info, drop_tables=False):    
    db_url = generate_db_url(db_name, db_info)
    if not database_exists(db_url):        
        create_database(db_url)
    db_handle = create_db_handle(db_url,app)        
    app.tables = ImportedTables(db_handle)
    create_TD_tables(db_handle, drop_tables=drop_tables)
    db_handle.engine.dispose()

def create_db_handle(db_url,flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_url    
    db_handle = SQLAlchemy(flask_app)
    return db_handle

def create_db_handle_no_app():
    db_handle = SQLAlchemy()
    return db_handle


def create_TD_tables(db_handle,drop_tables=False):
    db_handle.reflect()
    if drop_tables:
        db_handle.drop_all()
        db_handle.session.commit()
    db_handle.create_all()    

def check_table_exists(db_handle):
    db_handle.reflect()    
    if "role" in db_handle.metadata.tables:        
        return True
    else:
        return False

# FIXME : need to generate db_url by comparing "name" to good list of dbs
# FIXME : should be using host info in pg_info
#def generate_db_url(db_name, pg_info=None, use_sqlite=False):
def generate_db_url(db_name, db_info):
    if db_name is None or db_name == "":
        raise Exception("No db name specified while generating db url")

    if db_info is None :
        raise Exception("Missing postgress username or password while trying to build db url")       
    if db_info.is_sqlite():
        return "sqlite:////tmp/%s.db" % db_name    
    if db_info.is_postgres():        
        return "postgresql://%s:%s@localhost/%s" % (db_info.db_username,db_info.db_password,db_name)
        
            
def app_db_handle(app):
    return app.tables.db_handle

def app_db_tables(app):
    return app.tables


def check_if_ranking_funcs_exists(db_handle):
    result = db_handle.execute("SELECT prosrc FROM pg_proc WHERE proname = 'papa_scoring_func';")
    if not result.fetchone():
        DB.engine.execute("CREATE FUNCTION papa_scoring_func(rank real) RETURNS real AS $$ BEGIN IF rank = 1 THEN RETURN 100; ELSIF rank = 2 THEN RETURN 90; ELSIF rank = 3 THEN RETURN 85; ELSIF rank < 88 THEN  RETURN 100-rank-12; ELSIF rank >= 88 THEN RETURN 0; END IF; END; $$ LANGUAGE plpgsql;")
        DB.engine.execute("CREATE FUNCTION papa_scoring_finals_func(rank real) RETURNS real AS $$  BEGIN IF rank = 1 THEN RETURN 3; ELSIF rank = 2 THEN RETURN 2; ELSIF rank = 3 THEN RETURN 1; ELSIF rank = 4 THEN RETURN 0; END IF; END; $$ LANGUAGE plsgsql;")    

#FIXME : this should be getting app passed in
def init_papa_tournaments_divisions(tables,use_stripe=False,stripe_sku=None):
    db = tables.db_handle
    new_tournament = tables.Tournament(
        tournament_name="Main",
        single_division=False        
    )
    db.session.add(new_tournament)
    db.session.commit()
    for division_name in ['A','B','C','D']:
        new_division=tables.Division(
            active=True,
            team_tournament=False,
            scoring_type="HERB",
            division_name=division_name,
            number_of_scores_per_entry=1,
            finals_num_qualifiers=24
        )
        if use_stripe:
            new_division.use_stripe=True
            new_division.stripe_sku=stripe_sku
        else:
            new_division.local_price=5
        db.session.add(new_division)
        db.session.commit()
        new_tournament.divisions.append(new_division)
        db.session.commit()
    new_metadivision = tables.MetaDivision(
        meta_division_name="Classics"
    )
    db.session.add(new_metadivision)
    db.session.commit()

    new_tournament = tables.Tournament(
        tournament_name='Split Flipper',
        single_division=True        
    )
    db.session.add(new_tournament)
    db.session.commit()
    new_division=tables.Division(
        active=True,
        team_tournament=True,
        scoring_type="HERB",
        division_name="test team tournament_all",
        number_of_scores_per_entry=1,
        use_stripe=True,
        stripe_sku="stripe-test team tournament",
        finals_num_qualifiers=24
    )
    if use_stripe:
        new_division.use_stripe=True
        new_division.stripe_sku=stripe_sku
    else:
        new_division.local_price=5    
    db.session.add(new_division)
    db.session.commit()
    new_tournament.divisions.append(new_division)
    db.session.commit()
    for tournament_name in ['Classics 1','Classics 2','Classics 3']:
        new_tournament = tables.Tournament(
            tournament_name=tournament_name,
            single_division=True        
        )        
        db.session.add(new_tournament)
        db.session.commit()
        new_division=tables.Division(
            active=True,
            team_tournament=False,
            scoring_type="HERB",
            division_name=tournament_name+"_all",
            number_of_scores_per_entry=1,
            use_stripe=True,
            stripe_sku="stripe-"+tournament_name,
            finals_num_qualifiers=24
        )
        if use_stripe:
            new_division.use_stripe=True
            new_division.stripe_sku=stripe_sku
        else:
            new_division.local_price=5
        db.session.add(new_division)
        db.session.commit()
        new_tournament.divisions.append(new_division)
        new_metadivision.divisions.append(new_division)
        db.session.commit()        
    
        
