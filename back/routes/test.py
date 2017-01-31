from blueprints import admin_manage_blueprint
from flask import jsonify,current_app,request
from werkzeug.utils import secure_filename
import json
import os
import subprocess
from util import db_util
from routes.utils import fetch_entity

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@admin_manage_blueprint.route('/test/player_fast', methods=['GET'])
def test_players_fast():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.all() if player.active is True}
    return jsonify({'data':players})
    # check if the post request has the file part            

@admin_manage_blueprint.route('/test/player_prereg_fast', methods=['GET'])
def test_prereg_players_fast():    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    players = {player.player_id:player.to_dict_fast() for player in tables.Player.query.filter_by(pre_reg_paid=True,active=False).all()}
    return jsonify({'data':players})
    # check if the post request has the file part            
    
@admin_manage_blueprint.route('/test/players_with_tickets/<division_id>', methods=['GET'])
def test_players_with_tickets(division_id):    
    db = db_util.app_db_handle(current_app)
    tables = db_util.app_db_tables(current_app)
    division = fetch_entity(tables.Division,division_id)     
    if division.meta_division_id:
        players_with_tickets = tables.Player.query.join(tables.Token).filter_by(used=False,
                                                                                paid_for=True,
                                                                                voided=False,
                                                                                metadivision_id=division.meta_division_id).all()        
    else:
        players_with_tickets = tables.Player.query.join(tables.Token).filter_by(used=False,
                                                                                paid_for=True,
                                                                                voided=False,
                                                                                division_id=division_id).all()
    return jsonify({'data':{player.player_id:player.to_dict_fast() for player in players_with_tickets if player.active is True}})    
    # check if the post request has the file part            

@admin_manage_blueprint.route('/test/media_upload', methods=['POST'])
def test_upload_file():    
    # check if the post request has the file part            
    if 'file' not in request.files:                                
        return jsonify({})        
    file = request.files['file']            
    if file.filename == '':            
        return jsonify({})        
    if file:                        
        filename = secure_filename(file.filename)                        
        save_path=os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        file.close()
        #convert /var/www/html/pics/player_1.jpg  -resize 128x128  /var/www/html/pics/resize_player_1.jpg
        subprocess.call(["convert", save_path,"-resize", "128x128","-define","jpeg:extent=15kb", "%s_resize"%save_path])        
        subprocess.call(["mv","%s_resize"%save_path,save_path])
    return jsonify({'poop':filename})

