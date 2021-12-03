## Grafana

To install grafana
```bash
brew install grafana
brew services start grafana
```

Default user is `admin` and password `admin`

Config files, DB, and grafana.ini path
```bash
ls -la /usr/local/var/lib/grafana/grafana.db
ls -la /usr/local/etc/grafana/grafana.ini
```
The ispindle [dashboard](dashboards/ispindle-dashboard.json) can be imported using curl
```bash
https://community.grafana.com/t/import-dashboard-from-file-via-api/22266

Import all Monitoring Artist AWS dashboards in one go (example script, bash/curl/jq required):

#!/bin/bash

grafana_host="http://localhost:3000"
grafana_cred="admin:admin"
grafana_folder="dashboard"

ds=(1516 677 139 674 590 659 758 623 617 551 653 969 650 644 607 593 707 575 1519 581 584 2969 8050 11099 11154 11155 12979 13018 13040 13104 13892 14189 14391 14392 14954 14955 15016);
folderId=$(curl -s -k -u "$grafana_cred" $grafana_host/api/folders | jq -r --arg grafana_folder  "$grafana_folder" '.[] | select(.title==$grafana_folder).id')
if [ -z "$folderId" ] ; then echo "Didn't get folderId" ; else echo "Got folderId $folderId" ; fi
for d in "${ds[@]}"; do
  echo -n "Processing $d: "
  j=$(curl -s -k -u "$grafana_cred" $grafana_host/api/dashboards/$d | jq .json)
  payload="{\"dashboard\":$j,\"overwrite\":true"
  if [ ! -z "$folderId" ] ; then payload="${payload}, \"folderId\": $folderId }";  else payload="${payload} }" ; fi
  curl -s -k -u "$grafana_cred" -XPOST -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    $grafana_host/api/dashboards/import; echo ""
done                
```

## Backup and restore

Python tool to backup/restore grafana: https://github.com/ysde/grafana-backup-tool

To recover a lost [password](https://jenciso.github.io/blog/how-to-recovery-the-admin-password-in-grafana/)
```bash
sqlite3 /usr/local/var/lib/grafana/grafana.db
> SQLite version 3.32.3 2020-06-18 14:16:19
> Enter ".help" for usage hints.
> sqlite> update user set password = '59acf18b94d7eb0694c61e60ce44c110c7a683ac6a8f09580d626f90f4a242000746579358d77dd9e570e83fa24faa88a8a6', salt = 'F3FAxVm33R' where login = 'admin';
> sqlite> .exit
```

To backup/restore your [datasource](https://rmoff.net/2017/08/08/simple-export/import-of-data-sources-in-grafana/)

```bash
mkdir -p config/datasources
curl -s "http://localhost:3000/api/datasources" -u "admin:admin"  |jq -c -M '.[]' | split -l 1 - config/datasources/

for i in data_sources/*; do \
    curl -X "POST" "http://localhost:3000/api/datasources" \
    -H "Content-Type: application/json" \
     --user admin:admin \
     --data-binary @$i
done
```

## Links

Pi + grafana: https://blog.anoff.io/2021-01-howto-grafana-on-raspi/
