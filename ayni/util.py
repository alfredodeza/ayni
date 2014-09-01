

def normalize_fqdn(fqdn):
    """
    Ensure some basic normalization on fqdn values
    """
    if not fqdn:
        return None

    if fqdn.endswith('/'):
        fqdn = fqdn.strip('/')

    # bare fqdn, fallback to http://
    if not fqdn.startswith('http'):
        fqdn = "http://%s" % fqdn
    return fqdn
