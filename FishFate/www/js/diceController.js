/**
 * Created by asakawa on 7/26/16.
 */
var app = angular.module('FishFate');
app.controller('diceController', function ($scope) {
$scope.diceRoll = {
    numberDice: '5'
  };

   $scope.submitRollDice = function (){
    rotateDice()
  };
  /* dynamically display the selected number of coins */
  $scope.displayDice = function(){ displayNumberDice(); };

    function displayNumberDice(){
    var dieArray = [
      $('#die0'),
      $('#die1'),
      $('#die2'),
      $('#die3'),
      $('#die4')
    ];
    switch ($scope.diceRoll.numberDice){
      case '1':
        dieArray[1].fadeOut('fast');
        dieArray[2].fadeOut('fast');
        dieArray[3].fadeOut('fast');
        dieArray[4].fadeOut('fast');
        break;
      case '2':
        dieArray[1].fadeIn('fast');
        dieArray[2].fadeOut('fast');
        dieArray[3].fadeOut('fast');
        dieArray[4].fadeOut('fast');
        break;
      case '3':
        dieArray[1].fadeIn('fast');
        dieArray[2].fadeIn('fast');
        dieArray[3].fadeOut('fast');
        dieArray[4].fadeOut('fast');
        break;
      case '4':
        dieArray[1].fadeIn('fast');
        dieArray[2].fadeIn('fast');
        dieArray[3].fadeIn('fast');
        dieArray[4].fadeOut('fast');
        break;
      case '5':
        dieArray[1].fadeIn('fast');
        dieArray[2].fadeIn('fast');
        dieArray[3].fadeIn('fast');
        dieArray[4].fadeIn('fast');
        break;
      default:
        console.log('error, number of coins out of bounds');
        break;
    }
  }

  function rotateDice(){
    var diceArray = [$('#die0'), $('#die1'), $('#die2'), $('#die3'), $('#die4')];
    var diceIndex = 0;

    var diceTrigger = setInterval(function (){
      if (diceIndex == 5)
        clearInterval(diceTrigger);
        if (diceIndex < diceArray.length){
          animateDie(diceArray[diceIndex]);
          diceIndex++;
        }


    }, 100);
  }



  function animateDie(element){
    element.rotate({
      angle: 0,
      animateTo: 360,
      duration: 1900
    });
    element.animate({
      top: '-200px'
    }, 500, function(){
      element.animate({
        top: 0
      }, 500, function(){
        element.animate({
          top: '-10px'
        }, 150, function(){
          element.animate({
            top: 0
          }, 150)
        })
      })
    })
  }

});
