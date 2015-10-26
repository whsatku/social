(function(){

var app = angular.module('app.userprofile', []);

app.controller('UserProfileInfoController', function($scope, $http, $location, $stateParams){
    var userID = $stateParams.user;
    $http.get('/api/user/'+userID+'/userInfo').success(function(data){
        $scope.userprofile = data;
    });
});

})();