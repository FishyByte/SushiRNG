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

app.config(function($stateProvider, $urlRouterProvider){
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

app.controller('fishController', function($scope, $ionicHistory){

  var eightBallRevealed = true;
  var optionOpen = [false, false, false];
  var answers = [
    'do or do not,<br>there is<br>no try'
  ];

  /* go back button */
  $scope.goBack = function(){
    $ionicHistory.goBack();
  };


  /* menu selection options */
  $scope.selectEightBall = function(){
    showEightBall();
  };
  $scope.selectDiceRoll = function(){
    showDiceRoll();
  };
  $scope.selectCoinFlip = function(){
    showCoinFlip();
  };


  $scope.eightBall = {
    answer: answers[0]
  };

  $scope.submitEightBall = function(){
    animateEightBall();
  };

  /* animations */
  function animateEightBall(){
    var triangle = $('#triangle');
    var answer = $('#answer');

    if (eightBallRevealed == false){
      triangle.fadeIn('slow');
      answer.fadeIn('slow');
      eightBallRevealed = true;
    }
    else{
      triangle.fadeOut('slow');
      answer.fadeOut('slow');
      eightBallRevealed = false;
    }
  }
  //



  /**
   *  JQuery effects
   * */
  function showEightBall (){
    $('#fishBanner').animate({
      height: '50px'
    }, 'slow', function(){

      if (!optionOpen[0]) {
        $('#diceRoll').fadeOut('slow');
        $('#coinFlip').fadeOut('slow', function(){
          $('#eightBall').fadeIn('slow');
          optionOpen[0] = true;
          optionOpen[1] = optionOpen[2] = false;
        });
      }

    });

  }
  function showDiceRoll (){
    if (!optionOpen[1]) {
      $('#eightBall').fadeOut('slow');
      $('#coinFlip').fadeOut('slow', function(){
        $('#diceRoll').fadeIn('slow');
        optionOpen[1] = true;
        optionOpen[0] = optionOpen[2] = false;
      });
    }
  }
  function showCoinFlip () {
    if (!optionOpen[2]) {
      $('#eightBall').fadeOut('slow');
      $('#diceRoll').fadeOut('slow', function(){
        $('#coinFlip').fadeIn('slow');
        optionOpen[2] = true;
        optionOpen[0] = optionOpen[1] = false;
      });
    }
  }

  function hideAllOptions (){
    if (optionOpen[0])
      $('#eightBall').fadeOut('slow');
    if (optionOpen[1])
      $('#diceRoll').fadeOut('slow');
    if (optionOpen[2])
      $('#coinFlip').fadeOut('slow');

    optionOpen[0] = optionOpen[1] = optionOpen[2] = false
  }

});

