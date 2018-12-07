var app=angular.module('myApp',[]);

app.directive('fileModel', ['$parse', function($parse){
	return {
		restrict: 'A',
		link: function(scope, element, attrs){
			var model = $parse(attrs.fileModel);
			var modelSetter = model.assign;

			element.bind('change', function(){
				scope.$apply(function(){
					modelSetter(scope, element[0].files[0]);
				})
			})
		}
	}
}]);

app.service('multipartForm',['$http','$scope',function($http){
	this.post = function(uploadUrl, data){
		var fd = new FormData();
		for(var key in data)
			fd.append(key, data[key]);
		console.log(data+'data');
		$http.post(uploadUrl, fd, {
			transformRequest: angular.indentity,
			headers: { 'Content-Type': undefined }
		}).then(function (response){
		   console.log(response.data.value);
		   if(response.data.value == '1') {
			console.log("okay");

			var shot = document.createElement("img");
			shot.src = response.data.imageName;
			document.getElementById('output').appendChild(shot);

			var anc = document.createElement("a");
			// anc.href = response.data.imageName;
			anc.setAttribute("id","anch")
			anc.setAttribute("href",response.data.imageName)
			anc.setAttribute("download","");
			document.getElementById('output').appendChild(anc);

			var butt = document.createElement("button");
			butt.setAttribute("value","click here to download");
			butt.setAttribute("name","submit");
			document.getElementById('anch').appendChild(butt);
		   } else if(response.data.value == "2") {
			   console.log(response.data.encryptedMessage,"okay2");
			   $scope.result = response.data.encryptedMessage;
		   }	
			// if(response.data.numAffected){
			// console.log("ok");
      //       window.location="/";
      //    }
      //    else if(response.data.error){
      //    	console.log(response.data.error,"jjh");
      //    	document.getElementById("error").innerHTML="Already Registered";
      //    	document.getElementById("error").style="color:red;";
      //    }
	},function (err){console.log("error encrypt")});
	}
}]);

app.controller('myCtrl',['$scope','multipartForm',function ($scope,multipartForm){
$scope.myForm = {};
$scope.myForm.message = "";
$scope.myForm.key = "";
$scope.myForm.image = "";
$scope.dencryptKey = "";
$scope.messageImage = "";
$scope.myForm.submit=function (){
	var uploadUrl = '/encrypt';
	console.log($scope.myForm);
	multipartForm.post(uploadUrl,$scope.myForm);
}
$scope.Dencrypt=function (){
	var uploadUrl = '/dencrypt';
	var data = {
		key : $scope.dencryptKey,
		image : $scope.messageImage
	}
	multipartForm.post(uploadUrl,data);
}
}]);

// var app = angular.module('myApp', []);
// app.controller('myCtrl',['$scope','$http', function($scope,$http) {
//   $scope.submit=function(){
//     $scope.error="";
//   	if($scope.value){	
//     $http.get('/encrypt?num='+$scope.value).then(function(response){
//         // document.getElementById('output').style="display:block;";
//         $scope.details=response.data;
//         console.log($scope.details);  
//       },function(error){
//           console.log("error in http request");
//     });
//    }else{
//    	$scope.error="Please enter the value first";
//    	document.getElementById('output').style="display:none;";
//    }
//   }
// }]);
