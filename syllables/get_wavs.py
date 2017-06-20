#!/usr/bin/env python

"""
Get wav files for the segments in the ZeroSpeech2017 data.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2015-2017
"""

from datetime import datetime
from os import path
import argparse
import os
import re
import subprocess
import sys

sys.path.append(path.join(".."))

from paths import ZEROSPEECH_DATADIR

shell = lambda command: subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("lang", type=str, choices=["english", "french", "mandarin", "LANG1", "LANG2"])
    parser.add_argument("subset", type=str, choices=["train"])  #, "test"])
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

    raw_mfcc_scp = path.join(
        "..", "features", "mfcc", args.lang + "_" + args.subset, "scp", "mfcc.raw.segments.scp"
        )
    output_dir = path.join("wavs", args.lang + "_" + args.subset)
    if not path.isdir(output_dir):
        os.makedirs(output_dir)

    print("Reading: " + raw_mfcc_scp)
    wavs = []
    zerospeech_datadir = ZEROSPEECH_DATADIR
    if "LANG" in args.lang:
        zerospeech_datadir = path.join(zerospeech_datadir, "surprise")
    with open(raw_mfcc_scp) as f:
        for line in f:
            match = re.match("(.*)\.mfcc=.*\[(.*),(.*)\]", line)
            if not match:
                continue
            label = match.group(1)
            utt_label = label.split("_")[0]
            start = float(match.group(2))/100.
            end = float(match.group(3))/100.
            duration = end - start

            utt_label = utt_label.replace("-", "_")
            input_wav = path.join(zerospeech_datadir, args.subset, args.lang, utt_label + ".wav")
            output_wav = path.join(path.abspath(output_dir), label + ".wav")
            sox_cmd = "sox " + input_wav + " " + output_wav + " trim " + str(start) + " " + str(duration)
            shell(sox_cmd)
            wavs.append(output_wav)
    print("No. wavs: " + str(len(wavs)))
    
    wav_list_fn = path.join("wavs", args.lang + "_" + args.subset + ".list")
    print("Writing: " + wav_list_fn)
    with open(wav_list_fn, "w") as f:
        for wav in wavs:
            f.write(wav + "\n")

    print(datetime.now())


if __name__ == "__main__":
    main()

