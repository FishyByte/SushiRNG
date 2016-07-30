/**
 * Created by asakawa on 7/29/16.
 */
var app = angular.module('FishFate');
app.controller('aboutViewController', function ($scope) {
  /* array to hold all the jQuery elements */
  var listItems = [ $('#listItem0'), $('#listItem1'), $('#listItem2'), $('#listItem3'), $('#listItem4') ];

  /* this click function is called from the about view */
  $scope.clickListItem = function(index){

    listItems[index].fadeIn('fast');
      for (var i = 0; i < listItems.length; i++){
        if (i != index)
          listItems[i].fadeOut('fast');
    }
  };

});
