/**
 * Created by asakawa on 7/27/16.
 */
var app = angular.module('FishFate');
app.controller('eightBallController', function ($scope, $http) {

  /* boolean used to stop rapid button presses */
  var isActivated = false;

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
      '&emsp;&nbsp;Fins<br>&emsp;&nbsp;point to<br>&emsp;&nbsp;yes',//0
      '&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<br>Aye!',//1
      '&nbsp;Trouble<br>&ensp;Herring you<br>&nbsp;try again',//2
      '&emsp;Without<br>&emsp;&nbsp;a Trout&#39;s<br>&emsp;doubt',//3
      '&ensp;&nbsp;My<br>&emsp;fishes say<br>&ensp;&nbsp;no<br>',//4
      '&emsp;&ensp;&nbsp;As I<br>&emsp;&ensp;&nbsp;sea it<br>&emsp;&ensp;&nbsp;yes',//5
      '&emsp;You may<br>&emsp;Ray-ly<br>&emsp;on it',//6
      '&emsp;Gather<br>&emsp;your fish<br>&emsp;&nbsp;and ask<br>&emsp;&nbsp;again',//7
      '&emsp;Outhook<br>&emsp;not so<br>&emsp;good',//8
      '&emsp;It is Dace<br>&emsp;-cidedly<br>&ensp;&nbsp;so',//9
      '&emsp;&emsp;Dear<br>&emsp;&emsp;Cod<br>&emsp;&emsp;no',//10
      /*'&emsp;Very<br>&emsp;Flounder<br>&emsp;-ing',//11*/
      '&nbsp;Yes<br>&nbsp;Dolphinitely',//12
      '&ensp;&nbsp;It is certain<br>as a<br>&ensp;Sturgeon',//13
      '&emsp;Fish can&#39;t<br>&emsp;forecast<br>&emsp;now',//14
      '&nbsp;Most<br>&nbsp;bay-lievable',//15
      '&emsp;&ensp;&nbsp;Nope<br>&emsp;&ensp;&nbsp;Go<br>&emsp;&ensp;&nbsp;Fish',//16
      '&ensp;&nbsp;No oppor-<br>&ensp;&nbsp;Tuna-ty',//17
      '&ensp;&nbsp;The<br>&ensp;&nbsp;tides look<br>&emsp;good',//18
      '&emsp;&ensp;&nbsp;Don&#39;t<br>&emsp;&ensp;&nbsp;reel<br>&emsp;&ensp;&nbsp;on it'//19
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
      url: 'https://fish-bit-hub.herokuapp.com/get-ints',
      headers: {
          'quantity': '1',
          'max_value': (($scope.eightBall.answers.length) - 1)
        },      crossDomain: true
    }).then(function successCallback(response) {
      $scope.eightBall.resultIndex = parseInt(response.data);
      if (!isActivated){
        animateEightBall();
      }
    }, function errorCallback(response) {
      $scope.displayError(response.status);
    });
  };

  /**
   * animate the eight ball (sequential order):
   *    1. 'shake' 8-ball: right, left, right, origin
   *    2. reveal triangle/answer
   * */
  function animateEightBall() {
    isActivated = true;
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
            isActivated = false;
          });
        });
      });
    });
  }
});
