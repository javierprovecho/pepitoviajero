var express = require('express');
var unirest = require('unirest');
var app = express();

app.set('port', (process.env.PORT || 5000));
app.set('googleapikey', (process.env.GOOGLE));

app.get('/all', function(req, res) {
  unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .end(function(responseA){
      var data = responseA.body.contextElement;

      unirest.post('https://www.googleapis.com/geolocation/v1/geolocate')
        .query('key=' + app.get('googleapikey'))
        .type('json')
        .send({
          'cellTowers': [
            {
              'cellId': parseInt(data.attributes[0].value, 16),
              'locationAreaCode': parseInt(data.attributes[7].value, 16),
              'mobileCountryCode': data.attributes[9].value,
              'mobileNetworkCode': data.attributes[11].value,
            }
          ]
        })
        .end(function(responseB){
          model = {
            'luminance': parseFloat(data.attributes[8].value),
            'humidity': parseInt(data.attributes[6].value),
            'temperature': parseFloat(data.attributes[16].value),
            'color': data.attributes[3].value,
            'latitude': parseFloat(responseB.body.location.lat),
            'longitude': parseFloat(responseB.body.location.lng),
            'accuracy': parseInt(responseB.body.accuracy)
          };
          res.send(model);
        })
    });
});

var server = app.listen(app.get('port'), function () {
  var port = server.address().port;
  console.log('Pepito Viajero escuchando en el puerto %s', server.address().port);
});
