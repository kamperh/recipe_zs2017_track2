% Perform syllable segmentation for all the files in wavs.list.
% Herman Kamper, kamperh@gmail.com, 2015.

clear all;

% Read list of wav files
% basename = 'mandarin_train';
% basename = 'french_train';
% basename = 'english_train';
% basename = 'LANG1_train';
basename = 'LANG2_train';
fid = fopen(['../wavs/' basename '.list']);
wav_files = textscan(fid, '%s', 'Delimiter', '\n');
wav_files = wav_files{1};

% 2) Generate Gammatone filterbank center frequencies (log-spacing)
minfreq = 50;
maxfreq = 7500;
bands = 20;

cfs = zeros(bands,1);
const = (maxfreq/minfreq)^(1/(bands-1));

cfs(1) = 50;
for k = 1:bands-1
    cfs(k+1) = cfs(k).*const;
end


envelopes = cell(size(wav_files));
for i = 1:length(wav_files)
    disp([int2str(i) ': ' wav_files{i}]);
    
    % 1) Load audio file    
    [x,fs] = audioread(wav_files{i});

    if(fs ~= 16000)
        x = resample(x,16000,fs);
        fs = 16000;
    end

    % 3) Compute gammatone envelopes and downsample to 1000 Hz

    env = zeros(length(x),length(cfs));
    for cf = 1:length(cfs)
        [~, env(:,cf), ~, ~] = gammatone_c(x, fs,cfs(cf));
    end
    envelopes{i} = resample(env,1000,fs);
end

% 4) Run oscillator-based segmentation
Q_value = 0.5;  % Q-value of the oscillator, default = 0.5 = critical damping
center_frequency = 5; % in Hz
threshold = 0.01;

[bounds,bounds_t,osc_env,nucleii] = thetaOscillator(envelopes,center_frequency,Q_value,threshold);

save([basename '_bounds_t.mat'], 'wav_files', 'bounds_t')
