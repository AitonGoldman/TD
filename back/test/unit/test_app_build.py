import unittest
from mock import MagicMock
from pss_unit_test_base import PssUnitTestBase
from app import app_build,CustomJsonEncoder
from flask import Flask
from flask_principal import Principal

class AppBuildTest(PssUnitTestBase):    
    def setUp(self):
        #self.tables.Token.query = MagicMock()        
        #self.tables.Team.query = MagicMock()        
        #self.tables.Division.query = MagicMock()        
        #self.mock_app.tables = self.tables
        #self.mock_app.tables.db_handle = MagicMock()
        pass
    
    def test_get_base_app_for_existing_event(self):
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop',flask_secret_key='poop_key')]
        
        app.tables.Events.query.all.return_value=fake_events
        configured_app = app_build.get_base_app('poop',app,{})        
        custom_json_encoder = configured_app.json_encoder("test string to encode")
        principals = configured_app.my_principals
        self.assertTrue(type(custom_json_encoder) is CustomJsonEncoder.CustomJSONEncoder)
        self.assertTrue(type(principals) is Principal)
        self.assertTrue(type(configured_app.event_config) is dict)
        self.assertTrue('flask_secret_key' in configured_app.event_config)
        self.assertEquals(configured_app.event_config['flask_secret_key'],'poop_key')
        
        self.assertTrue(len(configured_app.event_config.keys()) > 0)
        self.assertEquals(len(configured_app.error_handler_spec[None].keys()),27)
        self.assertTrue(400 in configured_app.error_handler_spec[None])

        pass        
        
    def test_get_base_app_for_nonexistent_event(self):
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop4')]
        
        app.tables.Events.query.all.return_value=fake_events
        with self.assertRaises(Exception) as cm:
            app_build.get_base_app('poop',app,{})                    
        self.assertEquals(cm.exception.message,'event poop does not exist')

    def test_get_base_app_with_nonexistent_flask_secret_key(self):
        app = Flask('poop')        
        app.tables = MagicMock()
        fake_events = [self.tables.Events(name='poop2'),
                       self.tables.Events(name='poop3'),
                       self.tables.Events(name='poop')]
        
        app.tables.Events.query.all.return_value=fake_events
        with self.assertRaises(Exception) as cm:
            app_build.get_base_app('poop',app,{})                    
        self.assertEquals(cm.exception.message,"You didn't configure your flask secret key!")
        
        
