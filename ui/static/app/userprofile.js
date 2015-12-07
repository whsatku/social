(function(){

var app = angular.module('app.userprofile', []);

app.controller('UserProfileInfoController', function($scope, $http, $location, $stateParams, $rootScope){
    var userID = $stateParams.user;
    $scope.allowEdit = false;
    $scope.allowPost = true;
    $scope.nftext = "";
    if(userID == $rootScope.user.id) {
      $scope.allowEdit = true;
    }

    $http.get('/api/user/'+userID+'/userInfo').success(function(data){
      $scope.userprofile = data;
    });


    postID = $stateParams.postid;

    if(!postID) {
      $http.get('/api/newsfeed/wall/' + userID).success(function (data) {
        $scope.userfeed = data;
      });
    }
    else {
      $http.get('/api/newsfeed/post/' + postID).success(function(data){
        $scope.userfeed = [];
        $scope.userfeed.push(data);
      });
    }

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
