import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime
import signal
import dns.resolver
import csv
import time
import sys


# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("end of time")


signal.signal(signal.SIGALRM, handler)


def convert_to_YYYY_MM_DD(date_time_str) -> str:
    """
    Converts a date and time string to the format YYYY/MM/DD.

    Args:
        date_time_str: The date and time string to convert.

    Returns:
        The converted date and time string in YYYY/MM/DD format, or None if the input string
        cannot be parsed.
    """

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
    """
    Retrieves the certificate details for a given URL.

    Args:
        url: The URL of the website.

    Returns:
        A dictionary containing the certificate details, or an error message if an error occurs.
    """

    try:
        # Ensure the URL starts with "https://"
        url = "https://" + url if not url.startswith("https://") else url
        #print(url)

        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=2) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return cert
    except dns.resolver.NXDOMAIN:
        return "Error# DNS resolution failed"
    except socket.gaierror:
        return "Error# DNS resolution failed"
    except socket.timeout:
        return "Error# Timeout occurred"
    except Exception as e:
        return f"Error# {e}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python inspect_domain.py list_of_domain.csv")
        sys.exit(1)
        
    file_name = sys.argv[1]    

    with open(file_name, "r", newline="") as csv1, open(
        "/tmp/info.csv", "w", newline=""
    ) as csv2:
        reader = csv.reader(csv1)
        writer = csv.writer(csv2)

        for row in reader:
            #print(row)
            website_url = row[1]
            cert_details = get_certificate_details(website_url)

            if isinstance(cert_details, dict):
                not_after_date = convert_to_YYYY_MM_DD(cert_details["notAfter"])
                issuer_organization = cert_details["issuer"][1][0][1]
                writer.writerow([not_after_date, issuer_organization])
                print(f"{website_url}, {not_after_date}, {issuer_organization}")
            else:
                print(cert_details)
