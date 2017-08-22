from lib.flask_lib import blueprints
from flask import jsonify,current_app,request
from werkzeug.exceptions import BadRequest,Unauthorized
import json
from lib.serializer.generic import  generate_generic_serializer
from lib import serializer
from lib.route_decorators.db_decorators import load_tables
from sqlalchemy.orm import joinedload
from lib.serializer.deserialize import deserialize_json

def edit_tournament_machine_route(tournament_machine_id,request,app):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    existing_tournament_machine = app.tables.TournamentMachines.query.filter_by(tournament_machine_id=tournament_machine_id).first()    
    if existing_tournament_machine is None:
        raise BadRequest('Bad tournament machine submitted')
    deserialize_json(existing_tournament_machine,input_data,app)    
    if existing_tournament_machine.removed:
         existing_tournament_machine.removed=True
         existing_tournament_machine.active=False
         
    return existing_tournament_machine

def create_tournament_machine_route(request,tables):
    if request.data:        
        input_data = json.loads(request.data)
    else:
        raise BadRequest('Username or password not specified')
    if 'tournament_id' not in input_data or 'machine_id' not in input_data:
        raise BadRequest('Missing information')        
    existing_tournament_machine = tables.TournamentMachines.query.filter_by(machine_id=input_data['machine_id']).first()
    if existing_tournament_machine:
        if existing_tournament_machine.removed is False:
            raise BadRequest('Trying to add an already added machine')
        else:
            existing_tournament_machine.removed = False
            existing_tournament_machine.active = True
            return existing_tournament_machine
            
    existing_tournament = tables.Tournaments.query.filter_by(tournament_id=input_data['tournament_id']).first()
    existing_machine = tables.Machines.query.filter_by(machine_id=input_data['machine_id']).first()
    if existing_tournament is None or existing_machine is None:
        raise BadRequest('Trying to add to a bad tournament, or trying to add a bad machine')        

    new_tournament_machine = tables.TournamentMachines(machine_id=input_data['machine_id'],
                                                   tournament_machine_name=existing_machine.machine_name,
                                                   tournament_machine_abbreviation=existing_machine.abbreviation,
                                                   active=True)    
    tables.db_handle.session.add(new_tournament_machine)
    existing_tournament.tournament_machines.append(new_tournament_machine)    
    tables.db_handle.session.commit()
    return new_tournament_machine

@blueprints.event_blueprint.route('/tournament_machine',methods=['POST'])
@load_tables
def create_tournament_machine(tables):    
    new_tournament_machine = create_tournament_machine_route(request,tables)
    tournament_machine_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'new_tournament_machine':tournament_machine_serializer(new_tournament_machine)})

@blueprints.event_blueprint.route('/tournament_machine/<tournament_machine_id>',methods=['PUT'])
@load_tables
def edit_tournament_machine(tables,tournament_machine_id):    
    edited_tournament_machine = edit_tournament_machine_route(tournament_machine_id,request,current_app)    
    tables.db_handle.session.commit()
    tournament_machine_serializer = generate_generic_serializer(serializer.generic.ALL)
    return jsonify({'edited_tournament_machine':tournament_machine_serializer(edited_tournament_machine)})
    
