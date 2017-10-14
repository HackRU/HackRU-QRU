const xml2json        = require('xml-js');
const fs              = require('fs');
const express         = require('express'); // Handling Routes
const osascript       = require('node-osascript');
const request         = require('request');
const csrf            = new (require('csrf'));
const config          = require('./config.js');

const app = express();
const port = 8080;

const getQRImage = function getQRImageData(req,res,next){
  if(req.body.qrRetries != null)
    var url = 'http://ec2-54-186-192-209.us-west-2.compute.amazonaws.com:8080/images/'+req.query.email+'.png';
  else
    var url = 'http://ec2-54-186-192-209.us-west-2.compute.amazonaws.com:8080/viewqr?email='+req.query.email;

  var r = request.defaults({encoding:null});
  r.get(url,(err,response,body)=>{
    if(err){
      console.log(err);
    }else if(response.statusCode === 404 && (req.body.qrRetries == null || req.body.qrRetries < 3)){
      console.log('404 ERROR');
      //NOT SURE IF THIS IS COOL-> generate a new QRImage by passing in email to QRU server
      var qrurl = 'http://ec2-54-186-192-209.us-west-2.compute.amazonaws.com:8080/viewqr?email='+req.query.email;
      request.get(qrurl,(error,resp,bod)=>{
          if(req.body.qrRetries == null){
            req.body.qrRetries = 1;
          }else{
            req.body.qrRetries += 1;
          }
          getQRImageData(req,res,next);
      });
    } else{
      req.body.qrimage = new Buffer(body).toString('base64');
      return next();
    }
  });
}

const setUpAuth = function(secret){
    app.get('/auth', (req, res) => {
        if(req.query.pass != config.password){
            res.send(403, "Invalid request or password");
        }else{
            res.send(200, csrf.create(secret));
        }
    });

    app.get('/print', (req, res) => {
        if(!csrf.verify(secret, req.query.csrf)){
            res.send(403, "Invalid request");
        }else{
            req.body = {qrRetries: 0};
            getQRImage(req, res, () => {
                const qr = req.body.qrimage;

                console.log(qr);
                if(!qr){
                    res.send(503, "No QR code");
                    return;
                }

                let label = xml2json.xml2js(fs.readFileSync('qrLabel.label'), {compact: true});
                label.DieCutLabel.ObjectInfo[0].TextObject.StyledText.Element.String._text = req.query.first_name;
                label.DieCutLabel.ObjectInfo[1].TextObject.StyledText.Element.String._text = req.query.last_name;
                label.DieCutLabel.ObjectInfo[2].ImageObject.Image = qr;
                label.DieCutLabel.ObjectInfo[3].TextObject.StyledText.Element.String._text = req.query.email;
                fs.writeFileSync('qrLabel.label', xml2json.js2xml(label, {compact: true, attributesKeys: "_attributes", spaces: '  '}));
                osascript.executeFile('printLabel.applescript', {}, (err, result, raw) => {
                    if(err) res.send(503, err);
                    res.send(200, csrf.create(secret));
                });
            });
        }
    });
}

csrf.secret((err, secret) => {
    if(err){
        console.log(err);
        return;
    }
    setUpAuth(secret);
    app.listen(port);
});
