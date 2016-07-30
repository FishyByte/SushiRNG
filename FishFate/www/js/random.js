/**
 * Created by asakawa on 7/29/16.
 */

var app = angular.module('FishFate');
app.controller('randomController', function ($scope, $http, $ionicPopup) {

  $scope.randoms = {
    getInt: {
      maxValue: '255',
      response: ''
    }
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
        popUpResponse();

     }, function errorCallback(response) {
     console.log(response);
     });




  };


  var popUpResponse = function () {
    // Custom popup
    var myPopup = $ionicPopup.prompt({
      template: '<h1 style="text-align: center">{{randoms.getInt.response}}</h1>',
      scope: $scope,
      title: 'The fish retrieved this number for you',
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
