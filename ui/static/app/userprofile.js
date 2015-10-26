(function(){

var app = angular.module('app.userprofile', []);

app.controller('UserProfileInfoController', function($scope, $http, $location){
    console.log("hleelllooooo")
    var userID = $location.path().split('/')[2];
    $http.get('/api/user/'+userID).success(function(data){
        $scope.group = data;
    });
});

})();