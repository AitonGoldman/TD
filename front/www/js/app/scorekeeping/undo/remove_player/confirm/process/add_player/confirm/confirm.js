angular.module('app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm',['app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm').controller(
    'app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.player_name_to_add=$state.params.player_name_to_add;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.player_name=$state.params.player_name;
	$scope.player_id=$state.params.player_id;
	$scope.player_id_to_add=$state.params.player_id_to_add;
	$scope.division_id=$state.params.division_id;

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
