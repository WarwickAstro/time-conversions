# Time Conversion Tools

Code to convert times used for astronomical observations

# Converting JD to HJD or BJD_TDB

```sh
▶ python correct_jd_times.py -h
usage: correct_jd_times.py [-h] [--exptime EXPTIME]
                           jdfile ra dec observatory {hjd,bjd_tdb}

positional arguments:
  jdfile             file containing list of JDs
  ra                 RA of target (HH:MM:SS.ss
  dec                Dec of target (DD:MM:SS.ss)
  observatory        Observatory where data was taken, e.g. lapalma, paranal,
                     lasilla, SAAO
  {hjd,bjd_tdb}      type of time to convert to

optional arguments:
  -h, --help         show this help message and exit
  --exptime EXPTIME  If exptime is given, JD-START is assumed, otherwise JD-MID
```

For example, if we want to HJD correct some JD times (in the ```times.jd``` file)
for a target at RA=10:00:00 Dec=-20:00:00, observed from La Palma,  we can do the
following:

```sh
python correct_jd_times.py times.jd 10:00:00 -- -20:00:00 lapalma hjd
```

This will produce a ```times.jd.hjd``` file with the HJD corrected times.

**Note:** The double dash ```--``` before supplying a negative declination. This is
the standard *nix way of allowing positional arguments to start with a dash.

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
