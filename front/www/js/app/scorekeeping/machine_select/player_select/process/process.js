angular.module('app.scorekeeping.machine_select.player_select.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.player_select.process').controller(
    'app.scorekeeping.machine_select.player_select.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.player_id=$state.params.player_id;
	$scope.division_machine_id=$state.params.division_machine_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.player_info=$state.params.player_info;
        $scope.from_queue=$state.params.from_queue;
        if($scope.from_queue == 0){
            Modals.loading();
            add_player_to_machine_promise = TimeoutResources.AddPlayerToMachine(undefined,{site:$scope.site,division_id:$scope.division_id,division_machine_id:$scope.division_machine_id,player_id:$scope.player_info.player_id});
            //= TimeoutResources.GetEtcData();
            add_player_to_machine_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                console.log($scope.resources);
                Modals.loaded();
            });            
        }

        if($scope.from_queue == 1){
            Modals.loading();
            add_player_to_machine_promise = TimeoutResources.AddPlayerToMachineFromQueue(undefined,{site:$scope.site,division_machine_id:$scope.division_machine_id});
            //= TimeoutResources.GetEtcData();
            add_player_to_machine_promise.then(function(data){
                $scope.resources = TimeoutResources.GetAllResources();
                console.log($scope.resources);
                Modals.loaded();
            });            
        }
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);