/**
 * Created by asakawa on 7/29/16.
 */

var app = angular.module('FishFate');
app.controller('lotteryController', function ($scope, $http, $ionicPopup) {

  /* jQuery objects */
  var lotteryLines = [$('#lotteryLine0'), $('#lotteryLine1'), $('#lotteryLine2'), $('#lotteryLine3'), $('#lotteryLine4')]

  /* boolean used to time out users after making a request */
  var timeLocked = false;

  $scope.lottery = {
    quantity: 5,
    whichLottery: 'Powerball',
    results: []
  };

  /**
   * this function is called upon when the user clicks the
   * request button.
   *    1. first fade out all the lottery lines (if visible already)
   *    2. make the http get request with specified params
   *        a. if successful then display those results
   *        b. otherwise report error message
   */
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
    else{
      timeOutPopUp();
    }
  };

  /**
   * this function is called whenever there is an action
   * on the toggle switch. flip the boolean, and set the
   * 'whichLottery' param.
   */
  $scope.toggleLottery = function(){
    $scope.lottery.isPowerBall = !$scope.lottery.isPowerBall;
    if ($scope.lottery.isPowerBall)
      $scope.lottery.whichLottery = 'MegaMillions';
    else
      $scope.lottery.whichLottery = 'Powerball';
  };

  /**
   * display the results from the GET request, uses
   * jQuery to fade in each element.
   */
  function displayLottery(){
    timeLocked = true;
    /* display all the lottery lines in increasing intervals */
    for (var i = 0; i < $scope.lottery.quantity; i++)
      lotteryLines[i].fadeIn(400 * (i+1));
    /* setTimeout the user from making another request */
    setTimeout(function(){
      timeLocked = false;
    }, 1000 * 60 * 10); // ten minutes
  }

  /**
   *  hide all of the lottery lines
   */
  function hideLottery(){
      for (var i = 4; i >= 0; i--)
        lotteryLines[i].fadeOut(300);
  }

  function timeOutPopUp(){
        /* create a pop-up message to display error text */
    var timeOutPopUp = $ionicPopup.prompt({
      template: '<h4>The fish did all that work for you and you just want to throw it all away?</h4>',
      scope: $scope,
      title: '<h3 style="text-align:center">Poor Fishies...</h3>',
      buttons: [
        {
          text: '<b>NO</b>',
          type: 'button-assertive',
          onTap: function (e) {
            return 'nope';
          }
        },
        {
          text: '<b>YES</b>',
          type: 'button-assertive',
          onTap: function (e) {
            timeLocked = false;
            return $scope.getLottery();
          }
        }
      ]
    });
    timeOutPopUp.then(function (res) {

    });
  }


});
