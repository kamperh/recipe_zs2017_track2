ZeroSpeech2017 Segmentation and Clustering using ESKMeans
=========================================================


Data pre-processing
-------------------
Format the data from the different languages into the input format used by
`eskmeans`:

    # MFCCs
    ./get_data_downsample.py mandarin unsup_syl mfcc 10
    ./get_data_downsample.py --n_landmarks_max 4 mandarin unsup_syl mfcc 10
    ./get_data_downsample.py french unsup_syl mfcc 10
    ./get_data_downsample.py --n_landmarks_max 4 french unsup_syl mfcc 10
    ./get_data_downsample.py --n_landmarks_max 4 english unsup_syl mfcc 10
    ./get_data_downsample.py --n_landmarks_max 4 LANG1 unsup_syl mfcc 10
    ./get_data_downsample.py --n_landmarks_max 4 LANG2 unsup_syl mfcc 10

    # Okko's features
    ./get_data_downsample.py --n_landmarks_max 4 mandarin unsup_syl okko0 10
    ./get_data_downsample.py --n_landmarks_max 4 french unsup_syl okko0 10
    ./get_data_downsample.py --n_landmarks_max 4 english unsup_syl okko0 10
    ./get_data_downsample.py --n_landmarks_max 4 LANG1 unsup_syl okko0 10
    ./get_data_downsample.py --n_landmarks_max 4 LANG2 unsup_syl okko0 10

Get a subset of the data for a particular speaker:

    ./get_data_speaker.py data/mandarin/mfcc.n_10.unsup_syl/ A08

Get data for all the speakers individually:

    ./get_data_sd.py mandarin unsup_syl mfcc 10
    ./get_data_sd.py --n_landmarks_max 4 mandarin unsup_syl mfcc 10
    ./get_data_sd.py french unsup_syl mfcc 10
    ./get_data_sd.py --n_landmarks_max 4 french unsup_syl mfcc 10
    ./get_data_sd.py --n_landmarks_max 4 english unsup_syl mfcc 10


Single-speaker segmentation and clustering
------------------------------------------
Perform unsupervised acoustic segmentation and clustering for specific speaker:

    ./ksegment.py data/mandarin/mfcc.n_10.n_max_6.unsup_syl/A08

Perform unsupervised acoustic segmentation individually but in parallel over
all speakers:

    # Mandarin (12 speakers)
    stdbuf -oL ./spawn_ksegment_sd.py \
        --K_max 0.2landmarks \
        --min_duration 20 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.0 \
        data/mandarin/mfcc.n_10.n_max_4.unsup_syl
    # French (17 speakers)
    stdbuf -oL ./spawn_ksegment_sd.py \
        --min_duration 20 \
        --init_am_n_iter 0 \
        --segment_n_iter 10 \
        --n_slices_max 6 \
        data/french/mfcc.n_10.n_max_6.unsup_syl

    # English (69 speakers)
    time stdbuf -oL ./spawn_ksegment_sd.py \
        --K_max 0.2landmarks \
        --min_duration 20 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.0 \
        data/english/mfcc.n_10.n_max_4.unsup_syl

Perform ZeroSpeech2017 evaluation:

    # Mandarin
    ./segment_sd_to_zs.py \
        kmodels/mandarin/mfcc.n_10.n_max_4.unsup_syl/sd_548e240e99/models.txt
    python ../../src/zerospeech2017/track2/bin/mandarin_eval2.py -j 5 \
        kmodels/mandarin/mfcc.n_10.n_max_4.unsup_syl/sd_548e240e99/classes.txt \
        kmodels/mandarin/mfcc.n_10.n_max_4.unsup_syl/sd_548e240e99/zs_results

    # French
    ./segment_sd_to_zs.py \
        kmodels/french/mfcc.n_10.n_max_6.unsup_syl/sd_39443ae63c/models.txt
    python ../../src/zerospeech2017/track2/bin/french_eval2.py -j 5 \
        kmodels/french/mfcc.n_10.n_max_6.unsup_syl/sd_39443ae63c/classes.txt \
        kmodels/french/mfcc.n_10.n_max_6.unsup_syl/sd_39443ae63c/zs_results

    # English
    ./segment_sd_to_zs.py \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/sd_f2bbb86933/models.txt
    time python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/sd_f2bbb86933/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/sd_f2bbb86933/zs_results



Speaker-independent segmentation and clustering
-----------------------------------------------
Perform unsupervised acoustic segmentation and clustering for all speakers:

    # Mandarin
    ./ksegment.py data/mandarin/mfcc.n_10.n_max_6.unsup_syl
    ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 0 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/mandarin/okko0.n_10.n_max_4.unsup_syl
    ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 0 \
        --init_am_n_iter 10 \
        --segment_n_iter 0 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/mandarin/mfcc.n_10.n_max_4.unsup_syl
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/mandarin/okko0.n_10.n_max_4.unsup_syl/

    # French
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.5 \
        --n_cpus 15 \
        --n_batches 5 \
        data/french/mfcc.n_10.n_max_4.unsup_syl; time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/french/mfcc.n_10.n_max_4.unsup_syl; time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/french/mfcc.n_10.n_max_4.unsup_syl

    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 0 \
        --init_am_n_iter 5 \
        --segment_n_iter 0 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 1 \
        data/french/mfcc.n_10.n_max_4.unsup_syl; time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 0 \
        --init_am_n_iter 10 \
        --segment_n_iter 0 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 1 \
        data/french/mfcc.n_10.n_max_4.unsup_syl;

    # French: Okko's features
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 10 \
        --n_batches 5 \
        data/french/okko0.n_10.n_max_4.unsup_syl/


    # English
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl; time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl

    # English: Okko's features
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        --n_cpus 15 \
        --n_batches 5 \
        data/english/okko0.n_10.n_max_4.unsup_syl/

    # LANG1: MFCC
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.5 \
        --n_cpus 15 \
        --n_batches 5 \
        data/LANG1/mfcc.n_10.n_max_4.unsup_syl/

    # LANG1: Okko's features
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.5 \
        --n_cpus 15 \
        --n_batches 5 \
        data/LANG1/okko0.n_10.n_max_4.unsup_syl/

    # LANG2: MFCC
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.5 \
        --n_cpus 15 \
        --n_batches 5 \
        data/LANG2/mfcc.n_10.n_max_4.unsup_syl/

    # LANG2: Okko's features
    time ./ksegment.py \
        --K_max 0.1landmarks \
        --min_duration 5 \
        --init_am_n_iter 0 \
        --segment_n_iter 5 \
        --n_slices_max 4 \
        --p_boundary_init 0.5 \
        --n_cpus 15 \
        --n_batches 5 \
        data/LANG2/okko0.n_10.n_max_4.unsup_syl/

Perform ZeroSpeech2017 evaluation:

    ./segment_to_zs.py kmodels/mandarin/okko0.n_10.n_max_4.unsup_syl/45c0db0496/
    time python ../../src/zerospeech2017/track2/bin/mandarin_eval2.py \
        kmodels/mandarin/okko0.n_10.n_max_4.unsup_syl/45c0db0496/classes.txt \
        kmodels/mandarin/okko0.n_10.n_max_4.unsup_syl/45c0db0496/zs_results

    ./segment_to_zs.py kmodels/french/okko0.n_10.n_max_4.unsup_syl/6fac9cf55b/
    time python ../../src/zerospeech2017/track2/bin/french_eval2.py -j 10 \
        kmodels/french/okko0.n_10.n_max_4.unsup_syl/6fac9cf55b/classes.txt \
        kmodels/french/okko0.n_10.n_max_4.unsup_syl/6fac9cf55b/zs_results

    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/e1c019ed29/
    time python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/e1c019ed29/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/e1c019ed29/zs_results

    # LANG1
    ./segment_to_zs.py kmodels/LANG1/mfcc.n_10.n_max_4.unsup_syl/779ab9f219

    # LANG2
    ./segment_to_zs.py kmodels/LANG2/mfcc.n_10.n_max_4.unsup_syl/feb986626a


Packaging the results for ZeroSpeech2017 challenge evaluation
-------------------------------------------------------------
The final systems for submission are:

    kmodels/mandarin/mfcc.n_10.n_max_4.unsup_syl/f764a7a56d/
    kmodels/french/mfcc.n_10.n_max_4.unsup_syl/4f71f9796b/
    kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cf360cf9da/
    kmodels/LANG1/mfcc.n_10.n_max_4.unsup_syl/779ab9f219/
    kmodels/LANG2/mfcc.n_10.n_max_4.unsup_syl/feb986626a/


