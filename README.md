# Getting-Connection-Info

**domain_inspect - Probes the domain to understand cert issuer and the expiry**

This simple python script makes an SSL connection to the domain name and checks for the Certificate issuer and Expiry.

**Usage**: python domain_inspect.py list_of_domains.csv
<pre>
$ python3 inspect_domain.py top-10.csv  | grep -v Error
google.com, 2024/08/13, Google Trust Services LLC
www.google.com, 2024/08/13, Google Trust Services LLC
microsoft.com, 2025/05/06, Microsoft Corporation
safebrowsing.googleapis.com, 2024/08/13, Google Trust Services LLC
live.com, 2025/03/10, DigiCert Inc
netflix.com, 2024/10/24, DigiCert Inc
doubleclick.net, 2024/08/13, Google Trust Services LLC
</pre>

