(function(){

var app = angular.module('app.event', []);

app.controller('CreateEventController', function($scope, $state, $http, $stateParams){

    $scope.createEvent = function(){
        var name = $scope.new_event.ename;
        var description = $scope.new_event.edescription;

        var start_date = moment($scope.new_event.start_date)
            .add($scope.new_event.start_time);
        var end_date = moment($scope.new_event.end_date)
            .add($scope.new_event.end_time);

        var new_event = {
            name: name,
            start_date: start_date.toISOString(),
            end_date: end_date.toISOString(),
            description: description
        }


        $http.post('/api/event/create/' , new_event ).success(function(data){
            $state.go('root.event', {
                event: data.id
            }, {
                reload: true
            });
        });
    }
});

app.controller('EventController', function($scope, $http, $location, $uibModal){
    var eventID = $location.path().split('/')[2];
    $http.get('/api/event/'+eventID).success(function(data){
        $scope.event = data;
        console.log($scope.event)
    });

    $scope.invite = function(){
        var modal = $uibModal.open({
            templateUrl: 'templates/dialog/invite.html',
            controller: function($scope, $uibModalInstance){
                $scope.ok = function(){
                    $uibModalInstance.close($scope.invitee);
                };
                $scope.cancel = function(){
                    $uibModalInstance.dismiss();
                };
            }
        });
        modal.result.then(function(data){
            console.log(data);
        });
    };
});

})();