Downsampled Acoustic Word Embeddings
====================================

Creating the output directories:

    mkdir -p embeddings/mandarin_train
    mkdir -p embeddings/french_train
    mkdir -p embeddings/english_train

Perform the unsupervised syllable segmentation. Link the landmarks from the
unsupervised syllable segmentation:

    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zerospeech/zs2017/syllables/landmarks/mandarin_train/landmarks.unsup_syl.pkl \
            embeddings/mandarin_train/
    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zerospeech/zs2017/syllables/landmarks/french_train/landmarks.unsup_syl.pkl \
            embeddings/french_train/
    ln -s \
        /share/data/speech-multiview/kamperh/projects/edinburgh/zerospeech/zs2017/syllables/landmarks/english_train/landmarks.unsup_syl.pkl \
            embeddings/english_train/

Get the segmentation intervals over the landmarks:

    ./get_seglist.py mandarin train unsup_syl
    ./get_seglist.py french train unsup_syl
    ./get_seglist.py --n_landmarks_max 4 english train unsup_syl

Get the dense embeddings over the segmentation intervals:

    ./downsample_dense.py --frame_dims 13 mandarin train unsup_syl mfcc
    ./downsample_dense.py --frame_dims 13 french train unsup_syl mfcc
    ./downsample_dense.py --n_landmarks_max 4 --n 10 --frame_dims 13 english train unsup_syl mfcc
