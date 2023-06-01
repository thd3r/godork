<h1 align="center">
  Godork - Scrape Google search quickly
</h1>

<h1 align="center">
  <img src="static/godork-logo.png" alt="godork" width="250px">
  <br>
</h1>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Built%20with-Python-Blue"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
  <a href="https://github.com/thd3r/godork/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation-instructions">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#running-godork">Running godork</a> •
  <a href="#notes">Notes</a> • 
  <a href="https://github.com/thd3r">Follow me</a>
</p>

`godork` can scrape results from google searches quickly by using the [asyncio](https://docs.python.org/3/library/asyncio.html) library which uses **cooperative multitasking** in combination with [aiohttp](https://docs.aiohttp.org)

# Features

<h1 align="center">
  <img src="https://raw.githubusercontent.com/thd3r/godork/main/static/godork-run.png" alt="godork" width="700px">
  <br>
</h1>

 - Simple and modular code base making it easy to contribute.
 - Fast scanner
 - Scrape Google search titles and links quickly

# Installation Instructions

`godork` requires **python 3.8** or higher to install successfully. Run the following command to get the repo:

```sh
git clone https://github.com/thd3r/godork.git && python3 -m pip install -r requirements.txt
```

# Usage

```sh
python3 godork.py -h
```

This will display help for the tool. Here are all the switches it supports.

```console
                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r


usage: godork.py [ --query [default arguments] ] [ arguments ]

scrape Google search quickly

Options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        search query
  -p PAGE, --page PAGE  specify number of pages
  --hl HL               language
  --gl GL               country of the search
  -o OUTPUT, --output OUTPUT
                        write output in JSONL(ines) format  
```

# Running godork

### Scrape

It will run its tool to scrape titles and links from google search

```console
python3 godork.py --query "site:*.gov"

                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r


[INF] Engine  : Google
[INF] Query   : site:*.gov
[INF] Page    : 1

[WRN] Returns None if your IP address has been blocked by a search engine provider or some other reason.
[INF] Enumerating now for site:*.gov querys

Florida Board of Nursing - Licensing, Renewals & Information [https://floridasnursing.gov/]
SAM.gov | Home [https://sam.gov/]
Miami-Dade County Clerk of the Courts [https://www.miamidadeclerk.gov/]
Nevada Secretary of State | Home [https://www.nvsos.gov/]
National Science Foundation: NSF [https://www.nsf.gov/]
U.S. Bureau of Labor Statistics [https://www.bls.gov/]
Federal Aviation Administration [https://www.faa.gov/]
Cook County Government, Illinois | Cook County [https://www.cookcountyil.gov/]
Georgia Department of Agriculture: Homepage [https://agr.georgia.gov/]
Home | The Thrift Savings Plan (TSP) [https://www.tsp.gov/]

[INF] Saving results to file godork-2023-06-01-18:12:59.json
[INF] Found 10 links for site:*.gov querys in 1 seconds
```

# Specify Pages

```console
python3 godork.py --query "site:*.gov" --page 3

                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r


[INF] Engine  : Google
[INF] Query   : site:*.gov
[INF] Page    : 3

[WRN] Returns None if your IP address has been blocked by a search engine provider or some other reason.
[INF] Enumerating now for site:*.gov querys

Florida Board of Nursing - Licensing, Renewals & Information [https://floridasnursing.gov/]
SAM.gov | Home [https://sam.gov/]
Miami-Dade County Clerk of the Courts [https://www.miamidadeclerk.gov/]
Nevada Secretary of State | Home [https://www.nvsos.gov/]
National Science Foundation: NSF [https://www.nsf.gov/]
U.S. Bureau of Labor Statistics [https://www.bls.gov/]
Federal Aviation Administration [https://www.faa.gov/]
Cook County Government, Illinois | Cook County [https://www.cookcountyil.gov/]
Georgia Department of Agriculture: Homepage [https://agr.georgia.gov/]
Home | The Thrift Savings Plan (TSP) [https://www.tsp.gov/]
Census Bureau [https://www.census.gov/]
U.S. Embassy in Israel [https://il.usembassy.gov/]
TLO [https://capitol.texas.gov/]
Internal Revenue Service | An official website of the United States ... [https://www.irs.gov/]
Wisconsin Department of Workforce Development [https://dwd.wisconsin.gov/]
Georgia Department of Public Health [https://dph.georgia.gov/]
Home Page - Arkansas Governor - Sarah Huckabee Sanders [https://governor.arkansas.gov/]
Illinois.gov - IL Application for Benefits Eligibility (ABE) ABE Home ... [https://abe.illinois.gov/]
City of Bend | Home [https://www.bendoregon.gov/]
Colorado Secretary of State [https://www.coloradosos.gov/]
ILCC [https://ilcc.illinois.gov/]
SSA: The United States Social Security Administration [https://www.ssa.gov/]
Colorado PEAK: Log-In or Apply for Benefits [https://co.gov/PEAK]
Recreation.gov - Camping, Cabins, RVs, Permits, Passes & More [https://www.recreation.gov/]
Washington State's Paid Family and Medical Leave – Washington ... [https://paidleave.wa.gov/]
Search - SAM.gov [https://sam.gov/search/]
U.S. Embassy & Consulates in Japan: Homepage [https://jp.usembassy.gov/]
Stop Bullying.gov [https://www.stopbullying.gov/]
Department of Housing and Community Development [https://dhcd.maryland.gov/]
Arizona Department of Real Estate | [https://azre.gov/]

[INF] Saving results to file godork-2023-06-01-18:15:36.json
[INF] Found 30 links for site:*.gov querys in 2 seconds
```

# Specify Language

```console
python3 godork.py --query "site:*.gov" --page 3 --hl en

                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r


[INF] Engine  : Google
[INF] Query   : site:*.gov
[INF] Page    : 3

[WRN] Returns None if your IP address has been blocked by a search engine provider or some other reason.
[INF] Enumerating now for site:*.gov querys

Florida Board of Nursing - Licensing, Renewals & Information [https://floridasnursing.gov/]
SAM.gov | Home [https://sam.gov/]
Miami-Dade County Clerk of the Courts [https://www.miamidadeclerk.gov/]
Nevada Secretary of State | Home [https://www.nvsos.gov/]
National Science Foundation: NSF [https://www.nsf.gov/]
U.S. Bureau of Labor Statistics [https://www.bls.gov/]
Federal Aviation Administration [https://www.faa.gov/]
Cook County Government, Illinois | Cook County [https://www.cookcountyil.gov/]
Georgia Department of Agriculture: Homepage [https://agr.georgia.gov/]
Home | The Thrift Savings Plan (TSP) [https://www.tsp.gov/]
Census Bureau [https://www.census.gov/]
U.S. Embassy in Israel [https://il.usembassy.gov/]
TLO [https://capitol.texas.gov/]
Internal Revenue Service | An official website of the United States ... [https://www.irs.gov/]
Wisconsin Department of Workforce Development [https://dwd.wisconsin.gov/]
Georgia Department of Public Health [https://dph.georgia.gov/]
Home Page - Arkansas Governor - Sarah Huckabee Sanders [https://governor.arkansas.gov/]
Illinois.gov - IL Application for Benefits Eligibility (ABE) ABE Home ... [https://abe.illinois.gov/]
City of Bend | Home [https://www.bendoregon.gov/]
Colorado Secretary of State [https://www.coloradosos.gov/]
ILCC [https://ilcc.illinois.gov/]
SSA: The United States Social Security Administration [https://www.ssa.gov/]
Colorado PEAK: Log-In or Apply for Benefits [https://co.gov/PEAK]
Recreation.gov - Camping, Cabins, RVs, Permits, Passes & More [https://www.recreation.gov/]
Washington State's Paid Family and Medical Leave – Washington ... [https://paidleave.wa.gov/]
Search - SAM.gov [https://sam.gov/search/]
U.S. Embassy & Consulates in Japan: Homepage [https://jp.usembassy.gov/]
Stop Bullying.gov [https://www.stopbullying.gov/]
Department of Housing and Community Development [https://dhcd.maryland.gov/]
Arizona Department of Real Estate | [https://azre.gov/]

[INF] Saving results to file godork-2023-06-01-18:15:36.json
[INF] Found 30 links for site:*.gov querys in 2 seconds
```

# Specify Country of The Search

```console
python3 godork.py --query "site:*.gov" --page 3 --gl uk

                __         __  
  ___ ____  ___/ /__  ____/ /__
 / _ `/ _ \/ _  / _ \/ __/  '_/
 \_, /\___/\_,_/\___/_/ /_/\_\ 
/___/                                                                                                            
        v1.0.0 - @thd3r


[INF] Engine  : Google
[INF] Query   : site:*.gov
[INF] Page    : 3

[WRN] Returns None if your IP address has been blocked by a search engine provider or some other reason.
[INF] Enumerating now for site:*.gov querys

Florida Board of Nursing - Licensing, Renewals & Information [https://floridasnursing.gov/]
SAM.gov | Home [https://sam.gov/]
Miami-Dade County Clerk of the Courts [https://www.miamidadeclerk.gov/]
Nevada Secretary of State | Home [https://www.nvsos.gov/]
National Science Foundation: NSF [https://www.nsf.gov/]
U.S. Bureau of Labor Statistics [https://www.bls.gov/]
Federal Aviation Administration [https://www.faa.gov/]
Cook County Government, Illinois | Cook County [https://www.cookcountyil.gov/]
Georgia Department of Agriculture: Homepage [https://agr.georgia.gov/]
Home | The Thrift Savings Plan (TSP) [https://www.tsp.gov/]
Census Bureau [https://www.census.gov/]
U.S. Embassy in Israel [https://il.usembassy.gov/]
TLO [https://capitol.texas.gov/]
Internal Revenue Service | An official website of the United States ... [https://www.irs.gov/]
Wisconsin Department of Workforce Development [https://dwd.wisconsin.gov/]
Georgia Department of Public Health [https://dph.georgia.gov/]
Home Page - Arkansas Governor - Sarah Huckabee Sanders [https://governor.arkansas.gov/]
Illinois.gov - IL Application for Benefits Eligibility (ABE) ABE Home ... [https://abe.illinois.gov/]
City of Bend | Home [https://www.bendoregon.gov/]
Colorado Secretary of State [https://www.coloradosos.gov/]
ILCC [https://ilcc.illinois.gov/]
SSA: The United States Social Security Administration [https://www.ssa.gov/]
Colorado PEAK: Log-In or Apply for Benefits [https://co.gov/PEAK]
Recreation.gov - Camping, Cabins, RVs, Permits, Passes & More [https://www.recreation.gov/]
Washington State's Paid Family and Medical Leave – Washington ... [https://paidleave.wa.gov/]
Search - SAM.gov [https://sam.gov/search/]
U.S. Embassy & Consulates in Japan: Homepage [https://jp.usembassy.gov/]
Stop Bullying.gov [https://www.stopbullying.gov/]
Department of Housing and Community Development [https://dhcd.maryland.gov/]
Arizona Department of Real Estate | [https://azre.gov/]

[INF] Saving results to file godork-2023-06-01-18:15:36.json
[INF] Found 30 links for site:*.gov querys in 2 seconds
```

# Notes

**`godork` can't handle your IP address which has been blocked by search engine provider or other reasons.**
