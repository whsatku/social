(function(){

var app = angular.module('app.group', []);

app.controller('GroupController', function($scope, $stateParams, Restangular, $http, $location, $window, $state, $rootScope){
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
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
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

app.controller('GroupFeedController', function($scope, $stateParams, $http, $location, $timeout){
  $scope.newsfeed = [];
  $scope.nftext = "";
  postID = $stateParams.postid;
  var postLimit = 20;
  var groupID;
  if($stateParams.sub) {
    var groupID = $stateParams.sub;
  }
  else {
    groupID = $location.path().split('/')[2];
  }


  if(!postID) {
    $scope.allowPost = true;
    $scope.hasMoreStory = true;
    $http.get('/api/group/'+groupID+'/post&limit=' + postLimit ).success(function(data){
      $scope.newsfeed = data;
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }
      // POLLING
      (function tick() {
        $http.get('/api/group/' + groupID +'/post/new/' + $scope.newsfeed[0].id).success(function(data){
          if(data.length > 0 ){
            $scope.newstory = true;
            $timeout(function() { $scope.newstory = false; }, 3000);
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

  $http.get('/api/group/'+ $stateParams.id + '/subgroup').success(function(data){
    $scope.subgroups = data;
  });

  $scope.postStatus = function() {
    postData = {
      text : $scope.nftext,
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


app.controller('GroupInfoController', function($scope, $http, $location){
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });

    $http.get('/api/group/'+groupID+'/member/accepted').then(function(data){
        $scope.memberList = data.data;
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


    $http.get('/api/group/'+groupID).then(function(data){
        $scope.group = data.data;
    });

    $scope.editInfo = function(){
        $http.put('/api/group/'+groupID+'/edit/',$scope.group).success(function(data){
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
    $scope.gtype = 0;

    $scope.createGroup = function(){

        $scope.newgroup = {
            name: $scope.gname,
            description: $scope.gdescription,
            short_description: 'default',
            activities: 'default',
            type: $scope.gtype,


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
