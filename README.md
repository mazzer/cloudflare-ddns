# First steps #

To get the script to work against your Cloudflare account you must change the **tkn** and **email** keys in *api_params*.
The values can be found on the [Account page](https://www.cloudflare.com/my-account).

Setting these two values is the only thing needed before running the script and it will update all A records in all zones that have the same IP set as the root domain (or www subdomain if a root domain is missing).

## Example ##

### Zone example.com ###

* example.com 10.0.0.1
* test.example.com 10.0.0.1
* noupd.example.com 10.1.1.1

**Public IP: 10.0.0.2**

Running the script will update *`example.com`* and *`test.example.com`* to the new public IP. *`noupd.example.com`* will be left as-is because the IP
is not the same as the root domain IP.

### Zone example.org ###

By adding an entry into the *domains* in the settings you can make sure that these domain names are always updated to the public IP, no matter what their current IP address are.


```
#!python

domains = set(['public.example.org'])
```


* example.org 10.0.0.1
* test.example.org 10.0.0.1
* noupd.example.org 10.1.1.1
* public.example.org 11.22.0.1

**Public IP: 10.0.0.2**

Running the script will update *`example.org`* and *`test.example.org`* to the new public IP and also *`public.example.org`*. *`noupd.example.org`* will be left as-is because the IP is not the same as the root domain IP.

### Zone example.net ###


* www.example.org 10.0.0.1
* test.example.org 10.0.0.1
* noupd.example.org 10.1.1.1

**Public IP: 10.0.0.2**

Running the script will update *`www.example.net`* and *`test.example.net`* to the new public IP, because of the IP match from the `www` subdomain.