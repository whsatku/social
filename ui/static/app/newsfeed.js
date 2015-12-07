(function(){

var app = angular.module('app.newsfeed', ['ngAnimate']);


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


app.controller('NewsfeedController', function($scope, $stateParams, $http, $timeout){
  $scope.newsfeed = [];
  $scope.nftext = "";
  postID = $stateParams.id;
  var postLimit = 20;

  if(!postID) {
    $scope.allowPost = true;
    $scope.hasMoreStory = true;
    var newestID = 1;
    $http.get('/api/newsfeed/post&limit=' + postLimit ).success(function(data){
      $scope.newsfeed = data;
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }
      // POLLING
      (function tick() {
        if($scope.newsfeed.length > 0) {
          newestID = $scope.newsfeed[0].id;
        }
        $http.get('/api/newsfeed/new/' + newestID).success(function(data){
          if(data.length > 0 ){
            $scope.newstory = true;
            $timeout(function() { $scope.newstory = false; }, 3000);
            //$('.newstory').stop().fadeIn(400).delay(3000).fadeOut(400); //fade
            $scope.newsfeed.unshift.apply($scope.newsfeed, data);
          }
          $timeout(tick, 3000);
        });

      })();
      // END OF POLLING
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

  $scope.loadMoreStory = function() {
    var oldestID = $scope.newsfeed.slice(-1)[0].id;
    $http.get('/api/newsfeed/more/' + oldestID +'&limit=' + postLimit).success(function(data){
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }
      $scope.newsfeed.push.apply($scope.newsfeed, data);

    });
  };

});



app.controller('CommentController', function($rootScope, $scope, $http, $timeout){

  var loadCommentsByPostId = function(postID) {
    $http.get('/api/newsfeed/post/'+postID+'/comment/').success(function(commentsData){
      $scope.comments = commentsData;
    });
  };

  loadCommentsByPostId($scope.data.id);
	$scope.commentPost = function(postData) {
		var commentData = {
			text : $scope.comment,
			post : postData.id,
      user : {
        username : $rootScope.user.username,
      },
		};

		if (commentData.text.length > 0) {
      $scope.comment = "";
			$http.post('/api/newsfeed/comment/', commentData).then(function(response){
        console.log(response);
        // POLLING
        (function tick() {
          loadCommentsByPostId($scope.data.id);
          $timeout(tick, 3000);
        })();
        // END OF POLLING

			}, function(xhr){
					alert(xhr.data);
					console.log(xhr.data);
			});
		}
	};

});


})();
