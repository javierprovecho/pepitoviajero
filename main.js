var express = require('express');
var unirest = require('unirest');
var app = express();


app.get('/raw', function(req, res) {
  unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .end(function(response){
      res.send(response);
    });
});

app.get('/temperature', function(req, res) {
  unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .end(function(response){
      var temperature = response.body.contextElement.attributes[16];
      console.log(temperature);
      model = {
        'temperature': temperature.value
      };
      res.send(model);
    });
});

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});
