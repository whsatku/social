(function(){

var app = angular.module('app.event', []);

app.controller('CreateEventController', function($scope, $state, $http, $stateParams, $filter){

    // $scope.ename = "";
    // $scope.edescription = "";
    // $scope.start_date = "";
    // $scope.end_date = "";
    // $scope.start_time = "";
    // $scope.end_time = "";

    $scope.createEvent = function(){
        var name = $scope.new_event.ename;
        var description = $scope.new_event.edescription;
        var date1 = $filter('date')(new Date($scope.new_event.start_date), 'yyyy-MM-dd');
        var date2 = $filter('date')(new Date($scope.new_event.end_date), 'yyyy-MM-dd');
        // var time1 = $filter('date')(new Date($scope.new_event.start_time), 'HH:mm:ss');
        // var time2 = $filter('date')(new Date($scope.new_event.end_time), 'HH:mm:ss');
        


        console.log(date1);
        console.log(date2);
        console.log(time1);
        console.log(time2);

        // $scope.start_date = date1;
        // $scope.end_date = date2;
        // $scope.start_time = time1;
        // $scope.end_time = time2;


        shit = {
            name,
            date1,
            date2,
            description,
            time1,
            time2,
        }

        
        // $scope.new_event = {
        //     name: $scope.ename,
        //     start_date: $scope.start_date,
        //     end_date: $scope.end_date,
        //     description: $scope.edescription,
        //     start_time: $scope.start_time,
        //     end_time: $scope.end_time,
        // };


        $http.post('/api/event/create/' , shit ).success(function(data){
            $state.go('root.event', {
                id: data.id
            }, {
                reload: true
            });
        });
    }
});

})();