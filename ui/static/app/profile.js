(function(){

var app = angular.module('app.profile', []);

app.controller('FriendsController', function($scope, $stateParams, Restangular, $http, $location, $window){
    $scope.addFriend() = function(){
        console.log("add friends")
    }
});


})();

