
% 1) Load audio file
[x,fs] = wavread('example.wav');

if(fs ~= 16000)
    x = resample(x,16000,fs);
    fs = 16000;
end

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

% 3) Compute gammatone envelopes and downsample to 1000 Hz

env = zeros(length(x),length(cfs));
for cf = 1:length(cfs)
    [~, env(:,cf), ~, ~] = gammatone_c(x, fs,cfs(cf));
end
env = resample(env,1000,fs);

% 4) Run oscillator-based segmentation
Q_value = 0.5;  % Q-value of the oscillator, default = 0.5 = critical damping
center_frequency = 5; % in Hz
threshold = 0.01;

[bounds,bounds_t,osc_env,nucleii] = thetaOscillator(env,center_frequency,Q_value,threshold);

% 5) Plot outputs

t = 0:1/fs:length(x)/fs-1/fs;
x = x./max(x);
figure;hold on;
plot(t,x);
oscillator_output = osc_env{1};
oscillator_output = oscillator_output-min(oscillator_output);
oscillator_output = oscillator_output./max(oscillator_output);
t_osc = 0:1/1000:length(osc_env{1})/1000-1/1000;
plot(t_osc,oscillator_output,'r','LineWidth',2);
for k = 1:length(bounds_t{1})
    line([bounds_t{1}(k) bounds_t{1}(k)],[-1 1],'Color','black','LineStyle','--','LineWidth',2);
end
xlabel('time (s)');
ylabel('normalized amplitude');
title('syllabification demo');

% 6) Play syllables
for k = 1:length(bounds_t{1})-1
    disp('press button to hear the next syllable');
    pause;
    soundsc(x(bounds_t{1}(k)*fs:min(length(x),bounds_t{1}(k+1)*fs)),fs);
end


