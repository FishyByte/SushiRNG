/**
 * Created by asakawa on 7/26/16.
 */
var app = angular.module('FishFate');
app.controller('diceController', function ($scope) {

  /* this array holds jQuery id's */
  var diceArray = [$('#die0'), $('#die1'), $('#die2'), $('#die3'), $('#die4')];

  $scope.diceRoll = {
    numberDice: '5'
  };

  /* coin submit pressed, animate the coins */
  $scope.submitRollDice = function () { rotateDice() };
  /* dynamically display the selected number of coins */
  $scope.displayDice = function () { displayNumberDice(); };

  /**
   * This function is called when use user interacts with the number of dice
   * slider. It's used to display/hide the dice dynamically, which uses
   * jQuery's fadeIn/fadeOut
   * */
  function displayNumberDice() {
    /* switch through the four possible states */
    switch ($scope.diceRoll.numberDice) {
      case '1':
        diceArray[1].fadeOut('fast');
        diceArray[2].fadeOut('fast');
        diceArray[3].fadeOut('fast');
        diceArray[4].fadeOut('fast');
        break;
      case '2':
        diceArray[1].fadeIn('fast');
        diceArray[2].fadeOut('fast');
        diceArray[3].fadeOut('fast');
        diceArray[4].fadeOut('fast');
        break;
      case '3':
        diceArray[1].fadeIn('fast');
        diceArray[2].fadeIn('fast');
        diceArray[3].fadeOut('fast');
        diceArray[4].fadeOut('fast');
        break;
      case '4':
        diceArray[1].fadeIn('fast');
        diceArray[2].fadeIn('fast');
        diceArray[3].fadeIn('fast');
        diceArray[4].fadeOut('fast');
        break;
      case '5':
        diceArray[1].fadeIn('fast');
        diceArray[2].fadeIn('fast');
        diceArray[3].fadeIn('fast');
        diceArray[4].fadeIn('fast');
        break;
      default:
        console.log('error, number of coins out of bounds');
        break;
    }
  }

  /**
   * animate the dice, 'spin' animation and 'toss'
   * animation run in parallel:
   *
   * spin: uses css to rotate the die 360 degrees
   * toss: simulates a dice throw
   * */
  function animateDie(element) {
    element.rotate({
      angle: 0,
      animateTo: 360,
      duration: 1900
    });
    element.animate({
      top: '-200px'
    }, 500, function () {
      element.animate({
        top: 0
      }, 500, function () {
        element.animate({
          top: '-10px'
        }, 150, function () {
          element.animate({
            top: 0
          }, 150)
        })
      })
    })
  }

  function rotateDice() {
    var diceIndex = 0;

    var diceTrigger = setInterval(function () {
      if (diceIndex == diceArray.length)
        clearInterval(diceTrigger);
      if (diceIndex < diceArray.length) {
        animateDie(diceArray[diceIndex]);
        diceIndex++;
      }
    }, 100);
  }


});
