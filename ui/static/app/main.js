(function(){

var app = angular.module('app.main', [
	'ui.router',
	'restangular',
	'ui.bootstrap',
	'app.login'
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
			url: '/',
			templateUrl: 'templates/root.html',
			controller: 'MainAuthController'
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