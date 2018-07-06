#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 14:08:34 2018

@author: tnye
"""

# stdlib imports
import os.path
import argparse
import tempfile
from datetime import datetime

# third party
import numpy as np

# neic imports
from libcomcat.search import search
from mapio.shake import ShakeGrid
from mapio.geodict import GeoDict
from mapio.gridcontainer import GridHDFContainer


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass


def get_parser():
    desc = '''Download and stack ShakeMaps from ComCat into an HDF5 file.
    Create an HDF file containing spatially stacked ShakeMaps.  For example, if
    a given study area is contained in the box defined by longitude -100.129 to
    -95.592, and longitude 34.949 to 37.571, you can download all of the
    ShakeMaps in the 4 month period from 2017-01-01 to 2017-04-01, you would do
    this:
    %(prog)s oklahoma_2017.hdf -100.129 -95.592 34.949 37.571
    2017-01-01 2017-04-01 -m 1.0 9.9 -r 0.01. The resulting HDF5 file will
    contain stacked arrays, one per ground motion, at 0.1 degree resolution,
    where "stacked" means that each ShakeMap found in the given bounds is
    resampled to a grid defined by those bounds and input resolution.  If there
    are 35 ShakeMaps found, then each stacked array will contain 35 layers,
    where each layer corresponds to an individual resampled ShakeMap.
    '''

    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=CustomFormatter)
    # positional arguments
    parser.add_argument('outputfile', metavar='OUTFILE',
                        help='japan_shakes')
    parser.add_argument('130', metavar='LONMIN',
                        type=float,
                        help='Western boundary of desired grid')
    parser.add_argument('143', metavar='LONMAX',
                        type=float,
                        help='Eastern boundary of desired grid')
    parser.add_argument('32', metavar='LATMIN',
                        type=float,
                        help='Southern boundary of desired grid')
    parser.add_argument('41', metavar='LATMAX',
                        type=float,
                        help='Northern boundary of desired grid')
    parser.add_argument('2000-10-05', type=maketime,
                        help='Start time for search (defaults to ~30 days ago). YYYY-mm-dd or YYYY-mm-ddTHH:MM:SS')
    parser.add_argument('2008-06-15', type=maketime,
                        help='End time for search (defaults to current date/time). YYYY-mm-dd or YYYY-mm-ddTHH:MM:SS')

    # optional arguments
    parser.add_argument('-6.5', '--7.0', metavar=('minmag', 'maxmag'),
                        dest='magRange', type=float, nargs=2,
                        help='Min/max magnitude to restrict search.',
                        default=(5.5, 9.9))
    parser.add_argument('-r', '--resolution', metavar='RESOLUTION',
                        type=float, default=0.01,
                        help='Resolution for output grids.')

    return parser


def main(args):
    events = search(starttime=args.start,
                    endtime=args.end,
                    minlatitude=args.latmin,
                    maxlatitude=args.latmax,
                    minlongitude=args.lonmin,
                    maxlongitude=args.lonmax,
                    producttype='shakemap',
                    maxmagnitude=args.magRange[1],
                    minmagnitude=args.magRange[0])
    print('%i events found containing ShakeMaps.' % len(events))

    # Create the GeoDict to which the ShakeMaps will be resampled
    stack_dict = GeoDict.createDictFromBox(args.lonmin, args.lonmax,
                                           args.latmin, args.latmax,
                                           args.resolution, args.resolution)
    nrows, ncols = stack_dict.ny, stack_dict.nx
    imts = {}
    layer_names = {}
    event_info = {}
    layer_count = {}
    ic = 0
    for event in events:
        tnow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        if ic % 10 == 0:
            print('%s: Attempting to fetch ShakeMap for %s (%i of %i)' %
                  (tnow, event.id, ic, len(events)))
        ic += 1
        event_info[event.id] = event.toDict()
        try:
            detail = event.getDetailEvent()
        except Exception as e:
            fmt = 'Could not retrieve detail data for event %s, error "%s". Skipping.'
            print(fmt % (event.id, str(e)))
            continue
        if not detail.hasProduct('shakemap'):
            print('Event %s appears not to have a ShakeMap after all... skipping.'
                  % detail.id)
        shakemap = detail.getProducts('shakemap')[0]
        try:
            f, gridfile = tempfile.mkstemp()
            os.close(f)
            shakemap.getContent('grid.xml', gridfile)
            shakegrid = ShakeGrid.load(gridfile, samplegeodict=stack_dict,
                                       resample=True, doPadding=True)
            imtlist = list(shakegrid.getLayerNames())

            # remove the things that are not ground motions
            kill_list = ['stdpga', 'urat', 'svel']
            for layer in kill_list:
                if layer in imtlist:
                    imtlist.remove(layer)

            for imt in imtlist:
                imtdata = shakegrid.getLayer(imt).getData()
                if imt not in imts:
                    imts[imt] = np.zeros((nrows, ncols, len(events)))
                    layer_count[imt] = 0
                    idx = 0
                    layer_names[imt] = [event.id]
                else:
                    idx = layer_count[imt] + 1
                    layer_names[imt].append(event.id)
                    layer_count[imt] = layer_count[imt] + 1
                imts[imt][:, :, idx] = imtdata
        except Exception as e:
            print('Error fetching ShakeMap grid from %s -  "%s".  Skipping.' %
                  (event.id, str(e)))
        finally:
            os.remove(gridfile)

    # make sure all imts have valid grids in each vertical layer
    # trim off any layers that don't have any data in them.
    for imtname, imtcube in imts.items():
        height_diff = len(events) - (layer_count[imtname]+1)
        if height_diff:
            top_layer = layer_count[imtname]
            imts[imtname] = imtcube[:, :, 0:top_layer]

    # now create an HDF file, and stuff our data and metadata into it
    stack_file = GridHDFContainer.create(args.outputfile)
    stack_file.setDictionary('layer_names', layer_names)
    stack_file.setDictionary('event', event_info)
    metadata = stack_dict.asDict()
    for imtname, imtcube in imts.items():
        stack_file.setArray(imtname, imtcube, metadata=metadata,
                            compression=True)

    stack_file.close()


if __name__ == '__main__':
    parser = get_parser()
    pargs = parser.parse_args()
    main(pargs)
