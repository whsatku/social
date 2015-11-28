(function(){

var app = angular.module('app.search', []);

app.factory('search', function($http){
	return function(query){
		return $http.get('/api/search/?q=' + encodeURIComponent(query))
			.then(function(resp){
				return resp.data;
			});
	};
});

app.controller('SearchController', function($scope, search, $state){
    $scope.search = function(query){
    	return search(query);
    };
    $scope.goto = function($item, $model, $label){
    	if($item.type == 'user'){
    		$state.go('root.user.timeline', {
    			user: $item.id
    		});
    	}else if($item.type == 'group'){
    		$state.go('root.group', {
    			id: $item.id
    		});
    	}else{
    		console.error($item.type + ' unrecognized type');
    	}
    	$scope.searchQuery = '';
    }
});


})();
