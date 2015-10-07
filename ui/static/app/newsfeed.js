(function(){

var app = angular.module('app.newsfeed', []);


app.directive('myEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.myEnter);
                });

                event.preventDefault();
            }
        });
    };
});


app.controller('NewsfeedController', function($scope, $http){
	$scope.allowPost = true;
	$scope.newsfeed = null;
	$scope.nftext ="";
	$http.get('/api/newsfeed/post').success(function(data){
		$scope.newsfeed = data;
	})

	$scope.postStatus = function() {
		data = {
			text : $scope.nftext,
			target_type : 4,
			target_id : -1,
		};

		if (data.text.length > 0) {
			$http.post('/api/newsfeed/post/', data).then(function(){
				alert("Post Successful!");
				console.log("Post Successful!");
				location.reload();
			}, function(xhr){
					alert(xhr.data);
					console.log(xhr.data);
			});
		}
	};

});



app.controller('CommentController', function($scope, $http){
	$scope.commentPost = function(post_data) {
		console.log(post_data);
		console.log($scope.comment);
		data = {
			text : $scope.comment,
			post : post_data.id,
		};

		if (data.text.length > 0) {
			$http.post('/api/newsfeed/comment/', data).then(function(){
				alert("Comment Successful!");
				console.log("Comment Successful!");
				location.reload();
			}, function(xhr){
					alert(xhr.data);
					console.log(xhr.data);
			});
		}
	};

});


})();
