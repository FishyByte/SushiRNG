/**
 * Created by asakawa on 7/26/16.
 */
var app = angular.module('FishFate');
app.controller('coinController', function ($scope, $http) {

  /* boolean used to stop rapid button presses */
  var isActivated = false;

  /* array for coin id's */
  var coinIDs = ['#coin0', '#coin1', '#coin2', '#coin3'];

  $scope.coinFlip = {
    numberCoins: '4',
    coinValues: [0, 0, 0, 0]
  };

  /* dynamically display the selected number of coins */
  $scope.displayCoins = function () {
    displayNumberCoins();
  };
  /* coin submit pressed, animate the coins */
  $scope.submitCoinFlip = function () {
    delete $http.defaults.headers.common['X-Requested-With'];
    $http({
      method: "GET",
      url: 'https://fish-bit-hub.herokuapp.com/get-ints',
      headers: {
          'quantity': '4',
          'max_value': '1'
        },
      crossDomain: true
    }).then(function successCallback(response) {
      $scope.coinFlip.coinValues = response.data.split(' ');

      if (!isActivated)
        animateCoins();

    }, function errorCallback(response) {
      console.log(response);
    });
  };

  /**
   * This function is called when use user interacts with the number of coins
   * slider. It's used to display/hide the coins dynamically, which uses
   * jQuery's fadeIn/fadeOut
   * */
  function displayNumberCoins() {
    /* array for jQuery elements*/
    var coinArray = [$('#coin0'), $('#coin1'), $('#coin2'), $('#coin3')];

    /* switch through the four possible states */
    switch ($scope.coinFlip.numberCoins) {
      case '1':
        coinArray[1].fadeOut('fast');
        coinArray[2].fadeOut('fast');
        coinArray[3].fadeOut('fast');
        break;
      case '2':
        coinArray[1].fadeIn('fast');
        coinArray[2].fadeOut('fast');
        coinArray[3].fadeOut('fast');
        break;
      case '3':
        coinArray[1].fadeIn('fast');
        coinArray[2].fadeIn('fast');
        coinArray[3].fadeOut('fast');
        break;
      case '4':
        coinArray[1].fadeIn('fast');
        coinArray[2].fadeIn('fast');
        coinArray[3].fadeIn('fast');
        break;
      default:
        console.log('error, number of coins out of bounds');
        break;
    }
  }

  /**
   * loop through each of the coins and call spinCoin()
   * */
  function animateCoins() {
    isActivated = true;
    for (var coinIndex = 0; coinIndex < coinIDs.length; coinIndex++)
      spinCoin(coinIndex);
  }

  /**
   * this function uses css to spin an individual coin, the
   * only required param is for an index value to represent
   * each of the coins.
   *
   * @param elementIndex (integer)
   */
  function spinCoin(elementIndex) {
    /* init flip counts */
    var flipCounts = [0, 0, 0, 0];
    /* flips the coin on an interval */
    var trigger = setInterval(function () {
      if (flipCounts[elementIndex] == 1 + $scope.coinFlip.coinValues[elementIndex])
        clearInterval(trigger);
        document.querySelector(coinIDs[elementIndex]).classList.toggle("flip");
      flipCounts[elementIndex]++;
    }, 150);
    isActivated = false;
  }
});
