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
			url: '/groups/{id}',
			abstract: true,
			templateUrl: 'templates/group.html',
			controller: 'GroupController'
		})
		.state('root.group.info', {
			url: '/info',
			templateUrl: 'templates/groupinfo.html',
			controller: 'GroupInfoController'
		})
		.state('login', {
			url: '/login',
			templateUrl: 'templates/login.html'
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