#!/usr/bin/env python

"""
Perform speaker-dependent segmentation of all the speakers in a subset.

Options should be changed in `ksegment.py`.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2015
"""

from os import path
import argparse
import cPickle as pickle
import os
import hashlib
import subprocess
import sys

from get_data_sd import mandarin_speakers, french_speakers, english_speakers
from ksegment import default_options_dict, MODEL_DIR

sd_options = ["min_duration", "init_am_n_iter", "segment_n_iter", "n_slices_max","p_boundary_init"]

# mandarin_speakers = ["A08", "A33", "A36"]


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument(
        "data_dir", type=str, help="data directory; should contain a "
        "subdirectory for every speaker"
        )
    # parser.add_argument(
    #     "--rnd_seed", type=int, help="default: %(default)s",
    #     default=default_options_dict["rnd_seed"]
    #     )
    parser.add_argument(
        "--min_duration", type=int, help="default: %(default)s",
        default=default_options_dict["min_duration"]
        )
    parser.add_argument(
        "--init_am_n_iter", type=int, help="default: %(default)s",
        default=default_options_dict["init_am_n_iter"]
        )
    parser.add_argument(
        "--segment_n_iter", type=int, help="default: %(default)s",
        default=default_options_dict["segment_n_iter"]
        )
    parser.add_argument(
        "--n_slices_max", type=int, help="default: %(default)s",
        default=default_options_dict["n_slices_max"]
        )
    parser.add_argument(
        "--p_boundary_init", type=float, help="default: %(default)s",
        default=default_options_dict["p_boundary_init"]
        )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    _, lang, _ = path.normpath(args.data_dir).split(os.sep)

    if lang == "mandarin":
        speakers = mandarin_speakers
    elif lang == "french":
        speakers = french_speakers
    elif lang == "english":
        speakers = english_speakers
    else:
        assert False

    # Check that all speakers are in the set directory
    for speaker in speakers:
        assert path.isdir(path.join(args.data_dir, speaker))

    # Set options (this is actually just for hashing purposes)
    options_dict = default_options_dict.copy()
    options_dict["data_dir"] = path.normpath(args.data_dir)
    options_dict["min_duration"] = args.min_duration
    options_dict["init_am_n_iter"] = args.init_am_n_iter
    options_dict["segment_n_iter"] = args.segment_n_iter
    options_dict["p_boundary_init"] = args.p_boundary_init

    hasher = hashlib.md5(repr(sorted(options_dict.items())).encode("ascii"))
    hash_str = hasher.hexdigest()[:10]
    model_dir = path.join(
        MODEL_DIR, options_dict["data_dir"].replace("data" + os.sep, ""), "sd_" + hash_str
        )
    if not path.isdir(model_dir):
        os.makedirs(model_dir)
    log_dir = path.join(model_dir, "log")
    if not path.isdir(log_dir):
        os.mkdir(log_dir)
    models_fn = path.join(model_dir, "models.txt")
    options_dict_fn = path.join(model_dir, "options_dict.pkl")

    print "Writing:", options_dict_fn
    with open(options_dict_fn, "wb") as f:
        pickle.dump(options_dict, f, -1)

    models_fn = path.join(model_dir, "models.txt")
    # print "Writing:", models_fn
    # with open(models_fn, "w") as f:
    #     f.write("")  # empty out the log file

    # Construct command list
    cmd_list = []
    for speaker in sorted(speakers):
        data_dir = path.join(args.data_dir, speaker)
        cmd = "./ksegment.py "
        for option in sd_options:
            cmd += "--" + option + " " + str(options_dict[option]) + " "
        cmd += data_dir + " "
        cmd += ">> " + path.join(log_dir, "log." + speaker)
        cmd_list.append(cmd)

    # Spawn jobs
    # http://stackoverflow.com/questions/23611396/python-execute-cat-subprocess-in-parallel
    procs = []
    for cmd in cmd_list:
        proc = subprocess.Popen(cmd, shell=True)
        procs.append(proc)
    exit_codes = [proc.wait() for proc in procs]

    print str(sum([1 for i in exit_codes if i == 0])) + " out of " + str(len(procs)) + " succeeded"

    # Write model directories
    model_dirs = []
    for speaker in sorted(speakers):
        log_fn = path.join(log_dir, "log." + speaker)
        with open(log_fn) as f:
            for line in f:
                if line.startswith("Model directory: "):
                    model_dirs.append(line.replace("Model directory: ", "").strip())
                    break
    print "Writing:", models_fn
    with open(models_fn, "w") as f:
        for model_dir in model_dirs:
            f.write(model_dir + "\n")


if __name__ == "__main__":
    main()
