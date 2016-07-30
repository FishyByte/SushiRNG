/**
 * Created by asakawa on 7/29/16.
 */

var app = angular.module('FishFate');
app.controller('randomController', function ($scope, $http, $ionicPopup) {
  /* used for formatting the pop up responses */
  var titleArray = [
    'The fish retrieved this number for you',
    'The fish retrieved this binary string for you'
  ];



  $scope.randoms = {
    getInt: {
      maxValue: '255',
      response: ''
    },
    getBinary: { quantity: '20' }
  };
  // When button is clicked, the popup will be shown...
  $scope.getInt = function () {

     delete $http.defaults.headers.common['X-Requested-With'];
     $http({
     method: "GET",
     url: 'https://fish-bit-hub.herokuapp.com/get-ints',
     headers: {
     'quantity': '1',
     'max_value': $scope.randoms.getInt.maxValue
     },
     crossDomain: true
     }).then(function successCallback(response) {
        console.log('max:', $scope.randoms.getInt.maxValue, '   returned:', response.data);
        $scope.randoms.getInt.response = response.data;
        popUpResponse(0);

     }, function errorCallback(response) {
     console.log(response);
     });
  };


    $scope.getBinary = function () {

     delete $http.defaults.headers.common['X-Requested-With'];
     $http({
     method: "GET",
     url: 'https://fish-bit-hub.herokuapp.com/get-binary',
     headers: {
     'quantity': $scope.randoms.getBinary.quantity
     },
     crossDomain: true
     }).then(function successCallback(response) {
        console.log('max:', $scope.randoms.getInt.maxValue, '   returned:', response.data);
        $scope.randoms.getInt.response = response.data;
        popUpResponse(1);

     }, function errorCallback(response) {
     console.log(response);
     });
  };




  var popUpResponse = function (index) {

    // Custom popup
    var myPopup = $ionicPopup.prompt({
      template: '<h1 style="text-align: center">{{randoms.getInt.response}}</h1>',
      scope: $scope,
      title: titleArray[index],
      buttons: [
        {
          text: '<b>done</b>',
          type: 'button-assertive',
          onTap: function (e) {
            return 'done';
          }
        }
      ]
    });

    myPopup.then(function (res) {
      $scope.randoms.getInt.response = '';
    });
  }


});