from blueprints import admin_login_blueprint,admin_manage_blueprint
from flask import jsonify,current_app,request
import json
from werkzeug.exceptions import BadRequest,Conflict,Forbidden
from util import db_util
from util.permissions import Admin_permission, Desk_permission, Token_permission
from flask_login import login_required,current_user
from routes.utils import fetch_entity,calc_audit_log_remaining_tokens
import os
from flask_restless.helpers import to_dict
import datetime

def get_existing_token_count(player_id=None,team_id=None,div_id=None,metadiv_id=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)

    query = None
    if div_id:
        query =  tables.Token.query.filter_by(division_id=div_id,paid_for=True,used=False)
    if metadiv_id:
        query = tables.Token.query.filter_by(metadivision_id=metadiv_id,paid_for=True,used=False)
    if player_id:
        query = query.filter_by(player_id=player_id)
    if team_id:
        query = query.filter_by(team_id=team_id)
    return query.count()

def check_linked_division(division_id, player_id=None, team_id=None):
    #FIXME : this should have actual contents
    pass
        
def check_add_token_for_max_tokens(num_tokens,div_id=None,metadiv_id=None,player_id=None,team_id=None):        
    if player_id:
        existing_token_count = get_existing_token_count(div_id=div_id,metadiv_id=metadiv_id,player_id=player_id)        
    if team_id:
        existing_token_count = get_existing_token_count(div_id=div_id,team_id=team_id)
    if metadiv_id:
        existing_token_count = get_existing_token_count(metadiv_id=metadiv_id,player_id=player_id)
        #FIXME : we assume metadivisions are not also team divisions
    if int(num_tokens) + int(existing_token_count) > int(current_app.td_config['MAX_TICKETS_ALLOWED_PER_DIVISION']):
        raise Conflict('Token add requested will push you over the max tokens for this division')


def check_add_token_request_is_valid(tokens_data, tables):
    if tokens_data.has_key('player_id') is False:
        raise BadRequest('No player_id specified')
    if tokens_data.has_key('divisions') is False and tokens_data.has_key('meta_divisions') is False and tokens_data.has_key('teams') is False:
        raise BadRequest('No divisions specified for tokens')
    player_id = tokens_data['player_id']
    player = fetch_entity(tables.Player,tokens_data['player_id'])
    if tokens_data.has_key('team_id'):
        team_id = tokens_data['team_id']
        team = fetch_entity(tables.Player,team_id)
    elif len(player.teams) > 0:
        team_id=player.teams[0].team_id
    else:
        team_id=None
            
    for div_id in tokens_data['divisions']:
        division=fetch_entity(tables.Division,div_id)
        if division.team_tournament is True:
            raise BadRequest('Tried to add a token for a single player in a team tournament')
        if division.meta_division_id is not None:
            raise BadRequest('Tried to add a division token to a metadivision')                    
        num_tokens = tokens_data['divisions'][div_id][0]
        check_add_token_for_max_tokens(num_tokens,div_id=div_id,player_id=player_id)        
    for div_id in tokens_data['teams']:
        division=fetch_entity(tables.Division,div_id)
        if division.team_tournament is False:
            raise BadRequest('Tried to add a token for a team in a non-team tournament')
        num_tokens = tokens_data['teams'][div_id][0]
        if int(num_tokens) > 0:
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,team_id=team_id)        
    for metadiv_id in tokens_data['metadivisions']:
        meta_division=fetch_entity(tables.MetaDivision,metadiv_id)
        num_tokens = tokens_data['metadivisions'][metadiv_id][0]        
        check_add_token_for_max_tokens(num_tokens,metadiv_id=metadiv_id,player_id=player_id)                     
    
def create_division_tokens(num_tokens,div_id=None,metadiv_id=None,player_id=None,team_id=None, paid_for=1, comped=False, player_id_for_team_audit_log=None):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    tokens = []
    json_tokens = []
    for token_num in range(0,int(num_tokens)):
        new_token = tables.Token()    
        if player_id:
            new_token.player_id=player_id                    
        if team_id:
            new_token.team_id=team_id
        if div_id:
            new_token.division_id = div_id
        if metadiv_id:
            new_token.metadivision_id = metadiv_id
        new_token.paid_for = True if paid_for == 1 else False
        new_token.used=False
        new_token.comped=comped
        if hasattr(current_user,'user_id'):
            new_token.deskworker_id=current_user.user_id
        
        db.session.add(new_token)                
        db.session.commit()
        db.session.commit()
        tokens.append(to_dict(new_token))
    return tokens

@admin_manage_blueprint.route('/token/teams/<player_id>',methods=['GET'])
def get_team_tokens_for_player(player_id):
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    teams = fetch_entity(tables.Player,player_id)         

    token_dict = {'teams':{}}    
    team = Team.query.filter(Team.players.any(Player.player_id.__eq__(player.player_id))).first()    
    if team is None:
        return jsonify(token_dict)    
    tokens = Token.query.filter_by(team_id=team.team_id,paid_for=True).all()
    
    #FIXME : need only active divisions
    divisions = Division.query.all()
    for division in divisions:
        token_dict['teams'][division.division_id]=0
    for token in tokens:        
        if token.team_id != None:
            token_dict['teams'][token.division_id]=token_dict['teams'][token.division_id] + 1      
    return jsonify(token_dict)

def get_available_ticket_list(max_count,increments=None):        
    normal_cost = 5
    discount_count = 3
    discount_cost = 12
    cur_count = 0
    cur_value = 0
    #max_count = 25
    multiplier = 1    
    #increments = [[2,5],
    #               [4,10],
    #               [6,15],
    #               [9,20],
    #               [10,25],
    #               [12,30]]
    
    available_ticket_list = [[0,0]]
    available_ticket_list_pruned = []    
    if increments:
        for idx,increment in enumerate(increments):
            if increments[idx][0]>max_count:
                break
            available_ticket_list.append(increment)
        return available_ticket_list
    while(cur_count < max_count):
        cur_count = cur_count+1
        is_discount_count = cur_count%discount_count        
        multiplier = cur_count/discount_count
        if is_discount_count == 0 and cur_count != 1:                        
            ticket_cost = multiplier*discount_cost
        else:
            ticket_cost = cur_count*normal_cost            
        available_ticket_list.append([cur_count,ticket_cost])
    ticket_list_len = len(available_ticket_list)
    for idx,available_ticket in enumerate(available_ticket_list):
        if idx > 0 and idx < ticket_list_len-1:
            if available_ticket_list[idx][1] > available_ticket_list[idx+1][1]:
                continue
        available_ticket_list_pruned.append(available_ticket_list[idx])
    return available_ticket_list_pruned
    
@admin_manage_blueprint.route('/token/player_id/<player_id>',methods=['GET'])
def get_tokens_for_player(player_id):
    #FIXME : needs more protection?
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    player = fetch_entity(tables.Player,player_id)
    team_ids = tables.Team.query.filter(tables.Team.players.any(player_id=player.player_id)).all()
    tokens = tables.Token.query.filter_by(player_id=player.player_id, paid_for=True).all()
    token_dict = {'divisions':{},'metadivisions':{},'teams':{}}
    remaining_tokens_dict={'divisions':{},'metadivisions':{},'teams':{},
                           'divisions_remaining_token_list':{},
                           'teams_remaining_token_list':{},
                           'metadivisions_remaining_token_list':{}}
    #FIXME : need only active divisions
    divisions = tables.Division.query.all()    
    metadivisions = tables.MetaDivision.query.all()
    max_tickets_allowed = int(current_app.td_config['MAX_TICKETS_ALLOWED_PER_DIVISION'])
    for division in divisions:
        if division.team_tournament is False and division.meta_division_id is None:
            if division.tournament.single_division or division.tournament.single_division is False and division.division_id == player.linked_division_id:
                div_count = get_existing_token_count(player_id=player_id, div_id=division.division_id)                
                token_dict['divisions'][division.division_id]=div_count
                remaining_tokens = max_tickets_allowed - div_count
                remaining_tokens_dict['divisions'][division.division_id] = remaining_tokens                
                remaining_tokens_dict['divisions_remaining_token_list'][division.division_id]=get_available_ticket_list(remaining_tokens)
        if division.meta_division_id is not None:
            metadiv_count = get_existing_token_count(player_id=player_id,metadiv_id=division.meta_division_id)
            token_dict['metadivisions'][division.meta_division_id]= metadiv_count
            remaining_tokens = max_tickets_allowed - metadiv_count             
            remaining_tokens_dict['metadivisions'][division.meta_division_id] = remaining_tokens
            remaining_tokens_dict['metadivisions_remaining_token_list'][division.meta_division_id]=get_available_ticket_list(remaining_tokens)            
        if division.team_tournament is True:
            for team in team_ids:
                team_count = get_existing_token_count(team_id=team.team_id,div_id=division.division_id)
                remaining_tokens = max_tickets_allowed - team_count
                token_dict['teams'][division.division_id]= team_count
                remaining_tokens_dict['teams'][division.division_id] = remaining_tokens
                remaining_tokens_dict['teams_remaining_token_list'][division.division_id]=get_available_ticket_list(remaining_tokens)
                
    return jsonify({'data':{'tokens':token_dict,'available_tokens':remaining_tokens_dict,'player':player.to_dict_simple()}})

@admin_manage_blueprint.route('/token/confirm_paid_for', methods=['PUT'])
@login_required
def confirm_tokens():
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    tokens_data = json.loads(request.data)['total_tokens']
    for token in tokens_data:
        token = fetch_entity(tables.Token,token['token_id'])
        if token:
            token.paid_for=True
            tables.db_handle.session.commit()
        #DB.session.add(new_audit_log_entry)
        #tables.db_handle.session.commit()        
            
    return jsonify({'data':token.to_dict_simple()})

@admin_manage_blueprint.route('/token/paid_for/<int:paid_for>', methods=['POST'])
@login_required
@Token_permission.require(403)
def add_token(paid_for):
    if current_user.is_player and paid_for != 0:
        raise Forbidden('Stop being a dick, you assface')        
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)    
    total_tokens=[]
    #tokens = []
    tokens_data = json.loads(request.data)
    check_add_token_request_is_valid(tokens_data, tables)    
    player_id = tokens_data['player_id']
    if 'comped' in tokens_data:
        comped = tokens_data['comped']
    else:
        comped = False
    player = fetch_entity(tables.Player,tokens_data['player_id'])
    if tokens_data.has_key('team_id'):        
        team_id = tokens_data['team_id']
        team = fetch_entity(tables.Player,team_id)
    #else:
    elif len(player.teams) > 0:
        team_id=player.teams[0].team_id
    else:
        team_id=None
    # FIXME : we rely on team_id being passed in - should check for it here
    for div_id in tokens_data['divisions']:
        #num_tokens = tokens_data['divisions'][div_id]
        num_tokens = tokens_data['divisions'][div_id][0]
        if num_tokens > 0:
            tokens = create_division_tokens(num_tokens,div_id=div_id,player_id=player_id, paid_for=paid_for,comped=comped)
            total_tokens = total_tokens + tokens
    for metadiv_id in tokens_data['metadivisions']:
        num_tokens = tokens_data['metadivisions'][metadiv_id][0]
        if num_tokens > 0:
            tokens = create_division_tokens(num_tokens,metadiv_id=metadiv_id,player_id=player_id, paid_for=paid_for,comped=comped)
            total_tokens = total_tokens + tokens
    for div_id in tokens_data['teams']:
        num_tokens = tokens_data['teams'][div_id][0]
        if int(num_tokens) > 0:
            check_add_token_for_max_tokens(num_tokens,div_id=div_id,team_id=team_id)
            tokens = create_division_tokens(num_tokens,div_id=div_id,team_id=team_id,paid_for=paid_for,comped=comped,player_id_for_team_audit_log=player_id)
            total_tokens = total_tokens + tokens            
    db.session.commit()
    division_token_summary = {}
    for token in total_tokens:
        if token['division_id'] not in division_token_summary:
            if team_id:            
                token_division_id = token['division_id']            
                token_division = tables.Division.query.filter_by(division_id=token_division_id).first()
                if token_division and token_division.team_tournament:
                    division_token_summary[token['division_id']]=token
            if token['metadivision_id'] is not None:
                    division_token_summary[99]=token
            if token['division_id'] is not None:
                    division_token_summary[token['division_id']]=token                            

#    for token in total_tokens:
    for div_id,token in division_token_summary.iteritems():
        audit_log = tables.AuditLog()
        if paid_for == 1:
            audit_log.purchase_date = datetime.datetime.now()
        if paid_for == 0:
            audit_log.player_purchase_request_date = datetime.datetime.now()            
        if player_id:
            audit_log.player_id = player_id
        if team_id:            
            token_division_id = token['division_id']
            
            token_division = tables.Division.query.filter_by(division_id=token_division_id).first()
            if token_division and token_division.team_tournament:
                audit_log.team_id = team_id
            
        audit_log.token_id=token['token_id']
        audit_log.deskworker_id=current_user.user_id
        if token['team_id'] is not None:            
            audit_log.num_tokens_purchased_in_batch=int(tokens_data['teams'][str(token['division_id'])][0])
        elif token['division_id'] is not None:
            audit_log.num_tokens_purchased_in_batch=int(tokens_data['divisions'][str(token['division_id'])][0])
        elif token['metadivision_id'] is not None:
            audit_log.num_tokens_purchased_in_batch=int(tokens_data['metadivisions'][str(token['metadivision_id'])][0])                        
        #tokens_left_string = calc_audit_log_remaining_tokens(player_id,team_id)        
        #audit_log.remaining_tokens = tokens_left_string        
        db.session.add(audit_log)
        db.session.commit()
    tokens_left_string = calc_audit_log_remaining_tokens(player_id,team_id)        
    if paid_for == 1:
        audit_log = tables.AuditLog()
        audit_log.action="purchase_summary"
        audit_log.description=tokens_left_string
        audit_log.player_id=player_id
        db.session.add(audit_log)
        db.session.commit()
    total_divisions_tokens_summary = {}
    total_metadivisions_tokens_summary = {}
    for div_id in tokens_data['divisions']:
        total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token['division_id'])==str(div_id)])
    for div_id in tokens_data['teams']:
        total_divisions_tokens_summary[div_id] = len([token for token in total_tokens if str(token['division_id'])==str(div_id)])
    for metadiv_id in tokens_data['metadivisions']:
        total_metadivisions_tokens_summary[metadiv_id] = len([token for token in total_tokens if str(token['metadivision_id'])==str(metadiv_id)])
         
    return jsonify({'data':{'divisions':total_divisions_tokens_summary,
                            'metadivisions':total_metadivisions_tokens_summary,                            
                            'tokens':total_tokens}})


