/**
 * Created by asakawa on 7/27/16.
 */
var app = angular.module('FishFate');
app.controller('eightBallController', function ($scope) {

  /* answers array, these strings are pre-formatted for html */
  var answers = [
    'do or do not,<br>there is<br>no try'
  ];

  $scope.eightBall = {answer: answers[0]};
  $scope.submitEightBall = function () {
    animateEightBall();
  };

  /**
   * animate the eight ball (sequential order):
   *    1. hide triangle/answer
   *    2. 'shake' 8-ball
   *    3. reveal triangle/answer
   * */
  function animateEightBall() {

    /* jQuery id's */
    var triangle = $('#triangle');
    var answer = $('#answer');
    var eightBall = $('#eightBall01');

    triangle.fadeOut('fast');
    answer.fadeOut('fast');

    eightBall.animate({
      right: '160px'
    }, 300, function () {
      eightBall.animate({
        right: '140px'
      }, 300, function () {
        eightBall.animate({
          right: '160px'
        }, 300, function () {
          eightBall.animate({
            right: '150px'
          }, 300, function () {
            triangle.fadeIn('slow');
            answer.fadeIn('slow');
          });

        });
      });
    });
  }
});
