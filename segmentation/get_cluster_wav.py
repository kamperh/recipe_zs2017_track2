#!/usr/bin/env python

"""
Get the concatenated audio for a given cluster.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 2017
"""

from os import path
import argparse
import cPickle as pickle
import numpy as np
import os
import subprocess
import sys
import uuid

sys.path.append("..")

from paths import ZEROSPEECH_DATADIR

shell = lambda command: subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("model_dir", type=str, help="model directory")
    parser.add_argument("cluster_id", type=int, help="e.g. '100'")
    parser.add_argument("--pad", type=float, help="if given, add padding between tokens", default=0.25)
    parser.add_argument(
        "--no_shuffle", dest="shuffle", action="store_false",
        help="do not shuffle tokens, sort them by utterance label"
        )
    parser.set_defaults(shuffle=True)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    return parser.parse_args()


def cat_zs2017_wavs(lang, tokens, wav_fn, pad=None):

    if path.isfile(wav_fn):
        print("Warning: Deleting: " + wav_fn)
        os.remove(wav_fn)

    tmp_basename = str(uuid.uuid4())
    tmp_wav = tmp_basename + ".wav"

    zerospeech_datadir = ZEROSPEECH_DATADIR
    if "LANG" in lang:
        zerospeech_datadir = path.join(zerospeech_datadir, "surprise")

    print("Writing: " + wav_fn)
    for utt_label, start, end in tokens:
        utt_label = utt_label.replace("-", "_")
        input_wav = path.join(zerospeech_datadir, "train", lang, utt_label + ".wav")
        duration = end - start
        sox_cmd = "sox " + input_wav + " " + tmp_wav + " trim " + str(start) + " " + str(duration)
        if pad is not None:
            sox_cmd += " pad 0 " + str(pad)
        shell(sox_cmd)

        # Concatenate wavs
        if path.isfile(wav_fn):
            tmp_wav2 = tmp_basename + ".2.wav"
            shell("sox " + wav_fn + " " + tmp_wav + " " + tmp_wav2)
            os.rename(tmp_wav2, wav_fn)
            os.remove(tmp_wav)
        else:
            os.rename(tmp_wav, wav_fn)


#-----------------------------------------------------------------------------#
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    if "mandarin" in args.model_dir:
        lang = "mandarin"
    elif "french" in args.model_dir:
        lang = "french"
    elif "english" in args.model_dir:
        lang = "english"
    elif "LANG1" in args.model_dir:
        lang = "LANG1"
    elif "LANG2" in args.model_dir:
        lang = "LANG2"
    else:
        assert False, "language not in model directory name"

    fn = path.join(args.model_dir, "clusters_landmarks.pkl")
    print("Reading: " + fn)
    with open(fn, "rb") as f:
        unsup_transcript = pickle.load(f)
        unsup_landmarks = pickle.load(f)

    tokens = [] # (utt_label, start, end), e.g. ("s3803a", 413.97, 414.50)
    for utt in unsup_transcript:
        utt_label, interval = utt.split("_")
        utt_start, utt_end = interval.split("-")
        utt_start = int(utt_start)
        utt_end = int(utt_end)
        if args.cluster_id in unsup_transcript[utt]:
            indices = np.where(np.array(unsup_transcript[utt]) == args.cluster_id)[0]
            for token_start, token_end in np.array(unsup_landmarks[utt])[indices]:
                tokens.append(
                    (utt_label, float(utt_start + token_start)/100., float(utt_start + token_end)/100.)
                    )

    cat_zs2017_wavs(lang, tokens, path.join(args.model_dir, "pt" + str(args.cluster_id) + ".wav"), args.pad)


if __name__ == "__main__":
    main()
