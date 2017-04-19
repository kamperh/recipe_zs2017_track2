#!/usr/bin/env python

"""
Code the data to raw features without any normalization.

Author: Herman Kamper
Contact: h.kamper@sms.ed.ac.uk
Date: 2011-2017
"""

from datetime import datetime
from os import path
import argparse
import glob
import os
import sys

sys.path.append(path.join("..", "..", "src"))

from paths import ZEROSPEECH_DATADIR
from utils import shell

CONFIG_FN = path.join("config", "hcopy.wav.mfcc.wb.conf")


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("lang", type=str, choices=["english", "french", "mandarin"])
    parser.add_argument("subset", type=str, choices=["train", "test"])
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    print(datetime.now())

    if args.subset == "train":
        wavs = path.join(ZEROSPEECH_DATADIR, args.subset, args.lang, "*.wav")
    elif args.subset == "test":
        wavs = path.join(ZEROSPEECH_DATADIR, args.subset, args.lang, "*", "*.wav")

    basedir = args.lang + "_" + args.subset
    target_dir = path.join(basedir, "raw")
    scp_dir = path.join(basedir, "scp")
    log_dir = path.join(basedir, "log")

    for d in [target_dir, scp_dir, log_dir]:
        if not path.isdir(d):
            os.makedirs(d)
    target_dir = path.abspath(target_dir)

    raw_scp = path.join(scp_dir, "mfcc.raw.scp")
    print("Writing: " + raw_scp)
    with open(raw_scp, "w") as f:
        for wav_fn in sorted(glob.glob(wavs)):
            basename = path.splitext(path.split(wav_fn)[-1])[0]
            basename = basename.replace("_", "-")
            if args.subset == "test":
                basename = "{:03d}s-{:05d}".format(
                    int(path.split(path.split(wav_fn)[0])[-1][:-1]), int(basename)
                    )
            f.write(wav_fn + " " + path.join(target_dir, basename + ".mfcc") + "\n")

    print("Running: HCopy")
    shell(
        "HCopy -T 7 -A -D -V -S " + raw_scp + " -C " + CONFIG_FN + " > " + 
        path.join(log_dir, "mfcc.raw.log")
        )

    print(datetime.now())


if __name__ == "__main__":
    main()
