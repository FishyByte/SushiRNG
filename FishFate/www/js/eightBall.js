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
    /*
     Don't count on it.
     */
    answers: [
      'do or do not,<br>there is<br>no try',
      '&emsp;&nbsp;Signs<br>&emsp;&nbsp;point to<br>&emsp;&nbsp;yes',
      '&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;&nbsp;<br>Yes',
      '&emsp;&nbsp;Reply<br>&emsp;&nbsp;hazy, try<br>&emsp;&nbsp;again',
      '&emsp;&nbsp;Without<br>&emsp;&nbsp;a<br>&emsp;&nbsp;doubt',
      '&emsp;&nbsp;My<br>&emsp;&nbsp;sources<br>&emsp;&nbsp;say<br>&emsp;&nbsp;no<br>',
      '&emsp;&ensp;&nbsp;As I<br>&emsp;&ensp;&nbsp;see it<br>&emsp;&ensp;&nbsp;yes',
      '&emsp;You may<br>&emsp;rely<br>&emsp;on it',
      '&nbsp;Concentrate<br>&nbsp;and ask<br>&nbsp;again',
      '&emsp;&nbsp;Outlook<br>&emsp;&nbsp;not so<br>&emsp;&nbsp;good',
      '&ensp;&nbsp;It is<br>&emsp;decidedly<br>&ensp;&nbsp;so',
      '&ensp;&nbsp;Better not<br>&emsp;tell you<br>&emsp;now',
      '&emsp;Very<br>&emsp;doubtful',
      '&ensp;&nbsp;Yes<br>&emsp;definitely',
      '&emsp;&ensp;It is<br>&emsp;&ensp;certain',
      '&emsp;&ensp;Cannot<br>&emsp;&ensp;predict<br>&emsp;&ensp;now',
      '&emsp;&ensp;&nbsp;Most<br>&emsp;&ensp;&nbsp;likely',
      '&emsp;&ensp;&nbsp;Ask<br>&emsp;&ensp;&nbsp;again<br>&emsp;&emsp;later',
      '&emsp;&nbsp;My reply<br>&emsp;is<br>&emsp;no',
      '&emsp;&nbsp;Outlook<br>&emsp;&nbsp;good',
      '&emsp;&ensp;&nbsp;Don&#39;t<br>&emsp;&ensp;&nbsp;count<br>&emsp;&ensp;&nbsp;on it'
    ],
    resultIndex: 20
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
      $scope.eightBall.resultIndex = parseInt(response.data, 16) % 21; // replace with response.data
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
