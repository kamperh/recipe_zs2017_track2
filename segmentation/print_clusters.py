#!/usr/bin/env python

"""
Print cluster information.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2017
"""

from os import path
import argparse
import cPickle as pickle
import numpy as np
import sys


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("model_dir", type=str, help="model directory")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    fn = path.join(args.model_dir, "clusters_landmarks.pkl")
    print("Reading: " + fn)
    with open(fn, "rb") as f:
        unsup_transcript = pickle.load(f)
        unsup_landmarks = pickle.load(f)

    clusters = {}
    for utt_label in unsup_transcript:
        for cluster in unsup_transcript[utt_label]:
            if not cluster in clusters:
                clusters[cluster] = {}
                clusters[cluster]["size"] = 0
            clusters[cluster]["size"] += 1

    cluster_ids = sorted(clusters)
    sizes = [clusters[i]["size"] for i in cluster_ids]

    n_biggest = 20
    biggest_clusters = list(np.argsort(sizes)[-n_biggest:])
    biggest_clusters.reverse()
    print biggest_clusters
    print [sizes[i] for i in biggest_clusters]


if __name__ == "__main__":
    main()
