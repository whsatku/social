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

app.controller('EventController', function($scope, $http, $location, $uibModal, $rootScope){
    var eventID = $location.path().split('/')[2];
    $scope.isSelected = false;
    $scope.role = 0;
    $http.get('/api/event/'+eventID).success(function(data){
        $scope.event = data;
    });
    
    $http.get('/api/event/'+eventID+ '/member/' + $rootScope.user.id).success(function(data){
        $scope.role = data.role;
        if( data.role == 0) {
            $scope.isSelected = false;
        }
        else {
            $scope.isSelected = true;
        }
        console.log($scope.isSelected);
    });

    $scope.invite = function(){
        var modal = $uibModal.open({
            templateUrl: 'templates/dialog/invite.html',
            controller: function($scope, $uibModalInstance, $http){
                $http.get('/api/user/friends/invite/').success(function(data){
                    $scope.friends = data;
                    console.log($scope.friends);
                });
                
                $scope.ok = function(){
                    $uibModalInstance.close($scope.invitee);
                    console.log($scope.invitee);
                    $http.put('/api/event/'+ eventID +'/member/'+ $scope.invitee).success(function(data){
                        console.log('put');
                    });
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

        var decline = data.filter( function(member){return (member.role==4);} );
        $scope.decline_count = decline.length;

        $scope.members = data;
        $scope.member_count = data.length - decline.length;

        var ad = data.filter( function(member){return (member.role==1);} );
        $scope.admin = ad[0];

        var atten = data.filter( function(member){return (member.role==2);} );
        $scope.attendants = atten;
        $scope.attendants_count = atten.length;

        var may = data.filter( function(member){return (member.role==3);} );
        $scope.maybe = may;
        $scope.maybe_count = may.length;
    });

    $scope.going = function(){
        console.log('gogogogogogokuy');
        $http.put('/api/event/'+ eventID +'/member/'+ $rootScope.user.id + '/' + 2).success(function(data){
            console.log('put');
        });
    };

    $scope.decline = function(){
        console.log('kuy im not going');
        $http.put('/api/event/'+ eventID +'/member/'+ $rootScope.user.id + '/' + 4).success(function(data){
            console.log('put');
        });
    };

    $scope.maybef = function(){
        console.log('kuy i dont know');
        $http.put('/api/event/'+ eventID +'/member/'+ $rootScope.user.id + '/' + 3).success(function(data){
            console.log('put');
        });
    };

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