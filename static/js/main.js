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

app.service('multipartForm',['$http',function($http){
	this.post = function(uploadUrl, data){
		var fd = new FormData();
		for(var key in data)
			fd.append(key, data[key]);
		$http.post(uploadUrl, fd, {
			transformRequest: angular.indentity,
			headers: { 'Content-Type': undefined }
		}).then(function (response){
		   if(response.data.value == '1') {
			document.getElementById("outputEncrypt").style.display="block";
			var shot = document.getElementById("imgEncrypt");
			shot.setAttribute("src",response.data.imageName);

			var anc = document.getElementById("anchEncrypt");
			anc.setAttribute("href",response.data.imageName)

		   } else if(response.data.value == "2") {
			   document.getElementById("outputDencrypt").style.display="block";
			   document.getElementById("dencryptMessage").innerHTML=response.data.encryptedMessage;
		   }	
		},function (err){console.log("error")});
	}
}]);

app.controller('myCtrl',['$scope','multipartForm',function ($scope,multipartForm){
$scope.myForm = {};
$scope.myForm.message = "";
$scope.myForm.key = "";
$scope.myForm.image = "";
$scope.dencryptKey = "";
$scope.messageImage = "";
$scope.dencryptMessage = "";
$scope.myForm.submit=function (){
	var uploadUrl = '/encrypt';
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

$scope.Download = function () {
	var input = document.getElementById("dencryptMessage").value;
	document.getElementById("anchDownload").setAttribute('href', 'data:text/plain;charset=utf-8,' + 
  	encodeURIComponent(input));
  }
}]);
