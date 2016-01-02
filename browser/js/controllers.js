angular.module('starter.controllers', ['ionic', 'ngCordova'])

.controller('MapCtrl', function($scope, $ionicLoading, $interval, $http, $ionicPopup) {
  $scope.mapCreated = function(map) {
    $scope.map = map;
    $scope.icon = 'http://pepitoviajero.herokuapp.com/img/pepito-small.png';
    $scope.userIcon = 'http://pepitoviajero.herokuapp.com/img/user-position-small.png';
    $scope.updatePosition();
  };

  $scope.updatePosition = function(){
    $http.get('http://pepitoviajero.herokuapp.com/all')
      .then(function(response){
        $scope.position = new google.maps.LatLng(response.data.latitude, response.data.longitude);
        $scope.accuracy = response.data.accuracy;
        if($scope.marker && $scope.circle) {
          $scope.removeMarkers();
        } else {
            $scope.map.setCenter($scope.position);
        };
        $scope.createMarkers();
      }, function(error){ console.log(error);});
  };

  $scope.removeMarkers = function() {
    $scope.marker.setMap(null);
    $scope.circle.setMap(null);
  };

  $scope.createMarkers = function() {
    $scope.marker = new google.maps.Marker({
      position: $scope.position,
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
        center: $scope.position,
        radius: $scope.accuracy / 2
    });
  };

  $interval($scope.updatePosition, 10000);

  $scope.centerOnPepito = function() {
    $scope.map.setCenter($scope.position);
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
      $scope.userPosition = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
      if($scope.userPositionMarker) {
        $scope.userPositionMarker.setMap(null);
      };
      $scope.userPositionMarker = new google.maps.Marker({
        position: $scope.userPosition,
        map: $scope.map,
        label: '¡Estás aquí!',
        icon: $scope.userIcon
      });
      $scope.map.setCenter($scope.userPosition);
      $ionicLoading.hide();
    }, function (error) {
      $ionicLoading.hide();
      $ionicPopup.alert({
        title: 'Vaya...',
        template: 'No hemos podido localizarte',
        buttons: [
          {
            text: 'OK',
            type: 'button-stable',
          }
        ]
      });
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

.controller('StatusCtrl', function($scope, $http) {
  $http.get('http://pepitoviajero.herokuapp.com/all')
    .then(function(response) {
      $scope.data = response.data;
    }, function(error) {
      console.log(error);
    });
})

.controller('CameraCtrl', function($scope, $cordovaCamera) {
  document.addEventListener("deviceready", function () {

    var options = {
      quality: 50,
      destinationType: Camera.DestinationType.DATA_URL,
      sourceType: Camera.PictureSourceType.CAMERA,
      allowEdit: true,
      encodingType: Camera.EncodingType.JPEG,
      targetWidth: 100,
      targetHeight: 100,
      cameraDirection:1,
      popoverOptions: CameraPopoverOptions,
      saveToPhotoAlbum: false,
      correctOrientation:true
    };

    $cordovaCamera.getPicture(options).then(function(imageData) {
      //var image = document.getElementById('myImage');
      //image.src = "data:image/jpeg;base64," + imageData;
    }, function(err) {
      // error
    });

  }, false);
})

.controller('AboutCtrl', function($scope) {
  
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
