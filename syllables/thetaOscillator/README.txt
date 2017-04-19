This package contains codes for sonority-based syllabification of speech signals. 

Version 0.1 (5.10.2015)

------------
Basic pipeline:
    1) compute gammatone-envelopes for speech signals with 1000 Hz sampling rate
    2) call thetaOscillator.m with the envelopes as input 
    
See SylSegDemo.m for an example.

------------
(c) Okko Räsänen, okko.rasanen@aalto.fi , 2015.

If you use this algorithm in publications, please cite: 
 
Räsänen O., Doyle G. & Frank M. C. (2015). "Unsupervised word discovery 
from speech using automatic segmentation into syllable-like units". 
Proc. Interspeech'2015, Dresden, Germany.

(note that the paper has an outdated version of the segmenter, a better
reference for the present version will appear soon, hopefully). 
------------

Note that the package uses Gammatone-filterbank front-end by Ning Ma 
(http://staffwww.dcs.shef.ac.uk/people/N.Ma/resources/gammatone/). 
If you are not using 64-bit OS X environment, compile the function first with
"mex gammatone_c.c". 

Also uses peakdet.m from Eli Billauer.