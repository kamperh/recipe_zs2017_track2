Embedded Segmental K-Means for ZeroSpeech2017 Track 2
=====================================================

Warning
-------
This is a preliminary version of our system. This is not a final recipe, and
is still being worked on.


Overview
--------
A description of the challenge can be found here:
<http://sapience.dec.ens.fr/bootphon/2017/index.html>.


Disclaimer
----------
The code provided here is not pretty. But I believe that research should be
reproducible, and I hope that this repository is sufficient to make this
possible for the paper mentioned above. I provide no guarantees with the code,
but please let me know if you have any problems, find bugs or have general
comments.


Preliminaries
-------------
Clone the zerospeech repositories:

    mkdir ../src/
    git clone https://github.com/bootphon/zerospeech2017.git \
        ../src/zerospeech2017/
    # To-do: add installation and data download instructions
    git clone https://github.com/bootphon/zerospeech2017_surprise.git \
        ../src/zerospeech2017_surprise/

Clone the `eskmeans` repository:

    git clone https://github.com/kamperh/eskmeans.git \
        ../src/eskmeans/

Get the surprise data:
    
    cd ../src/zerospeech2017_surprise/
    source download_surprise_data.sh \
        /share/data/lang/users/kamperh/zerospeech2017/data/surprise/
    cd -

Update all the paths in `paths.py` to match your directory structure.


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


Acoustic word embeddings: downsampling
--------------------------------------
We use one of the simplest methods to obtain acoustic word embeddings:
downsampling. Different types of input features can be used. Run the steps in
[downsample/readme.md](downsample/readme.md).


Unsupervised segmentation and clustering
----------------------------------------
Segmentation and clustering is performed using the
[ESKMeans](https://bitbucket.org/kamperh/eskmeans/) package. Run the steps
in [segmentation/readme.md](segmentation/readme.md).


Dependencies
------------
- [Python](https://www.python.org/)
- [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/).
- [HTK](http://htk.eng.cam.ac.uk/): Used for MFCC feature extraction.
- [Matlab](https://www.mathworks.com/): Used for syllable boundary detection.


Collaborators
-------------
- [Herman Kamper](http://www.kamperh.com/)
- [Karen Livescu](http://ttic.uchicago.edu/~klivescu/)
- [Sharon Goldwater](http://homepages.inf.ed.ac.uk/sgwater/)
