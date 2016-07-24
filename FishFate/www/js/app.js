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

app.config(function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('home', {
      url: '/home',
      templateUrl: 'views/home.html'
    })
    .state('about', {
      url: '/menu',
      templateUrl: 'views/about.html'
    });
  $urlRouterProvider.otherwise('/home')
});

app.controller('fishController', function ($scope, $ionicHistory) {

  var optionOpen = [false, false, false];
  var answers = [
    'do or do not,<br>there is<br>no try'
  ];


  $scope.images = {
    demo: 'img/fishDemo_2.gif',
    heads: 'img/coinHeads.png',
    tails: 'img/coinTails.png',
  };

  $scope.coinFlip = {
    numberCoins: '4'
  };

  /* dynamically display the selected number of coins */
  $scope.displayCoins = function(){ displayNumberCoins(); };

  /* go back button */
  $scope.goBack = function () { $ionicHistory.goBack(); };

  /* menu selection options */
  $scope.selectEightBall = function () { showEightBall(); };
  $scope.selectDiceRoll  = function () { showDiceRoll();  };
  $scope.selectCoinFlip  = function () { showCoinFlip();  };


  $scope.eightBall = {
    answer: answers[0]
  };

  $scope.submitEightBall = function () {
    animateEightBall();
  };
  $scope.submitCoinFlip = function (){
    console.log("hit coin flip");
    animateCoins(1, 0, 1, 0);
  };

  /* animations */
  function animateEightBall() {
    var triangle = $('#triangle');
    var answer = $('#answer');
    var eightBall = $('#eightBall01');

    triangle.fadeOut('fast');
    answer.fadeOut('fast');

    eightBall.animate({
      right: '160px'
    }, 300, function (){
      eightBall.animate({
        right: '140px'
      }, 300, function(){
        eightBall.animate({
          right: '160px'
        }, 300, function(){
          eightBall.animate({
            right: '150px'
          }, 300 ,function (){
            triangle.fadeIn('slow');
            answer.fadeIn('slow');
          });

        });
      });
    });
  }

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

    /* initial flip becore interval */
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


  /**
   *  JQuery effects
   * */
  function showEightBall() {
    $('#fishBanner').animate({
      height: '50px'
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

