angular.module('starter.controllers', ['ionic'])

.controller('MapCtrl', function($scope, $ionicLoading) {
  $scope.mapCreated = function(map) {
    $scope.map = map;
    $scope.icon = 'http://pepitoviajero.herokuapp.com/img/pepito-small.png';
    $scope.marker = new google.maps.Marker({
      position: new google.maps.LatLng(43.07493, -89.381388),
      map: $scope.map,
      icon: $scope.icon
    });
    $scope.circle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: $scope.map,
        center: new google.maps.LatLng(43.07493, -89.381388),
        radius: 600
    });
  };

  $scope.centerOnMe = function () {
    console.log("Centering");
    if (!$scope.map) {
      return;
    };

    $ionicLoading.show({
      content: 'Getting current location...',
      showBackdrop: false
    });

    navigator.geolocation.getCurrentPosition(function (pos) {
      console.log('Got pos', pos);
      $scope.map.setCenter(new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude));
      $ionicLoading.hide();
    }, function (error) {
      alert('Unable to get location: ' + error.message);
    });
  };
})

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

.controller('EmotionCtrl', function($scope, $http, $interval, $ionicLoading, $ionicPopup) {
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
          template: '<div class="spinner"><div class="dot1"></div><div class="dot2"></div></div><br>Cargando emoción...'
        });
        var stop = $interval(function() {
          $http.get('http://pepitoviajero.herokuapp.com/all')
            .then(function(response) {
              if (response.data.color == red + ',' + green + ',' + blue){
                $ionicLoading.hide();
                $ionicPopup.alert({
                  title: '¡Hecho!',
                  template: 'En breve <b>Pepito</b> mostrará tu emoción seleccionada.',
                  buttons: [
                    {
                      text: '<span class="ion-social-twitter"></span> ¡Tuitéalo!',
                      type: 'button-calm',
                    }
                  ]
                });
                $interval.cancel(stop);
              };
            }, function(error) {
              $ionicLoading.hide();
              $ionicPopup.alert({
                title: 'Vaya...',
                template: 'No hemos podido transmitir la emoción a <b>Pepito</b> en este momento.<br><br>Inténtalo de nuevo más tarde.'
              });
              console.log('error: ', error);
              $interval.cancel(stop);
            });
        }, 2000);
      }, function(error) {
        $ionicPopup.alert({
          title: 'Vaya...',
          template: 'No hemos podido transmitir la emoción a <b>Pepito</b> en este momento.<br><br>Inténtalo de nuevo más tarde.'
        });
        console.log('error: ', error);
      });
  };
});
