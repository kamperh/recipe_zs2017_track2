ABX Evaluation of Frame-Level Features
======================================


Evaluating MFCCs
----------------

This is an example of how extracted MFCCs (or other features) would be
evaluated:

    # Mandarin 1s
    ./npz_to_zs2017.py mfcc \
        ../../features/mfcc/mandarin_test/numpy/mfcc.cmvn_dd.npz
    ../../../src/zerospeech2017/track1/eval/eval_track1.py \
        --njobs 4 -n 1 \
        mandarin 1 ../../../src/zerospeech2017/data/ mfcc/mandarin/1s \
        mfcc.results/1s
    cat mfcc.results/mandarin/1s/results.txt

    # French 120s
    ./npz_to_zs2017.py mfcc \
        ../../features/mfcc/french_test/numpy/mfcc.cmvn_dd.npz
    ../../../src/zerospeech2017/track1/eval/eval_track1.py \
        --njobs 3 -n 1 \
        french 120 ../../../src/zerospeech2017/data/ mfcc/french/120s \
        mfcc.results/french/120s
    cat mfcc.results/french/120s/results.txt

    # English 10s
    ./npz_to_zs2017.py mfcc \
        ../../features/mfcc/english_test/numpy/mfcc.cmvn_dd.npz
    ../../../src/zerospeech2017/track1/eval/eval_track1.py \
        --njobs 3 -n 1 \
        english 10 ../../../src/zerospeech2017/data/ mfcc/english/10s \
        mfcc.results/english/10s
    cat mfcc.results/english/10s/results.txt
