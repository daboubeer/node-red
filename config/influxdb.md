## Influxdb

Steps to be executed to install/delete influxdb on macos

```bash
brew uninstall influxdb
brew uninstall influxdb-cli
rm -rf /usr/local/etc/influxdb2
rm -rf ~/.influxdbv2
rm -rf /usr/local/var/lib/influxdb2/

brew install influxdb-cli
brew install influxdb
brew services restart influxdb

brew services stop influxdb
```

Next, setup the config, user/pwd, org, bucket and token
```bash
influx setup \
  -u dabou \
  -p adminadmin \
  -o daboubeer \
  -b Ispindel001 \
  -t RYYR7Rjah4DpWsuExELloKt_uCLT3yy2ubcSpKQLwlRTPNekJyugXNPAM-g7SCOTZAevBZHSUUJlshB8JD6mYA== \
  -r 0 -f
```