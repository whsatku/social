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
			console.log(xhr.data);
		});
	};
});

app.controller('GroupInfoController', function($scope, $stateParams, Restangular){
	var json = {
    "modules":
        [
                {
                	"imgUrl":"https://scontent-sin1-1.xx.fbcdn.net/hphotos-xaf1/v/t1.0-9/11159484_984861828200184_7594807741003164501_n.jpg?oh=cc1e01fd7bce04f27d70e4d5a618a203&oe=569AAA5D",
                    "userUrl":"https://www.facebook.com/Gin.Jeang"
                },

                {
                    "imgUrl":"https://fbcdn-sphotos-d-a.akamaihd.net/hphotos-ak-ash2/v/t1.0-9/270102_4939471837053_1765517720_n.jpg?oh=a6a3689c2ae9d4e37278a1cd45c79760&oe=569E378C&__gda__=1452319794_a11e19ad48a6388569863f4a75381c7d",
                    "userUrl":"https://www.facebook.com/supason.kotanut"
                },

                {
                	"imgUrl":"https://scontent.fbkk5-1.fna.fbcdn.net/hprofile-xtp1/v/t1.0-1/p160x160/12049578_10156592796035355_6325222840261409497_n.jpg?oh=3a8f491ad2beef7ec2f05ae98147173d&oe=568B59E3",
                    "userUrl":"https://www.facebook.com/smartz.tfc"
                },

                {
                	"imgUrl":"https://scontent.fbkk5-1.fna.fbcdn.net/hprofile-xaf1/v/t1.0-1/p160x160/10377003_10203709002237301_3336838098850946932_n.jpg?oh=274aa6f0f4b3cdd346665929411d3c9e&oe=56D230B2",
                    "userUrl":"https://www.facebook.com/Wuttipong.Khemphetjetsada"
                },

                {
                	"imgUrl":"https://scontent.fbkk5-1.fna.fbcdn.net/hprofile-xfp1/v/t1.0-1/c0.0.160.160/p160x160/10462570_782223021829390_4874625363248483923_n.jpg?oh=4e8f4c90f67d1abcf2f44aff2d202566&oe=5687B103",
                    "userUrl":"https://www.facebook.com/sorrawit.chan"
                },
        ]
  };
  
  $scope.memberlist = json;
});

})();