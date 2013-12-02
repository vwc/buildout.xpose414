Introduction
============

This is the development buildout for xpose414 site.

In order to bootstrap a development environment just do

```bash
$ ~/python/bin/virtualenv-2.7 xpose
$ cd ./xpose
$ python bootstrap.py -c development.cfg
$ bin/buildout -c develoment.cfg
```

Setup API Access
----------------

In order to access external APIs ou need to authenticate with the services. For
GA access the following details are required:

```json
{
  "installed": {
    "client_id": "[[INSERT CLIENT ID HERE]]",
    "client_secret": "[[INSERT CLIENT SECRET HERE]]",
    "redirect_uris": [],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```

Xovi API paramters:

```
    'key'     => 'myPersonalKey',
    'service' => 'user',
    'method'  => 'getCreditState',
    'format'  => 'json',
``




