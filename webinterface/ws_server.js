#!/usr/bin/env node

// webserver with websockets

// Requirements:
//  npm install websocket

// config
var queues = ["bf", "dict", "gpu"];
// end config

var WebSocketServer = require('websocket').server;
var http = require("http");
var fs = require('fs')
var server = http.createServer(callback).listen(1337, "127.0.0.1");
console.log("Webserver running on port 1337...");

function callback(request, response) {
    var head = "<!doctype html>" +
        "<html>\n";
    response.writeHead(200, "OK Node", {"content-type": "text/html; charset=utf-8"});
    response.write(head);
    fs.readFile("ws_client.html", function (err, data) {
        body = data + "</html>";
        response.end(body)
    })
}


var wsServer = new WebSocketServer({
    httpServer: server,
});


wsServer.on('request', function (request) {
    var connection = request.accept();
    console.log((new Date()) + ' Connection accepted.');
    connection.on('message', function (message) {
        if (message.type === 'utf8') {
            var msg = message.utf8Data;
            console.log('Received Hash: ' + msg);

            // Dispatch to workers
            var amqp = require('amqplib/callback_api');

            amqp.connect('amqp://localhost', function (err, conn) {
                queues.forEach(function (q) {
                    conn.createChannel(function (err, ch) {
                        ch.assertQueue(q, {durable: true});
                        ch.sendToQueue(q, new Buffer(msg), {persistent: true});
                        console.log(" [x] Sent '%s' to queue '%s'", msg, q);
                    });
                });
            });
            // end dispatching code

            // todo: handle result messages
            connection.sendUTF("i didn't do nuffin");
        }
    });
    connection.on('close', function (reasonCode, description) {
        console.log((new Date()) + ' Peer ' + connection.remoteAddress + ' disconnected.');
    });
});