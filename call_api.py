import requests

def api_call(inurl, seurl,country, store = 'False'):
    '''
    "inurl" is the input url which is suspected to be phishing site.
    "seurl" is the select url in which only the domain name of the orginal site is to be given as in put.
    "country" here is the iso code of the country that is 'in' for 'India' etc.
    '''
    inurl = inurl.lower()
    seurl = seurl.lower()
    country = country.lower()
    # inurl is the input url, seurl is the orginal domain and store is the permission to store data if it is a phishing site
    URL = "http://127.0.0.1:5000/api/"
    data = {'check-url': inurl, 'org-url': seurl, 'country':country, 'save-scan-data':store}
    req = requests.post(url = URL,data=data) # sends a POST request to the PhishBuster API
    return req.json() # Reading data with json

if __name__ == '__main__':
    print(api_call(inurl='suspected-url.com/path',seurl='original.com',country='in',store='True'))

