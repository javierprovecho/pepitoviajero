var express = require('express');
var unirest = require('unirest');
var async = require('async');
var app = express();

app.set('port', (process.env.PORT || 5000));
app.set('googleapikey', process.env.GOOGLE);
app.set('id', process.env.ID);

app.get('/all', function(req, res) {
  var id = app.get('id');
  if (req.query.id) {
    var id = req.query.id;
  };

  async.waterfall([
      function(callback){
        unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/' + id)
          .header('Accept', 'application/json')
          .header('Fiware-Service', 'todosincluidos')
          .header('Fiware-ServicePath', '/iot')
          .end(function(responseA){
            if (responseA.status != 200) {
              res.status(400).send();
              return;
            };
            var data = responseA.body.contextElement;
            callback(null, data);
          });
      },
      function(data, callback){
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
            if (responseB.status != 200) {
              res.status(400).send();
              return;
            };

            var voltage = parseFloat(data.attributes[17].value);

            model = {
              'luminance': parseFloat(data.attributes[8].value),
              'humidity': parseInt(data.attributes[6].value),
              'temperature': parseFloat(data.attributes[16].value),
              'color': data.attributes[3].value,
              'latitude': parseFloat(responseB.body.location.lat),
              'longitude': parseFloat(responseB.body.location.lng),
              'accuracy': parseInt(responseB.body.accuracy),
              'battery': parseInt((voltage - 5.4) * 100.0 / 2.5)
            };

            callback(null, model);
          });
      },
      function(model, callback) {
        unirest.get('https://maps.googleapis.com/maps/api/geocode/json')//?latlng=40.4208935,-3.7019758')
          .query('latlng=' + model['latitude'] + ',' + model['longitude'])
          .end(function(responseC){
            if (responseC.status != 200) {
              res.status(400).send();
              return;
            };

            model['city'] = responseC.body.results[0].address_components[2]
              .long_name;

            res.send(model);
          });
      }
  ]);
});

app.post('/setcolor', function(req, res) {
  var id = app.get('id');
  if (req.query.id) {
    var id = req.query.id;
  };

  unirest.post('http://hackathon.ttcloud.net:10026/v1/contextEntities/' + id +
      '/attributes/color')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .type('json')
    .send({
      'value': req.query.red + ',' + req.query.green + ',' + req.query.blue
    })
    .end(function(responseA){
      if (responseA.body.code != 200) {
        res.status(400).send();
        return;
      };
      res.status(204).send();
    });
});

var server = app.listen(app.get('port'), function () {
  var port = server.address().port;
  console.log('Pepito Viajero escuchando en el puerto %s.',
    server.address().port);
});
