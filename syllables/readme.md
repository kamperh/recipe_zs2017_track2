Unsupervised Syllable Segmentation
==================================

Extract the wav files for the segments of the different corpora:

    ./get_wavs.py mandarin train
    ./get_wavs.py french train
    ./get_wavs.py english train

This also writes the lists like `wavs/mandarin_train.list` containing the
absolute paths to the wav files.

Move to directory with Okko's syllable segmentation code, open Matlab, and run
the unsupervised syllable segmentation:

    cd thetaOscillator
    matlab -desktop
    process_wavs  % execute in Matlab
    exit
    cd ..

To process the different corpora, edit the `basename` variable in
`process_wavs.m` with the appropriate language and subset.

Get the landmarks extracted above in the appropriate Python format:

    ./get_syl_landmarks.py mandarin train
    ./get_syl_landmarks.py french train
    ./get_syl_landmarks.py english train
