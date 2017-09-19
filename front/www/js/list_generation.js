angular.module('list_generation',[]);
angular.module('list_generation')
    .factory('listGeneration',
             [function() {
                 var toggle_view_item_actions = function(item){
                     if(item.display_actions==undefined){
                         item.display_actions=true;
                         return;
                     }
                     item.display_actions=item.display_actions==false;
                 };
                 var generate_set_list_items_ui_sref_and_args = function(sref,display_label_field){
                     var set_list_items_ui_sref_and_args = function(i) {                                     
                         i.ui_sref=sref;
                         i.label_to_display=i[display_label_field];                
                     };
                     return set_list_items_ui_sref_and_args;
                 };
                 var generate_tournament_machine_actions = function(){
                     var set_actions = function(i){

                     };
                     return set_actions;
                 };
                 var generate_set_list_items_actions_and_args = function(display_label_field,advanced_sref,wizard_sref,basic_sref,display_active_toggle) {
                     var set_list_items_actions_and_args = function(i) {                                     
                         i.actions_ui_sref_list = [{label:"Advanced Editing",ui_sref:advanced_sref}];
                         if(i.wizard_configured == false){
                             basic_edit_action = {label:"Wizard Configuration",ui_sref:wizard_sref};
                         } else {
                             basic_edit_action = {label:"Basic Editing",ui_sref:basic_sref};
                         }
                         i.actions_ui_sref_list.splice(0,0,basic_edit_action);
                         if(display_active_toggle==undefined){
                             i.actions_ng_click_list=[{label:"Toggle active",ng_click:'toggle_item_active(item,event_name)'}];
                         }                         
                         i.label_to_display=i[display_label_field];
                         
                     };             
                     return set_list_items_actions_and_args;
                 };

                 var set_active_inactive_icon = function(i){                     
                     if(i.active == undefined){                                                
                        return;                        
                    }
                    if(i.active == true){                        
                        i.icon='ion-play';
                    } else {                        
                        i.icon='ion-stop';
                    }                     
                 };

                 return {
                     generate_set_list_items_ui_sref_and_args:generate_set_list_items_ui_sref_and_args,
                     toggle_view_item_actions:toggle_view_item_actions,
                     generate_set_list_items_actions_and_args:generate_set_list_items_actions_and_args,
                     set_active_inactive_icon:set_active_inactive_icon,
                     generate_tournament_machine_actions:generate_tournament_machine_actions
                 };
             }
             ]
            );