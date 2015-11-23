(function(){

var app = angular.module('app.profile', []);

app.controller('FriendsController', function($scope, $stateParams, Restangular, $http, $location, $window){
    $scope.user = $stateParams.user;
});


})();
