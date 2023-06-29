#!/usr/bin/python3

import time


class Timer():
  """Times stuff."""
  
  def __init__(self, start_now=None, start_text=None, end_text=None, logger=None):
    if start_now is None: start_now = False
    if start_text is None: start_text = "Starting timer . . ."
    if end_text is None: end_text = "Took {:0.2f} seconds.\n"
    if logger is None: logger = print
    
    self.start_text = start_text
    self.end_text = end_text
    self.logger = logger
    self._start_time = None
    
    if start_now: self.start()
    
  def _get_time(self):
    return time.time()
  
  def elasped_time(self):
    return self._get_time() - self._start_time
  
  def start(self):
    if self.logger: self.logger(self.start_text)
    self._start_time = self._get_time()
  
  def _stop(self):
    elapsed_time = self.elasped_time()
    if self.logger: self.logger(self.end_text.format(elapsed_time))
  
  def stop(self):
    self._stop()
    self._start_time = None
  
  def update(self, start_now=True, start_text=None, end_text=None, logger=None):
    self._stop()
    self.__init__(start_now  = self.start_now  if start_now  is None else start_now, 
                  start_text = self.start_text if start_text is None else start_text, 
                  end_text   = self.end_text   if end_text   is None else end_text, 
                  logger     = self.logger     if logger     is None else logger)
  


def create_global_timer(start_text=None, log_it=True, start_now=True, **kwargs):
  if log_it:
    global _TIMER
    _TIMER = Timer(start_now=start_now, start_text=start_text, **kwargs)


def update_global_timer(start_text=None, log_it=True, **kwargs):
  if log_it:
    global _TIMER
    _TIMER.update(start_text=start_text, **kwargs)


def stop_global_timer(log_it=True, **kwargs):
  if log_it:
    global _TIMER
    _TIMER.stop(**kwargs)
    del globals()["_TIMER"]


def globally_time(function, *args, **kwargs):
  if function == 0:
    create_global_timer(*args, **kwargs)
  elif function == 1:
    update_global_timer(*args, **kwargs)
  elif function == 2:
    stop_global_timer(*args, **kwargs)
  else:
    raise Exception("You need to enter 0, 1, or 2 for function.")


def log_timing(start_text=None, log_it=True, **kwargs):
  if start_text is not None:
    if "_TIMER" not in globals():
      create_global_timer(start_text=start_text, log_it=log_it, **kwargs)
    else:
      update_global_timer(start_text=start_text, log_it=log_it, **kwargs)
  else:
    stop_global_timer(log_it=log_it, **kwargs)
    


if __name__ == "__main__":
  import gc
  
  t = Timer()
  print("Test 1:\n")
  
  t.start()
  time.sleep(1)
  t.stop()
  del t
  gc.collect()
  
  
  print("\nTest 2:\n")
  t = Timer(start_now=True, start_text="Waiting for a bit . . .", end_text="Took {:0.4f} seconds.\n")
  time.sleep(2)
  t.update(start_text="Waiting a bit more . . .")
  time.sleep(1)
  t.update(start_text="Last time . . .", end_text="Took {:0.1f} seconds.\n")
  time.sleep(1)
  t.stop()
  
  print("\nTest 3:\n")
  create_global_timer("Doing stuff . . . ")
  time.sleep(1)
  update_global_timer("Doing more stuff and things . . .", end_text="{:0.3f} seconds, or something.\n")
  time.sleep(2)
  update_global_timer("You probably shouldn't see this . . .", False, end_text="{:0.2f} seconds... You shouldn't see this either....\n")
  time.sleep(1)
  update_global_timer(start_text="Last one . . .", end_text="yo, it's been {:0.1f} seconds.\n")
  time.sleep(2)
  stop_global_timer()
  
  print("\nTest 3:\n")
  globally_time(0, "Doing stuff . . . ")
  time.sleep(1)
  globally_time(1, "Doing more stuff and things . . .", end_text="{:0.3f} seconds, or something.\n")
  time.sleep(2)
  globally_time(1, "You probably shouldn't see this . . .", False, end_text="{:0.2f} seconds... You shouldn't see this either....\n")
  time.sleep(1)
  globally_time(1, start_text="Last one . . .", end_text="yo, it's been {:0.1f} seconds.\n")
  time.sleep(2)
  globally_time(2)
  
  print("\nTest 4:\n")
  log_timing("Doing stuff . . . ")
  time.sleep(1)
  log_timing("Doing more stuff and things . . .", end_text="{:0.3f} seconds, or something.\n")
  time.sleep(2)
  log_timing("You probably shouldn't see this . . .", False, end_text="{:0.2f} seconds... You shouldn't see this either....\n")
  time.sleep(1)
  log_timing(start_text="Last one . . .", end_text="yo, it's been {:0.1f} seconds.\n")
  time.sleep(2)
  log_timing()
  
  print("\nAlright, that's it.")
  
  
