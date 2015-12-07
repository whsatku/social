(function(){

var app = angular.module('app.userprofile', []);

app.controller('UserProfileInfoController', function($scope, $http, $location, $stateParams, $rootScope, $timeout){
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
      $http.get('/api/newsfeed/wall/' + userID + '&limit=' + postLimit ).success(function (data) {
        $scope.userfeed = data;
        if(data.length < postLimit) {
          $scope.hasMoreStory = false;
        }
        // POLLING
        (function tick() {
          $http.get('/api/newsfeed/wall/' + userID + '/new/' + $scope.userfeed[0].id).success(function(data){
            if(data.length > 0 ){
              $scope.newstory = true;
              $timeout(function() { $scope.newstory = false; }, 3000);
              $scope.userfeed.unshift.apply($scope.userfeed, data);
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

  app.controller('EditUserController', function($scope, $http, $window){


    var userId;
    $http.get('/api/auth/check').success(function(data){
      userId = data.id
    });

    $scope.saveInfo = function(){
      var firstname = $scope.userprofile.firstname;
      var lastname = $scope.userprofile.lastname;
      var birthday = moment($scope.userprofile.birthday);
      var gender = $scope.userprofile.gender;
      var faculty = $scope.userprofile.faculty;
      var major = $scope.userprofile.major;
      var country = $scope.userprofile.country;
      var city = $scope.userprofile.city;

      var edit_profile = {
        firstname: firstname,
        lastname: lastname,
        birthday: birthday.format('YYYY-MM-DD'),
        gender: gender,
        faculty: faculty,
        major: major,
        country: country,
        city: city
      }

      $http.put('/api/user/'+userId+'/userInfo/',edit_profile).success(function(data){
            $window.location.reload();
            console.log(data.birthday);
          });
    }
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
