# !usr/bin/env python
# -*- coding: utf8 -*-

import config_default

class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            raise AttributeError(r'`Dict` object has no attribute `%s`' % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defauts, override):
    r = {}
    for k, v in defauts:
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.iteritems():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

try:
    import config_override
    configs = merge(config_default, config_override)
except ImportError:
    pass

configs = toDict(configs)