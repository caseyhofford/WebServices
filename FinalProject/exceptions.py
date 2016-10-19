class PastTripError(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"This trip has already started")

class LocationFormatError(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"Either destination or current location is misformatted")

class CantGetThereFromHere(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"Item or category must be specified")
