(function(){

var app = angular.module('app.group', []);

app.controller('GroupController', function($scope, $stateParams, Restangular, $http, $location){
    $scope.GroupApi = Restangular.one('group', $stateParams.id);
    $scope.joinStatus = 0;
    $scope.joinGroup = function(){
        $scope.GroupApi.all('member/pending').post().then(function(){
            $scope.joinStatus = 1;
        }, function(xhr){
            alert(xhr.data);
            console.log(xhr.data);
        });
    };
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID+'/detail/').success(function(data){
        $scope.group = data;
    });
});

app.controller('GroupInfoController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID+'/detail/').success(function(data){
        $scope.group = data;
    });
});

app.controller('GroupManageController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID+'/member/accepted').then(function(data){
        $scope.groupMember = data.data;
    });
    $http.get('/api/group/'+groupID+'/member/pending').then(function(data){
        $scope.groupMember_pending = data.data;
    });

    
    function acceptMember(pk){
        console.log("acceptMember : " + pk)
        $http.put('/api/group/'+groupID+'/member/'+pk).then(function(data){
            console.log();
        });
    }
    $scope.acceptMember = acceptMember;
})

})();