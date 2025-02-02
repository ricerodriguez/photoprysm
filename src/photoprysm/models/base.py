import re
import json
from dataclasses import dataclass, fields, asdict
from typing import Any, Self, Optional

# Semi-private
def snake(_camel: str):
    '''Taken from https://stackoverflow.com/a/1176023'''
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', _camel)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()

def camel(_snake: str):
    '''Modified from https://stackoverflow.com/a/1176023'''
    rv = ''.join(word.title() for word in _snake.split('_'))
    rv = re.sub(r'(uid|json|http|id)', lambda x: x.group(1).upper(), rv)
    return rv

def _asjson(cls: dataclass) -> str:
    d0 = asdict(cls)
    d1 = {}
    for k,v in d0.items():
        if v is None: continue
        key = camel(k)
        d1[key] = v
    return json.dumps(d1)

def _askwargs(**kwargs):
    d = {}
    for k, v in kwargs.items():
        if v is None: continue
        d[snake(k)] = v
    return d

@dataclass
class ModelBase:
    '''Base model for the all models.'''
    def __init_subclass__(cls: Self, /, required: Optional[list[str]] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if required:
            cls.__required_attrs__ = set(required)
        else: cls.__required_attrs__ = set()

    @property
    def json(self):
        d = {}
        for attr in fields(self):
            value = getattr(self, attr.name, None)
            if value is None: continue
            d[camel(attr.name)] = value
        return json.dumps(d)
        
    @classmethod
    def fromjson(cls: Self, djson: dict[str,Any]):
        '''Alternative constructor. Builds the instance from the JSON response.'''
        # Required attribute names are passed in as args
        required_attrs = {}
        for arg in cls.__required_attrs__:
            if djson.get(camel(arg)) is None:
                raise TypeError(f'JSON response missing required arg \'{arg}\'.')
            else: required_attrs[arg] = djson.get(camel(arg))
        inst = cls(**required_attrs)
        # Now we set the rest of the attributes
        for attr in fields(cls):
            setattr(inst, attr.name, djson.get(camel(attr.name)))
        return inst
