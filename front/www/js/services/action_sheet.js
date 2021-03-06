angular.module('TD_services.action_sheets',[]);
angular.module('TD_services.action_sheets')
    .factory('ActionSheets',
             ['$state','$timeout',
              '$ionicLoading','$ionicModal',
              '$rootScope', '$ionicActionSheet','Modals','TimeoutResources',
              function($state,$timeout,
                       $ionicLoading,$ionicModal,
                       $rootScope,$ionicActionSheet,Modals,
                       TimeoutResources) {        
                  
                  var choose_action = function(site,division_id,tournament,dest_route){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Edit Tournament' },
                              { text: 'Activate/Deactivate Tournament' }
                          ],                    
                          titleText: 'Tournament Actions',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  $state.go(dest_route,{division_id:division_id});
                              }
                              if(index == 1){
                                  if(tournament.active == true){
                                      new_tournament_status=false;
                                      tournament.active=false;
                                  } else {                                
                                      new_tournament_status=true;
                                      tournament.active=true;
                                  }
                                  Modals.loading();
                                  active_promise = TimeoutResources.UpdateDivision(undefined,{site:site},{division_id:division_id,active:new_tournament_status});
                                  active_promise.then(function(data){
                                      Modals.loaded();
                                  });
                              }
                              return true;
                          }
                      });
                  };
                  var choose_confirm_action = function(target){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Leave Confirm Page' }                              
                          ],                    
                          titleText: '<b style="color:red">You are leaving a confirm screen without completing the action!  Are you sure you want to do this?</b>',
                          cancelText: 'Cancel',
                          cancel: function() {
                              //player_info.linked_division_id = player_info.old_linked_division_id;
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              $state.go(target);
                              return true;
                          }
                      });
                  };                  
                  
                  var choose_change_div = function(player_info){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Continue' }                              
                          ],                    
                          titleText: '<b>This will void all tickets in the old division!  Are you sure you want to do this?</b>',
                          cancelText: 'Cancel',
                          cancel: function() {
                              player_info.linked_division_id = player_info.old_linked_division_id;
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              return true;
                          }
                      });
                  };                  
                  var choose_player_action = function(player_id){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Edit Player' },
                              { text: 'View Player Info' }
                          ],                    
                          titleText: 'Player Actions',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  $state.go('.edit_player',{player_id:player_id});
                              }
                              if(index == 1){
                                  $state.go('.player_info',{player_id:player_id});
                              }
                              return true;
                          }
                      });
                  };
                  var choose_queue_action = function(player_name, player_id, queue_remove_function){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Remove '+player_name },                              
                          ],                    
                          titleText: 'Remove Player From Queue?',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  queue_remove_function(player_id);
                              }
                              return true;
                          }
                      });
                  };                  
                  var queue_no_action = function(){            
                      var hideSheet = $ionicActionSheet.show({                    
                          titleText: 'No one is playing the machine.<br>See the scorekeeper to start playing it.',
                          cancelText: 'Ok'
                      });
                  };                  
                  
                  var choose_void_action = function(division_machine_id,prefixroute){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'VOID' },                              
                          ],                    
                          titleText: 'DO YOU WANT TO VOID THIS TICKET',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  if(prefixroute!=undefined){
                                      void_route = prefixroute+".void";
                                  } else {
                                      void_route = '.void';
                                  }
                                  $state.go(void_route,{process_step:{process:true}});                                  
                              }
                              return true;
                          }
                      });
                  };
                  var choose_machine_action = function(division_machine,remove_machine){            
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'REMOVE MACHINE' },
                              { text: 'Upload Backglass Pic'}
                          ],                    
                          titleText: 'Choose action for machine',
                          cancelText: 'Cancel',
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              if(index == 0){
                                  remove_machine(division_machine);
                              }
                              if(index == 1){
                                  $state.go('.upload_pic',{division_machine_id:division_machine.division_machine_id});
                              }
                              
                              return true;
                          }
                      });
                  };
                  var player_paid_in_line_registration_confirm = function(){
                      var hideSheet = $ionicActionSheet.show({
                          buttons: [
                              { text: 'Player Paid' }
                          ],
                          titleText: '<b style="color:red">Confirm Player Paid Door Fee</b>',
                          cancelText: 'Cancel',
                          cancel: function() {
                              //player_info.linked_division_id = player_info.old_linked_division_id;
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              $state.go('.door_fee_process',{process_step:{process:true}});
                              return true;
                          }
                      });
                      
                  }
                  var choose_ifpa_lookup_action = function(ifpa_search_results,result,limit_divisions_based_on_ranking){            
                      cancel_text='Cancel';
                      result.looked_up = true;
                      buttons = [];
                      console.log(ifpa_search_results);
                      if(ifpa_search_results == "No players found"){
                          title_text = "No results returned!";
                          cancel_text='Ok';
                          ifpa_search_results=[];
                      }
                      if(ifpa_search_results.length > 4){
                          title_text = "Too many results returned! Refine your search.";
                      }
                      if(ifpa_search_results.length > 0 && ifpa_search_results.length <=4){
                          for(i in ifpa_search_results){
                              button_text = ifpa_search_results[i].first_name+" "+ifpa_search_results[i].last_name+" : "+ifpa_search_results[i].wppr_rank;
                              buttons.push({result:ifpa_search_results[i],text: button_text});
                          }
                          title_text = "Choose correct player";
                      }
                      var hideSheet = $ionicActionSheet.show({
                          buttons: buttons,                    
                          titleText: title_text,
                          cancelText: cancel_text,
                          cancel: function() {
                              // add cancel code..
                          },
                          buttonClicked: function(index) {
                              //result.rank = buttons[index].result.wppr_rank;
                              console.log(buttons[index].result.wppr_rank);
                              limit_divisions_based_on_ranking(buttons[index].result.wppr_rank);
                              result.result = buttons[index].result;
                              return true;
                          }
                      });
                  };
                  
                  return {
                      choose_machine_action:choose_machine_action,
                      choose_action:choose_action,
                      choose_player_action:choose_player_action,
                      choose_ifpa_lookup_action:choose_ifpa_lookup_action,
                      choose_change_div:choose_change_div,
                      choose_void_action:choose_void_action,
                      choose_queue_action:choose_queue_action,
                      queue_no_action:queue_no_action,
                      choose_confirm_action:choose_confirm_action,
                      player_paid_in_line_registration_confirm:player_paid_in_line_registration_confirm
                  };
              }]);
