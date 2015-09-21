(function(){

var app = angular.module('app.group', []);

app.controller('GroupController', function($scope, $stateParams, Restangular){
	$scope.GroupApi = Restangular.one('group', $stateParams.id);
	$scope.joinStatus = 0;
	$scope.joinGroup = function(){
		$scope.GroupApi.all('member').post().then(function(){
			$scope.joinStatus = 1;
		}, function(xhr){
			alert(xhr.data);
		});
	};
});

app.controller('GroupInfoController', function(){
});

})();