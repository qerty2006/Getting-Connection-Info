import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
import signal

# Register an handler for the timeout
def handler(signum, frame):
     raise Exception("end of time")
        
signal.signal(signal.SIGALRM, handler) 

def convert_to_YYYY_MM_DD(date_time_str) -> str:
  try:
    # Define the input format with spaces separating elements
    input_format = "%b %d %H:%M:%S %Y %Z"
    # Parse the datetime string
    date_time_obj = datetime.strptime(date_time_str, input_format)
    # Define the desired output format
    output_format = "%Y/%m/%d"
    # Format the datetime object as a string in YYYY/MM/DD
    return date_time_obj.strftime(output_format)
  except ValueError:
    # Handle cases where the string cannot be parsed in the expected format
    return None


def get_certificate_details(url):
    try:
        url = "https://"+url if not url.startswith("https://") else url
        print(url)
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                signal.alarm(1)
                cert = ssock.getpeercert()
                return cert
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
  import csv
  with open('top-1m.csv', "r", newline='') as csv1, open('info.csv', "w", newline='') as csv2:
      reader = csv.reader(csv1)
      writer = csv.writer(csv2)

      for row in reader:
          print(row)
          website_url = row[1]
          cert_details = get_certificate_details(website_url)
          if  isinstance(cert_details, dict):
              writer.writerow([convert_to_YYYY_MM_DD(cert_details["notAfter"]), cert_details["issuer"][1][0][1]])
              print(convert_to_YYYY_MM_DD(cert_details["notAfter"])+",",cert_details["issuer"][1][0][1])
          else:
            print(cert_details)
          

