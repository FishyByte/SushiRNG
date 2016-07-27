/**
 * Created by asakawa on 7/27/16.
 */
var app = angular.module('FishFate');
app.controller('eightBallController', function ($scope) {


  var answers = [
    'do or do not,<br>there is<br>no try'
  ];


  $scope.eightBall = {
    answer: answers[0]
  };

  $scope.submitEightBall = function () {
    animateEightBall();
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
});
