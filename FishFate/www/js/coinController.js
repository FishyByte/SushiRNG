/**
 * Created by asakawa on 7/26/16.
 */
var app = angular.module('FishFate');
app.controller('coinController', function ($scope) {

  var coinIDs    = ['#coin0', '#coin1' ,'#coin2' , '#coin3'];
  var coinArray  = [ $('#coin0'), $('#coin1'), $('#coin2'), $('#coin3') ];

  /* dynamically display the selected number of coins */
  $scope.displayCoins = function(){ displayNumberCoins(); };

  $scope.submitCoinFlip = function (){
    animateCoins();
  };
  $scope.coinFlip = {
    numberCoins: '4',
    coinValues: [1, 0, 1, 0]
  };

  function displayNumberCoins(){
    switch ($scope.coinFlip.numberCoins){
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
  function animateCoins () {
    for (var i = 0; i < coinIDs.length; i++){
      if (i < coinIDs.length)
        spinCoin(i);
    }

  }
  function spinCoin(elementIndex) {

    /* init flip counts */
    var flipCounts = [0, 0, 0, 0];

      var trigger = setInterval(function () {
        if (flipCounts[elementIndex] == 10 + $scope.coinFlip.coinValues[elementIndex])
          clearInterval(trigger);
        document.querySelector(coinIDs[elementIndex]).classList.toggle("flip");
        flipCounts[elementIndex]++;
      }, 150);
  }


});
