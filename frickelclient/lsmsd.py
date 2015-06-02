import json
import requests
from requests.auth import HTTPBasicAuth


class LsmsdError(Exception):
    def __init__(self, endpoint, data, response):
        self.endpoint = endpoint
        self.data = data
        self.response = response


class lsmsd:
    def __init__(self, host, username, password):
        self._host = host
        self._auth = HTTPBasicAuth(username, password)

    def _get_request(self, endpoint):
        res = requests.get(self._host+endpoint, auth=self._auth)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise LsmsdError(endpoint, None, res)

    def _post_request(self, endpoint, data):
        res = requests.post(self._host+endpoint, json.dumps(data),
                            auth=self._auth,
                            headers={"Content-Type": "application/json"})
        if res.status_code == 200:
            item_id = int(res.text.split("/")[2].split('"')[0])
            return self.get_item(item_id)
        else:
            raise LsmsdError(endpoint, data, res)

    def _put_request(self, endpoint, data):
        res = requests.put(self._host+endpoint, json.dumps(data),
                           auth=self._auth,
                           headers={"Content-Type": "application/json"})
        if res.status_code != 200:
            raise LsmsdError(endpoint, data, res)

    def _delete_request(self, endpoint, data=None):
        res = requests.delete(self._host+endpoint, data=json.dumps(data),
                              auth=self._auth,
                              headers={"Content-Type": "application/json"})
        if res.status_code != 200:
            raise LsmsdError(endpoint, data, res)

    def get_items(self):
        return self._get_request("items")

    def get_item(self, id):
        return self._get_request("items/%i" % id)

    def create_item(self, name=None, description=None, maintainer=None,
                    owner=None, parent=None):
        data = {
            "Name": name,
            "Description": description,
            "Maintainer": maintainer,
            "Owner": owner,
            "Parent": parent
        }

        return self._post_request("items", data)

    def update_item(self, item):
        data = item

        return self._put_request("items", data)

    def delete_item(self, id):
        self._delete_request("/items/{id}".format(id=id))
