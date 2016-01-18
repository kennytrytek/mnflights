from google.appengine.ext import ndb


class Hole(object):
    def __init__(self, number, par):
        """
        :type number: int
        :param number: Hole number.
        :type par: int
        :param par: Par for the Hole.
        """
        self.number = number
        self.par = par


class HoleListProperty(ndb.TextProperty):
    @staticmethod
    def toints(a, b):
        return int(a), int(b)

    def _to_base_type(self, value):
        return ' '.join([':'.join([str(h.number), str(h.par)]) for h in value])

    def _from_base_type(self, value):
        return [Hole(*self.toints(*numpar.split(':')))
                for numpar in value.split(' ')]


class Course(ndb.Model):
    name = ndb.TextProperty(indexed=False)
    holes = HoleListProperty(indexed=False)
