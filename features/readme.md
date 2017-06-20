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

Lang1 train:

    ./get_raw_htk.py LANG1 train
    ./get_segments_scp.py LANG1 train
    ./get_cmvn_dd_htk.py LANG1 train
    mkdir LANG1_train/numpy
    ./write_htk_npz.py \
        LANG1_train/cmvn_dd LANG1_train/numpy/mfcc.cmvn_dd.npz

Lang2 train:

    # Fix VADs first
    ./get_raw_htk.py LANG2 train
    ./get_segments_scp.py LANG2 train
    ./get_cmvn_dd_htk.py LANG2 train
    mkdir LANG2_train/numpy
    ./write_htk_npz.py \
        LANG2_train/cmvn_dd LANG2_train/numpy/mfcc.cmvn_dd.npz


Okko features
-------------
Move to the directory:

    cd okko0

Mandarin train:

    mkdir mandarin_train
    ./okko_to_npz.py \
        /scratch/okko_zerospeech/features_to_Herman/mandarin/10s/feats.mat \
        mandarin_train/full_audio.npz
    ./get_npz_keys.py \
        ../mfcc/mandarin_train/numpy/mfcc.cmvn_dd.npz \
        mandarin_train/segments.txt
    ./get_segments_from_npz.py \
        mandarin_train/full_audio.npz \
        mandarin_train/segments.txt \
        mandarin_train/segments.npz


French train:

    mkdir french_train
    ./okko_to_npz.py \
        /scratch/okko_zerospeech/features_to_Herman/french/10s/feats.mat \
        french_train/full_audio.npz
    ./get_npz_keys.py \
        ../mfcc/french_train/numpy/mfcc.cmvn_dd.npz \
        french_train/segments.txt
    ./get_segments_from_npz.py \
        french_train/full_audio.npz \
        french_train/segments.txt \
        french_train/segments.npz

English train:

    mkdir english_train
    ./okko_to_npz.py \
        /scratch/okko_zerospeech/features_to_herman_v2/english/10s/feats.mat \
        english_train/full_audio.npz
    ./get_npz_keys.py \
        ../mfcc/english_train/numpy/mfcc.cmvn_dd.npz \
        english_train/segments.txt
    ./get_segments_from_npz.py \
        english_train/full_audio.npz \
        english_train/segments.txt \
        english_train/segments.npz


Lang1 train:

    mkdir LANG1_train
    ./okko_to_npz.py \
        /scratch/okko_zerospeech/features_to_herman_v2/LANG1/10s/feats.mat \
        LANG1_train/full_audio.npz
    ./get_npz_keys.py \
        ../mfcc/LANG1_train/numpy/mfcc.cmvn_dd.npz \
        LANG1_train/segments.txt
    ./get_segments_from_npz.py \
        LANG1_train/full_audio.npz \
        LANG1_train/segments.txt \
        LANG1_train/segments.npz


Lang2 train:

    mkdir LANG2_train
    ./okko_to_npz.py \
        /scratch/okko_zerospeech/features_to_herman_v2/LANG2/10s/feats.mat \
        LANG2_train/full_audio.npz
    ./get_npz_keys.py \
        ../mfcc/LANG2_train/numpy/mfcc.cmvn_dd.npz \
        LANG2_train/segments.txt
    ./get_segments_from_npz.py \
        LANG2_train/full_audio.npz \
        LANG2_train/segments.txt \
        LANG2_train/segments.npz
