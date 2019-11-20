from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from models import History


class HistoryModelView(ModelView):
    datamodel = SQLAInterface(History)

class GroupModelView(ModelView):
    datamodel = SQLAInterface(History)
    related_views = [HistoryModelView]

