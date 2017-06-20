#!/usr/bin/env python

"""
Get the SCP containing the active speech segments.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2011-2017
"""

from os import path
import argparse
import os
import sys

sys.path.append(path.join("..", ".."))

from paths import ZEROSPEECH_TOOLDIR, ZEROSPEECH_DATADIR
from utils import shell


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("lang", type=str, choices=["english", "french", "mandarin", "LANG1", "LANG2"])
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

    basedir = args.lang + "_" + args.subset
    list_dir = path.join(basedir, "lists")
    scp_dir = path.join(basedir, "scp")
    feat_dir = path.join(basedir, "raw")
    output_list = path.join(list_dir, "segments.list")
    output_scp = path.join(scp_dir, "mfcc.raw.segments.scp")

    for d in [list_dir]:
        if not path.isdir(d):
            os.makedirs(d)
    feat_dir = path.abspath(feat_dir)

    if args.subset == "train":
        
        if "LANG" in args.lang:
            vad_fn = path.join(
                ZEROSPEECH_DATADIR, "surprise", "train", args.lang, args.lang +
                "_VAD.csv"
                )
        else:
            vad_fn = path.join(
                ZEROSPEECH_TOOLDIR, "track2", "baseline", "baseline_" +
                args.lang, "data", args.lang + "_vad"    
                )
        print("Reading: " + vad_fn)
        segments = []  # (utterance, start_frame, end_frame)
        with open(vad_fn) as f:
            f.readline()
            for line in f:
                utt_label, start, end = line.strip().split(",")
                utt_label = utt_label.replace("_", "-")
                if "LANG" in args.lang:
                    start = int(round(float(start)*100))
                    end = int(round(float(end)*100))
                else:
                    start = int(start)
                    end = int(end)
                segments.append((utt_label, start, end))

        print("Running: HList for lengths")
        lengths = {}
        for line in shell(
                "HList -z -h " + path.join(feat_dir, "*.mfcc" +
                " | paste - - - - - ")
                ).split("\n"):
            if len(line) == 0:
                continue
            line = line.split(" ")
            line = [i for i in line if i != ""]
            utt_label = line[line.index("Source:") + 1]
            utt_label = path.splitext(path.split(utt_label)[-1])[0]
            frames = line[line.index("Samples:") + 1]
            lengths[utt_label] = int(frames)

        print("Writing: " + output_scp)
        missing = []
        with open(output_scp, "w") as f:
            for basename, start, end in segments:
                if basename not in lengths:
                    if basename not in missing:
                        print("Warning: Missing audio: " + basename)
                        missing.append(basename)
                    continue
                if start == end:
                    print("Warning: Skipping: {} ({} to {})".format(basename, start, end))
                    continue
                if end > lengths[basename]:
                    if start > lengths[basename]:
                        print("Warning: Problem with lengths (truncating): " + basename)
                        print lengths[basename]
                        print start
                        print end
                        assert False
                        continue
                    end = lengths[basename] - 1
                segment_label = "{}_{:08d}-{:08d}.mfcc".format(basename, start, end)
                # segment_label = "%s_%06d-%06d.mfcc" % (basename, start, end)
                f.write(
                    segment_label + "=" + path.join(feat_dir, basename + ".mfcc") +
                    "[" + str(start) + "," + str(end) + "]\n"
                    )

    elif args.subset == "test":

        raw_scp = path.join(scp_dir, "mfcc.raw.scp")
        print("Reading: " + raw_scp)
        lines = []
        with open(raw_scp) as f:
            for line in f:
                features_fn = line.strip().split(" ")[-1]
                basename = path.splitext(path.split(features_fn)[-1])[0]
                start = 0
                if basename.startswith("001s"):
                    end = 98
                elif basename.startswith("010s"):
                    end = 998
                elif basename.startswith("120s"):
                    end = 11998
                segment_label = "{}_{:05d}-{:05d}.mfcc".format(basename, start, end)
                lines.append(segment_label + "=" + features_fn + "[" + str(start) + "," + str(end) + "]")

        print("Writing: " + output_scp)
        with open(output_scp, "w") as f:
            f.write("\n".join(lines))
            f.write("\n")


if __name__ == "__main__":
    main()
