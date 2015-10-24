angular.module('starter.controllers', ['ionic'])

.controller('DashCtrl', function($scope) {})

.controller('ChatsCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  };
})

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope, $http, $interval, $ionicLoading, $ionicPopup) {
  $scope.changeColor = function(red, green, blue) {
    $http.get('http://pepitoviajero.herokuapp.com/setcolor',
      {
        params:{
          'red': red,
          'green': green,
          'blue': blue
        }
      })
      .then(function(response) {
        $ionicLoading.show({
          template: '<div class="spinner">  <div class="dot1"></div>  <div class="dot2"></div></div><br>Cargando emoción...'
        });
        var stop = $interval(function() {
          $http.get('http://pepitoviajero.herokuapp.com/all')
            .then(function(response) {
              if (response.data.color == red + ',' + green + ',' + blue){
                $ionicLoading.hide();
                $interval.cancel(stop);
              };
            }, function(error) {
              $ionicLoading.hide();
              $interval.cancel(stop);
            });
        }, 2000);
        console.log('funciona!');
      }, function(error) {
        var alertPopup = $ionicPopup.alert({
          title: 'Vaya...',
          template: 'Nuestros monos no han podido cambiar la emoción de Pepito.'
        });
        alertPopup.then(function(res) {});
        console.log('no funciona: ', error);
      });
  };
  $scope.settings = {
    enableFriends: true
  };
});
