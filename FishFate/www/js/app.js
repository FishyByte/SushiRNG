
var app = angular.module('FishFate', ['ionic']);

/**
 * standard ionic ish
 * */
app.run(function ($ionicPlatform) {
  $ionicPlatform.ready(function () {
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if (window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
});



app.controller('fishController', function ($scope, $ionicHistory) {

  $scope.images = {
    demo:  'img/fishDemo_2.gif',
    heads: 'img/coinHeads.png',
    tails: 'img/coinTails.png',
    die:   'img/fishDie.png',
    about: {
      graph: 'img/graph.png'
    }
  };

  /* go back button */
  $scope.goBack = function () { $ionicHistory.goBack(); };
});

