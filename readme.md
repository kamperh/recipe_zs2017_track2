ZeroSpeech2017
==============


Preliminaries
-------------
Install the zerospeech tools in `../src/zerospeech2017`:

    git clone https://github.com/bootphon/zerospeech2017.git \
        ../src/zerospeech2017
    # To-do: add installation and data download instructions
    git clone https://github.com/bootphon/zerospeech2017_surprise.git \
        ../src/zerospeech2017_surprise/

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



