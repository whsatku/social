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
        });
    };

    $http.get('/api/event/'+eventID+'/member').success(function(data){
        $scope.members = data;

        $scope.member_count = data.length;
        console.log($scope.member_count);

        var ad = data.filter( function(member){return (member.role==1);} );
        $scope.admin = ad[0];
    });
});

app.controller('EventBrowseController', function($scope, $http){
    var temp;
    var events_without_first = new Array();

    function shuffle(o){
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
        return o;
    }

    $http.get('/api/event/all').success(function(data){
        console.log(data);
        shuffle(data);
        $scope.all_event = data;
        $scope.first_event = data[0];
        temp = data;
        for (i=0; i<temp.length; i++){
            events_without_first.push(temp[i]);
        }
        events_without_first.shift();
        $scope.events = events_without_first;
    });
});

})();