(function(){

var app = angular.module('app.group', ['ngFileUpload']);

app.controller('GroupController', function($scope, $stateParams, Restangular, $http, $location, $window, $state, $rootScope){
    $scope.group = {
      isAuthorized : false,
      isPostable : false,
      isInfoVisible : false,
    };
    var redirectSubpage = function(id){
        id = id || $stateParams.id;
        var isMember = ($rootScope.group_list || []).filter(function(item){
            return item.id == id;
        });
        $state.go(isMember ? 'root.group.feed' : 'root.group.info', {
            id: id
        }, {inherit: false});
    };
    if($state.is('root.group')){
        redirectSubpage();
    }
    $scope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams){
        if(toState.name == 'root.group'){
            event.preventDefault();
            redirectSubpage(toParams.id);
        }
    });

    $scope.GroupApi = Restangular.one('group', $stateParams.id);
    $scope.joinGroup = function(){
        $scope.GroupApi.all('member/').post().then(function(){
            $state.reload();
        }, function(xhr){
            console.error(xhr.data);
        });
    };
    $scope.LeaveGroup = function(){
      $http.delete('/api/group/'+groupID+'/member/'+$rootScope.user.id).success(function(data){
          $state.reload();
      });
    };
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
        if(data.type == 0) {
          $scope.group.isAuthorized = true;
          console.log($scope.group.isAuthorized);
        }
        else if(data.type == 2) {
          $scope.group.isInfoVisible = false;
        }
        if( data.member_status == 1 || data.member_status == 2) {
          $scope.group.isPostable = true;
          $scope.group.isAuthorized = true;
          $scope.group.isInfoVisible = true;
        }

    });
});

app.controller('CreateSubGroupController', function($scope, $http, $location, $stateParams, $state){
  $scope.name = "";
  $scope.createSubGroup = function() {
    var name={
      name: $scope.name
    };
    $http.post('/api/group/'+ $stateParams.id + '/subgroup',name).success(function(data){
      $state.go('root.group.feed', {
          id: $stateParams.id
      }, {
          reload: true
      });
    });
  };
});

app.controller('GroupFeedController', function($scope, $rootScope, $stateParams, $http, $location, $state, $timeout, $interval){
  $scope.newsfeed = [];
  $scope.nftext = "";
  $scope.allowSubmission = false;
  $scope.pin = false;
  $scope.user = $rootScope.user;
  postID = $stateParams.postid;
  var postLimit = 20;
  var groupID;
  if($stateParams.sub) {
    groupID = $stateParams.sub;
  }
  else {
    groupID = $location.path().split('/')[2];
  }

  if(!postID) {
    $scope.hasMoreStory = true;
    var newestID = 0;
    $http.get('/api/group/'+groupID+'/post&limit=' + postLimit ).success(function(data){
      $scope.newsfeed = data;
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }
      // POLLING
      var updateNewStory = function () {
        if($scope.newsfeed.length > 0) {
          newestID = $scope.newsfeed.map(function(post) {return post.id;}).reduce(
            function(thisPost, thatPost) {
              return Math.max(thisPost,thatPost);
            }
          );
        }
        $http.get('/api/group/' + groupID +'/post/new/' + newestID).success(function(data){
          if(data.length > 0 ){
            $scope.newstory = true;
            $timeout(function() { $scope.newstory = false; }, 3000);
            $scope.newsfeed.unshift.apply($scope.newsfeed, data);
          }
        });
      };
      $interval(updateNewStory, 10000);
    });
  }
  else {
    $scope.allowPost = false;
    $http.get('/api/newsfeed/post/' + postID).success(function(data){
      $scope.newsfeed.push(data);
    });
  }

  $http.get('/api/group/'+ $stateParams.id + '/subgroup').success(function(data){
    $scope.subgroups = data;
  });

  $scope.postStatus = function() {
    var postData = {
      text : $scope.nftext,
      allow_submission: $scope.allowSubmission,
      pinned: $scope.pin
    };

    if (postData.text.length > 0) {
      $http.post('/api/group/'+groupID+'/post', postData).then(function(response){
        $scope.nftext="";
        $scope.newsfeed.unshift(response.data);
      }, function(xhr){
          alert(xhr.data);
          console.log(xhr.data);
      });
    }
  };

  $scope.unpin = function(post){
    $http.post('/api/group/' + groupID + '/post/' + post.id + '/unpin').then(function(response){
      Object.assign(post, response.data);
    });
  };

  $scope.loadMoreStory = function() {
    var oldestID = $scope.newsfeed.slice(-1)[0].id;
    $http.get('/api/group/' + groupID +'/post/more/' + oldestID +'&limit=' + postLimit).success(function(data){
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }
      $scope.newsfeed.push.apply($scope.newsfeed, data);

    });
  };

});



app.controller('GroupCommentController', function($rootScope, $scope, $http, $interval, Upload){

  $scope.comment = '';
  $scope.file = null;

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
    if($scope.file){
      if(commentData.text.length === 0){
        commentData.text = '_magic_fileupload';
      }
      $scope.comments.push(commentData);
      $scope.comment = "";

      commentData.file = $scope.file;
      $scope.file = null;

      Upload.upload({
        url: '/api/newsfeed/comment/',
        data: commentData
      }).then(function(response){
        console.log(response);
        loadCommentsByPostId($scope.data.id);
        $interval(function() {loadCommentsByPostId($scope.data.id);}, 15000);
      }, function(xhr){
          alert(xhr.data);
          console.log(xhr.data);
      });
    }else if (commentData.text.length > 0) {
      //$scope.comments.push(commentData);
      $scope.comment = "";
      $http.post('/api/newsfeed/comment/', commentData).then(function(response){
        console.log(response);
        $interval(function() {loadCommentsByPostId($scope.data.id);}, 15000);
      }, function(xhr){
          alert(xhr.data);
          console.log(xhr.data);
      });
    }
  };

});


app.controller('GroupInfoController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];

    $http.get('/api/group/'+groupID+'/member/accepted').then(function(data){
        $scope.memberList = data.data;
    });

});

app.controller('GroupManageController', function($scope, $state, $http, $location, $stateParams, Upload){

    var groupID = $location.path().split('/')[2];
    function fetchMember(){
        $http.get('/api/group/'+groupID+'/member/accepted').then(function(data){
            $scope.groupMember = data.data;
        });
        $http.get('/api/group/'+groupID+'/member/pending').then(function(data){
            $scope.groupMember_pending = data.data;
        });
    }
    function fetchSubgroup(){
      $http.get('/api/group/'+ $stateParams.id + '/subgroup').success(function(data){
        $scope.subgroups = data;
      });
    }

    fetchMember();
    fetchSubgroup();

    function acceptMember(pk){
        $http.put('/api/group/'+groupID+'/member/'+ pk).then(function(data){
            fetchMember();
        });
    }
    function denyMember(pk){
        $http.delete('/api/group/'+groupID+'/member/'+ pk).then(function(data){
            fetchMember();
        });
    }
    $scope.acceptMember = acceptMember;
    $scope.denyMember = denyMember;

    $scope.deleteSubgroup = function (id){
      data = {
        group_id : id
      };
      $http.put('/api/group/'+ $stateParams.id + '/subgroup',data).success(function(data){
        fetchSubgroup();
      });

    };

    $http.get('/api/group/'+groupID).then(function(data){
        $scope.group = data.data;
    });

    $scope.editInfo = function(){
        $http.put('/api/group/'+groupID+'/edit/',$scope.group).success(function(data){
        });
    };

    $scope.uploadCover = function(files) {
      $scope.file = null;
      $scope.file = files[0];
      Upload.upload({
          url: '/api/group/'+groupID+'/editCover/',
          method: 'PUT',
          data: {
          cover: $scope.file,
          }
        }).success(function(data, status, headers, config){
          $scope.messagec = [];
          $scope.messagec.push("Upload Successful!");
          $state.reload();
        }).error(function(data, status, headers, config) {
          $scope.messagec = [];
          $scope.messagec.push("Invalid File Type");
        });
    };

    $scope.updateMember = function(pk, this_role){
      $http.post('/api/group/'+groupID+'/member/'+ pk + "/", {"role": this_role}).success(function(data){
          $state.reload();
      });
    };

});


app.controller('GroupCategoryController', function($scope, $http, $stateParams){
    var category = $stateParams.cat;
    var temp;
    var groups_without_first = new Array();
    $scope.category = category;

    function shuffle(o){
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
        return o;
    }

    $http.get('/api/group/category/get/'+ category ).success(function(data){
        shuffle(data);
        $scope.g = data[0];
        temp = data;
        for (i=0; i<temp.length; i++){
            groups_without_first.push(temp[i]);
        }
        groups_without_first.shift();
        $scope.groups = groups_without_first;
    });

    $http.get('/api/group/category/all').success(function(data){
        $scope.allCategory = data;
    });

    $http.get('/api/group/all').success(function(data){
        shuffle(data);
        $scope.allGroups = data;
    });
});


app.controller('CreateGroupController', function($scope, $state, $http, $stateParams){

    $scope.gname = "";
    $scope.gdescription = "";
    $scope.privacy = 0;
    $scope.gtype = 0;

    $scope.createGroup = function(){

        $scope.newgroup = {
            name: $scope.gname,
            description: $scope.gdescription,
            short_description: 'default',
            activities: 'default',
            type: $scope.privacy,
            gtype: $scope.gtype,


        };


        $http.post('/api/group/create/' , $scope.newgroup ).success(function(data){
            $state.go('root.group.info', {
                id: data.id
            }, {
                reload: true
            });
        });

    };

});

})();
