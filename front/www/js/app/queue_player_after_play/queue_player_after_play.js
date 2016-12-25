angular.module('app.queue_player_after_play',['app.queue_player_after_play.confirm',
    /*REPLACEMECHILD*/]);
angular.module('app.queue_player_after_play').controller(
    'app.queue_player_after_play',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.player_id=$state.params.player_id;
	$scope.division_id=$state.params.division_id;
	$scope.player_name=$state.params.player_name;
        //FIXME : need to add this info at the scorekeeping route level
        $scope.division_name=$state.params.division_name;
        $scope.division_machine_just_played_id=$state.params.division_machine_just_played_id;
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        console.log('--');
        console.log($scope.division_id);
        console.log($scope.division_machine_just_played_id);
        division_machines_promise = TimeoutResources.GetDivisionMachines(undefined,{site:$scope.site,division_id:$scope.division_id});        
        Modals.loading();
        division_machines_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });             
    }]
);
