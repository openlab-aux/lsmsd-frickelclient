from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import Required


class ItemForm(Form):
    name = TextField("Name", validators=[Required()])
    description = TextAreaField("Description", validators=[Required()])
    owner = TextField("Owner")
    maintainer = TextField("Maintainer")
