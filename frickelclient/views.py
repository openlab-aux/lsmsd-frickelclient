from flask import render_template, request, redirect, url_for

from frickelclient import app
from frickelclient import lsmsd_api
from frickelclient.forms import ItemForm
import requests
import json


@app.route("/dinge")
@app.route("/")
def list_items():
    items = lsmsd_api.get_items()
    return render_template("list_items.html", items=items)


@app.route("/ding/<int:id>")
def show_item(id):
    item = lsmsd_api.get_item(id)
    if item['Parent'] != 0:
        parent = lsmsd_api.get_item(item['Parent'])
        item['Parent'] = parent

    return render_template("list_single_item.html", item=item)


@app.route("/dinge/add", methods=['GET', 'POST'])
def add_item():
    form = ItemForm(request.form)
    if form.validate_on_submit():
        item = lsmsd_api.create_item(name=form.name.data,
                                     description=form.description.data,
                                     owner=form.owner.data,
                                     maintainer=form.maintainer.data,
                                     parent=int(form.container.data),
                                     usage=form.usage.data,
                                     discard=form.discard.data)

        return redirect(url_for("show_item", id=item['Id']))
    else:
        return render_template("add_item.html", form=form)


@app.route("/dinge/delete/<int:id>")
def delete_item(id):
    lsmsd_api.delete_item(id)
    return redirect(url_for("list_items"))


@app.route("/dinge/edit/<int:id>", methods=['GET', 'POST'])
def edit_item(id):
    item = lsmsd_api.get_item(id)
    form = ItemForm(request.form)

    # POST
    if form.validate_on_submit():
        item["Name"] = form.name.data
        item["Description"] = form.description.data
        item["Owner"] = form.owner.data
        item["Maintainer"] = form.maintainer.data
        item["Parent"] = int(form.container.data)
        item["Usage"] = form.usage.data
        item["Discard"] = form.discard.data

        lsmsd_api.update_item(item)
        return redirect(url_for("show_item", id=item['Id']))
    # GET
    else:
        form.name.data = item["Name"]
        form.description.data = item["Description"]
        form.maintainer.data = item["Maintainer"]
        form.owner.data = item["Owner"]
        form.container.data = str(item["Parent"])
        form.usage.data = item["Usage"]
        form.discard.data = item["Discard"]

        return render_template("edit_item.html", form=form)


@app.route("/dinge/label/<int:id>", methods=["POST"])
def print_label(id):
    item = lsmsd_api.get_item(id)

    if item is None:
        return "NOT FOUND", 404

    url = app.config["KLAUSKLEBER_AAS_URL"]
    data = {"id": str(item['Id']),
            "name": item['Name'],
            "maintainer": item['Maintainer'],
            "owner": item['Owner'],
            "use_pol": item['Usage'],
            "discard_pol": item['Discard']}

    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain'}

    try:
        r = requests.post(url, data=json.dumps(data), headers=headers,
                          timeout=5)
    except requests.ConnectionError:
        return "KLAUSKLEBER UNREACHABLE", 501

    if r.status_code == 200:
        return "OK", 200
    else:
        return "FAIL", 501


@app.route("/dinge/search", methods=["POST"])
def search_items():
    all_items = lsmsd_api.get_items()
    found_items = []
    query = request.form['search']

    for item in all_items:
        if query.lower() in item["Name"].lower() or \
           query.lower() in item["Description"].lower():
            found_items.append(item)

    return render_template("list_items_search.html", items=found_items,
                           query=query)
