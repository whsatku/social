(function(){

var app = angular.module('app.userprofile', ['ngFileUpload']);

app.controller('UserProfileInfoController', function($scope, $http, $location, $stateParams, $rootScope, $timeout, $interval){
    $scope.user = $rootScope.user;
    var userID = $stateParams.user;
    $scope.allowEdit = false;
    $scope.nftext = "";
    if(userID == $rootScope.user.id) {
      $scope.allowEdit = true;
    }

    $http.get('/api/user/'+userID+'/userInfo').success(function(data){
      $scope.userprofile = data;
    });

    $http.get('/api/user/friends/' + userID).success(function (data) {
      $scope.members = [];
      for(i=0 ; i<14 ; i++) {
        var randomIndex = Math.floor(Math.random()*data.length);
        $scope.members.push(data.splice(randomIndex, 1)[0]);
        if(data.length <= 0) {
          break;
        }
      }
      $scope.moreFriendsCount = data.length;
    });

    // USERFEED
    postID = $stateParams.postid;
    var postLimit = 20;

    if(!postID) {
      $scope.allowPost = true;
      $scope.hasMoreStory = true;
      var newestID = 1;
      $http.get('/api/newsfeed/wall/' + userID + '&limit=' + postLimit ).success(function (data) {
        $scope.userfeed = data;
        if(data.length < postLimit) {
          $scope.hasMoreStory = false;
        }

        var updateNewStory = function() {
          if($scope.userfeed.length > 0) {
            newestID = $scope.userfeed[0].id;
          }
          $http.get('/api/newsfeed/wall/' + userID + '/new/' + newestID).success(function(data){
            if(data.length > 0 ){
              $scope.newstory = true;
              $timeout(function() { $scope.newstory = false; }, 3000);
              $scope.userfeed.unshift.apply($scope.userfeed, data);
            }
          });
        }
        $interval(updateNewStory, 3000);

      });
    }
    else {
      $scope.allowPost = false;
      $http.get('/api/newsfeed/post/' + postID).success(function(data){
        $scope.userfeed = [];
        $scope.userfeed.push(data);
      });
    }

    $scope.loadMoreStory = function() {
      var oldestID = $scope.userfeed.slice(-1)[0].id;
      $http.get('/api/newsfeed/wall/' + userID + '/more/' + oldestID +'&limit=' + postLimit).success(function(data){
        if(data.length < postLimit) {
          $scope.hasMoreStory = false;
        }
        $scope.userfeed.push.apply($scope.userfeed, data);

      });
    };

    $scope.postStatus = function() {
      postData = {
        text : $scope.nftext,
        target_type : 4,
        target_id : userID,
      };

      if (postData.text.length > 0) {
        $http.post('/api/newsfeed/post/', postData).then(function(response){
          console.log(response);
          $scope.nftext="";
          $scope.userfeed.unshift(response.data);
        }, function(xhr){
            alert(xhr.data);
            console.log(xhr.data);
        });
      }
    };


});

  app.controller('EditUserController', function($scope, $http, $state, $window, Upload){


    var userId;

    $http.get('/api/auth/check').success(function(data){
      userId = data.id
    });

    $scope.saveInfo = function(){

      Upload.upload({
        url: '/api/user/'+userId+'/userInfo/',
        method: 'PUT',
        data: {
        firstname: $scope.userprofile.firstname,
        lastname: $scope.userprofile.lastname,
        birthday: moment($scope.userprofile.birthday).format('YYYY-MM-DD'),
        gender: $scope.userprofile.gender,
        faculty: $scope.userprofile.faculty,
        major: $scope.userprofile.major,
        country: $scope.userprofile.country,
        city: $scope.userprofile.city,
        created: true
        }
      }).success(function(data){
            $state.reload();
      });
    };

    $scope.uploadPicture = function(files) {
      $scope.file = null
      // var picture = new FormData();
      // //Take the first selected file
      // picture.append("picture", files[0]);
      $scope.file = files[0]
      Upload.upload({
          url: '/api/user/'+userId+'/userPicture/',
          method: 'PUT',
          data: {
          picture: $scope.file,
          }
        }).success(function(data){
          $state.reload();
          });
    };

  });

app.controller('UserFriendController', function($scope, $http, $location, $stateParams){
    var userID = $stateParams.user;
    $http.get('/api/user/friends/' + userID).success(function(data){
      $scope.friends = data;
      $scope.friendsCount = data.length;
    });
    $scope.unFriend = function(otherUserId){
    	$http.delete('/api/user/friend/' + otherUserId ).success(function(data){
    	});
    };
});

app.controller('AddFriendController', function($scope, $http, $location, $stateParams, $rootScope){
    $scope.userId = $rootScope.user.id;
    $scope.otherUserId = $stateParams.user;
    $scope.isFriend = false;

    $http.get('/api/user/friends/' + $scope.otherUserId).success(function(data){
      $scope.friendsCount = data.length;
    });

    $http.get('/api/user/'+$scope.otherUserId+'/userInfo').success(function(data){
        $scope.userprofile = data;
    });
    $scope.isFriendAPI = function(){
      $http.get('/api/user/friend/isFriend/' + $scope.otherUserId ).success(function(data){
        $scope.isFriend = data;
    	});
    };
    $scope.unFriend = function(){
    	$http.delete('/api/user/friend/' + $scope.otherUserId ).success(function(data){
        $scope.isFriendAPI();
    	});
    };
    $scope.addFriend = function(){
    	$http.post('/api/user/friend/' + $scope.otherUserId ).success(function(data){
        $scope.isFriendAPI();
    	});
    };


    $scope.isFriendAPI();

});

})();
