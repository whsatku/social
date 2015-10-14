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
	});

	$scope.postStatus = function() {
		postData = {
			text : $scope.nftext,
			target_type : 4,
			target_id : -1,
		};

		if (postData.text.length > 0) {
			$http.post('/api/newsfeed/post/', postData).then(function(response){
				console.log(response);
        $scope.nftext="";
				$scope.newsfeed.unshift(response.data);
			}, function(xhr){
					alert(xhr.data);
					console.log(xhr.data);
			});
		}
	};

});



app.controller('CommentController', function($rootScope, $scope, $http){

  var loadCommentsByPostId = function(postID) {
    $http.get('/api/newsfeed/post/'+postID+'/comment/').success(function(commentsData){
      $scope.comments = commentsData;
    });
  };

  loadCommentsByPostId($scope.data.id);
  $scope.comments = null;

	$scope.commentPost = function(postData) {
		commentData = {
			text : $scope.comment,
			post : postData.id,
      datetime : 'Just now',
      user : {
        username : $rootScope.user,
      },
		};

		if (commentData.text.length > 0) {
      $scope.comments.push(commentData);
      $scope.comment = "";
			$http.post('/api/newsfeed/comment/', commentData).then(function(response){
        console.log(response);
        loadCommentsByPostId($scope.data.id);
			}, function(xhr){
					alert(xhr.data);
					console.log(xhr.data);
			});
		}
	};

});


})();
