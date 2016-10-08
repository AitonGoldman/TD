angular.module('TD_services.user', []);
angular.module('TD_services.user').factory('User', function() {
    var logged_in_user = undefined;
    var logged_in_player = undefined;
    var logged_in_status = false;
    var type_of_user = undefined;
    return {
        logged_in: function(){
            return logged_in_status;  
        },
        logged_in_user: function() {
            if(type_of_user == "user"){
                return logged_in_user;
            }
            if(type_of_user == "user"){
                return logged_in_user;
            }
            return undefined;
        },        
        set_logged_in_user: function(new_user) { logged_in_user = new_user; type_of_user = "user";logged_in_status=true},
        set_logged_in_player: function(new_player) { logged_in_player = new_player; type_of_user = "player"; logged_in_status=true;},
        
        has_role: function(role) { 
            return logged_in_user && logged_in_user.roles && (
                logged_in_user.roles.indexOf(role) != -1
            );
        },
    };
});

