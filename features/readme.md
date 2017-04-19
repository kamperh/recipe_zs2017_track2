Feature Extraction for ZeroSpeech2017
=====================================

MFCCs
-----

Move to the MFCC feature extraction directory:

    cd mfcc

Extract the MFCCs with CMVN and deltas and delta-delta features for the
different corpora and subsets.

Mandarin train:

    ./get_raw_htk.py mandarin train
    ./get_segments_scp.py mandarin train
    ./get_cmvn_dd_htk.py mandarin train
    mkdir mandarin_train/numpy
    ./write_htk_npz.py \ 
        mandarin_train/cmvn_dd mandarin_train/numpy/mfcc.cmvn_dd.npz

Mandarin test:

    ./get_raw_htk.py mandarin test
    ./get_segments_scp.py mandarin test
    ./get_cmvn_dd_htk.py mandarin test
    mkdir mandarin_test/numpy
    ./write_htk_npz.py \ 
        mandarin_test/cmvn_dd mandarin_test/numpy/mfcc.cmvn_dd.npz

French train:

    ./get_raw_htk.py french train
    ./get_segments_scp.py french train
    ./get_cmvn_dd_htk.py french train
    mkdir french_train/numpy
    ./write_htk_npz.py \ 
        french_train/cmvn_dd french_train/numpy/mfcc.cmvn_dd.npz

French test:

    ./get_raw_htk.py french test
    ./get_segments_scp.py french test
    ./get_cmvn_dd_htk.py french test
    mkdir french_test/numpy
    ./write_htk_npz.py \ 
        french_test/cmvn_dd french_test/numpy/mfcc.cmvn_dd.npz

English train:

    ./get_raw_htk.py english train
    ./get_segments_scp.py english train
    ./get_cmvn_dd_htk.py english train
    mkdir english_train/numpy
    ./write_htk_npz.py \ 
        english_train/cmvn_dd english_train/numpy/mfcc.cmvn_dd.npz

English test:

    ./get_raw_htk.py english test
    ./get_segments_scp.py english test
    ./get_cmvn_dd_htk.py english test
    mkdir english_test/numpy
    ./write_htk_npz.py \ 
        english_test/cmvn_dd english_test/numpy/mfcc.cmvn_dd.npz
