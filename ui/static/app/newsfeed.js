(function(){

var app = angular.module('app.newsfeed', []);

app.controller('NewsfeedController', function($scope, $http){
	$scope.allowPost = true;
	$scope.newsfeed = null;
	$http.get('/api/newsfeed/post').success(function(data){
		$scope.newsfeed = data;
		console.log(data);
	})
});

})();