# lsmsd frickelclient

Simple Flask webclient for [lsmsd][].

## Install

``` shell
mkvirtualenv frickelclient
pip install requests flask flask-script flask-wtf
```

## Configure

Edit `config.py` to point to the [lsmsd][] endpoint (probably needs a `/` at the end).

## Run

    python manage.py runserver

## Debug

    python manage.py runserver -d

[lsmsd]: https://github.com/openlab-aux/lsmsd
