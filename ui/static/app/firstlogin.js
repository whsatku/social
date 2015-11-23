(function(){

var app = angular.module("app.firstlogin", []);

	
	app.controller("FirstLoginController", function($scope, $http, $state){
		$scope.userprofile = {
		user: "",
		faculty: "",
		country: "",
		};


		var userId;
		$http.get('/api/auth/check').success(function(data){
			userId = data.id
			$http.get('/api/user/'+userId+'/userInfo/').success(function(data){
				if(data.created){
					$state.go('root.newsfeed');
				}
			});
		});

		$scope.saveInfo = function(){
			$scope.userprofile.created = true;
			$http.put('/api/user/'+userId+'/userInfo/',$scope.userprofile).success(function(data){
	        	$state.go('root.newsfeed');
	        });
		}
	});
})();