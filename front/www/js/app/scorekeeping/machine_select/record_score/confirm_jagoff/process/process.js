angular.module('app.scorekeeping.machine_select.record_score.confirm_jagoff.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm_jagoff.process').controller(
    'app.scorekeeping.machine_select.record_score.confirm_jagoff.process',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $ionicHistory.nextViewOptions({disableBack:true});            

            $scope.site=$state.params.site;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.team_tournament=$state.params.team_tournament;
	$scope.player_name=$state.params.player_name;
	$scope.score=$state.params.score;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_id=$state.params.division_id;
	$scope.player_id=$state.params.player_id;
            $scope.queue_args={queue_args:{division_machine_id:$scope.division_machine_id,division_machine_name:$scope.division_machine_name,team_tournament:false}};
        
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});

        declare_jagoff_promise = TimeoutResources.DeclareJagoff(queues_promise,{site:$scope.site,division_machine_id:$scope.division_machine_id});
     
        
        // = TimeoutResources.GetEtcData();
        declare_jagoff_promise.then(function(data){
        $scope.resources = TimeoutResources.GetAllResources();
            $scope.division_machine_queue_length = $scope.resources.queues.data[$scope.division_machine_id].queues.length;
            if($scope.division_machine_queue_length > 0){
                $scope.division_machine_queue_player = $scope.resources.queues.data[$scope.division_machine_id].queues[0].player.player_name;
            }            
            Modals.loaded();
        });
    }]
);
