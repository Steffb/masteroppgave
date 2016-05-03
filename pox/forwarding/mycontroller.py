

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""

from helper_functions import *


log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.


_flood_delay = 0



class LearningSwitch (object):
  """ This class represents an switch instance """
 
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent
    try:
      connections[dpid_to_name[connection.dpid]]= connection
    
    except:
      print 'Unable to add the connection for %d'%(connection.dpid)

    #Exp 1
    #connect_gre_tunnels(connection)
    
    #Exp 2
    #connect_gre_in_gre(connection)

    #Exp 3
    #connect_ipsec_gre_tunnels(connection)

    #Exp 4
    ipsec_connect_gre_in_gre(connection)

    if(connection.dpid in dpid_to_name.keys() and  dpid_to_name[connection.dpid] == 'R1'):
 
      pass
    if(connection.dpid in dpid_to_name.keys() and  dpid_to_name[connection.dpid] == 'R2'):

      pass
    if(connection.dpid in dpid_to_name.keys() and  dpid_to_name[connection.dpid] == 'R3'):
      pass
    if(connection.dpid in dpid_to_name.keys() and  dpid_to_name[connection.dpid] == 'C1'):
      pass
    if(connection.dpid in dpid_to_name.keys() and  dpid_to_name[connection.dpid] == 'C2'): 
      pass

      #create_flow(connection, in_port,out_port):
    


    # Our table
    self.macToPort = {}

    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    # We just use this to know when to log a helpful message
    self.hold_down_expired = _flood_delay == 0

    #log.debug("Initializing LearningSwitch, transparent=%s",
    #          str(self.transparent))

  def _handle_PacketIn (self, event):
    # Triggered when switch doesn't have a matching flowrule
    print '[packet_in] from '+dpid_to_name[event.dpid]
    packet = event.parsed
    print '[packet_in] content:\n '+str(packet )
   


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
    
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)
    
    try:
      print dpid_to_name[event.dpid]+ ' connected'
    except:
      print str(event.dpid)+ ' was is not in local dict'
    
    



def launch (transparent=False, hold_down=_flood_delay):
  """
  Starts an L2 learning switch.
  """

  #exp1 creates gre tunnels between c1,c2,r1,r2
  #gre_between_all()

  #exp2
  #gre_in_gre()

  #exp3
  #ipsec_gre_between_all()

  #exp4
  ipsec_gre_in_gre()

  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")
  print 'running core'
  core.registerNew(l2_learning, str_to_bool(transparent))

  


