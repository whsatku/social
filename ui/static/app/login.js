(function(){

var app = angular.module("app.login", []);

app.controller("LoginController", function($scope, $rootScope, Restangular, $state){
	var endpoint = Restangular.all("auth/login");

	$scope.auth = {
		"username": "",
		"password": ""
	};

	$scope.login = function(){
		$scope.error = null;
		$scope.loggingIn = true;
		endpoint.post($scope.auth).then(function(data){
			$rootScope.user = data;
			$state.go('root.newsfeed');
		}, function(request){
			if ( request.data["detail"] ) {
				$scope.error = request.data.detail;
			}else{
				$scope.error = request.statusText;
			}
			$scope.loggingIn = false;
		});
	}
});

})();