## Node red

The data (tilt, gravity, temperature, ...) collected by the IoT [ispindle](https://www.ispindel.de/docs/README_en.html) can be forwarded to a server, MQTT broker, brewery web site, ...

The following `node-red flow` has been designed to:
- Collect from a MQTT broker running on a laptop (or raspberry pi) the ispindle data
- Post them on:
  - [ubidots](https://stem.ubidots.com/accounts/signin/)
  - [littlebock](https:www.littlebock.fr)
  - [Brew Spy](https://brew-spy.com/how-to-ispindel.html)
  - Local [influxdb](https://www.influxdata.com/)
- Save the data within a local file named as `ispindel_dd-mm-yyyy.txt`

![image](flow.png)

## How to play with it

Before to start the flow locally:
- Configure your iSpindle to send the data to a MQTT broker (mosquitto,...)
- Install [node-red](https://nodered.org/) and 
- Deploy [mosquitto](http://mosquitto.org/) as MQTT broker
- Install [influxdb](https://www.influxdata.com/) (optional)

Edit the mosquitto config file (e.g: /usr/local/etc/mosquitto/mosquitto.conf) to append the following 2 parameters
supporting to access the broker without user/pwd and to use non localhost as hostname
```
CONFIG_FILE=/usr/local/etc/mosquitto/mosquitto.conf
cat <<EOF >> $CONFIG_FILE
listener 1883
allow_anonymous true
EOF
```
Open a terminal, start the MQTT broker (e.g: `brew services start mosquitto`)

Next, configure the following ENV vars to specify different parameters as the:

`DEVICE_NAME`: the name of the ispindle as defined using the ispindle `configuration` section. Example: `ispindle001`. This name is used by the IoT ispindle
to publish to different topics the data collected such as `ispindle/<DEVICE_NAME>/#`. 
**NOTE**: This name is also used to set the property of message payload `ubidotsDeviceLabel` to publish the data on `ubidots`

`DEVICE_ID`: ID of the Arduino shipset as defined under the ispindle `information` section. Example: `11223344`

`MQTT_BROKER_IP`: IP address of your pi, laptop where the MQTT broker is running. Example: `192.68.1.80`

`MQTT_BROKER_NAME`: Local name of the MQTT broker as displayed within the `ndoe-red` UI. Example: `mqtt-mac`

`LITTLEBOCK_API`: digits to be passed to the API endpoint `/api/log/ispindle/1111/2222` and used to call the server `www.litlebock.fr`. Example: `1111/22222`

`UBIDOTS_TOKEN`: Ubidots API TOKEN. Example: `BBF-xxxxxxxxxxxx`

`BREW_SPY_TOKEN`: Brew Spy token.

`INFLUXDB_URL`: URL of the influxdb server. Example: `http://localhost:8086`

`INFLUXDB_TOKEN`: [Token](https://docs.influxdata.com/influxdb/cloud/security/tokens/) needed to access influxdb v2.0. Optional

**IMPORTANT**: As it possible that you do not want to send the data to all the recipients supported but the ones you want,
then pass as ENV var the list of the recipients as showed hereafter

```bash
# Some examples. Just set one time the ENV var
export RECIPIENTS="ubidots,littlebock"
export RECIPIENTS="ubidots,littlebock,brewspy"
export RECIPIENTS="littlebock"
export RECIPIENTS=""
```

Define next the others env vars within the terminal
```bash
export DEVICE_NAME="YOUR_ISPINDLE_NAME"
export DEVICE_ID="YOUR_ISPINDLE_ID"
export UBIDOTS_TOKEN="YOUR_UBIDOTS_TOKEN"
export MQTT_BROKER_IP="YOUR_MQTT_IP"
export MQTT_BROKER_NAME="YOUR_MQTT_NAME"
export LITTLEBOCK_API="YOUR_LITTLEBOCK_API"
export INFLUXDB_URL="http://<IP_OR_HOSTNAME>:<PORT>"
```
When done, you can launch node-red using the project available under the folder `./flows`.
```bash
node-red -u ./flows

```

### Useful links

- node-red and ubidots: https://help.ubidots.com/en/articles/1440402-connect-node-red-with-ubidots
- Connect `ispindle` to Littlebock, how to calibrate it: https://homebrewing.slammy.net/category/homebrewing/support/
- How to build/debug the Arduino ispindle project: https://dle-dev.com/index.php/2020/10/02/vscode-et-platformio/
- Cloud providers limitation: https://www.mikeandpen.net/beer/ispindel-influx-grafana/
- influxdb, mosquitto, grafana on pi: https://gist.github.com/xoseperez/e23334910fb45b0424b35c422760cb87