/**
 * Created by asakawa on 7/29/16.
 */

var app = angular.module('FishFate');
app.controller('lotteryController', function ($scope, $http, $ionicPopup) {

  /* jQuery objects */
  var lotteryLines = [$('#lotteryLine0'), $('#lotteryLine1'), $('#lotteryLine2'), $('#lotteryLine3'), $('#lotteryLine4')]
  var timeLocked = false;

  $scope.lottery = {
    quantity: 5,
    whichLottery: 'Powerball',
    results: []
  };
  // When button is clicked, the popup will be shown...
  $scope.getLottery = function () {
    if(!timeLocked){
      hideLottery();
      delete $http.defaults.headers.common['X-Requested-With'];
      $http({
        method: "GET",
        url: 'https://fish-bit-hub.herokuapp.com/get-lottery',
        headers: {
          'quantity': $scope.lottery.quantity,
          'which-lottery': $scope.lottery.whichLottery
        },
        crossDomain: true
      }).then(function successCallback(response) {
        $scope.lottery.results = response.data.split(' ');
        displayLottery();
      }, function errorCallback(response) {
        $scope.displayError(response.status);
      });
    }
  };

  $scope.toggleLottery = function(){
    $scope.lottery.isPowerBall = !$scope.lottery.isPowerBall;
    if ($scope.lottery.isPowerBall)
      $scope.lottery.whichLottery = 'MegaMillions';
    else
      $scope.lottery.whichLottery = 'Powerball';
  };

  function displayLottery(){
    timeLocked = true;
    for (var i = 0; i < $scope.lottery.quantity; i++){
      lotteryLines[i].fadeIn(400 * (i+1));
    }
    setTimeout(function(){
      timeLocked = false;
    }, 1000 * 3);


  }
  function hideLottery(){
      for (var i = 4; i >= 0; i--) {
        lotteryLines[i].fadeOut(300);
      }
  }

});
