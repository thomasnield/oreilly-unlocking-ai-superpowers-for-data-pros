# This is fixed, but I had this issue and forgot
# how to update certificates to download files in Python.
# I got this error:
# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)>
# Let's ask AI how to fix it

import pandas as pd

url = r"https://www.ncei.noaa.gov/stormevents/csv?eventType=%28C%29+Tornado&beginDate_mm=05&beginDate_dd=01&beginDate_yyyy=2024&endDate_mm=05&endDate_dd=31&endDate_yyyy=2025&county=ALL&hailfilter=0.00&tornfilter=0&windfilter=000&sort=DT&submitbutton=Search&statefips=48%2CTEXAS"
df = pd.read_csv(url, dtype={"BEGIN_TIME" : str, "END_TIME" : str})
df