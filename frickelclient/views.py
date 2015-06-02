from flask import render_template, request, redirect, url_for

from frickelclient import app
from frickelclient import lsmsd_api
from frickelclient.forms import ItemForm


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
                                     parent=int(form.parent.data))

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

    if form.validate_on_submit():
        item["Name"] = form.name.data
        item["Description"] = form.description.data
        item["Owner"] = form.owner.data
        item["Maintainer"] = form.maintainer.data
        item["Parent"] = int(form.container.data)

        lsmsd_api.update_item(item)
        return redirect(url_for("show_item", id=item['Id']))
    else:
        form.name.data = item["Name"]
        form.description.data = item["Description"]
        form.maintainer.data = item["Maintainer"]
        form.owner.data = item["Owner"]
        form.container.data = str(item["Parent"])

        return render_template("edit_item.html", form=form)
