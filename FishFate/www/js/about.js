/**
 * Created by asakawa on 7/29/16.
 */
var app = angular.module('FishFate');
app.controller('aboutViewController', function ($scope) {

  var LIST_HEIGHT = $('#aboutBlock').height();
  var VIEW_HEIGHT = $('#aboutView').height();
  var PADDING = 10;
  var height = VIEW_HEIGHT - LIST_HEIGHT - PADDING;

  /* array to hold all the jQuery elements */
  var listItems = [$('#listItem0'), $('#listItem1'), $('#listItem2'), $('#listItem3'), $('#listItem4')];
  var listElements = [$('#listElement0'), $('#listElement1'), $('#listElement2'), $('#listElement3'), $('#listElement4')];
  /* an array to keep track of which elements in the list are displayed */
  var isDisplayed = [false, false, false, false, false];

  /* this click function is called from the about view */
  $scope.clickListItem = function (index) {
    closeAll(index);
    openOne(index);
  };

  function openOne(index) {
    if (!isDisplayed[index]) {
      listElements[index].animate({
        height: height
      }, 'fast', function () {
        listItems[index].fadeIn('fast', function () {
          isDisplayed[index] = true;
        });
      });
    }

  }

  function closeOne(index) {
    listItems[index].fadeOut('fast', function (i) {
      listElements[index].animate({
        height: '30px'
      }, 'fast', function () {
        isDisplayed[index] = false;
      })
    });
  }

  function closeAll(index) {
    for (var i = 0; i < listItems.length; i++) {
      if (isDisplayed[i] && i != index)
        closeOne(i);
    }
  }


});
