/**
 * Created by asakawa on 7/27/16.
 */
var app = angular.module('FishFate');
app.controller('eightBallController', function ($scope, $http) {

  /* jQuery id's */
  var triangle = $('#triangle');
  var answer = $('#answer');
  var eightBall = $('#eightBall01');

  /* scope variables, holds the eight ball responses */
  $scope.eightBall = {
    /* answers array, these strings are pre-formatted for html */
    answers: [
      'do or do not,<br>there is<br>no try',
      'asdfasdfasdf,<br>asdfasdfsdf'
    ],
    resultIndex: 0
  };

  /**
   * submit eight ball:
   *  1. fade out answer and triangle
   *  2. make http GET request
   *  3. upon completion of successful request, then call animate
   */
  $scope.submitEightBall = function () {
    triangle.fadeOut(50);
    answer.fadeOut(50);

    delete $http.defaults.headers.common['X-Requested-With'];
    $http({
      method: "GET",
      url: 'https://fish-bit-hub.herokuapp.com/getBytes',
      headers: {'number-bytes-requested': 1},
      crossDomain: true
    }).then(function successCallback(response) {
      console.log(parseInt(response.data, 16));
      $scope.eightBall.resultIndex = parseInt(response.data, 16) % 2; // replace with response.data
      animateEightBall();
    }, function errorCallback(response) {
      console.log(response);
    });
  };

  /**
   * animate the eight ball (sequential order):
   *    1. 'shake' 8-ball: right, left, right, origin
   *    2. reveal triangle/answer
   * */
  function animateEightBall() {
    eightBall.animate({
      right: '160px'
    }, 200, function () {
      eightBall.animate({
        right: '140px'
      }, 300, function () {
        eightBall.animate({
          right: '160px'
        }, 200, function () {
          eightBall.animate({
            right: '150px'
          }, 200, function () {
            triangle.fadeIn('slow');
            answer.fadeIn('slow');
          });
        });
      });
    });
  }
});
