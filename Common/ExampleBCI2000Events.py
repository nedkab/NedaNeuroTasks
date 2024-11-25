import socket
import time

host = 'localhost'
port = 3999


def connectAndRunCommand(cmd: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.)
        s.connect((host, port))
        s.sendall(f'{cmd}\n'.encode('ascii'))
        # first result printed is just standard BCI200 prompt regardless of command
        resp = s.recv(1024).decode()
        time.sleep(0.1)
        # second response is result of command, with extra command prompt '>' afterwards
        resp = s.recv(4096).decode().strip()
        if resp.endswith('>'):
            resp = resp[:-1].strip()
        if len(resp) > 0:
            print(resp)
        
        return resp

def initialize():
    """
    BCI2000 events must be added (declared) before system startup
    """
    connectAndRunCommand('Add event PsychoPy 8 0')

def assertEventExists():
    """
    Make sure that an event was initialized correctly
    """
    resp = connectAndRunCommand('exists event psychopy')
    assert resp=='true'

def triggerEvent():
    """
    As a simple test, do socket connection and triggering together here.
    
    But in actual use, will want to pre-connect socket to improve timing 
    precision of the actual trigger event.
    """
    resp = connectAndRunCommand('Pulse event psychopy 1')
    assert len(resp) == 0
        


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test BCI2000 triggering')
    parser.add_argument('action')
    args = parser.parse_args()
    
    if args.action == 'initialize':
        initialize()
        
    elif args.action == 'assertEventExists':
        assertEventExists()
        
    elif args.action == 'trigger':
        triggerEvent()
        
    else:
        # e.g. 'start', 'stop',...
        connectAndRunCommand(args.action)
    
    
    

