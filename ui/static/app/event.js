(function(){

var app = angular.module('app.event', []);

app.controller('CreateEventController', function($scope, $state, $http, $stateParams){

    $scope.createEvent = function(){
        var name = $scope.new_event.ename;
        var description = $scope.new_event.edescription;

        var start_date = moment($scope.new_event.start_date)
            .add($scope.new_event.start_time);
        var end_date = moment($scope.new_event.end_date)
            .add($scope.new_event.end_time);

        if(start_date.isAfter(end_date)){
          $scope.error = 'Start cannot be after end date';
          return;
        }

        var new_event = {
            name: name,
            start_date: start_date.toISOString(),
            end_date: end_date.toISOString(),
            description: description
        }

        $http.post('/api/event/create/' , new_event ).success(function(data){
            $state.go('root.event', {
                event: data.id
            }, {
                reload: true
            });
        });
    }
});

app.controller('EventController', function($scope, $http, $location, $uibModal, $rootScope, $state){
    var eventID = $location.path().split('/')[2];
    $scope.role = 0;
    $http.get('/api/event/'+eventID).success(function(data){
        data.start_date = data.start_date.replace("Z", " ");
        data.end_date = data.end_date.replace("Z", " ");
        data.start_date = data.start_date.replace("T", " ");
        data.end_date = data.end_date.replace("T", " ");
        $scope.event = data;
    });

    $http.get('/api/event/'+eventID+ '/member/' + $rootScope.user.id).success(function(data){
        $scope.role = data.role;
        if(data.role == null) {
          $scope.role = 0;
        }
        else if(data.role == 2) {
          $scope.roletext = "Going";
        }
        else if(data.role == 3) {
          $scope.roletext = "Maybe";
        }
        else if(data.role == 4) {
          $scope.roletext = "Decline";
        }
    });

    $scope.invite = function(){
        var modal = $uibModal.open({
            templateUrl: 'templates/dialog/invite.html',
            controller: function($scope, $uibModalInstance, $http){
                $http.get('/api/user/friends/invite/').success(function(data){
                    $scope.friends = data;
                    console.log($scope.friends);
                });
                $scope.ok = function(){
                    $uibModalInstance.close($scope.invitee);
                    $http.put('/api/event/'+ eventID +'/member/'+ $scope.invitee.id).success(function(data){
                        console.log('put ' + $scope.invitee.id);
                    });
                };
                $scope.cancel = function(){
                    $uibModalInstance.dismiss();
                };
            }
        });
        modal.result.then(function(data){
        });
    };

    $scope.changeTime = function(){
        var mainScope = $scope;
        var modal = $uibModal.open({
            templateUrl: 'templates/dialog/changetime.html',
            controller: function($scope, $uibModalInstance, $http){
                $scope.event = angular.copy(mainScope.event);
                $scope.event.start_date = moment($scope.event.start_date).toDate();
                $scope.event.end_date = moment($scope.event.end_date).toDate();
                $scope.ok = function(){
                    if(moment($scope.event.start_date).isAfter($scope.event.end_date)){
                      $scope.error = 'Start cannot be after end date';
                      return;
                    }
                    $uibModalInstance.close($scope.event);
                };
                $scope.cancel = function(){
                    $uibModalInstance.dismiss();
                };
            }
        });
        modal.result.then(function(data){
          $scope.event.start_date = data.start_date;
          $scope.event.end_date = data.end_date;
          $http.post('/api/event/'+ $scope.event.id + '/', $scope.event).success(function(){
            $state.reload();
          });
        });
    };

    var updateMember = function () {
      $http.get('/api/event/'+eventID+'/member').success(function(data){

          var decline = data.filter( function(member){return (member.role==4);} );
          $scope.decline_count = decline.length;

          $scope.members = data;
          $scope.member_count = data.length - decline.length;

          var ad = data.filter( function(member){return (member.role==1);} );
          $scope.admin = ad[0];

          var atten = data.filter( function(member){return (member.role==2);} );
          $scope.attendants = atten;
          $scope.attendants_count = atten.length;

          var may = data.filter( function(member){return (member.role==3);} );
          $scope.maybe = may;
          $scope.maybe_count = may.length;
      });
    };
    updateMember();

    $scope.going = function(){
        $http.put('/api/event/'+ eventID +'/member/'+ $rootScope.user.id + '/' + 2).success(function(data){
            $scope.roletext = "Going";
            $scope.role = 2;
            updateMember();
        });
    };

    $scope.decline = function(){
        $http.put('/api/event/'+ eventID +'/member/'+ $rootScope.user.id + '/' + 4).success(function(data){
            $scope.roletext = "Decline";
            $scope.role = 4;
            updateMember();
        });
    };

    $scope.maybef = function(){
        $http.put('/api/event/'+ eventID +'/member/'+ $rootScope.user.id + '/' + 3).success(function(data){
            $scope.roletext = "Maybe";
            $scope.role = 3;
            updateMember();
        });
    };

});

app.controller('EventBrowseController', function($scope, $http){
    var temp;
    var events_without_first = new Array();

    function shuffle(o){
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
        return o;
    }

    $http.get('/api/event/all').success(function(data){
        shuffle(data);

        for (i=0; i<data.length; i++){
          data[i].start_date = data[i].start_date.replace("Z", " ");
          data[i].end_date = data[i].end_date.replace("Z", " ");
          data[i].start_date = data[i].start_date.replace("T", " ");
          data[i].end_date = data[i].end_date.replace("T", " ");
        }

        $scope.all_event = data;
        $scope.first_event = data[0];
        temp = data;

        for (i=0; i<temp.length; i++){
            events_without_first.push(temp[i]);
        }

        events_without_first.shift();
        $scope.events = events_without_first;
    });
});

app.controller('EventFeedController', function($scope, $rootScope, $stateParams, $http, $timeout, $interval){
  $scope.newsfeed = [];
  $scope.nftext = "";
  $scope.user = $rootScope.user;

  postID = $stateParams.postid;
  var eventID = $stateParams.event;
  $scope.eventID = eventID;
  var postLimit = 20;

  if(!postID) {
    $scope.allowPost = true;
    $scope.hasMoreStory = true;
    var newestID = 1;
    $http.get('/api/event/' + eventID + '/post&limit=' + postLimit ).success(function(data){
      $scope.newsfeed = data;
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }

      var updateNewStory = function () {
        if($scope.newsfeed.length > 0) {
          newestID = $scope.newsfeed.map(function(post) {return post.id}).reduce(
            function(thisPost, thatPost) {
              return Math.max(thisPost,thatPost);
            }
          );
        }
        $http.get('/api/event/' + eventID + '/post/new/' + newestID).success(function(data){
          if(data.length > 0 ){
            $scope.newstory = true;
            $timeout(function() { $scope.newstory = false; }, 3000);
            $scope.newsfeed.unshift.apply($scope.newsfeed, data);
          }
        });

        $interval(updateNewStory, 3000);

      }
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
		};

		if (postData.text.length > 0) {
			$http.post('/api/event/' + eventID + '/post', postData).then(function(response){
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
    $http.get('/api/event/' + eventID + '/post/more/' + oldestID +'&limit=' + postLimit).success(function(data){
      if(data.length < postLimit) {
        $scope.hasMoreStory = false;
      }
      $scope.newsfeed.push.apply($scope.newsfeed, data);

    });
  };

});

})();
