## Node red

Les données collectées par le [ispindle](https://www.ispindel.de/docs/README_en.html) peuvent être envoyées vers un site qui gère vos recettes et/ou brassins 
voir également vers des plateformes qui agrègent des données :

- Brewfather
- Little Bock
- Grainfather
- Ubidots
- Blynk
- Brew Spy

Néanmoins, le iSpindle ne peut être configuré que pour envoyer ses données que sur une seule plateforme et ne peut en occurrence gérer des pertes de données si le site distant ne répond plus.

Ce projet a été développé afin de palier à ces limitations en offrant la possibilité de récolter les données sur un broker MQTT et ensuite de router les données vers différents
destinataires que vous pouvez paramétriser comme par exemple :

 - [Ubidots](https://ubidots.com/)
 - [littlebock](https:www.littlebock.fr)
 - [Brew Spy](https://brew-spy.com/how-to-ispindel.html)
 - [influxdb](https://www.influxdata.com/)
 
**Note**: Les données sont également sauvegardées dans un fichier localement et qui est nommé comme suit: `ispindel_dd-mm-yyyy.txt`

![image](flow.png)

## Comment utiliser l'outil !

Avant de démarrer l' application `node-red` localement, veillez à :

- Configurer votre iSpindle pour envoyer les données vers le broker MQTT,
- Installer les logiciels suivants:
  - [node-red](https://nodered.org/),
  - [mosquitto](http://mosquitto.org/),
  - [influxdb](https://www.influxdata.com/) (optional)
  - [Grafana](https://grafana.com/) (optional)

### Mosquitto

Le logiciel libre [Mosquitto](https://mosquitto.org/) de la fondation Eclipse est une application qui permet de 
stocker dans des files des messages et ensuite de les dispatcher vers des clients connectés. Le protocole de transport
des message et de communication supporté est [MQTT](https://mqtt.org/).

TODO: Ajouter les instructions pour l'installer

Ensuite, il faut éditer le fichier de configuration `mosquitto.conf` pour y ajouter les 2 options suivantes et ceci afin de permettre
l' accès des clients de manière anonyme, non sécurisée afin que ceux-ci souscrivent aux files pour consommer les messages contenant les données deiSpindle.

```
CONFIG_FILE=/usr/local/etc/mosquitto/mosquitto.conf
cat <<EOF >> $CONFIG_FILE
listener 1883
allow_anonymous true
EOF
```

Ouvrir sur votre ordinateur un terminal et démarrer le service `mosquitto`
```bash
systemctl start mosquitto
```

### Node-red

Le routage des messages se fait via des routes ou flux qui sont géré(e)s par le logiciel `node-red`.
Afin d' éviter de devoir éditer manuellement les flux pour configurer différentes options, des
variables d' environnement ont été définies et vous permettront de configurer les paramètres suivants:

`DEVICE_NAME`: le nom du `ispindle` comme défini via le menu `configuration` de l' interface que vous avez configuré via le réseau Wifi - iSpindle. Exemple : `ispindle001`. 
Ce nom est utilisé par le logiciel du spindle pour publier les données sur différentes files, une par type de données `tilt,temperature,...`. Dès lors, les données seront récoltées par le broker sous 
le chemin d'accès suivant `ispindle/<DEVICE_NAME>/#`. Le symbole `#` est utilisé pour indiquer le nom d' une des files

**Note**: Ce nom est aussi utilisé pour configurer la propriété `ubidotsDeviceLabel` quand les données sont publiées sur `ubidots`

`DEVICE_ID`: ID du shipSet arduino comme défini dans la section `information` du ispindle. Exemple: `11223344`

`MQTT_BROKER_IP`: Adresse IP de votre ordinateur, RaspberryPI sur lequel le broker MQTT est en service. Exemple: `192.68.1.80`

`MQTT_BROKER_NAME`: Nom local du broker MQTT comme défini dans l' interface graphique de `node-red` UI. Example: `mqtt-mac`. TODO: revoir cette ligne

`LITTLEBOCK_API`: Identifiants de LittleBock utilisé pour confiurer le chemein ou API suivant `/api/log/ispindle/1111/2222` et utilisé pour appeler le serveur `www.litlebock.fr`. Exemple: `1111/22222`

`UBIDOTS_TOKEN`: API TOKEN d' Ubidots. Exemple: `BBF-xxxxxxxxxxxx`

`BREW_SPY_TOKEN`: Token de Brew Spy.

`INFLUXDB_URL`: URL serveur InfluxDB. Exemple: `http://localhost:8086`

`INFLUXDB_TOKEN`: [Token](https://docs.influxdata.com/influxdb/cloud/security/tokens/) nécessaire pour être authentifé avec le serveur `influxdb v2.0`. TODO: Revoir cette ligne car le token doit malheureusement être ajouté via le UI node red et être codé en dur. 

**IMPORTANT**: Comme il est possible que vous ne souhaitiez pas envoyer les données vers TOUS les destinataires, mais seulement ceux qui vous intéressent ou pour lequel(s) vous disposez d' un accès et identifiant, 
utilisez à cette fin la variable d' environnement suivante :

```bash
# Qqs examples
export RECIPIENTS="ubidots,littlebock"
export RECIPIENTS="ubidots,littlebock,brewspy"
export RECIPIENTS="littlebock"
export RECIPIENTS=""
```

Pour configurer les variables d'environnement, ouvrez un terminal et définisez-les: 
```bash
export DEVICE_NAME="YOUR_ISPINDLE_NAME"
export DEVICE_ID="YOUR_ISPINDLE_ID"
export UBIDOTS_TOKEN="YOUR_UBIDOTS_TOKEN"
export MQTT_BROKER_IP="YOUR_MQTT_IP"
export MQTT_BROKER_NAME="YOUR_MQTT_NAME"
export LITTLEBOCK_API="YOUR_LITTLEBOCK_API"
export INFLUXDB_URL="http://<IP_OR_HOSTNAME>:<PORT>"
```
ensuite, lancez le projet `node-red` et le flux/routage défini dans le répertoire `./flows`.
```bash
node-red -u ./flows

```

### Liens utiles

- node-red et ubidots: https://help.ubidots.com/en/articles/1440402-connect-node-red-with-ubidots
- Connecter `ispindle` à Littlebock et comment le calibrer: https://homebrewing.slammy.net/category/homebrewing/support/
- Comment débogger le projet Arduino ispindle: https://dle-dev.com/index.php/2020/10/02/vscode-et-platformio/
- Limitation des fournisseurs cloud pour iSpindle: https://www.mikeandpen.net/beer/ispindel-influx-grafana/
- Influxdb, mosquitto, grafana sur Raspberry pi: https://gist.github.com/xoseperez/e23334910fb45b0424b35c422760cb87