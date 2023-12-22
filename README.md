# SolarEdge API

This is a package for connecting to the SolarEdge API. It has been tested on Inverter data only.

## Usage

```python
import solaredge

def main():
    with  SolaredgeClient(apikey='solaredge_apikey') as client:
        for site in client.get_sites():
            pprint.pprint(site)

run(main())
```

The sample programs use a .env file with the serial and password contained in it

```text
solaredge_apikey = "1234567abcedf"
```
