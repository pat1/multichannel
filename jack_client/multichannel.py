#!/usr/bin/env python3

"""Create a JACK client that copies input audio directly to the outputs.

This is somewhat modeled after the "thru_client.c" example of JACK 2:
http://github.com/jackaudio/jack2/blob/master/example-clients/thru_client.c

If you have a microphone and loudspeakers connected, this might cause an
acoustical feedback!

"""
import sys
import os
import jack
import threading
import queue
import binascii

###################################
NUMCHANNEL=3
clientname="multichannel"
servername=None

#rcf-3
SYSTEMPLAYBACK1='system:playback_1'
SYSTEMPLAYBACK2='system:playback_2'

SYSTEMCAPTURE1='system:capture_1'
SYSTEMCAPTURE2='system:capture_2'

#other sites
#SYSTEMPLAYBACK1='Audio interno Stereo analogico:playback_FL'
#SYSTEMPLAYBACK2='Audio interno Stereo analogico:playback_FR'
#
#SYSTEMCAPTURE1='Audio interno Stereo analogico:capture_FL'
#SYSTEMCAPTURE2='Audio interno Stereo analogico:capture_FR'


##################################

NUMTRACK=NUMCHANNEL*2
idmix1=NUMTRACK
idmix2=NUMTRACK+1

dab_left_ports=(
    'daber:left'
    ,'dablo:left'
    ,'dabto:left'
)
dab_right_ports=(
    'daber:right'
    ,'dablo:right'
    ,'dabto:right'
)

dab_ports=[]
for i in range(NUMCHANNEL):
    dab_ports.append(dab_left_ports[i])
    dab_ports.append(dab_right_ports[i])

client = jack.Client(clientname, servername=servername)

if client.status.server_started:
    print('JACK server started')
if client.status.name_not_unique:
    print(f'unique name {client.name!r} assigned')
    sys.exit("multichannel is a already running ?")
    
#event = threading.Event()
shutdown_request=False
q = queue.Queue()

@jack.set_error_function
def error(msg):
    print('Error:', msg)

@jack.set_info_function
def info(msg):
    print('Info:', msg)

#@client.set_client_registration_callback
#def client_registration(name, register):
    #print('client', repr(name), ['unregistered', 'registered'][register])

    #capture = client.get_ports( is_output=True)
    #if not capture:
    #    print('No capture ports')

    #for src, dest in zip(capture, client.inports):
    #    client.connect(src, dest)


@client.set_port_registration_callback
def port_registration(port, register):
    #print(repr(port), ['unregistered', 'registered'][register])
    if (register):
        if (port.name[:3]=="dab"):
            message={"action":"dab","port":port}            
            q.put(message)
        if(port.name[:9] == "autoradio"):
            message={"action":"channel","port":port}
            q.put(message)
        #if(port.name[:17] == "Midi-Bridge:WEMOS"):
        if(port.name[:3] == "a2j"):
            message={"action":"midi","port":port}
            q.put(message)
            
        #event.set()
            
@client.set_process_callback
def process(frames):
    assert len(client.inports) == len(client.outports)
    assert frames == client.blocksize
    for i, o in zip(client.inports, client.outports):
        o.get_buffer()[:] = i.get_buffer()

    for offset, data in midi_port.incoming_midi_events():
        #print('{}: 0x{}'.format(client.last_frame_time + offset,
        #                          binascii.hexlify(data).decode()))
        #print(int.from_bytes(data))

        try:
            out_midi_port.clear_buffer()
            out_midi_port.write_midi_event(offset, data)
        except:
            print ("error sending midi message")
        
        if (int.from_bytes(data) == 11538432):
            message={"action":"switch","multichannel":False}
        elif(int.from_bytes(data) == 11538559):
            message={"action":"switch","multichannel":True}

        q.put(message)

        #Pobbiamo gestire dalla bottoniera:
        # bottone 1
        # 0xb01000
        # 0xb0107f
    
        # bottone 2
        # 0xb11000
        # 0xb1107f

        # bottone 3
        # 0xb21000
        # 0xb2107f

        # bottone 4
        # 0xb31000
        # 0xb3107f

@client.set_shutdown_callback
def shutdown(status, reason):
    print('JACK shutdown!')
    print('status:', status)
    print('reason:', reason)
    shutdown_request=True
    #event.set()
    q.put(None)

def connect_monochannel():
    
    # diconnect output channels
    for i in range(NUMTRACK):
        try:
            client.outports[i].disconnect(dab_ports[i])
        except:
            pass
        
    # connect mixer to streams 
    target_ports = client.get_ports(name_pattern='daber:left',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.connect(client.outports[idmix1],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dablo:left',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.connect(client.outports[idmix1],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dabto:left',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.connect(client.outports[idmix1],target_ports[0])
    except:
        pass
    
    target_ports = client.get_ports(name_pattern='daber:right',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.connect(client.outports[idmix2],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dablo:right',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.connect(client.outports[idmix2],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dabto:right',is_input=True, is_audio=True)
    try:
            if(len(target_ports) >0 ): client.connect(client.outports[idmix2],target_ports[0])
    except:
        pass


def connect_multichannel():

    # diconnect output mixer
    for dab_left_port in dab_left_ports:
        try:
            client.outports[idmix1].disconnect(dab_left_port)
        except:
            pass

    for dab_right_port in dab_right_ports:
        try:
            client.outports[idmix2].disconnect(dab_right_port)
        except:
            pass

    # disconnect streams from mixer
    target_ports = client.get_ports(name_pattern='daber:left',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.disconnect(client.outports[idmix1],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dablo:left',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.disconnect(client.outports[idmix1],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dabto:left',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.disconnect(client.outports[idmix1],target_ports[0])
    except:
        pass
    
    target_ports = client.get_ports(name_pattern='daber:right',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.disconnect(client.outports[idmix2],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dablo:right',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.disconnect(client.outports[idmix2],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern='dabto:right',is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0 ): client.disconnect(client.outports[idmix2],target_ports[0])
    except:
        pass

    # connect channels to streams
    target_ports = client.get_ports(name_pattern='daber:left',is_input=True, is_audio=True)
    if(len(target_ports) >0): client.connect(client.outports[0],target_ports[0])
    target_ports = client.get_ports(name_pattern='daber:right',is_input=True, is_audio=True)
    if(len(target_ports) >0): client.connect(client.outports[1],target_ports[0])
    
    target_ports = client.get_ports(name_pattern='dablo:left',is_input=True, is_audio=True)
    if(len(target_ports) >0): client.connect(client.outports[2],target_ports[0])
    target_ports = client.get_ports(name_pattern='dablo:right',is_input=True, is_audio=True)
    if(len(target_ports) >0): client.connect(client.outports[3],target_ports[0])
    
    target_ports = client.get_ports(name_pattern='dabto:left',is_input=True, is_audio=True)
    if(len(target_ports) >0): client.connect(client.outports[4],target_ports[0])
    target_ports = client.get_ports(name_pattern='dabto:right',is_input=True, is_audio=True)
    if(len(target_ports) >0): client.connect(client.outports[5],target_ports[0])


#def connect(port):
#    source_ports = client.get_ports(name_pattern='autoradio:out_*',is_output=True, is_audio=True)    
#    numports=len(source_ports)
#    print("num source ports:",numports)
#
#    #due canali
#    if (numports == 1 or numports == 2):
#
#
#    #sette canali
#    if (numports == 6):

        
def connectmixer():
    target_ports = client.get_ports(name_pattern=SYSTEMPLAYBACK1,is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0): client.connect(client.outports[0],target_ports[0])
    except:
        pass
    target_ports = client.get_ports(name_pattern=SYSTEMPLAYBACK2,is_input=True, is_audio=True)
    try:
        if(len(target_ports) >0): client.connect(client.outports[1],target_ports[0])
    except:
        pass

    source_ports = client.get_ports(name_pattern=SYSTEMCAPTURE1,is_output=True, is_audio=True)
    try:
        if(len(source_ports) >0): client.connect(source_ports[0],client.inports[idmix1])
    except:
        pass
    source_ports = client.get_ports(name_pattern=SYSTEMCAPTURE2,is_output=True, is_audio=True)
    try:
        if(len(source_ports) >0): client.connect(source_ports[0],client.inports[idmix2])
    except:
        pass


def connectmidi():
    #source_ports = client.get_ports(name_pattern='Midi-Bridge:WEMOS*',is_output=True, is_midi=True)
    source_ports = client.get_ports(name_pattern='a2j:WEMOS*',is_output=True, is_midi=True)
    try:
        client.connect(source_ports[0],client.midi_inports[0])
    except:
        pass
    
    target_ports = client.get_ports(name_pattern='a2j:WEMOS*',is_input=True, is_midi=True)
    try:
        client.connect(client.midi_outports[0],target_ports[0])
    except:
        pass


    
midi_port=client.midi_inports.register('input')
out_midi_port = client.midi_outports.register('output')
                    
# create channels ports
for number in range(1,NUMTRACK+1,1):
    client.inports.register(f'cinput_{number}')
    client.outports.register(f'coutput_{number}')

# create mixer in/out ports
for number in (1,2):
    client.inports.register(f'mixerin_{number}')
    client.outports.register(f'mixerout_{number}')


class multichannel_status():
    def __init__(self,midiconnect=False, dabconnect=False,
                 switch_multichannel=False, autoradio_multichannel=False, multichannel_status=False):

        self.midiconnect=midiconnect
        self.dabconnect=dabconnect
        self.switch_multichannel=switch_multichannel
        self.autoradio_multichannel=autoradio_multichannel
        self.multichannel_status=multichannel_status

        
    def elaborate(self,message):
        
        if (message["action"] == "midi"):
            self.midiconnect=True
        
        elif (message["action"] == "switch"):
            self.switch_multichannel=message["multichannel"]    
        elif (message["action"] == "dab" ):
            self.dabconnect=True
            
        elif (message["action"] == "channel"):
            source_ports = client.get_ports(name_pattern='autoradio:out_*',is_output=True, is_audio=True)
            numports=len(source_ports)
            #print("num source ports:",numports)
            if (numports <= 2):
                #zero , uno o due canali
                self.autoradio_multichannel = False
            elif (numports >= 6):
                #sei canali
                self.autoradio_multichannel = True 

    
with client:
    # When entering this with-statement, client.activate() is called.
    # This tells the JACK server that we are ready to roll.
    # Our process() callback will start running now.

    # Connect the ports.  You can't do this before the client is activated,
    # because we can't make connections to clients that aren't running.
    # Note the confusing (but necessary) orientation of the driver backend
    # ports: playback ports are "input" to the backend, and capture ports
    # are "output" from it.

    #capture = client.get_ports(is_physical=True, is_output=True)
    #if not capture:
    #    raise RuntimeError('No physical capture ports')

    #for src, dest in zip(capture, client.inports):
    #    client.connect(src, dest)

    #playback = client.get_ports(is_physical=True, is_input=True)
    #if not playback:
    #    raise RuntimeError('No physical playback ports')

    #for src, dest in zip(client.outports, playback):
    #    client.connect(src, dest)

    connect_monochannel()
    connectmidi()
    connectmixer()
    
    print('Press Ctrl+C to stop')
    multichannel = False
    try:


        status=multichannel_status()
                        
        while (True):
            #event.wait()
            message = q.get()
            if (shutdown_request):
                break
            print(message)
            status.elaborate(message)

            while (not q.empty()):
                message = q.get()
                if (shutdown_request):
                    break
                print(message)
                status.elaborate(message)

            #print(message,status.midiconnect, status.dabconnect, status.switch_multichannel,
            #      status.autoradio_multichannel, status.multichannel_status)
                
            if (status.midiconnect):
                connectmidi()
                status.midiconnect=False

            multichannel = status.switch_multichannel and status.autoradio_multichannel
            
            if ((multichannel != status.multichannel_status) or status.dabconnect):
                if (multichannel):
                    connect_multichannel()
                    connectmixer()
                else:
                    connect_monochannel()
                    connectmixer()
                    
                status.multichannel_status=multichannel
                status.dabconnect=False
            
    except KeyboardInterrupt:
        print('\nInterrupted by user')

# When the above with-statement is left (either because the end of the
# code block is reached, or because an exception was raised inside),
# client.deactivate() and client.close() are called automatically.
