class NotFoundException(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"404 Not Found")

class NegativeQuantity(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"Your request would result in a negative quantity")

class RootDeleteError(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"You cannot delete the whole database")

class ItemOrCategoryMissing(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,"Item or category must be specified")

class OptionIncorrect(Exception):
  def __init__(self,*args,**kwargs):
      Exception.__init__(self,'Option parameter was incorrectly specified')

class AuthenticationError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,'Authentication Failed')
