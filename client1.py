import xmlrpc.client
import sys

# Default port for the master server
DEFAULT_PORT = 8800 

def main():
    # Use the provided port if given, otherwise default to 8800
    master_port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    server_url = f"http://localhost:{master_port}/"

    try:
        with xmlrpc.client.ServerProxy(server_url) as proxy:
            # Query by name
            name = 'xander'
            print(f'Client => Asking for person with name: {name}')
            result = proxy.getbyname(name)
            print(result)

            # Query by location
            location = 'Kansas City'
            print(f'Client => Asking for person who lived at: {location}')
            result = proxy.getbylocation(location)
            print(result)

            # Query by location and year
            location = 'New York City'
            year = 2002
            print(f'Client => Asking for person who lived in {location} in {year}')
            result = proxy.getbyyear(location, year)
            print(result)

    except ConnectionRefusedError:
        print(f"Error: Could not connect to master server at {server_url}. Is the server running?")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
