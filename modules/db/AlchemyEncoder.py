import datetime
import json
from decimal import Decimal

from sqlalchemy.ext.declarative import DeclarativeMeta
from modules.helper import DateHelper


def to_json(tab_obj, **kwargs):
    """
    Pour transformer des objets Sqlalchemy en json
    :param obj: tableau d'ojet à parser
    :param kwargs: parametre només supplémentaires
    :return: chaine json
    """
    # an SQLAlchemy class
    tabJsonObj=[]

    date_format = kwargs.get('date_format', None)

    for obj in tab_obj:
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            # an SQLAlchemy class
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'query_class' and x != 'query']:
                data = obj.__getattribute__(field)
                try:
                    if isinstance(data, (datetime.date, datetime.datetime)):
                        if date_format:
                            s = DateHelper.to_str(data, date_format)
                        else:
                            s = data.isoformat()
                    elif isinstance(data, Decimal):
                        s = str(data)
                    elif isinstance(data, str):
                        s = data
                    else:
                        s = json.dumps(data) # this will fail on non-encodable values, like other classes

                    fields[field] = s
                except TypeError:
                    fields[field] = None
            tabJsonObj.append(fields)
        else:
            tabJsonObj.append(json.JSONEncoder.default(obj))

    return json.dumps(tabJsonObj)
