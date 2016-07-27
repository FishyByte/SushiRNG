/**
 * Created by asakawa on 7/26/16.
 */
var app = angular.module('FishFate');
app.controller('coinController', function ($scope) {

  /* dynamically display the selected number of coins */
  $scope.displayCoins = function(){ displayNumberCoins(); };

  $scope.submitCoinFlip = function (){
    animateCoins(1, 0, 1, 0);
  };

  function displayNumberCoins(){
    var coinArray = [
      $('#coin0'),
      $('#coin1'),
      $('#coin2'),
      $('#coin3')
    ];
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


  function animateCoins (zero, one, two, three) {
    var flipCounts = [0, 0, 0, 0];
    var coins = ['#coin0', '#coin1' ,'#coin2' , '#coin3'];

    /* initial flip before interval */
    flipOnce(coins[0]);
    flipOnce(coins[1]);
    flipOnce(coins[2]);
    flipOnce(coins[3]);

    /* coin 0 */
    var trigger0 = setInterval(function(){
      if (flipCounts[0] == 10 + zero)
        clearInterval(trigger0);
      flipOnce(coins[0]);
      flipCounts[0]++;
    }, 150);

    /* coin 1 */
    var trigger1 = setInterval(function(){
      if (flipCounts[1] == 10 + one)
        clearInterval(trigger1);
      flipOnce(coins[1]);
      flipCounts[1]++;
    }, 150);

    /* coin 2 */
    var trigger2 = setInterval(function(){
      if (flipCounts[2] == 10 + two)
        clearInterval(trigger2);
      flipOnce(coins[2]);
      flipCounts[2]++;
    }, 150);

    /* coin 3 */
    var trigger3 = setInterval(function(){
      if (flipCounts[3] == 10 + three)
        clearInterval(trigger3);
      flipOnce(coins[3]);
      flipCounts[3]++;
    }, 150);
  }
  function flipOnce(element){ document.querySelector(element).classList.toggle("flip"); }



});
