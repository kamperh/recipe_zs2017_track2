#!/usr/bin/env python

"""
Get all the speaker-dependent data for this language.

Author: Herman Kamper
Contact: kamperh@gmail.com
Date: 
"""

from os import path
import argparse
import sys

import get_data_speaker

mandarin_speakers = [
    "A08", "A33", "A36", "B02", "B06", "B08", "C04", "C08", "C19", "D07", "D08", "D21"
    ]
french_speakers = [
    "F01", "F02", "F03", "F04", "F05", "F07", "F08", "F09", "F10", "M01",
    "M02", "M03", "M04", "M05", "M06", "M08", "M09"
    ]
english_speakers = [
    "s0019", "s0023", "s0055", "s0081", "s0107", "s0112", "s0580", "s0597",
    "s0925", "s1001", "s1392", "s1425", "s1463", "s1536", "s1724", "s1740",
    "s1769", "s2004", "s2299", "s2404", "s2517", "s2544", "s2628", "s2769",
    "s2785", "s3020", "s3046", "s3274", "s3389", "s3446", "s3448", "s3482",
    "s3914", "s4018", "s4057", "s4108", "s4222", "s4590", "s4629", "s4731",
    "s4899", "s5092", "s5093", "s5157", "s5278", "s5400", "s5583", "s5723",
    "s5727", "s5740", "s5968", "s6233", "s6454", "s6519", "s6544", "s6637",
    "s6683", "s6877", "s6993", "s7061", "s7313", "s7460", "s7540", "s7553",
    "s7730", "s7932", "s8075", "s8080", "s8713"
    ]


#-----------------------------------------------------------------------------#
#                              UTILITY FUNCTIONS                              #
#-----------------------------------------------------------------------------#

def check_argv():
    """Check the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0], add_help=False)
    parser.add_argument("lang", type=str, choices=["mandarin", "french", "english"], help="language")
    parser.add_argument("landmarks", type=str, choices=["unsup_syl"], help="landmarks set")
    parser.add_argument(
        "feature_type", type=str, help="input feature type",
        choices=["mfcc"]
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
#                                MAIN FUNCTION                                #
#-----------------------------------------------------------------------------#

def main():
    args = check_argv()

    if args.lang == "mandarin":
        speakers = mandarin_speakers
    elif args.lang == "french":
        speakers = french_speakers
    elif args.lang == "english":
        speakers = english_speakers

    data_dir = path.join(
        "data", args.lang, args.feature_type + ".n_" + str(args.n_samples) +
        ".n_max_" + str(args.n_landmarks_max) + "." + args.landmarks
        )
    print "Output directory:", data_dir

    for speaker in speakers:
        print
        get_data_speaker.get_data_speaker(speaker, data_dir)


if __name__ == "__main__":
    main()

