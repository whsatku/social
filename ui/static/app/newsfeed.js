(function(){

var app = angular.module('app.newsfeed', []);

app.controller('NewsfeedController', function($scope, $http){
	$scope.allowPost = true;
	$scope.newsfeed = null;
	$http.get('/api/newsfeed/post').success(function(data){
		$scope.newsfeed = data;
	})

	$scope.postStatus = function() {
		console.log("sss");
		data = {
			text : $scope.nftext,
		};

		$http.post('/api/newsfeed/post/', data).then(function(){
			console.log("Post Successful!");
		}, function(xhr){
				alert(xhr.data);
				console.log(xhr.data);
		});
	};

});

})();
