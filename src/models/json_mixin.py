import json
import pickle

from sqlalchemy.ext.declarative import DeclarativeMeta


def _default(obj):
    return {'_python_object': pickle.dumps(obj)}


json.JSONEncoder.default = _default


def _object_hook(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct


json.JSONDecoder.object_hook = _object_hook


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None, exclude=()):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()
               if column.key not in exclude}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__, exclude=exclude)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__, exclude=exclude) for i in value]
        return res

    def to_json(self, rel=None, exclude=None):
        def extended_encoder(x):
            try:
                return str(x)
            except TypeError:
                pass

            try:
                return x.isoformat()
            except TypeError:
                pass

        def remove_nulls(d, obj_filters=obj_filters):
            if obj_filters is None or 'nulls' not in obj_filters:
                return d

            if isinstance(d, list):
                list_dict = []
                for l in d:
                    list_dict.append(
                        dict((k, remove_nulls(v, obj_filters=obj_filters)) for k, v in l.iteritems() if v is not None))
                return list_dict

            if not isinstance(d, dict):
                return d

            return dict((k, remove_nulls(v, obj_filters=obj_filters)) for k, v in d.iteritems() if v is not None)

        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT

        return json.dumps(remove_nulls(self.to_dict(rel, exclude=exclude), obj_filters=filters), default=extended_encoder,
                          indent=4)