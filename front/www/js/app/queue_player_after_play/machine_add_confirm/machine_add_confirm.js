angular.module('app.queue_player_after_play.machine_add_confirm',['app.queue_player_after_play.machine_add_confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.queue_player_after_play.machine_add_confirm').controller(
    'app.queue_player_after_play.machine_add_confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_machine_just_played_name=$state.params.division_machine_just_played_name;
	$scope.division_name=$state.params.division_name;
	$scope.player_id=$state.params.player_id;
	$scope.division_machine_to_add_to_name=$state.params.division_machine_to_add_to_name;
	$scope.division_machine_to_add_to_id=$state.params.division_machine_to_add_to_id;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_just_played_id=$state.params.division_machine_just_played_id;
	$scope.player_name=$state.params.player_name;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
