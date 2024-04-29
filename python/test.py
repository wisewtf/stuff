import requests
import argparse

def main(type, query):
    servers_url = "https://www.whatsmydns.net/api/servers"
    
    try:
        servers_response = requests.get(servers_url)
        servers_response.raise_for_status()
        servers = servers_response.json()

        output = "Query results:\n\n"
        
        for server in servers:
            server_id = server['id']
            location = server['location']
            details_url = f"https://www.whatsmydns.net/api/details?server={server_id}&type={type}&query={query}"
            
            print(server_id)

            details_response = requests.get(details_url)
            details_response.raise_for_status()
            details_data = details_response.json()

            responses = [entry['response'] for entry in details_data['data']]
            responses_flat = ', '.join([resp for sublist in responses for resp in sublist])
            
            output += f"Country: {location}\n"
            output += f"Results: {responses_flat}\n"
            output += "----------\n"
        
        print(output)
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch DNS records for specified domain and record type")
    parser.add_argument('-t', '--type', type=str, help='Type of DNS record', required=True)
    parser.add_argument('-q', '--query', type=str, help='The DNS query domain', required=True)
    
    args = parser.parse_args()
    
    main(args.type, args.query)
