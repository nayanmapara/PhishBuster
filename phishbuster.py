from urllib.parse import urlparse
import re
import tldextract
import requests

def url_syntax(url_changes):
    url_search_http = re.search("http", url_changes) # finds if there is http in url using regular expressions
    if url_search_http is None:
        url_http = "http://" + url_changes # adds http:// if not there in the url
    else:
        url_http = url_changes # returns the input url
    return url_http # Returns the url with 'http://'

def subdomain_re(domain_url):
    sub_addr = tldextract.extract(domain_url).subdomain # removing sub domain from the url
    if sub_addr is not None:  
        extract_domain = tldextract.extract(domain_url).domain # returns domain
        extract_ext = tldextract.extract(domain_url).suffix # returns domain extention
        filtered_sub = extract_domain + '.' + extract_ext # combines domain and the extention
    else:
        filtered_sub = domain_url # returning input if no sub domain is found
    return filtered_sub # Removes subdomain and returns the value

def unshorten_url(url): # unshortens the url
    try:
        session = requests.Session()  # so connections are recycled
        unshort_url = session.head(url, allow_redirects=True) # send a head request to the url
        return unshort_url.url # return the final url
    except:
        return url # returns url when the website is offline

def phishbuster_url(url_input): # removes ~@ (which are used for disgusing the url) and path
    corrected_url = url_syntax(url_input) # removing path and hinding characters from the url
    unshorten_url_input = unshorten_url(corrected_url) # unshortening the url
    url_search = re.search("~@", unshorten_url_input) # Finding the hiding characters using regular expressions
    if url_search is not None:
        domain = urlparse(unshorten_url_input).netloc # removing https:// and path from the url
        remove_to_hide_element = re.split("~@", domain) # removing hiding character from the url 
        domain_url = remove_to_hide_element[1]
    else:
        domain = urlparse(unshorten_url_input).netloc # removing https:// and path from the url
        domain_url = domain
    return domain_url # returns a domain name eg. google.com / with sub domain www.google.com

def comparing_url(url_phish,url_org,country):
    input_url = phishbuster_url(url_phish) # removing path and hinding characters from the url
    final_url = subdomain_re(input_url) # removing sub domain from the url
    regional = tldextract.extract(url_org).domain +'.'+ country.lower() # adding country to the url
    if final_url == url_org or final_url == regional:
        output_comparison = bool(False) # Returns False for non-phishing sites
    else:
        output_comparison = bool(True) # Returns True for phishing sites
    return output_comparison # Returns 'True' / 'False'
    
if __name__ == "__main__":
    print(comparing_url('input.url','orginal_domain.name','country'))