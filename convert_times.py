"""
Code to times in any format to times in any other format

Inputs can be: JD_UTC_f*, HJD_f*, BJD_TDB_f*
where f* denotes the exposure timestamp location (see below)

Timestamp types can be: START, MID, END

Outputs can be: JD_UTC_f*, HJD_f*, BJD_TDB_f*
again where f* denotes the exposure timestamp location

Timestamp locations are generally required as MID
"""
import sys
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
    p.add_argument('input_times',
                   help='file containing list of times to convert')
    p.add_argument('input_format',
                   help='type of time we are converting from',
                   choices=['jd', 'mjd', 'hjd', 'bjd'])
    p.add_argument('input_timestamps',
                   help='type of input timestamps we have',
                   choices=['start', 'mid', 'end'])
    p.add_argument('output_format',
                   help='type of time we are converting to',
                   choices=['jd', 'mjd', 'hjd', 'bjd'])
    p.add_argument('ra',
                   type=str,
                   help='RA of target (HH:MM:SS.ss)')
    p.add_argument('dec',
                   type=str,
                   help='Dec of target (DD:MM:SS.ss)')
    p.add_argument('observatory',
                   help='Observatory where data was taken, e.g. '\
                        'lapalma, paranal, lasilla, SAAO')
    p.add_argument('exptime',
                   type=float,
                   help='Exptime of observations')
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

    # check for unnecessary conversion
    if args.input_format == args.output_format and args.input_timestamps == 'mid':
        print('No conversion needed, times are in requested format')
        sys.exit(0)

    # get the location of the observatory
    location = EarthLocation.of_site(args.observatory)

    # read in the input times - assumes first column if >1 col
    tinp = np.loadtxt(args.input_times, usecols=[0], unpack=True)

    # first correct the times to the same start, mid, end frame as needed
    # correction is assuming to be in units of half_exptime
    correction = (args.exptime/2.)*u.second
    if args.input_frame == 'mid':
        print('No timestamp correction needed')
    elif args.input_frame == 'start':
        print('Converting START --> MID')
        tinp = tinp + correction
    elif args.input_frame == 'end':
        print('Converting END --> MID')
        tinp = tinp - correction

    # set up the astropy time inputs and convert them to JD-UTC-MID
    if args.input_format == 'jd':
        print('Input times in JD, applying no initial correction')
        time_inp = Time(tinp, format='jd', scale='utc', location=location)
    elif args.input_format == 'mjd':
        print('Input times in MJD, applying no initial correction')
        time_inp = Time(tinp, format='mjd', scale='utc', location=location)
    elif args.input_format == 'hjd':
        print('Input times in HJD, removing heliocentric correction')
        time_inp = Time(tinp, format='jd', scale='utc', location=location)
        _, ltt_helio = getLightTravelTimes(args.ra, args.dec, time_inp)
        time_inp = Time(time_inp.utc - ltt_helio, format='jd', scale='utc', location=location)
    elif args.input_format == 'bjd':
        print('Input times in BJD, removing barycentric correction')
        time_inp = Time(tinp, format='jd', scale='tdb', location=location)
        ltt_bary, _ = getLightTravelTimes(args.ra, args.dec, time_inp)
        time_inp = Time(time_inp.tdb - ltt_bary, format='jd', scale='tdb', location=location).utc
    else:
        print('Unknown input time format, exiting...')
        sys.exit(1)

    # now convert to the output format requested
    if args.output_format == 'jd':
        new_time = time_inp.jd
    elif args.output_format == 'mjd':
        new_time = time_inp.mjd
    elif args.output_format == 'hjd':
        _, ltt_helio = getLightTravelTimes(args.ra, args.dec, time_inp)
        new_time = time_inp + ltt_helio
    elif args.output_format == 'bjd':
        ltt_bary, _ = getLightTravelTimes(args.ra, args.dec, time_inp)
        new_time = time_inp.tdb + ltt_bary
    else:
        print('Unknown output time format, exiting...')

    # save out the new time file
    np.savetxt('{}.{}'.format(args.input_times, args.output_format),
               np.c_[new_time.value],
               fmt='%.8f',
               header=args.output_format)
