#!/usr/bin/env python

"""
Get the ZeroSpeech2017 data and format for segmentation.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2015-2017
"""

from os import path
import argparse
import cPickle as pickle
import glob
import numpy as np
import re
import sys
import os

WORDEMBEDS_DIR = "../../../../downsample/embeddings"  # relative to data/lang/embeding_label/
OUTPUT_DIR = "data"


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("lang", type=str, choices=["english", "french", "mandarin"])
    parser.add_argument("landmarks", type=str, choices=["gtphone", "unsup_syl"], help="landmarks set")
    parser.add_argument(
        # "feature_type", type=str, help="input feature type", choices=["mfcc", "cae.d_10", "cae.d_13"]
        "feature_type", type=str, help="input feature type", choices=["mfcc"] #, "cae.d_10", "cae.d_13"]
        )
    parser.add_argument(
        "n_samples", type=int, help="the number of samples used in downsampling"
        )
    parser.add_argument(
        "--n_landmarks_max", type=int,
        help="maximum number of landmarks to cross (default: %(default)s)", default=6
        )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                              GET DATA FUNCTIONS                             #
#-----------------------------------------------------------------------------#

def get_vec_ids_dict(lengths_dict, n_landmarks_max):
    """
    Every N(N + 1)/2 length vector `vec_ids` contains all the indices for a
    particular utterance. For t = 1, 2, ..., N the entries `vec_ids[i:i
    + t]` contains the IDs of embedding[0:t] up to embedding[t - 1:t], with i =
    t(t - 1)/2. Written out: `vec_ids` = [embed[0:1], embed[0:2], embed[1:2],
    embed[0:3], ..., embed[N-1:N]].
    """
    vec_ids_dict = {}
    for utt in sorted(lengths_dict.keys()):
        i_embed = 0
        n_slices = lengths_dict[utt]
        vec_ids = -1*np.ones((n_slices**2 + n_slices)/2, dtype=int)
        for cur_start in range(n_slices):
            for cur_end in range(cur_start, min(n_slices, cur_start + n_landmarks_max)):
                cur_end += 1
                t = cur_end
                i = t*(t - 1)/2
                vec_ids[i + cur_start] = i_embed
                i_embed += 1
        vec_ids_dict[utt] = vec_ids
        # print(utt, lengths_dict[utt], vec_ids)
    return vec_ids_dict


def get_durations_dict(landmarks_dict, n_landmarks_max):
    durations_dict = {}
    for utt in sorted(landmarks_dict.keys()):
        landmarks = [0,] + landmarks_dict[utt]
        N = len(landmarks)  # should be n_slices + 1
        durations = -1*np.ones(((N - 1)**2 + (N - 1))/2, dtype=int)
        j = 0
        for t in xrange(1, N):
            for i in range(t):
                if t - i > N - 1:
                    j += 1
                    continue
                durations[j] = landmarks[t] - landmarks[i]
                j += 1
        durations_dict[utt] = durations
    return durations_dict


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    data_dir = path.join(
        OUTPUT_DIR, args.lang, args.feature_type + ".n_" + str(args.n_samples)
        + ".n_max_" + str(args.n_landmarks_max) + "." + args.landmarks
        )
    print("Output directory: " + data_dir)
    if not path.isdir(data_dir):
        os.makedirs(data_dir)

    # Create symbolic link to embeddings file
    src_dense_embeddings_fn = path.join(
        WORDEMBEDS_DIR, args.lang + "_train", "downsample_dense." + args.feature_type + ".n_" +
        str(args.n_samples) + ".n_max_" + str(args.n_landmarks_max) + "." + args.landmarks + ".npz"
        )
    target_dense_embeddings_fn = path.join(data_dir, "dense_embeddings.npz")

    if not path.islink(target_dense_embeddings_fn):
        print("Linking: " + src_dense_embeddings_fn)
        os.symlink(src_dense_embeddings_fn, target_dense_embeddings_fn)

    # Create symbolic link to landmarks file
    src_landmarks_fn = path.join(
        WORDEMBEDS_DIR, args.lang + "_train", "landmarks." + args.landmarks + ".pkl"
        )
    target_landmarks_fn = path.join(data_dir, "landmarks.pkl")
    if not path.islink(target_landmarks_fn):
        print("Linking: " + src_landmarks_fn)
        os.symlink(src_landmarks_fn, target_landmarks_fn)

    print("Reading: " + target_landmarks_fn)
    with open(target_landmarks_fn, "rb") as f:
        landmarks_dict = pickle.load(f)
    print("No. of utterances: " + str(len(landmarks_dict)))

    lengths_dict = dict([(i, len(landmarks_dict[i])) for i in landmarks_dict.keys()])
    utt_ids = landmarks_dict.keys()

    print("Getting vec_ids")
    vec_ids_dict = get_vec_ids_dict(lengths_dict, args.n_landmarks_max)
    print("Getting durations")
    durations_dict = get_durations_dict(landmarks_dict, args.n_landmarks_max)
    print("No. of utterances: " + str(len(durations_dict)))

    vec_ids_dict_fn = path.join(data_dir, "vec_ids.pkl")
    durations_dict_fn = path.join(data_dir, "durations.pkl")
    print("Writing: " + vec_ids_dict_fn)
    with open(vec_ids_dict_fn, "wb") as f:
        pickle.dump(vec_ids_dict, f, -1)
    print("Writing: " + durations_dict_fn)
    with open(durations_dict_fn, "wb") as f:
        pickle.dump(durations_dict, f, -1)


if __name__ == "__main__":
    main()
