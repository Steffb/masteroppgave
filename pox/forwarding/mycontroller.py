

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""
import paramiko
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
from pox.lib.addresses import IPAddr, EthAddr
import time
from pprint import pprint

log = core.getLogger()

username='mininet'

server='192.168.56.101'

class sshInfo:
    def __init__(self ,ip_address , name, password, name=None):
      self.name = name
      self.ip_address = ip_address
      self.name = name
      self.password = password


dpid_to_name = {2:'C2',1:'C1',165681365082191:'R3', 257735962336073:'R2', 191817531570252:'R1'}
name_to_dpid = {'C2': 2, 'C1': 1, 'R3': 165681365082191, 'R2': 257735962336073, 'R1': 191817531570252}
name_to_sshInfo = {
'R1': sshInfo('192.168.56.106','ubuntu' ,'reverse', name='R1'),
'R2': sshInfo('192.168.56.107','ubuntu' ,'reverse', name='R2'),
'R3': sshInfo('192.168.56.108','ubuntu' ,'reverse', name='R3'),
'C1': sshInfo('192.168.56.101','mininet','mininet', name='C1'),
'C2': sshInfo('192.168.56.105','mininet','mininet', name='C2')
}
connections = {}

def display_attr(object):
  pprint (vars(object))


def exec_ssh_command(sshInfo, command):
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(sshInfo.ip_address, username=sshInfo.name, password=sshInfo.password)
      if(command[:3]=='ovs'): command= 'sudo '+command
      stin, out, err = ssh.exec_command(command)
      print '[exec_ssh_command (in)] %s'%(command)
      print '[exec_ssh_command (out)] %s'%(out.read())
      if(err.read()): print '[exec_ssh_command (error)] %s'%(err.read())
      ssh.close()



'''def create_gre_tunnel(sshInfo, bride, dst_ip)
    #stin, out, err = ssh.exec_command('sudo ovs-vsctl add-port s1 s1-gre -- set interface s1-gre type=ipsec_gre options:remote_ip=192.168.56.101 options:psk=hello')
    #ssh.exec_command('sudo ovs-ofctl add-flow s1 in_port=2,actions=output:1')
    #ssh.exec_command('sudo ovs-ofctl add-flow s1 in_port=1,actions=output:2')'''

  '''
  def createflow(name, in_port, output):
       
        msg = of.ofp_flow_mod()
        msg.hard_timeout=5
        msg.match = of.ofp_match(in_port = 2)

        msg.actions.append(of.ofp_action_output(port = 1))
        #msg.actions.append(of.ofp_action_vlan_vid(vlan_vid=2))
        connection.send(msg)
      msg = of.ofp_flow_mod()
      my_match = of.ofp_match(in_port = 1 , dl_dst= EthAddr("00:00:00:00:00:22"))
      #my_match.nw_dst="10.0.0.0/24"
      msg.match= my_match
      msg.actions.append(of.ofp_action_output(port = 2))
      event.connection.send(msg)
        msg = of.ofp_flow_mod()
        my_match = of.ofp_match(in_port = 1 , dl_dst= EthAddr("00:00:00:00:00:22"))
        #my_match.nw_dst="10.0.0.0/24"
        msg.match= my_match
        msg.actions.append(of.ofp_action_output(port = 2))
        connection.send(msg)
'''
     
# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

def

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
    print 'handle packet in '
   
     #Just for reference 
  def _handle_PacketIn2 (self, event):
    """
    #Handle packet in messages from the switch to implement above algorithm.
    """
    
    packet = event.parsed

    def flood (message = None):
      """ #Floods the packet 
      """
      
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:
        # Only flood if we've been connected for a little while...

        if self.hold_down_expired is False:
          # Oh yes it is!
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)
        #log.debug("%i: flood %s -> %s", event.dpid,packet.src,packet.dst)
        # OFPP_FLOOD is optional; on some switches you may need to change
        # this to OFPP_ALL.
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass
        #log.info("Holding down flood for %s", dpid_to_str(event.dpid))
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    def drop (duration = None):
      """
      #Drops this packet and optionally installs a flow to continue
      #dropping similar ones for a while
      """
     
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    self.macToPort[packet.src] = event.port # 1

    if not self.transparent: # 2
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop() # 2a
        return

    if packet.dst.is_multicast:
      flood() # 3a
    else:
      if packet.dst not in self.macToPort: # 4
        flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a
      else:
        port = self.macToPort[packet.dst]
        if port == event.port: # 5
          # 5a
          log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        # 6
        log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port = port))
        msg.data = event.ofp # 6a
        self.connection.send(msg)
        


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
    #display_attr(event.source)






def launch (transparent=False, hold_down=_flood_delay):
  """
  Starts an L2 learning switch.
  """
  
  #print 'Output'
  #print stin
  #print out
  #print err

  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")
  print 'running core'
  core.registerNew(l2_learning, str_to_bool(transparent))


