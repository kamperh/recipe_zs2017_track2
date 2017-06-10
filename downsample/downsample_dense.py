#!/usr/bin/env python

"""
Perform dense downsampling over indicated segmentation intervals.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2015-2017
"""

from datetime import datetime
from os import path
import argparse
import cPickle as pickle
import numpy as np
import scipy.signal as signal
import sys

OUTPUT_DIR = "embeddings"


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("lang", type=str, choices=["english", "french", "mandarin"])
    parser.add_argument("subset", type=str, choices=["train"])  #, "test"])
    # parser.add_argument("landmarks", type=str, choices=["gtphone", "unsup_syl"], help="landmarks set")
    parser.add_argument("landmarks", type=str, choices=["unsup_syl"], help="landmarks set")
    parser.add_argument(
        # "feature_type", type=str, help="input feature type", choices=["mfcc", "cae.d_10", "cae.d_13"]
        "feature_type", type=str, help="input feature type", choices=["mfcc"]
        )
    parser.add_argument("--n", type=int, help="number of samples (default: %(default)s)", default=10)
    parser.add_argument(
        "--frame_dims", type=int, default=None,
        help="only keep these number of dimensions"
        )
    parser.add_argument(
        "--n_landmarks_max", type=int,
        help="maximum number of landmarks to cross (default: %(default)s)", default=6
        )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def downsample_utterance(features, seglist, n):
    """
    Return the downsampled matrix with each row an embedding for a segment in
    the seglist.
    """
    embeddings = []
    for i, j in seglist:
        y = features[i:j+1, :].T
        y_new = signal.resample(y, n, axis=1).flatten("C")
        embeddings.append(y_new)
    return np.asarray(embeddings)


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    if args.feature_type == "mfcc":
        input_npz_fn = path.join(
            "..", "features", "mfcc", args.lang + "_" + args.subset, "numpy", "mfcc.cmvn_dd.npz"
            )
    else:
        assert False

    print("Reading: " + input_npz_fn)
    input_npz = np.load(input_npz_fn)
    d_frame = input_npz[input_npz.keys()[0]].shape[1]
    print("No. of utterances: " + str(len(input_npz.keys())))

    seglist_pickle_fn = path.join(
        OUTPUT_DIR, args.lang + "_" + args.subset, "seglist." + args.landmarks
        + ".n_max_" + str(args.n_landmarks_max) + ".pkl"
        )
    print("Reading: " + seglist_pickle_fn)
    with open(seglist_pickle_fn, "rb") as f:
        seglist_dict = pickle.load(f)
    print("No. of utterances: " + str(len(seglist_dict)))

    print("Frame dimensionality: " + str(d_frame))
    if args.frame_dims is not None and args.frame_dims < d_frame:
        d_frame = args.frame_dims
        print("Reducing frame dimensionality: " + str(d_frame))

    print("No. of samples: " + str(args.n))

    print(datetime.now())
    print("Downsampling")
    downsample_dict = {}
    for i, utt in enumerate(input_npz.keys()):
        downsample_dict[utt] = downsample_utterance(
            input_npz[utt][:, :args.frame_dims], seglist_dict[utt], args.n
            )
    print(datetime.now())

    output_npz_fn = path.join(
        OUTPUT_DIR, args.lang + "_" + args.subset, "downsample_dense." + args.feature_type +
        ".n_" + str(args.n) + ".n_max_" + str(args.n_landmarks_max)  + "." + args.landmarks + ".npz"
        )
    print("Writing: " + output_npz_fn)
    np.savez_compressed(output_npz_fn, **downsample_dict)


if __name__ == "__main__":
    main()
