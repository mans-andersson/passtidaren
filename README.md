# README

***Confirmed to be working 2022-03-29***

***Warning: You are responsible for any trouble you may run into using this script***

This script can be used to book a time slot to get a Swedish passport.
It will repeatedly scan and try to book a time that fits your chosen criteria.

### Dependencies
You need Chromedriver installed. Download and unzip from [here](https://chromedriver.chromium.org/downloads). 
Make sure chromedriver binary is available in PATH, for example by moving it to `/usr/local/bin`.

Make sure Python package selenium is installed by running `pip install selenium`.

## Usage
Example usage: `python3 passtid.py --url=https://bokapass.nemoq.se/Booking/Booking/Index/stockholm --email=namn@example.com --phone=0701234567 --name="Kalle Anka" --locations="Sthlm City,Globen,Solna" --months=mar,apr,maj`

These are the required flags:

- `--url=` Lets you specify the region to start from. Get links to all available regions [here](https://polisen.se/tjanster-tillstand/pass-och-nationellt-id-kort/boka-tid-hitta-passexpedition).

- `--email=` Specify your email.

- `--phone=` Specify your phone numer.

- `--name=` Specify your full name within quotation marks.

- `--locations=` Comma separated list of locations where you are interested in a time slot. Has to be within your chosen district (your district depends on chosen url).

- `--months=` Comma separated list of the months where you are interested in getting a time slot (three letter version).

Get more info by runninng `python3 passtid.py --help`.