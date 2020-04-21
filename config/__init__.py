from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


# {'event_date': { $gte: ISODate('2020-04-21T00:00:00.000+00:00'), $lt: ISODate('2020-04-22T00:00:00.000+00:00')} }
# {'token_details': 1, _id: 0}
# {'token_details': 1}



{ "key.token_details": 1}