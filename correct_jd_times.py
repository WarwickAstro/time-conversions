"""
Code to take the JD-MID or JD-START
+ EXPTIME and convert to HJD-MID
"""
import argparse as ap
import numpy as np
from astropy.time import Time
from astropy.coordinates import (
    SkyCoord,
    EarthLocation
    )
import astropy.units as u

# pylint: disable=invalid-name
# pylint: disable=redefined-outer-name
# pylint: disable=no-member

def argParse():
    """
    Parse the command line arguments

    Parameters
    ----------
    None

    Returns
    -------
    argparse argument object

    Raises
    ------
    None
    """
    p = ap.ArgumentParser()
    p.add_argument('jdfile',
                   help='file containing list of JDs')
    p.add_argument('ra',
                   help='RA of target (HH:MM:SS.ss')
    p.add_argument('dec',
                   help='Dec of target (DD:MM:SS.ss)')
    p.add_argument('observatory',
                   help='Observatory where data was taken, e.g. '\
                        'lapalma, paranal, lasilla, SAAO')
    p.add_argument('time_type',
                   help='type of time to convert to',
                   choices=['hjd', 'bjd_tdb'])
    p.add_argument('--exptime',
                   help='If exptime is given, JD-START is assumed',
                   type=float)
    return p.parse_args()

def getLightTravelTimes(ra, dec, time_to_correct):
    """
    Get the light travel times to the helio- and
    barycentres

    Parameters
    ----------
    ra : str
        The Right Ascension of the target in hourangle
        e.g. 16:00:00
    dec : str
        The Declination of the target in degrees
        e.g. +20:00:00
    time_to_correct : astropy.Time object
        The time of observation to correct. The astropy.Time
        object must have been initialised with an EarthLocation

    Returns
    -------
    ltt_bary : float
        The light travel time to the barycentre
    ltt_helio : float
        The light travel time to the heliocentre

    Raises
    ------
    None
    """
    target = SkyCoord(ra, dec, unit=(u.hourangle, u.deg), frame='icrs')
    ltt_bary = time_to_correct.light_travel_time(target)
    ltt_helio = time_to_correct.light_travel_time(target, 'heliocentric')
    return ltt_bary, ltt_helio

if __name__ == "__main__":
    args = argParse()
    location = EarthLocation.of_site(args.observatory)
    jd = np.loadtxt(args.jdfile, usecols=[0], unpack=True)
    time_jd = Time(jd, format='jd',
                   scale='utc', location=location)
    if args.exptime:
        time_jd = time_jd + (args.exptime/2.)*u.second
    ltt_bary, ltt_helio = getLightTravelTimes(args.ra, args.dec, time_jd)
    if args.time_type == 'hjd':
        new_time = time_jd.utc + ltt_helio
    else:
        new_time = time_jd.tdb + ltt_bary
    # save out the new time file
    np.savetxt('{}.{}'.format(args.jd_file, args.time_type),
               np.c_[new_time],
               fmt='%.8f',
               header=args.time_type)
