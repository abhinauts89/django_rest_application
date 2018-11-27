var app = angular.module('myApp', []);
app.controller('formCtrl',['$scope','$http', function($scope,$http) {

  $scope.environments=[
    {
        'url':'https://qc1.nbicagents.com',
        'env':'QC1'
    },
    {
        'url':'https://dc.nbicagents.com',
        'env':'DC'
    },
    {
        'url':'https://qa.nbicagents.com',
        'env':'QA'
    }];

  $scope.programCodes =[
   {
     'id': '1',
      'programCodeKey': "DF",
      'programCodeValue': "DF",

      'formCodes': [{
         'id': '11',
         'formCodeKey': "DP-3",
         'formCodeVal': "DP-3"
     }]
   },
   {
     'id': '2',
      'programCodeKey': "HO",
      'programCodeValue': "HO",
      'formCodes':  [{
         'id': '21',
         'formCodeKey': "HO-3",
         'formCodeVal': "HO-3"
     }, {
         'id': '22',
         'formCodeKey': "HO-4",
         'formCodeVal': "HO-4"
     }]
   }];


    $scope.states=[
    {'key':'NJ','value':'NJ'},
    {'key':'NY','value':'NY'},
    {'key':'CT','value':'CT'},
    {'key':'MA','value':'MA'},
    {'key':'RI','value':'RI'},
    ];

	$scope.getRequest=function(){
     $http({
             url : " http://127.0.0.1:8000/automatedSanity/",
			 method: "POST",
			 data : $scope.data,
             dataType: "json",
           })
           .then(function (response){
            console.log(response);
           },function (error){
            alert("Error while receiving response!!");
           });
      };


}]);