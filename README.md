## Node red

The data (tilt, gravity, temperature, ...) collected by the IoT [ispindle](https://www.ispindel.de/docs/README_en.html) can be forwarded to a server, MQTT broker, brewery web site, ...

The following `node-red flow` has been designed to collect from a MQTT broker running on a laptop (or raspberry pi)
the data which are then enriched in order to post them on [ubidots](https://stem.ubidots.com/accounts/signin/) or [littlebock](https:www.littlebock.fr)

## How to play with it

Before to start the flow locally, install:
- [node-red](https://nodered.org/) and 
- [mosquitto](http://mosquitto.org/) as MQTT broker

Edit the mosquitto config file (e.g: /usr/local/etc/mosquitto/mosquitto.conf) to append the following 2 parameters
supporting to access the broker without user/pwd and to use non localhost as hostname
```
listener 1883
allow_anonymous true
```
Open a terminal, start the MQTT broker (e.g: `brew services start mosquitto`)

To be able to work with the `ubidots_out` node flow, it is needed to specify as `token` your own [Api Token](https://stem.ubidots.com/accounts/me/apiCredentials).
So, edit the file `flows.json` and search about the type `ubidots_dots` and then change the field value of the `token`
```json
  {
    "id": "9882cb140721248b",
    "type": "ubidots_out",
    "z": "a490cb4b563e3faf",
    "name": "",
    "token": "BBFF-xxxxxxxxTO_BE_CHANGEDxxxxxx",
...
```
Change also within the `flows.json` file, the `mqtt-broker` object to specify the IP address (see `broker`) of your pi, laptop where the MQTT broker is running.

**NOTE**: You can also change the name displayed within the node-red editor (e.g `mosquitto-mac`)
```json
  {
    "id": "e7a90bd264380835",
    "type": "mqtt-broker",
    "name": "mosquitto-mac",
    "broker": "192.168.1.90",
    "port": "1883",
...
```
When done, you can launch node-red using the project available under the folder `./flows`.

Use the following ENV vars to specify the: 
`DEVICE_NAME` : the name of the ispindle as defined using the ispindle `configuration` section
`DEVICE_ID` : ID of the Arduino shipset as defined under the ispindle `information` section

```bash
export DEVICE_NAME="Ispindel001"
export DEVICE_ID="14559617"
node-red -u ./flows
```

**NOTE**: Don't forget to pass as parameter the device name to be used to report the data to `https://stem.ubidots.com/app/devices/` web page but also to 
access properly the MQTT topics as by convention, ispindle will publish them using as topics name `ispindle/<DEVICE_NAME>/#` where `DEVICE_NAME` could be by example what you encoded within
the ispindle config `Ispindel001` !!

### Useful links

- node-red and ubidots: https://help.ubidots.com/en/articles/1440402-connect-node-red-with-ubidots
- Connect `ispindle` to Littlebock, how to calibrate it: https://homebrewing.slammy.net/category/homebrewing/support/
- How to build/debug the Arduino ispindle project: https://dle-dev.com/index.php/2020/10/02/vscode-et-platformio/