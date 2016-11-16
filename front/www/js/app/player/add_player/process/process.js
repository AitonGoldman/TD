angular.module('app.player.add_player.process',[/*REPLACEMECHILD*/]);
angular.module('app.player.add_player.process').controller(
    'app.player.add_player.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        $scope.player_info=$state.params.player_info;        
        $scope.player_info.ifpa_ranking=$scope.player_info.ifpa_result.result.wppr_rank;
        $scope.player_info.ifpa_result=undefined;
        Modals.loading();
        player_add_promise = TimeoutResources.AddPlayer(undefined,{site:$scope.site},$scope.player_info);
        // = TimeoutResources.GetEtcData();
        player_add_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);