(function(){

var app = angular.module('app.main', [
    'ui.router',
    'restangular',
    'ui.bootstrap',
    'app.login',
    'app.newsfeed',
    'app.group',
    'app.userprofile',
    'app.event',
    'app.firstlogin',
	'angularMoment',
]);

app.config(function(RestangularProvider){
    RestangularProvider.setBaseUrl('/api');
});
app.run(function($rootScope){
    $rootScope.app_base = '/';
});

app.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/');
    $stateProvider
        .state('root', {
            templateUrl: 'templates/root.html',
            controller: 'MainController',
            resolve: {
                user: function(Restangular){
                    return Restangular.one('auth/check').get().then(function(user){
                        return user;
                    }, function(error){
                        return null;
                    });
                }
            },
        })
        .state('root.newsfeed', {
            url: '/',
            templateUrl: 'templates/newsfeed.html',
            controller: 'NewsfeedController'
        })
				.state('root.nfpost', {
						url: '/post/{id:int}',
						templateUrl: 'templates/newsfeed.html',
						controller: 'NewsfeedController'
				})
        .state('root.group', {
            url: '/groups/{id:int}',
            templateUrl: 'templates/group.html',
            controller: 'GroupController'
        })
        .state('root.group.info', {
            url: '/info',
            templateUrl: 'templates/groupinfo.html',
            controller: 'GroupInfoController'
        })
        .state('root.group.feed', {
            url: '/feed',
            templateUrl: 'templates/groupfeed.html',
            controller: 'GroupFeedController'
        })
				.state('root.group.post', {
						url: '/post/{postid:int}',
						templateUrl: 'templates/groupfeed.html',
						controller: 'GroupFeedController'
				})
        .state('root.group.manage', {
            url: '/manage',
            templateUrl: 'templates/groupmanage.html',
            controller: 'GroupManageController'
        })
        .state('root.lfg', {
            url: '/groups/browse',
            templateUrl: 'templates/groupbrowser.html',
            controller: 'GroupCategoryController'
        })
        .state('root.lfgcat', {
            url: '/groups/browse/{cat}',
            templateUrl: 'templates/groupbrowser_cat.html',
            controller: 'GroupCategoryController'
        })
        .state('root.creategroup', {
            url: '/groups/create',
            templateUrl: 'templates/groupcreate.html',
            controller: 'CreateGroupController'
        })
        .state('root.event', {
        	url: '/event/{event:int}',
        	templateUrl: 'templates/event.html',
            controller: 'EventController'
        })
        .state('root.eventcreate', {
        	url: '/event/create',
        	templateUrl: 'templates/eventcreate.html',
        	controller: 'CreateEventController'
        })
        .state('root.eventbrowse', {
        	url: '/event/browse',
        	templateUrl: 'templates/eventbrowse.html'
        })
        .state('root.user', {
            url: '/{user:int}',
            abstract: true,
            templateUrl: 'templates/user.html',
            controller: 'AddFriendController'
        })
        .state('root.user.timeline', {
            url: '/',
            templateUrl: 'templates/usertimeline.html',
            controller: 'UserProfileInfoController'
        })
        .state('root.user.friends', {
            url: '/friends',
            templateUrl: 'templates/userfriends.html',
            controller: 'UserFriendController'
        })
        .state('root.user.edit', {
            url: '/edit',
            templateUrl: 'templates/useredit.html'
        })
        .state('login.firstlogin', {
            url: '/firstlogin',
            templateUrl: 'templates/firstlogin.html',
            controller: 'FirstLoginController'
        })
        .state('login', {
            url: '/login',
            templateUrl: 'templates/login.html',
            controller: 'LoginController'
        });
});


app.controller('MainController', function($rootScope, user, $http, $uibModal, $state){
    $rootScope.user = user;
    if(!user){
        $state.go('login');
        return;
    }
    $http.get('/api/user/'+user.id+'/userInfo/').success(function(data) {
       if(!data.created){
        $state.go('login.firstlogin');
       }
       return;
    });
    $http.get('/api/group/').success(function(data){
        $rootScope.group_list = data;
    });

    $rootScope.logout = function(){
        var modal = $uibModal.open({
            templateUrl: 'templates/dialog/confirm.html',
            backdrop: 'static',
            keyboard: false,
            controller: function($scope, $uibModalInstance){
                $scope.message = 'Do you want to logout from current user?';
                $scope.ok = function(){
                    $scope.message = 'Logging out...';
                    $scope.hideButtons = true;
                    $http.post('/api/auth/logout').success(function(){
                        $uibModalInstance.close();
                    }, function(){
                        $scope.message = 'Could not log you out.';
                    });
                };
                $scope.cancel = function(){
                    $uibModalInstance.dismiss();
                };
            }
        });
        modal.result.then(function(){
            window.location.reload();
        });
    };
});

app.controller('NotificationController', function($rootScope, $scope, $http, $timeout){

	var countNotification = function(notificationsData) {
		var count = 0;
		notificationsData.map(function(notiData) {
			count += !notiData.read;
		});
		return count;
	};

	(function tick() {
		$http.get('/api/notification/get/').success(function(data){
			$rootScope.notifications = data;
			data.map(function(noti) {
				noti.link_item = angular.fromJson(noti.link_item);
				noti.reference_detail = angular.fromJson(noti.reference_detail);
			});
			$rootScope.notificationCount = countNotification(data);
			$timeout(tick, 3000);
		});

	})();

	$scope.readNotificationId = function (notificationId){
		$http.get('/api/notification/read/' + notificationId).success(function(data){
			console.log(data);
		}).error(function(err) {
			console.log(err);
		});
	};
});

app.controller('PendingFriendController', function($scope, $rootScope, $http, $interval){
    var updatePendingFriend = function(){
        $http.get('/api/user/friend/pending').success(function(data){
            $rootScope.pendingFriends = data;
        });
    };

    $scope.acceptFriend = function(otherUserId){
      $http.put('/api/user/friend/isFriend/' + otherUserId ).success(function(data){
        updatePendingFriend();
    	});
    };
    $scope.rejectFriend = function(otherUserId){
      $http.delete('/api/user/friend/isFriend/' + otherUserId ).success(function(data){
        updatePendingFriend();
    	});
    };
    updatePendingFriend();
    $interval(updatePendingFriend, 60000);


});

})();
