# Create Systemd service

Raspberry / Ubuntu 20.04.1 LTS SystemD service script.

## Prerequisis

Have Python3 with vitual env (see https://news.julien-anne.fr/ubuntu-20-04-python3-et-virtualenv-installation-et-erreurs-potentielles/)
Then adapt the path in the service file:

Copy the service file `webhool-bot.service` in `/lib/systemd/system/`

```
sudo cp scripts/webhool-bot.service /lib/systemd/system/
```

Then reload the systemctl daemon and enable the service:

```
sudo systemctl restart daemon-reload
sudo systemctl enable webhook-bot.service
sudo systemctl start webhook-bot.service
```

To see app log use `journalctl` command:

```
sudo journalctl -f -u webhook-bot.service
```