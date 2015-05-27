from flask import Flask
from frickelclient import lsmsd

app = Flask(__name__)
app.config.from_object("frickelclient.config")
lsmsd_api = lsmsd.lsmsd(app.config["LSMSD_HOST"],
                        app.config["LSMSD_USER"],
                        app.config["LSMSD_PASS"])

from frickelclient import views
