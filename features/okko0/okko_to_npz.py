#!/usr/bin/env python

"""
Convert Okko's features file to Numpy archive format.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2017
"""

from __future__ import print_function
from os import path
import argparse
import numpy as np
import sys
import tables


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("mat_fn", type=str, help="Okko's Matlab filename")
    parser.add_argument("npz_fn", type=str, help="output filename")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()
    
    print("Reading:", args.mat_fn)
    mat = tables.open_file(args.mat_fn)

    n_audio = mat.root.files_train[0].shape[0]
    print("No. audio files:", n_audio)

    filenames = []
    for i_audio in xrange(n_audio):
        filenames.append("".join([chr(i[0]) for i in mat.root.files_train[0][i_audio][0]]))
    audio_keys = [path.splitext(path.split(i)[-1])[0] for i in filenames]

    features_dict = {}
    for i_audio in xrange(n_audio):
        features = mat.root.F_train_iter[0][i_audio][0]
        features_dict[audio_keys[i_audio].replace("_", "-")] = features.T

    print("Writing:", args.npz_fn)
    np.savez(args.npz_fn, **features_dict)


if __name__ == "__main__":
    main()
