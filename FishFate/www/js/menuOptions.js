/**
 * Created by asakawa on 7/27/16.
 */
var app = angular.module('FishFate');
app.controller('menuOptionsController', function ($scope) {

  var optionOpen = [false, false, false];
  /* menu selection options */
  $scope.selectEightBall = function () { showEightBall(); };
  $scope.selectDiceRoll  = function () { showDiceRoll();  };
  $scope.selectCoinFlip  = function () { showCoinFlip();  };



  /**
   *  JQuery effects
   * */
  function showEightBall() {

    var viewHeight = $('.view').height();
    var eightBallHeight = $('#eightBall').height();
    var menuOptionsHeight = $('#menuOptions').height();



    var bannerHeight = $('#fishBanner').height();


    var dynamicHeight = viewHeight - eightBallHeight - menuOptionsHeight - 78;

    if (dynamicHeight > bannerHeight)
      dynamicHeight = bannerHeight;

    $('#fishBanner').animate({
      height: dynamicHeight
    }, 'fast', function () {
      if (!optionOpen[0]) {
        $('#diceRoll').fadeOut('fast');
        $('#coinFlip').fadeOut('fast', function () {
          $('#eightBall').fadeIn('fast');
          optionOpen[0] = true;
          optionOpen[1] = optionOpen[2] = false;
        });
      }

    });

  }

  function showDiceRoll() {
    $('#fishBanner').animate({
      height: $('.backgroundGif').height()
    }, 'fast', function () {
      if (!optionOpen[1]) {
        $('#eightBall').fadeOut('fast');
        $('#coinFlip').fadeOut('fast', function () {
          $('#diceRoll').fadeIn('fast');
          optionOpen[1] = true;
          optionOpen[0] = optionOpen[2] = false;
        });
      }
    });
  }

  function showCoinFlip() {
    $('#fishBanner').animate({
      height: $('.backgroundGif').height()

    }, 'fast', function () {
      if (!optionOpen[2]) {
        $('#eightBall').fadeOut('fast');
        $('#diceRoll').fadeOut('fast', function () {
          $('#coinFlip').fadeIn('fast');
          optionOpen[2] = true;
          optionOpen[0] = optionOpen[1] = false;
        });
      }
    });
  }

  function hideAllOptions() {

    if (optionOpen[0])
      $('#eightBall').fadeOut('fast');
    if (optionOpen[1])
      $('#diceRoll').fadeOut('fast');
    if (optionOpen[2])
      $('#coinFlip').fadeOut('fast');

    optionOpen[0] = optionOpen[1] = optionOpen[2] = false
  }


});
