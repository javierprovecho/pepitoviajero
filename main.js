var express = require('express');
var unirest = require('unirest');
var app = express();

var getData = function() {
  unirest.get('http://hackathon.ttcloud.net:10026/v1/contextEntities/UOE9AW')
    .header('Accept', 'application/json')
    .header('Fiware-Service', 'todosincluidos')
    .header('Fiware-ServicePath', '/iot')
    .end(function(response){
      return response
  });
  return null;
}
app.get('/all', function (req, res) {
  res.send(getData());
});

var server = app.listen(3000, function () {

  var host = server.address().address;
  var port = server.address().port;

  console.log('Example app listening at http://%s:%s', host, port);

});
