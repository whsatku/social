(function(){

var app = angular.module('app.group', []);

app.controller('GroupController', function($scope, $stateParams, Restangular, $http, $location, $window){
    $scope.GroupApi = Restangular.one('group', $stateParams.id);
    $scope.joinStatus = 0;
    $scope.joinGroup = function(){
        $scope.GroupApi.all('member/').post().then(function(){
            $scope.joinStatus = 1;
            $window.location.reload();
        }, function(xhr){
                console.log(xhr.data);
        });
    };
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });
});


app.controller('GroupFeedController', function($scope, $http, $location){
	$scope.allowPost = true;
	$scope.newsfeed = null;
	$scope.nftext ="";
  var groupID = $location.path().split('/')[2];
	$http.get('/api/group/'+groupID+'/post').success(function(data){
		$scope.newsfeed = data;
	});

	$scope.postStatus = function() {
		postData = {
			text : $scope.nftext,
		};

		if (postData.text.length > 0) {
			$http.post('/api/group/'+groupID+'/post/', postData).then(function(response){
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



app.controller('GroupCommentController', function($rootScope, $scope, $http){

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


app.controller('GroupInfoController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });
});

app.controller('GroupManageController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    function fetchMember(){
        $http.get('/api/group/'+groupID+'/member/accepted').then(function(data){
            $scope.groupMember = data.data;
        });
        $http.get('/api/group/'+groupID+'/member/pending').then(function(data){
            $scope.groupMember_pending = data.data;
        });
    }

    fetchMember();

    function acceptMember(pk){
        console.log("acceptMember : " + pk);
        $http.put('/api/group/'+groupID+'/member/'+ pk).then(function(data){
            fetchMember();
        });
    }
    function denyMember(pk){
        console.log("delete : " + pk);
        $http.delete('/api/group/'+groupID+'/member/'+ pk).then(function(data){
            fetchMember();
        });
    }
    $scope.acceptMember = acceptMember;
    $scope.denyMember = denyMember;


    $http.get('/api/group/'+groupID).then(function(data){
        $scope.group = data.data;
    });

    $scope.editInfo = function(){
        $http.put('/api/group/'+groupID+'/edit/',$scope.group).success(function(data){
        });
    }
})



app.controller('GroupCategoryController', function($scope, $http, $stateParams){
    category = $stateParams.cat;
    $http.get('/api/group/category/'+ category ).success(function(data){
        $scope.groups = data;
    });

});

})();

