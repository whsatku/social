(function(){

var app = angular.module('app.main', [
    'ui.router',
    'restangular',
    'ui.bootstrap',
    'app.login',
    'app.newsfeed',
    'app.group',
    'app.userprofile',
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
        .state('root.group.manage', {
            url: '/manage',
            templateUrl: 'templates/groupmanage.html',
            controller: 'GroupManageController'
        })
        .state('root.lfg', {
            url: '/groups/browse',
            templateUrl: 'templates/groupbrowser.html',
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
        .state('root.user', {
            url: '/{user:int}',
            abstract: true,
            templateUrl: 'templates/user.html'
        })
        .state('root.user.timeline', {
            url: '/',
            templateUrl: 'templates/usertimeline.html',
            controller: 'UserProfileInfoController'
        })
        .state('login', {
            url: '/login',
            templateUrl: 'templates/login.html',
            controller: 'LoginController'
        });
});

app.controller('MainController', function($rootScope, user, $http){
    $rootScope.user = user;
    $http.get('/api/group/').success(function(data){
        $rootScope.group_list = data;
    });
});
app.controller('NotificationController', function($rootScope){
    $rootScope.notificationCount = Math.floor(Math.random() * 20);
});

})();
