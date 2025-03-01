from xmlrpc.server import SimpleXMLRPCServer
import sys
import json

# Storage of data
data_table = {}

def load_data(group):
    """ Load the appropriate JSON file into data_table """
    file_name = "data-am.json" if group == "am" else "data-nz.json"
    try:
        with open(file_name, "r") as file:
            global data_table
            data_table = json.load(file)
        print(f"Loaded data for {group}: {len(data_table)} records")
    except Exception as e:
        print(f"Error loading {file_name}: {e}")


def getbyname(name):
    """ Returns person information matching the "name" """
    return {"error": False, "result": [data_table[name]]} if name in data_table else {"error": True, "result": []}


def getbylocation(location):
    """ Returns people who lived in a specific location """
    results = [record for record in data_table.values() if record["location"] == location]
    return {"error": False, "result": results}


def getbyyear(location, year):
    """ Returns people who lived in a specific location in a specific year """
    results = [record for record in data_table.values() if record["location"] == location and record["year"] == year]
    return {"error": False, "result": results}


def main():
    if len(sys.argv) < 3:
        print("Usage: worker.py <port> <group: am or nz>")
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    load_data(group)
    
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Worker listening on port {port}...")
    
    # Register RPC functions
    server.register_function(getbyname, "getbyname")
    server.register_function(getbylocation, "getbylocation")
    server.register_function(getbyyear, "getbyyear")
    
    server.serve_forever()


if __name__ == "_main_":
    main()
