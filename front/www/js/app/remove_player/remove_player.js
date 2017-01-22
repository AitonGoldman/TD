angular.module('app.remove_player',['app.remove_player.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.remove_player').controller(
    'app.remove_player',[
        '$scope','$state','TimeoutResources','Utils','Modals','$animate','$filter',
        function($scope, $state, TimeoutResources, Utils,Modals,$animate,$filter) {
            $animate.enabled(false);
            $scope.test_submit = function(){
                if($scope.selected_players.length != 0 && $scope.selected_players[0].division_machine != undefined){
                    console.log($scope.selected_players[0]);
                    $state.go('.confirm',{player_id:$scope.selected_players[0].player_id,
                                          player_name:$scope.selected_players[0].full_name,
                                          machine_name:$scope.selected_players[0].division_machine.division_machine_name,
                                          division_machine_id:$scope.selected_players[0].division_machine.division_machine_id});
                }
            };
            $scope.keyDown = function(event){
                if(event.keyCode == 9 || event.keyCode==13){
                    //$state.go('.token_select',{player_id:$scope.selected_players[0].player_id});
                }
                //keyCode 9               
            };
            $scope.site=$state.params.site;
            
            $scope.player = {};
            $scope.utils = Utils;
            Modals.loading();
            $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                            
            
            players_promise = TimeoutResources.GetPlayers($scope.bootstrap_promise,{site:$scope.site});            
            // = TimeoutResources.GetEtcData();
            players_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                $scope.flattened_players = _.values($scope.resources.players.data);
                $animate.enabled(true);                              
                Modals.loaded();
            });
            $scope.selected_players=[];
            $scope.onPlayerIdChange = function(){                
                $scope.poop = true;
                $scope.selected_players = $filter('filter')($scope.flattened_players,{player_id:parseInt($scope.player.player_id)},true);
                if($scope.selected_players!=undefined && $scope.selected_players.length!=0){
                    $scope.player_img_id=$scope.selected_players[0].player_id;
                }                
            };
    }]
);
