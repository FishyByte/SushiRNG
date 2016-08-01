
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



app.controller('fishController', function ($scope, $ionicHistory, $ionicPopup) {

  $scope.images = {
    demo:         'img/fishDemo_2.gif',
    heads:        'img/coinHeads.png',
    tails:        'img/coinTails.png',
    die:          'img/fishDie.png',
    fishFateIcon: 'img/iconMed.png',

    about: {
      position:   'img/fishPosition.png',
      graph:      'img/graph.png',
      tankSetup:  'img/tankSetup.png'
    }
  };

  /* go back button */
  $scope.goBack = function () { $ionicHistory.goBack(); };

  /* error message */
  $scope.displayError = function (){
    // Custom popup
    var myPopup = $ionicPopup.prompt({
      template: '<h1 style="text-align:center"></h1>',
      scope: $scope,
      title: titleArray[index],
      buttons: [
        {
          text: '<b>done</b>',
          type: 'button-assertive',
          onTap: function (e) {
            return 'done';
          }
        }
      ]
    });

    myPopup.then(function (res) {
      $scope.randoms.getInt.response = '';
      $scope.randoms.getBinary.response = '';
    });
  }
});

