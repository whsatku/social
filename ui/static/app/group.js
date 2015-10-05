(function(){

var app = angular.module('app.group', []);

app.controller('GroupController', function($scope, $stateParams, Restangular, $http, $location){
	$scope.GroupApi = Restangular.one('group', $stateParams.id);
	$scope.joinStatus = 0;
	$scope.joinGroup = function(){
		$scope.GroupApi.all('member').post().then(function(){
			$scope.joinStatus = 1;
		}, function(xhr){
			alert(xhr.data);
			console.log(xhr.data);
		});
	};
    var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });
});

app.controller('GroupInfoController', function($scope, $http, $location){
	var groupID = $location.path().split('/')[2];
    $http.get('/api/group/'+groupID).success(function(data){
        $scope.group = data;
    });
});

})();