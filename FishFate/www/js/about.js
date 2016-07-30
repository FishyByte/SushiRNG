/**
 * Created by asakawa on 7/29/16.
 */
var app = angular.module('FishFate');
app.controller('menuOptionsController', function ($scope) {
  var listItems = [ $('#listItem0'), $('#listItem1'), $('#listItem2'), $('#listItem3'), $('#listItem4'),
  ];
  $scope.clickListItem = function(index){
    hideAllItems();

  }
  function hideAllItems (callback, index) {
    for (var i = 0; i < listItems.length; i++){
      listItems[i].fadeOut('fast');
      callback(index);
    }
  }
  function showOneItem(index){
    listItems[index].fadeIn('fast');
  }
});
