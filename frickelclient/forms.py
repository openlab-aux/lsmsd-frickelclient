from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SelectField
from wtforms.validators import Required

from frickelclient import lsmsd_api


class ItemForm(Form):
    name = TextField("Name", validators=[Required()])
    description = TextAreaField("Description", validators=[Required()])
    container = SelectField("Container",
                            validators=[Required()])
    owner = TextField("Owner")
    maintainer = TextField("Maintainer")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.container.choices = [("0", "None")]
        self.container.choices.extend(
            [(str(item['Id']), item['Name']) for item in lsmsd_api.get_items()]
        )
