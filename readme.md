ZeroSpeech2017 Experiments
==========================


Preliminaries
-------------
Install the zerospeech tools in `../src/zerospeech2017`:

    # To-do
    ...

Alter all the paths in `paths.py` to match your directory structure.



Feature extraction
------------------
Extract MFCC features by running the steps in
[features/readme.md](features/readme.md).



Unsupervised syllable boundary detection
----------------------------------------
We use the unsupervised syllable boundary detection algorithm described in:

- O. J. Räsänen, G. Doyle, and M. C. Frank, "Unsupervised word discovery from
  speech using automatic segmentation into syllable-like units," in *Proc.
  Interspeech*, 2015.

Obtain the syllabe boundaries by running the steps in
[syllables/readme.md](syllables/readme.md).
