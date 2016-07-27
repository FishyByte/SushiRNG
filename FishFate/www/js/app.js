// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
var app = angular.module('FishFate', ['ionic']);


app.run(function ($ionicPlatform) {
  $ionicPlatform.ready(function () {
    if (window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if (window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
});



app.controller('fishController', function ($scope, $ionicHistory) {
  var optionOpen = [false, false, false];



  $scope.images = {
    demo:  'img/fishDemo_2.gif',
    heads: 'img/coinHeads.png',
    tails: 'img/coinTails.png',
    die:   'img/fishDie.png',
    about: {
      graph: 'img/graph.png'
    }
  };

  $scope.coinFlip = {
    numberCoins: '4'
  };







  /* go back button */
  $scope.goBack = function () { $ionicHistory.goBack(); };

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

    console.log('view', viewHeight);
    console.log('8ball', eightBallHeight);
    console.log('menuOptions', menuOptionsHeight);

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

