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


app.controller('NewsfeedController', function($scope, $stateParams, $http){
  $scope.newsfeed = [];
  $scope.nftext = "";
  postID = $stateParams.id;

  if(!postID) {
    $scope.allowPost = true;
    $http.get('/api/newsfeed/post/').success(function(data){
      $scope.newsfeed = data;
    });
  }
  else {
    $scope.allowPost = false;
  	$http.get('/api/newsfeed/post/' + postID).success(function(data){
  		$scope.newsfeed.push(data);
  	});
  }

	$scope.postStatus = function() {
		postData = {
			text : $scope.nftext,
			target_type : 4,
      target_id : null,
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



app.controller('CommentController', function($rootScope, $scope, $http, $timeout){

  var loadCommentsByPostId = function(postID) {
    $http.get('/api/newsfeed/post/'+postID+'/comment/').success(function(commentsData){
      $scope.comments = commentsData;
    });
  };

  loadCommentsByPostId($scope.data.id);
  // (function tick() {
  //   $http.get('/api/newsfeed/post/'+$scope.data.id+'/comment/').success(function(commentsData){
  //     console.log("BRUHX");
  //     $scope.comments = commentsData;
  //     $timeout(tick, 1000);
  //   });
  // })();


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
