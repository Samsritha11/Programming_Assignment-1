from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys

workers = {
    'worker-1': ServerProxy("http://localhost:23001/"),
    'worker-2': ServerProxy("http://localhost:23002/")
}
      
def getbylocation(location):
    """ Forwards location queries to both workers and combines results. """
    result1 = workers["worker-1"].getbylocation(location)
    result2 = workers["worker-2"].getbylocation(location)
    return {"error": False, "result": result1["result"] + result2["result"]}

def getbyname(name):
    """ Forwards name queries to the correct worker. """
    worker = workers["worker-1"] if name[0] < 'n' else workers["worker-2"]
    return worker.getbyname(name)

def getbyyear(location, year):
    """ Forwards location and year queries to both workers and combines results. """
    result1 = workers["worker-1"].getbyyear(location, year)
    result2 = workers["worker-2"].getbyyear(location, year)
    return {"error": False, "result": result1["result"] + result2["result"]}

def main():
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8800
    
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Master server listening on port {port}...")

    server.register_function(getbyname, "getbyname")
    server.register_function(getbylocation, "getbylocation")
    server.register_function(getbyyear, "getbyyear")
    
    server.serve_forever()

if __name__ == "__main__":
    main()
