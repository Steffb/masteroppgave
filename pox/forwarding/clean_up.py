
# This script cleans up all the flows and bridges created on C1,C2,R1,R2
from helper_functions import *


class l2_learning (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  This is the running object 

  _handle_connection is running once for each switch connecting

  """
  def __init__ (self, transparent):
    
    core.openflow.addListeners(self)
    self.transparent = transparent

  def _handle_ConnectionUp (self, event):
    
    
    clean_ports(event.connection, 'br0')
    try:
      print dpid_to_name[event.dpid]+ ' cleaned ports'
    except:
      print str(event.dpid)+ ' was is not in local dict'
    #display_attr(event.source)

def launch (transparent=False):
  """
  Starts an L2 learning switch.
  """
  print '[##Running 	clean_up############]'
  #exp1 creates gre tunnels between c1,c2,r1,r2
  #gre_between_all()

  #exp2
  #gre_in_gre()

 
  try:
    global _flood_delay
    _flood_delay = int(str(0), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")
  print 'running core'
  core.registerNew(l2_learning, str_to_bool(transparent))

  


