
import socket, os, time, errno
import jsonrpclib

def wait_server(server, port):
    
    print("Wait for %s... " % server)

    sock = socket.socket()
    
    while True:
        
        try:
            
            sock.connect((server, port))
        
        except:

            time.sleep(1)
            
        else:
            
            sock.close()
            break

    print("success")

    return True

def wait_coin(host):

    print("Wait for %s..." % host)

    while True:

        try:
            
            rpc = jsonrpclib.ServerProxy(host)
            rpc.getwalletinfo()

            break

        except (ConnectionRefusedError, ConnectionResetError, jsonrpclib.jsonrpc.ProtocolError):

            time.sleep(1)

    print("success")

    return True

wait_server("db", 5432)

wait_coin("http://test:test@bitcoin:18332")
wait_coin("http://test:test@litecoin:19332")
wait_coin("http://test:test@dash:19994")

os.system("python3 manage.py makemigrations")
os.system("python3 manage.py makemigrations coin pool device")
os.system("python3 manage.py migrate")
os.system("python3 manage.py release")
os.system("python3 manage.py create_debug_dataset")

pidfile = "/tmp/celerybeat.pid"

try:

    os.remove(pidfile)
    
except FileNotFoundError:
    
    pass

os.system("celery worker -A coin -D --pidfile=%s" % pidfile)

