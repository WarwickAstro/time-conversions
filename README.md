# Time Conversion Tools

Code to convert times used for astronomical observations

# Converting between JD_UTC, MJD_UTC, HJD_UTC and BJD\_TDB

Input values are expected in the following formats:

   1. JD\_UTC
   1. MJD\_UTC
   1. HJD\_UTC
   1. BJD\_TDB

Input timestamps can be from the ```start```, ```mid``` or ```end``` of the exposures.
A mid-point correction is applied first, if required.

After mid-point correction the times are converted to ```JD_UTC_MID```, then the final
conversion to the output format is done.

Outputs are given in the following formats:

   1. JD\_UTC\_MID
   1. MJD\_UTC\_MID
   1. HJD\_UTC\_MID
   1. BJD\_TDB\_MID

The following assumptions are made:

   1. The times to convert are in the first column of the file listed
   1. The output timestamps should be corrected to exposure mid-point

# Usage

```sh
▶ python convert_times.py -h
usage: convert_times.py [-h]
                        input_times {jd,mjd,hjd,bjd} {start,mid,end}
                        {jd,mjd,hjd,bjd} ra dec observatory exptime

positional arguments:
  input_times       file containing list of times to convert
  {jd,mjd,hjd,bjd}  type of time we are converting from
  {start,mid,end}   type of input timestamps we have
  {jd,mjd,hjd,bjd}  type of time we are converting to
  ra                RA of target (HH:MM:SS.ss)
  dec               Dec of target (DD:MM:SS.ss)
  observatory       Observatory where data was taken, e.g. lapalma, paranal
                    lasilla, SAAO
  exptime           Exptime of observations

optional arguments:
  -h, --help        show this help message and exit
```

For example, if we want to HJD correct some JD\_UTC\_MID times (in the ```times.txt``` file)
for a target at RA=10:00:00 Dec=-20:00:00, observed from La Palma with 60s exposures,  we can do the
following:

```sh
python convert_times.py times.txt jd mid hjd 10:00:00 -- -20:00:00 lapalma 60
```

(**Note:** The double dash ```--``` before the minus sign in the negative declination, this is
UNIX way of specifying arguments that start with a dash)

This will produce a ```times.txt.hjd``` file with the HJD corrected times.

If the JD values in ```times.txt``` are not already corrected to the mid-exposure point,
but are JD\_UTC\_START values instead, you would specify ```start``` instead of ```mid```
in the command above:

```sh
python convert_times.py times.txt jd start hjd 10:00:00 -- -20:00:00 lapalma 60
```

Observatory names can be found using the following:

```python
>>> from astropy.coordinates import EarthLocation
>>> EarthLocation.get_site_names()
['', '', '', 'ALMA', 'Anglo-Australian Observatory', 'Apache Point', 'Apache Point Observatory', 'Atacama Large Millimeter Array', 'BAO', 'Beijing XingLong Observatory', 'Black Moshannon Observatory', 'CHARA', 'Canada-France-Hawaii Telescope', 'Catalina Observatory', 'Cerro Pachon', 'Cerro Paranal', 'Cerro Tololo', 'Cerro Tololo Interamerican Observatory', 'DCT', 'Discovery Channel Telescope', 'Dominion Astrophysical Observatory', 'Gemini South', 'Hale Telescope', 'Haleakala Observatories', 'Happy Jack', 'Jansky Very Large Array', 'Keck Observatory', 'Kitt Peak', 'Kitt Peak National Observatory', 'La Silla Observatory', 'Large Binocular Telescope', 'Las Campanas Observatory', 'Lick Observatory', 'Lowell Observatory', 'Manastash Ridge Observatory', 'McDonald Observatory', 'Medicina', 'Medicina Dish', 'Michigan-Dartmouth-MIT Observatory', 'Mount Graham International Observatory', 'Mt Graham', 'Mt. Ekar 182 cm. Telescope', 'Mt. Stromlo Observatory', 'Multiple Mirror Telescope', 'NOV', 'National Observatory of Venezuela', 'Noto', 'Observatorio Astronomico Nacional, San Pedro Martir', 'Observatorio Astronomico Nacional, Tonantzintla', 'Palomar', 'Paranal Observatory', 'Roque de los Muchachos', 'SAAO', 'SALT', 'SRT', 'Siding Spring Observatory', 'Southern African Large Telescope', 'Subaru', 'Subaru Telescope', 'Sutherland', 'Vainu Bappu Observatory', 'Very Large Array', 'W. M. Keck Observatory', 'Whipple', 'Whipple Observatory', 'aao', 'alma', 'apo', 'bmo', 'cfht', 'ctio', 'dao', 'dct', 'ekar', 'example_site', 'flwo', 'gemini_north', 'gemini_south', 'gemn', 'gems', 'greenwich', 'haleakala', 'irtf', 'keck', 'kpno', 'lapalma', 'lasilla', 'lbt', 'lco', 'lick', 'lowell', 'mcdonald', 'mdm', 'medicina', 'mmt', 'mro', 'mso', 'mtbigelow', 'mwo', 'noto', 'ohp', 'paranal', 'salt', 'sirene', 'spm', 'srt', 'sso', 'tona', 'vbo', 'vla']
```

# Contributors

James McCormac

# License

MIT
