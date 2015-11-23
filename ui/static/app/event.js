(function(){

var app = angular.module('app.event', []);

app.controller('CreateEventController', function($scope, $state, $http, $stateParams){

    $scope.ename = "";
    $scope.edescription = "";
    $scope.start_date = "";
    $scope.end_date = "";
    $scope.start_time = "";
    $scope.end_time = "";

    $scope.createEvent = function(){

        $scope.new_event = {
            name: $scope.ename,
            start_date: $scope.start_date,
            end_date: $scope.end_date,
            description: $scope.edescription,
            start_time: $scope.start_time,
            end_time: $scope.end_time,
        };


        $http.post('/api/event/create/' , $scope.new_event ).success(function(data){
            $state.go('root.event', {
                id: data.id
            }, {
                reload: true
            });
        });
    }
});

})();