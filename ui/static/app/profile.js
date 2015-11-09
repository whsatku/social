(function(){

var app = angular.module('app.profile', []);

app.controller('FriendsController', function($scope, $stateParams, Restangular, $http, $location, $window){
    $scope.user = $stateParams.user;
    console.log($stateParams.user);
    $scope.addFriend() = function(){
        console.log("add friends")
    }
});


})();
