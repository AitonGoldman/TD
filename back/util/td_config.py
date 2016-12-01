from configobj import ConfigObj
import os 


def get_config_values_from_env():
    config_dict = {}
    config_dict['DB_USERNAME']=None
    config_dict['DB_PASSWORD']=None
    config_dict['DB_TYPE']=None
    config_dict['FLASK_SECRET_KEY']=None
    config_dict['MAX_TICKETS_ALLOWED_PER_DIVISION']=None
    config_dict['STRIPE_API_KEY']=None
    config_dict['QUEUE_BUMP_AMOUNT']=None
    for key,value in config_dict.iteritems():
        config_dict[key]=os.getenv(key,None)
    return config_dict

def get_config_values_from_file(config_dict,td_config_filename=None,db_config_filename=None):
    if td_config_filename is None:
        td_config_filename=os.getenv('TD_CONFIG_FILENAME',None)
    if db_config_filename is None:
        db_config_filename=os.getenv('DB_CONFIG_FILENAME',None)

    if td_config_filename is None or db_config_filename is None:
        return config_dict
    td_config=ConfigObj(td_config_filename)
    db_config=ConfigObj(db_config_filename)

    for key,value in config_dict.iteritems():
        config_dict[key]=td_config.get(key) if config_dict[key] is None else config_dict[key]
        config_dict[key]=db_config.get(key) if config_dict[key] is None else config_dict[key]        
    return config_dict

def sanity_check_config_dict(config_dict):
    if config_dict['FLASK_SECRET_KEY'] is None:
        raise Exception("You didn't configure your flask secret key!")    
    if config_dict['DB_TYPE'] is None :
        raise Exception("You didn't configure a db_type!")    
    
def get_db_config():
    config_dict = get_config_values_from_env()
    return get_config_values_from_file(config_dict)    
    

def assign_loaded_configs_to_app(app,
                         td_config_filename=None,                         
                         db_config_filename=None):    
    config_dict = get_config_values_from_env()
    config_dict = get_config_values_from_file(config_dict,td_config_filename,db_config_filename)    
    
    sanity_check_config_dict(config_dict)
    app.td_config = config_dict
    app.secret_key = app.td_config['FLASK_SECRET_KEY']
    return config_dict
