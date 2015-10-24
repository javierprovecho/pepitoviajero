var express = require('express');
var unirest = require('unirest');
var app = express();

app.set('port', (process.env.PORT || 5000));

app.get('/raw', function(req, res) {
  unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .end(function(response){
      res.send(response);
    });
});

app.get('/all', function(req, res) {
  unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .end(function(response){
      var luminance = response.body.contextElement.attributes[8];
      var humidity = response.body.contextElement.attributes[6];
      var temperature = response.body.contextElement.attributes[16];
      model = {
        'luminance': luminance.value,
        'humidity': humidity.value,
        'temperature': temperature.value
      };
      res.send(model);
    });
});

var server = app.listen(app.get('port'), function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});
