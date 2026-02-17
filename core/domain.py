import dns.resolver
from dns.exception import DNSException


def domain_has_mx(domain: str) -> bool:
    if not domain:
        return False
    try:
        dns.resolver.resolve(domain, "MX", lifetime=5.0)
        return True
    except DNSException:
        return False
