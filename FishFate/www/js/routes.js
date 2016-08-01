/**
 * Created by asakawa on 7/26/16.
 */

angular.module('FishFate').config(function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('home', {
      url: '/home',
      templateUrl: 'views/home.html'
    })
    .state('lottery', {
      url: '/lottery',
      templateUrl: 'views/lottery.html'
    })
    .state('random', {
      url: '/random',
      templateUrl: 'views/random.html'
    })
    .state('about', {
      url: '/menu',
      templateUrl: 'views/about.html'
    });
  $urlRouterProvider.otherwise('/home')
});
