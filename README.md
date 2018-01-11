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
  --exptime EXPTIME  If exptime is given, JD-START is assumed
```

# Contributors

James McCormac

# License

MIT
