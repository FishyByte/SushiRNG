/**
 * Created by asakawa on 7/27/16.
 */
var app = angular.module('FishFate');
app.controller('menuOptionsController', function ($scope) {

  /* array to keep track of which option is currently selected */
  var optionOpen = [false, false, false];

  /* variable to make height of element static */
  var COIN_HEIGHT = 0

  /* menu selection options */
  $scope.selectEightBall = function () {
    showEightBall();
  };
  $scope.selectDiceRoll = function () {
    showDiceRoll();
  };
  $scope.selectCoinFlip = function () {
    showCoinFlip();
  };

  /**
   *  the following three functions are used to display
   *  the three menu options. These are animated
   *  using jQuery.
   *
   *  This is the following algorithm that each
   *  menu option follows:
   *
   *    1. animate the banner to shrink so that all the
   *       option block fits on the display
   *    2. if any other option is open then fade it out
   *    3. fade in the selected option
   * */
  function showEightBall() {
    $('#fishBanner').animate({
      height: getHeight($('#eightBall').height())
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
      height: getHeight($('#diceRoll').height())
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
    // coin flip div changes height, this corrects that
    if (COIN_HEIGHT === 0)
      COIN_HEIGHT = $('.backgroundGif').height();

    $('#fishBanner').animate({
      height: COIN_HEIGHT
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

  /**
   * This function is used to calculate the height of all the 8-ball
   * elements. if the calculated height is greater than the banner
   * height then return the caluclated height, otherwise return the
   * banner height.
   * */
  function getHeight(elementHeight, offset) {
    var viewHeights = [
      $('.backgroundGif').height(), // demo banner
      $('.view').height(),          // height of entire view
      $('#menuOptions').height(),   // height of menu options
      elementHeight + 78,
      // height of option element + offset
    ];
    /* loop through elements subtracting from the view height */
    for (var i = 2; i < viewHeights.length; i++) {

      viewHeights[1] -= viewHeights[i];
    }

    /* return whichever is bigger */
    if (viewHeights[1] > viewHeights[0])
      return viewHeights[0]; // banner height
    else
      return viewHeights[1]; // calculated height
  }

  /**
   * hides all the options (initial start state)
   * */
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
