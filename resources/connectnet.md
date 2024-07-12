```bash
nmcli device wifi connect "MiWiFi" password "miclavesecrета"
```

nmcli device wifi list
nmcli device wifi connect SSID-Name password wireless-password

```
iwconfig wlan0 essid "NOMBRE_DE_LA_RED" key s:"CONTRASEÑA_DE_LA_RED"
dhclient wlan0

```
Reemplaza "wlan0" con el nombre de tu interfaz Wi-Fi si es diferente.

Con wpa_supplicant (para redes protegidas con WPA/WPA2):
```bash
wpa_passphrase "NOMBRE_DE_LA_RED" "CONTRASEÑA_DE_LA_RED" > wpa.conf
wpa_supplicant -B -i wlan0 -c wpa.conf
dhclient wlan0
```

Si tu sistema usa systemd-networkd, puedes crear un archivo de configuración:

```bash
nano ~/.config/systemd/network/25-wireless.network
```

y anadir
```bash
[Match]
Name=wlan0

[Network]
DHCP=yes

[DHCP]
RouteMetric=20
```

Luego, crear un archivo para la conexión Wi-Fi:

```shell
wpa_passphrase "NOMBRE_DE_LA_RED" "CONTRASEÑA_DE_LA_RED" > ~/.config/wpa_supplicant/wpa_supplicant-wlan0.conf
```
finalmente:
```bash
systemctl --user start wpa_supplicant@wlan0
```

