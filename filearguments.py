class FileArguments:
  """ Class that handles getting and testing the arguments to a file (i.e. python file.py [args])."""
  
  class BreakOutOfTry(Exception):
    pass

  def __init__(self, form=None, get=False, fill_empties_with_none=False):
    """Initializes the contraints on the arguments."""
    if form is not None:
      try:
        if len(form) == 0: # empty list
          form = None
          raise self.BreakOutOfTry
        for f in iter(form):
          if type(f) is not type(type(1)):
            raise TypeError
      except self.BreakOutOfTry: pass
      except TypeError: raise ValueError("FileArguments Input Error: Form must be either None or an iterable whose elements are the type of the variable desired.")
      
    self.args = []
    self._args_checked = False
    self.form = form
    self.fill_empties_with_none = fill_empties_with_none
    if get: self.get_args()
  
  def _get_args(self):
    """Gets the arguments without checking them"""
    import sys
    self.args = sys.argv[1:]
    return self.args

  def _check_args(self):
    """Checks the arguments for if they are compatible with the desired contraints"""
    if not self._args_checked:
        if self.form is not None:
          end_nones = 0
          if len(self.form) > len(self.args):
            if self.fill_empties_with_none:
              end_nones = len(self.form) - len(self.args)
              self.args.extend([None for _ in range(end_nones)])
            else:
              raise ValueError("Not enough arguments. Requires {} arguments and instead {} were entered.".format(len(self.form), len(self.args)))
          if len(self.form) < len(self.args):
            raise ValueError("Too many enough arguments. Requires {} arguments and instead {} were entered.".format(len(self.form), len(self.args)))
          
          max_i = len(self.form) - end_nones
          for i, f in enumerate(self.form):
            if i >= max_i:
                break
            try:
              self.args[i] = f(self.args[i])
            except:
              raise ValueError("Incorrect type entered in argument {}: {}. Requires the datatype: {}.".format(i, self.args[i], f))
    self._args_checked = True
    
  def get_args(self):
    """Gets the arguments and checks if they are of the right form."""
    self._get_args()
    self._check_args()
    return self.args


def get_filearguments(*form, fill_empties_with_none=False):
  """Shortens getting the file arguments"""
  return FileArguments(form, get=True, fill_empties_with_none=fill_empties_with_none).args

