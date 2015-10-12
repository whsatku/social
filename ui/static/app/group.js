(function(){

var app = angular.module('app.group', []);

app.controller('GroupController', function($scope, $stateParams, Restangular, $http, $location, $window){
    $scope.GroupApi = Restangular.one('group', $stateParams.id);
    $scope.joinStatus = 0;
    $scope.joinGroup = function(){
        $scope.GroupApi.all('member/').post().then(function(){
            $scope.joinStatus = 1;
            $window.location.reload();
        }, function(xhr){
                console.log(xhr.data);
        });
    };
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });
});

app.controller('GroupInfoController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });
});

app.controller('GroupManageController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    function fetchMember(){
        $http.get('/api/group/'+groupID+'/member/accepted').then(function(data){
            $scope.groupMember = data.data;
        });
        $http.get('/api/group/'+groupID+'/member/pending').then(function(data){
            $scope.groupMember_pending = data.data;
        });
    }

    fetchMember();

    function acceptMember(pk){
        console.log("acceptMember : " + pk);
        $http.put('/api/group/'+groupID+'/member/'+ pk).then(function(data){
            fetchMember();
        });
    }
    function denyMember(pk){
        console.log("delete : " + pk);
        $http.delete('/api/group/'+groupID+'/member/'+ pk).then(function(data){
            fetchMember();
        });
    }
    $scope.acceptMember = acceptMember;
    $scope.denyMember = denyMember;
})

app.controller('AdminPageController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    
    $http.get('/api/group/'+groupID).then(function(data){
        $scope.group = data.data;
    });
    console.log("admin")
    $scope.editInfo = function(){
        console.log("hello")
        console.log("desc : " + $scope.group.description);
        console.log("sh_desc : " + $scope.group.short_description);
        console.log("ac : " + $scope.group.activities);
        console.log($scope.group);
        $http.put('/api/group/'+groupID+'/edit/',$scope.group).success(function(data){
                   });
    }
   
})

})();