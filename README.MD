A Work Instructions Flask App

This app is intended to display work instructions for an operator working through a process. The page shows the user an image and written instructions, as well 
as inputs to record data. This data can be downloaded lata as a csv file.

The work instructions can be set through the app, with different instructions and data for different parts.

# Setup

Create `config.py` in the root folder from `example-confs/config-example.py` and edit config options. Modify the secret key to a random string

Run `npm install` in the `/app/static` directory to download js dependencies.
Run `npm run build` to build the bootstrap styles.

Run `pip install -r requirements.txt` in a virtual environment if necessary.

Gunicorn is recommended, install with `pip install gunicorn`

To run at startup, an example config for systemd is provided in the `example-confs` folder. Copy to `/etc/systemd/system` and run `sudo systemctl daemon-reload` then `sudo systemctl enable work_instructions`. Make sure to edit the paths in the service config files.

For security, the app should be run by a different user. For example, create a user called flask `useradd flask` and give them ownership of the app `chown -R flask /home/user/work_instructions_webapp`. Ensure the app is started by the same user in your systemd service files.

The software ideally uses nginx as a reverse proxy. This can be installed with `sudo apt install nginx`. An example config is included in this repo. In order for the android app to work correctly, the proxy server must pass on the IP address of the android client.
