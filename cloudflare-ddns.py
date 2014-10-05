# !/usr/bin/env python

import json
import urllib
import urllib2

url = 'https://www.cloudflare.com/api_json.html'

api_params = {
    'tkn': 'cloudflare_api_token',
    'email': 'your_cloudflare@email',
}

domains = set(['all', 'subdomain', 'to', 'always', 'keep', 'up-to-date'])


def get_zone_names():
    load_records_data = dict(api_params.items() + {
        'a': 'zone_load_multi',
    }.items())

    response = json.load(urllib2.urlopen(url, data=urllib.urlencode(load_records_data)))
    return [z['zone_name'] for z in response['response']['zones']['objs']]


def get_a_records(domain):
    load_records_data = dict(api_params.items() + {
        'a': 'rec_load_all',
        'z': domain,
    }.items())

    response = json.load(urllib2.urlopen(url, data=urllib.urlencode(load_records_data)))

    return dict((r['name'], r) for r in response['response']['recs']['objs'] if r['type'] == 'A')


def get_current_ip(domain, a_records):
    return a_records.get(domain, {}).get('content') or a_records.get('www.%s' % domain, {}).get('content')


def update_dns_ip(domain, dns_record, new_ip):
    post_data = dict(api_params.items() + {
        'a': 'rec_edit',
        'z': domain,
        'type': 'A',
        'id': dns_record.get('rec_id'),
        'name': dns_record.get('name'),
        'content': new_ip,
        'ttl': dns_record.get('ttl'),
        'service_mode': dns_record.get('service_mode'),
    }.items())

    urllib2.urlopen(url, data=urllib.urlencode(post_data))


public_ip = json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin']
for zone in get_zone_names():
    domain_records = get_a_records(zone)
    curr_zone_ip = get_current_ip(zone, domain_records)

    for subdomain in domain_records.values():
        if subdomain['content'] != public_ip:
            if subdomain['content'] == curr_zone_ip or subdomain['name'] in domains:
                update_dns_ip(zone, subdomain, public_ip)
