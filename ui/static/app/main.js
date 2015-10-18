(function(){

var app = angular.module('app.main', [
	'ui.router',
	'restangular',
	'ui.bootstrap',
	'app.login',
	'app.newsfeed',
	'app.group'
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
			controller: 'MainAuthController'
		})
		.state('root.newsfeed', {
			url: '/',
			templateUrl: 'templates/newsfeed.html',
			controller: 'NewsfeedController'
		})
		.state('root.group', {
			url: '/groups/{id:int}',
			abstract: true,
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
		})
		.state('root.lfg', {
			url: '/groups/browse',
			templateUrl: 'templates/groupbrowser.html',
		})
		.state('root.lfgcat', {
			url: '/groups/browse/{cat}',
			templateUrl: 'templates/groupbrowser_cat.html',
		})
		.state('login', {
			url: '/login',
			templateUrl: 'templates/login.html',
			controller: 'LoginController'
		});
});

app.controller('MainAuthController', function($rootScope, Restangular, $state){
	$rootScope.user = null;
	Restangular.one('auth/check').get().then(function(user){
		$rootScope.user = user;
	}, function(){
		$state.go('login');
	});
});

})();
