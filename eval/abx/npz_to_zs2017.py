#!/usr/bin/env python

"""
Convert a Numpy archive into ZeroSpeech2017 frame-level evaluation format.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2017
"""

from datetime import datetime
from os import path
import argparse
import numpy as np
import os
import sys

FRAME_DUR = 25E-3
FRAME_RATE = 10E-3


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("output_dir", type=str, help="base directory to write features to")
    parser.add_argument("npz_fn", type=str, help="Numpy archive")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def npz_to_zs2017(npz_fn, output_dir, strip_dims=None):

    print("Reading: " + npz_fn)
    features = np.load(npz_fn)
    print("No. segments: " + str(len(features.keys())))
    utt_labels = set([i.split("_")[0] for i in features.keys()])
    print("No. utterance labels: " + str(len(utt_labels)))

    for d in ["1s", "10s", "120s"]:
        d = path.join(output_dir, d)
        if not path.isdir(d):
            os.makedirs(d)

    print("Writing to directory: " + output_dir)
    utterances_written = set()
    i_segment = 0
    for segment_label in sorted(features):
        utt_label, interval = segment_label.split("_")
        start, end = interval.split("-")
        start = float(start)/100.
        end = float(end)/100.
        test_duration = utt_label[:4].lstrip("0")
        utt_label = str(int(utt_label[5:]))  # .lstrip("0")

        utt_features_fn = path.join(output_dir, test_duration, utt_label + ".fea")
        utterances_written.add(utt_features_fn)
        cur_features = features[segment_label][:, :strip_dims]
        if cur_features.shape[0] == 1:
            # This is necessary, otherwise the evaluation scripts break
            print "Warning:", segment_label, "only has one frame, doubling"
            cur_features = np.vstack([cur_features[0], cur_features[0]])

        with open(utt_features_fn, "a") as f:
            time = start + FRAME_DUR/2.
            for feat_vector in cur_features:
                f.write("%.18e" % time + " " + " ".join(["%.18e" % d for d in feat_vector]) + "\n")
                time += FRAME_RATE
        i_segment += 1

    print("Wrote {} segments to {} utterance feature files".format(i_segment, len(utterances_written)))


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()
    
    if "mandarin" in args.npz_fn:
        lang = "mandarin"
    elif "french" in args.npz_fn:
        lang = "french"
    elif "english" in args.npz_fn:
        lang = "english"

    output_dir = path.join(args.output_dir, lang)
    if not path.isdir(output_dir):
        os.makedirs(output_dir)

    print(datetime.now())
    npz_to_zs2017(args.npz_fn, output_dir)
    print(datetime.now())


if __name__ == "__main__":
    main()
