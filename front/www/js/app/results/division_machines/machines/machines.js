angular.module('app.results.division_machines.machines',['app.results.division_machines.machines.machine',
    /*REPLACEMECHILD*/]);
angular.module('app.results.division_machines.machines').controller(
    'app.results.division_machines.machines',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        division_machines_promise = TimeoutResources.GetFromResultsDivisionMachines($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
                
        division_machines_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();

            $scope.flattened_division_machines = _.values($scope.resources.division_machines.data);
            $scope.flattened_division_machines.sort(function (a, b) {
                //return (a.division_machine_id > b.division_machine_id ? 1 : -1);
                return (a.division_machine_name > b.division_machine_name ? 1 : -1);
            });            
            
            Modals.loaded();
        });
    }]
);
