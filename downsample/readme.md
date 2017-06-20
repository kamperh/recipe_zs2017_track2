Downsampled Acoustic Word Embeddings
====================================

Creating the output directories:

    mkdir -p embeddings/mandarin_train
    mkdir -p embeddings/french_train
    mkdir -p embeddings/english_train
    mkdir -p embeddings/LANG1_train
    mkdir -p embeddings/LANG2_train

Perform the unsupervised syllable segmentation. Link the landmarks from the
unsupervised syllable segmentation:

    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zs2017/syllables/landmarks/mandarin_train/landmarks.unsup_syl.pkl \
        embeddings/mandarin_train/
    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zs2017/syllables/landmarks/french_train/landmarks.unsup_syl.pkl \
        embeddings/french_train/
    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zs2017/syllables/landmarks/english_train/landmarks.unsup_syl.pkl \
        embeddings/english_train/
    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zs2017/syllables/landmarks/LANG1_train/landmarks.unsup_syl.pkl \
        embeddings/LANG1_train/
    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zs2017/syllables/landmarks/LANG2_train/landmarks.unsup_syl.pkl \
        embeddings/LANG2_train/

Get the segmentation intervals over the landmarks:

    ./get_seglist.py mandarin train unsup_syl
    ./get_seglist.py --n_landmarks_max 4 mandarin train unsup_syl
    ./get_seglist.py french train unsup_syl
    ./get_seglist.py --n_landmarks_max 4 french train unsup_syl
    ./get_seglist.py --n_landmarks_max 4 english train unsup_syl
    ./get_seglist.py --n_landmarks_max 4 LANG1 train unsup_syl
    ./get_seglist.py --n_landmarks_max 4 LANG2 train unsup_syl

Get the dense embeddings over the segmentation intervals:

    # MFCCs
    ./downsample_dense.py --frame_dims 13 mandarin train unsup_syl mfcc
    ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 mandarin train unsup_syl mfcc
    ./downsample_dense.py --frame_dims 13 french train unsup_syl mfcc
    ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 french train unsup_syl mfcc
    ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 english train unsup_syl mfcc
    ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 LANG1 train unsup_syl mfcc
    ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 LANG2 train unsup_syl mfcc

    # Okko's features
    ./downsample_dense.py --n_landmarks_max 4 --n 10 mandarin train unsup_syl okko0
    # ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13  mandarin train unsup_syl okko0
    # ./downsample_dense.py --n_landmarks_max 4 --n 10 french train unsup_syl okko0
    ./downsample_dense.py --n_landmarks_max 4 --n 10 french train unsup_syl okko0
    # ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 english train unsup_syl okko0
    ./downsample_dense.py --n_landmarks_max 4 --n 10 english train unsup_syl okko0
    ./downsample_dense.py --n_landmarks_max 4 --n 10 LANG1 train unsup_syl okko0
    ./downsample_dense.py --n_landmarks_max 4 --n 10 LANG2 train unsup_syl okko0
