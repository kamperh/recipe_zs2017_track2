ZeroSpeech2017 Segmentation and Clustering using ESKMeans
=========================================================


Data pre-processing
-------------------

Format the data from the different languages into the input format used by
`eskmeans`:

    ./get_data_downsample.py mandarin unsup_syl mfcc 10
    ./get_data_downsample.py french unsup_syl mfcc 10
    ./get_data_downsample.py --n_landmarks_max 4 english unsup_syl mfcc 10

Get a subset of the data for a particular speaker:

    ./get_data_speaker.py data/mandarin/mfcc.n_10.unsup_syl/ A08

Get data for all the speakers individually:

    ./get_data_sd.py mandarin unsup_syl mfcc 10
    ./get_data_sd.py french unsup_syl mfcc 10
    ./get_data_sd.py --n_landmarks_max 4 english unsup_syl mfcc 10


Single-speaker segmentation and clustering
------------------------------------------

Perform unsupervised acoustic segmentation and clustering for specific speaker:

    ./ksegment.py data/mandarin/mfcc.n_10.n_max_6.unsup_syl/A08

Perform unsupervised acoustic segmentation individually but in parallel over
all speakers:

    # Mandarin (12 speakers)
    stdbuf -oL ./spawn_ksegment_sd.py \
        --min_duration 20 \
        --init_am_n_iter 0 \
        --segment_n_iter 10 \
        --n_slices_max 6 \
        --p_boundary_init 0.5 \
        data/mandarin/mfcc.n_10.n_max_6.unsup_syl
    # French (17 speakers)
    stdbuf -oL ./spawn_ksegment_sd.py \
        --min_duration 20 \
        --init_am_n_iter 0 \
        --segment_n_iter 10 \
        --n_slices_max 6 \
        data/french/mfcc.n_10.n_max_6.unsup_syl

    # English (69 speakers)
    stdbuf -oL ./spawn_ksegment_sd.py \
        --min_duration 20 \
        --init_am_n_iter 0 \
        --segment_n_iter 10 \
        --n_slices_max 4 \
        --p_boundary_init 1.0 \
        data/english/mfcc.n_10.n_max_4.unsup_syl

Perform ZeroSpeech2017 evaluation:

    # Mandarin
    source ~/zerospeech2017.sh 
    ./segment_sd_to_zs.py \
        kmodels/mandarin/mfcc.n_10.n_max_6.unsup_syl/sd_07f3103b5a/models.txt
    python ../../src/zerospeech2017/track2/bin/mandarin_eval2.py -j 5 \
        kmodels/mandarin/mfcc.n_10.n_max_6.unsup_syl/sd_07f3103b5a/classes.txt \
        kmodels/mandarin/mfcc.n_10.n_max_6.unsup_syl/sd_07f3103b5a/zs_results

    # French
    ./segment_sd_to_zs.py \
        kmodels/french/mfcc.n_10.n_max_6.unsup_syl/sd_39443ae63c/models.txt
    python ../../src/zerospeech2017/track2/bin/french_eval2.py -j 5 \
        kmodels/french/mfcc.n_10.n_max_6.unsup_syl/sd_39443ae63c/classes.txt \
        kmodels/french/mfcc.n_10.n_max_6.unsup_syl/sd_39443ae63c/zs_results

    # English
    ./segment_sd_to_zs.py \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/???/models.txt
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/???/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/???/zs_results




Speaker-independent segmentation and clustering
-----------------------------------------------

Perform unsupervised acoustic segmentation and clustering for all speakers:

    ./ksegment.py data/mandarin/mfcc.n_10.unsup_syl
    ./ksegment.py --n_cpus 3 --n_batches 5 --min_duration 25 \
        data/french/mfcc.n_10.unsup_syl


Perform ZeroSpeech2017 evaluation:

    ./segment_to_zs.py kmodels/mandarin/mfcc.n_10.unsup_syl/cfc7c0d053/
    python ../../src/zerospeech2017/track2/bin/mandarin_eval2.py \
        kmodels/mandarin/mfcc.n_10.unsup_syl/cfc7c0d053/classes.txt \
        kmodels/mandarin/mfcc.n_10.unsup_syl/cfc7c0d053/zs_results

    ./segment_to_zs.py kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a/
    python ../../src/zerospeech2017/track2/bin/french_eval2.py -j 5 \
        kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a/classes.txt \
        kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a/zs_results

    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/zs_results


Notebook
--------


Current best English systems:

    kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd  # ES-KMeans
    kmodels/english/mfcc.n_10.n_max_4.unsup_syl/244a01dd96  # ES-KMeans with min_duration 5
    kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360  # SylClust

Current best French systems:

    kmodels/french/mfcc.n_10.unsup_syl/60d1d79918  # ES-KMeans

Current best Mandarin systems:

    kmodels/mandarin/mfcc.n_10.unsup_syl/cfc7c0d053



    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 5 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\


Stuff to run:

    # English batch 1
    time ./ksegment.py --init_am_n_iter 10 --segment_n_iter 0 \
        --K_max 0.1landmarks \
        --p_boundary_init 1.0 data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --init_am_n_iter 5 --segment_n_iter 0 \
        --K_max 0.1landmarks \
        --p_boundary_init 1.0 data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 15 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 25 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.1landmarks --p_boundary_init 0 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.1landmarks --p_boundary_init 1.0 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\

    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360/zs_results [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915/zs_results  [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/zs_results  [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5/zs_results  [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0/zs_results  [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974/zs_results [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe/zs_results [done]
    ./segment_to_zs.py kmodels/english/mfcc.n_10.n_max_4.unsup_syl/244a01dd96
    python ../../src/zerospeech2017/track2/bin/english_eval2.py -j 5 \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/244a01dd96/classes.txt \
        kmodels/english/mfcc.n_10.n_max_4.unsup_syl/244a01dd96/zs_results




    # English/French batch 2
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.075landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.125landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.15landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\
    time ./ksegment.py --init_am_n_iter 10 --segment_n_iter 0 \
        --K_max 0.1landmarks \
        --p_boundary_init 1.0 data/french/mfcc.n_10.unsup_syl/ ;\
    time ./ksegment.py --init_am_n_iter 5 --segment_n_iter 0 \
        --K_max 0.1landmarks \
        --p_boundary_init 1.0 data/french/mfcc.n_10.unsup_syl/ ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.075landmarks --p_boundary_init 0.5 \
        data/french/mfcc.n_10.unsup_syl ;\
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.15landmarks --p_boundary_init 0.5 \
        data/french/mfcc.n_10.unsup_syl ;\    
    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.175landmarks --p_boundary_init 0.5 \
        data/french/mfcc.n_10.unsup_syl ;\




English systems:

    ./ksegment.py --init_am_n_iter 10 --segment_n_iter 0 \
        --K_max 0.1landmarks \
        --p_boundary_init 1.0 data/english/mfcc.n_10.n_max_4.unsup_syl/
    
    Iteration: 0, K: 28553, n_mean_updates: 432099, sample_time: 17723.9808681, sum_neg_sqrd_norm: -221302.743954
    Iteration: 1, K: 37010, n_mean_updates: 207950, sample_time: 17623.203171, sum_neg_sqrd_norm: -193902.17024
    Iteration: 2, K: 37267, n_mean_updates: 95632, sample_time: 17624.3310928, sum_neg_sqrd_norm: -183848.791848
    Iteration: 3, K: 37415, n_mean_updates: 53630, sample_time: 17611.6666858, sum_neg_sqrd_norm: -179572.230409
    Iteration: 4, K: 37439, n_mean_updates: 32980, sample_time: 17610.6534901, sum_neg_sqrd_norm: -177305.039292
    Iteration: 5, K: 37452, n_mean_updates: 21646, sample_time: 17610.1753099, sum_neg_sqrd_norm: -175980.925447
    Iteration: 6, K: 37464, n_mean_updates: 14445, sample_time: 17618.9378319, sum_neg_sqrd_norm: -175164.927895
    Iteration: 7, K: 37468, n_mean_updates: 9900, sample_time: 17628.7709892, sum_neg_sqrd_norm: -174637.860406
    Iteration: 8, K: 37472, n_mean_updates: 6889, sample_time: 17622.021414, sum_neg_sqrd_norm: -174291.797323
    Iteration: 9, K: 37476, n_mean_updates: 5087, sample_time: 17620.151252, sum_neg_sqrd_norm: -174040.51633
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360/am_init_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/3f79f6a360

    ./ksegment.py --init_am_n_iter 5 --segment_n_iter 0 \
        --K_max 0.1landmarks \
        --p_boundary_init 1.0 data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\    
    
    Iteration: 0, K: 28553, n_mean_updates: 432099, sample_time: 17428.3613369, sum_neg_sqrd_norm: -221302.743954
    Iteration: 1, K: 37010, n_mean_updates: 207950, sample_time: 17534.9937341, sum_neg_sqrd_norm: -193902.17024
    Iteration: 2, K: 37267, n_mean_updates: 95632, sample_time: 17521.462605, sum_neg_sqrd_norm: -183848.791848
    Iteration: 3, K: 37415, n_mean_updates: 53630, sample_time: 17520.2850242, sum_neg_sqrd_norm: -179572.230409
    Iteration: 4, K: 37439, n_mean_updates: 32980, sample_time: 17526.5748839, sum_neg_sqrd_norm: -177305.039292
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915/am_init_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/4f87868915
    2017-05-05 19:14:23.488762

    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\

    Iteration: 0, components: 39564, n_tokens: 307586, sample_time: 5918.79882097, sum_neg_len_sqrd_norm: -6186509.97975, sum_neg_sqrd_norm: -140423.095459
    Iteration: 1, components: 41874, n_tokens: 307642, sample_time: 5895.50119996, sum_neg_len_sqrd_norm: -4773977.74284, sum_neg_sqrd_norm: -130929.357341
    Iteration: 2, components: 42006, n_tokens: 308088, sample_time: 5856.49252701, sum_neg_len_sqrd_norm: -4597068.15149, sum_neg_sqrd_norm: -128792.762331
    Iteration: 3, components: 42028, n_tokens: 308257, sample_time: 5912.94000602, sum_neg_len_sqrd_norm: -4534301.44997, sum_neg_sqrd_norm: -127971.213104
    Iteration: 4, components: 42035, n_tokens: 308351, sample_time: 5818.37356114, sum_neg_len_sqrd_norm: -4507502.01466, sum_neg_sqrd_norm: -127578.288629
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/segmenter_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/cb92e6b0dd

    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 15 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\

    Iteration: 0, components: 40167, n_tokens: 357221, sample_time: 6134.18926907, sum_neg_len_sqrd_norm: -5933065.63193, sum_neg_sqrd_norm: -160777.129501
    Iteration: 1, components: 42312, n_tokens: 358038, sample_time: 6171.34754491, sum_neg_len_sqrd_norm: -4647322.04386, sum_neg_sqrd_norm: -149033.657978
    Iteration: 2, components: 42461, n_tokens: 358637, sample_time: 6151.74270511, sum_neg_len_sqrd_norm: -4454023.42214, sum_neg_sqrd_norm: -146154.798737
    Iteration: 3, components: 42474, n_tokens: 358936, sample_time: 6028.67658997, sum_neg_len_sqrd_norm: -4382533.0921, sum_neg_sqrd_norm: -145022.780514
    Iteration: 4, components: 42481, n_tokens: 359075, sample_time: 6062.94544792, sum_neg_len_sqrd_norm: -4350036.25265, sum_neg_sqrd_norm: -144438.219258
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5/segmenter_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/b0a1ef19f5

    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 25 --K_max 0.1landmarks --p_boundary_init 0.5 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\

     an integer will result in an error in the future
      sum_neg_len_sqrd_norm += vec_embed_neg_len_sqrd_norms[i + t - k]
    ../../src/eskmeans/eskmeans/eskmeans_wordseg.py:644: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
      q_t = (vec_embed_neg_len_sqrd_norms[i:i + t][-n_slices_max:] + gammas[:t][-n_slices_max:])
    ../../src/eskmeans/eskmeans/eskmeans_wordseg.py:657: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
      sum_neg_len_sqrd_norm += vec_embed_neg_len_sqrd_norms[i + t - k]
    ../../src/eskmeans/eskmeans/eskmeans_wordseg.py:644: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
      q_t = (vec_embed_neg_len_sqrd_norms[i:i + t][-n_slices_max:] + gammas[:t][-n_slices_max:])
    ../../src/eskmeans/eskmeans/eskmeans_wordseg.py:657: VisibleDeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
      sum_neg_len_sqrd_norm += vec_embed_neg_len_sqrd_norms[i + t - k]
    Iteration: 4, components: 41339, n_tokens: 265521, sample_time: 5632.44517303, sum_neg_len_sqrd_norm: -4661263.51637, sum_neg_sqrd_norm: -113126.944253
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0/segmenter_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/7bbe8538a0

    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.1landmarks --p_boundary_init 0 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\

    Iteration: 0, components: 43700, n_tokens: 280271, sample_time: 5806.77883196, sum_neg_len_sqrd_norm: -5305400.93966, sum_neg_sqrd_norm: -122234.90835
    Iteration: 1, components: 43732, n_tokens: 281551, sample_time: 5787.66154385, sum_neg_len_sqrd_norm: -4283753.59743, sum_neg_sqrd_norm: -118128.685594
    Iteration: 2, components: 43734, n_tokens: 281841, sample_time: 5722.83464885, sum_neg_len_sqrd_norm: -4202855.12225, sum_neg_sqrd_norm: -117313.179393
    Iteration: 3, components: 43734, n_tokens: 281984, sample_time: 5787.097682, sum_neg_len_sqrd_norm: -4176255.26025, sum_neg_sqrd_norm: -116970.894309
    Iteration: 4, components: 43734, n_tokens: 282057, sample_time: 5759.17280006, sum_neg_len_sqrd_norm: -4164228.69236, sum_neg_sqrd_norm: -116785.95461
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974/segmenter_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/ffdafe0974

    time ./ksegment.py --segment_n_iter 5 --n_cpus 15 --n_batches 5 \
        --min_duration 20 --K_max 0.1landmarks --p_boundary_init 1.0 \
        data/english/mfcc.n_10.n_max_4.unsup_syl/ ;\

    Iteration: 0, components: 34498, n_tokens: 318426, sample_time: 5960.34613109, sum_neg_len_sqrd_norm: -6475851.42718, sum_neg_sqrd_norm: -151658.878299
    Iteration: 1, components: 39741, n_tokens: 315761, sample_time: 5964.75847292, sum_neg_len_sqrd_norm: -4977390.34675, sum_neg_sqrd_norm: -137070.42497
    Iteration: 2, components: 40125, n_tokens: 316138, sample_time: 5859.00084615, sum_neg_len_sqrd_norm: -4747924.76596, sum_neg_sqrd_norm: -133911.533203
    Iteration: 3, components: 40155, n_tokens: 316222, sample_time: 5855.11993694, sum_neg_len_sqrd_norm: -4663957.03663, sum_neg_sqrd_norm: -132773.367294
    Iteration: 4, components: 40171, n_tokens: 316279, sample_time: 5876.59489393, sum_neg_len_sqrd_norm: -4629762.13318, sum_neg_sqrd_norm: -132225.439337
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe/segmenter_record_dict.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe/clusters_landmarks.pkl
    Writing: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe/eskmeans.pkl
    Model directory: kmodels/english/mfcc.n_10.n_max_4.unsup_syl/49cd4f07fe













Best Mandarin system:

    ./ksegment.py --K_max 0.2landmarks --n_cpus 2 --n_batches 5 \
        --min_duration 20 --p_boundary_init 0 --segment_n_iter 10 \
        data/mandarin/mfcc.n_10.unsup_syl
    cat kmodels/mandarin/mfcc.n_10.unsup_syl/cfc7c0d053/zs_results/token_type


No. initial embeddings: 298189
Segmenting for 1 iterations
Iteration: 0, components: 13591, n_tokens: 208644, sample_time: 8916.15953994, sum_neg_len_sqrd_norm: -4385166.46953,
 sum_neg_sqrd_norm: -113237.763268
Writing: kmodels/french/mfcc.n_10.unsup_syl/b4e7a6710e/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/b4e7a6710e/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/b4e7a6710e/eskmeans.pkl
Model directory: kmodels/french/mfcc.n_10.unsup_syl/b4e7a6710e
2017-04-24 11:59:37.803434


Iteration: 0, components: 26489, n_tokens: 210912, sample_time: 16749.2878389, sum_neg_len_sqrd_norm: -4080566.61122,
 sum_neg_sqrd_norm: -98570.2636696
Iteration: 1, components: 28236, n_tokens: 209714, sample_time: 16728.386955, sum_neg_len_sqrd_norm: -3252688.20725, 
sum_neg_sqrd_norm: -89943.1785606
Iteration: 2, components: 28290, n_tokens: 209887, sample_time: 16731.1071131, sum_neg_len_sqrd_norm: -3101172.90784,
 sum_neg_sqrd_norm: -88263.6023048
Iteration: 3, components: 28300, n_tokens: 209955, sample_time: 16726.3749251, sum_neg_len_sqrd_norm: -3055405.76783,
 sum_neg_sqrd_norm: -87690.3744684
Iteration: 4, components: 28301, n_tokens: 209971, sample_time: 16726.2307692, sum_neg_len_sqrd_norm: -3037321.21072,
 sum_neg_sqrd_norm: -87419.7513688
Writing: kmodels/french/mfcc.n_10.unsup_syl/732d46d73d/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/732d46d73d/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/732d46d73d/eskmeans.pkl
Model directory: kmodels/french/mfcc.n_10.unsup_syl/732d46d73d


Iteration: 0, components: 29804, n_tokens: 154168, sample_time: 6821.217098, sum_neg_len_sqrd_norm: -3160160.3114, sum_neg_sqrd_norm: -69656.6486212
Iteration: 1, components: 29810, n_tokens: 159738, sample_time: 6962.86025786, sum_neg_len_sqrd_norm: -2648942.16415, sum_neg_sqrd_norm: -69408.5392839
Iteration: 2, components: 29810, n_tokens: 160639, sample_time: 6836.6015799, sum_neg_len_sqrd_norm: -2581394.36492, sum_neg_sqrd_norm: -69039.0538447
Iteration: 3, components: 29810, n_tokens: 161030, sample_time: 6844.37515903, sum_neg_len_sqrd_norm: -2556893.30162, sum_neg_sqrd_norm: -68856.36665
Iteration: 4, components: 29810, n_tokens: 161213, sample_time: 6905.31135201, sum_neg_len_sqrd_norm: -2545068.11074, sum_neg_sqrd_norm: -68722.0268515
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/eskmeans.pkl
Model directory: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543



(zerospeech) kamperh@cpu18:.../zerospeech/zs2017/segmentation (master)$ time ./ksegment.py --segment_n_iter 5  --n_cp
us 15 --n_batches 5 --min_duration 20  --K_max 0.1landmarks         data/french/mfcc.n_10.unsup_syl
2017-04-25 15:08:20.001832
Writing: kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab/options_dict.pkl 
Options: {'init_am_n_iter': 0, 'data_dir': 'data/french/mfcc.n_10.unsup_syl', 'model_dir': 'kmodels/french/mfcc.n_10.
unsup_syl', 'segment_n_iter': 5, 'seed_assignments': None, 'p_boundary_init': 1.0, 'n_slices_max': 6, 'rnd_seed': 42,
 'seed_bounds': None, 'min_duration': 20, 'K_max': '0.1landmarks', 'init_am_assignments': 'spread', 'n_slices_min': 0
, 'n_batches': 5, 'wip': 0, 'n_iter_inbetween_kmeans': 0, 'n_cpus': 15} 
Reading from directory: data/french/mfcc.n_10.unsup_syl
No. of utterances: 51263
No. of landmarks: 298189
K_max: 29818
Embedding dimensionality: 130
2017-04-25 15:09:55.305533
Normalizing embeddings
No. of embeddings: 1150350
Setting up model
Initializing boundaries randomly with probability 1.0
No. initial embeddings: 298189
Segmenting for 5 iterations
Iteration: 0, components: 23572, n_tokens: 209510, sample_time: 6147.85276008, sum_neg_len_sqrd_norm: -4297864.40332,
 sum_neg_sqrd_norm: -100143.619345
Iteration: 1, components: 27023, n_tokens: 206764, sample_time: 6146.85840917, sum_neg_len_sqrd_norm: -3247229.33718,
 sum_neg_sqrd_norm: -89577.6922023
Iteration: 2, components: 27230, n_tokens: 207098, sample_time: 6053.23769689, sum_neg_len_sqrd_norm: -3088374.69555,
 sum_neg_sqrd_norm: -87534.8382889
Iteration: 3, components: 27255, n_tokens: 207217, sample_time: 6155.89046788, sum_neg_len_sqrd_norm: -3032496.8042, 
sum_neg_sqrd_norm: -86801.6762043
Iteration: 4, components: 27258, n_tokens: 207266, sample_time: 6136.83060193, sum_neg_len_sqrd_norm: -3009504.64501,
 sum_neg_sqrd_norm: -86454.1039305
Writing: kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab/eskmeans.pkl
Model directory: kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab



(zerospeech) kamperh@cpu18:.../zerospeech/zs2017/segmentation (master)$     python ../../src/zerospeech2017/track2/bin/french_eval2.py -j 5 \
>         kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab/classes.txt \
>         kmodels/french/mfcc.n_10.unsup_syl/bd6a3457ab/zs_results
(zerospeech) kamperh@cpu18:.../zerospeech/zs2017/segmentation (master)$
(zerospeech) kamperh@cpu18:.../zerospeech/zs2017/segmentation (master)$ time ./ksegment.py --segment_n_iter 5  --n_cpus 15 --n_batches 5 --min_duration 20  --K_max 0.1landmarks  --p_boundary_init 0 data/french/mfcc.n_10.unsup_syl     2017-04-26 09:38:36.115774
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/options_dict.pkl
Options: {'init_am_n_iter': 0, 'data_dir': 'data/french/mfcc.n_10.unsup_syl', 'model_dir': 'kmodels/french/mfcc.n_10.unsup_syl', 'segment_n_iter': 5, 'seed_assignments': None, 'p_boundary_init': 0.0, 'n_slices_max': 6, 'rnd_seed': 42, 'seed_bounds': None, 'min_duration': 20, 'K_max': '0.1landmarks', 'init_am_assignments': 'spread', 'n_slices_min': 0, 'n_batches': 5, 'wip': 0, 'n_iter_inbetween_kmeans': 0, 'n_cpus': 15}
Reading from directory: data/french/mfcc.n_10.unsup_syl
No. of utterances: 51263
No. of landmarks: 298189
K_max: 29818
Embedding dimensionality: 130
2017-04-26 09:40:12.715790
Normalizing embeddings
No. of embeddings: 1150350
Setting up model
Initializing boundaries at start and end of utterance
No. initial embeddings: 33606
Segmenting for 5 iterations
Iteration: 0, components: 29804, n_tokens: 154168, sample_time: 6821.217098, sum_neg_len_sqrd_norm: -3160160.3114, sum_neg_sqrd_norm: -69656.6486212
Iteration: 1, components: 29810, n_tokens: 159738, sample_time: 6962.86025786, sum_neg_len_sqrd_norm: -2648942.16415, sum_neg_sqrd_norm: -69408.5392839
Iteration: 2, components: 29810, n_tokens: 160639, sample_time: 6836.6015799, sum_neg_len_sqrd_norm: -2581394.36492, sum_neg_sqrd_norm: -69039.0538447
Iteration: 3, components: 29810, n_tokens: 161030, sample_time: 6844.37515903, sum_neg_len_sqrd_norm: -2556893.30162, sum_neg_sqrd_norm: -68856.36665
Iteration: 4, components: 29810, n_tokens: 161213, sample_time: 6905.31135201, sum_neg_len_sqrd_norm: -2545068.11074, sum_neg_sqrd_norm: -68722.0268515
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/eskmeans.pkl
Model directory: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543
2017-04-26 19:17:17.847349
real    578m43.071s
user    2169m3.149s
sys     1544m8.771s
(zerospeech) kamperh@cpu18:.../zerospeech/zs2017/segmentation (master)$     ./segment_to_zs.py kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/
Reading: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/classes.txt
No. of classes: 29810
No. of tokens: 161213
(zerospeech) kamperh@cpu18:.../zerospeech/zs2017/segmentation (master)$     python ../../src/zerospeech2017/track2/bin/french_eval2.py -j 5 \
>         kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/classes.txt \
>         kmodels/french/mfcc.n_10.unsup_syl/4b0126a543/zs_results



time ./ksegment.py --segment_n_iter 5  --n_cpus 15 --n_batches 5 --min_duration 20  --K_max 0.1landmarks  --p_boundary_init 0.5 data/french/mfcc.n_10.unsup_syl
Iteration: 0, components: 27080, n_tokens: 200525, sample_time: 7102.03651094, sum_neg_len_sqrd_norm: -4094404.61365, sum_neg_sqrd_norm: -91468.3405446
Iteration: 1, components: 28486, n_tokens: 200531, sample_time: 7041.81788206, sum_neg_len_sqrd_norm: -3110262.36442, sum_neg_sqrd_norm: -85003.7072579
Iteration: 2, components: 28591, n_tokens: 200903, sample_time: 7028.81323123, sum_neg_len_sqrd_norm: -2985409.40198, sum_neg_sqrd_norm: -83586.6385353
Iteration: 3, components: 28604, n_tokens: 201073, sample_time: 7087.66660094, sum_neg_len_sqrd_norm: -2942568.89123, sum_neg_sqrd_norm: -83064.4836057
Iteration: 4, components: 28610, n_tokens: 201149, sample_time: 7147.23621416, sum_neg_len_sqrd_norm: -2924661.53784, sum_neg_sqrd_norm: -82825.8817849
Writing: kmodels/french/mfcc.n_10.unsup_syl/60d1d79918/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/60d1d79918/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/60d1d79918/eskmeans.pkl
*** Model directory: kmodels/french/mfcc.n_10.unsup_syl/60d1d79918




Iteration: 0, components: 27080, n_tokens: 200525, sample_time: 7106.17595911, sum_neg_len_sqrd_norm: -4094404.61365, sum_neg_sqrd_norm: -91468.3405446
Iteration: 1, components: 28486, n_tokens: 200531, sample_time: 6924.30537105, sum_neg_len_sqrd_norm: -3110262.36442, sum_neg_sqrd_norm: -85003.7072579
Iteration: 2, components: 28591, n_tokens: 200903, sample_time: 6934.17604804, sum_neg_len_sqrd_norm: -2985409.40198, sum_neg_sqrd_norm: -83586.6385353
Iteration: 3, components: 28604, n_tokens: 201073, sample_time: 6981.82736683, sum_neg_len_sqrd_norm: -2942568.89123, sum_neg_sqrd_norm: -83064.4836057
Iteration: 4, components: 28610, n_tokens: 201149, sample_time: 7022.46911311, sum_neg_len_sqrd_norm: -2924661.53784, sum_neg_sqrd_norm: -82825.8817849
Iteration: 5, components: 28610, n_tokens: 201179, sample_time: 6938.20119405, sum_neg_len_sqrd_norm: -2916178.5909, sum_neg_sqrd_norm: -82695.4346624
Iteration: 6, components: 28611, n_tokens: 201210, sample_time: 6938.78359795, sum_neg_len_sqrd_norm: -2911656.95018, sum_neg_sqrd_norm: -82621.2479643
Iteration: 7, components: 28611, n_tokens: 201229, sample_time: 7224.77944207, sum_neg_len_sqrd_norm: -2908723.00064, sum_neg_sqrd_norm: -82574.8900493
Iteration: 8, components: 28611, n_tokens: 201241, sample_time: 6993.54714108, sum_neg_len_sqrd_norm: -2906919.79696, sum_neg_sqrd_norm: -82546.873275
Iteration: 9, components: 28611, n_tokens: 201245, sample_time: 7001.05689812, sum_neg_len_sqrd_norm: -2905782.81373, sum_neg_sqrd_norm: -82525.4454977
Iteration: 10, components: 28612, n_tokens: 201250, sample_time: 7088.26522207, sum_neg_len_sqrd_norm: -2905046.00738, sum_neg_sqrd_norm: -82513.6433795
Iteration: 11, components: 28612, n_tokens: 201253, sample_time: 7034.30847502, sum_neg_len_sqrd_norm: -2904576.70731, sum_neg_sqrd_norm: -82504.7797078
Iteration: 12, components: 28612, n_tokens: 201251, sample_time: 6714.94862008, sum_neg_len_sqrd_norm: -2904198.92447, sum_neg_sqrd_norm: -82493.8238575
Iteration: 13, components: 28613, n_tokens: 201251, sample_time: 7014.42559314, sum_neg_len_sqrd_norm: -2903907.35167, sum_neg_sqrd_norm: -82488.1745821
Iteration: 14, components: 28613, n_tokens: 201255, sample_time: 6835.20025396, sum_neg_len_sqrd_norm: -2903727.33065, sum_neg_sqrd_norm: -82485.7935821
Writing: kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a/segmenter_record_dict.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a/clusters_landmarks.pkl
Writing: kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a/eskmeans.pkl
Model directory: kmodels/french/mfcc.n_10.unsup_syl/b2ff1e967a



