function [bounds,bounds_t,env,nuclei,outs] = thetaOscillator(ENVELOPE,f,Q,thr,verbose)
%function [bounds,bounds_t,env,nuclei] = thetaOscillator(ENVELOPE,f,Q,thr)
%
% Performs oscillator-based syllabification of the input signal.
% Technically, this mechanical oscillator model corresponds to a second
% order electronic resonator with equivalent characteristics (f, Q).
% 
% Input amplitude envelopes on multiple frequency bands are first used to
% drive a bank for harmonic damped oscillators tuned to a center frequency
% "f" and Q-factor "Q". Oscillator amplitudes are then combined across 
% frequencies by taking log-sum of the N most energetic bands. Finally,
% valley picking is used to determine syllable boundary positions using 
% a threshold "thr" to determine the required depth of the valley.
% 
% Inputs:
%       ENVELOPE   : M x 1 cell-array of M signals, each N(m) X F in size                    
%                    OR
%                    N x F matrix 
%                    where N(m) is the number of samples and F number of
%                    frequency bands (e.g., critical band envelopes)
%                    
%       f          : Center frequency of the oscillator (default = 5 Hz)
%       Q          : Q-value of the oscillator (default = 0.5)
%       thr        : detection threshold of the syllable boundaries 
%                    (default = 0.025)                  
% Outputs:
%       bounds     : M x 1 cell array of boundaries (in 1000 Hz samples) 
%       bounds_t   : M x 1 cell array of boundaries in time (seconds)
%       env        : M X 1 cell array of oscillator envelopes 
%       nucleii    : M x 1 cell array of nucleii locations (in samples)
%
%
%
% Code (c) Okko Rasanen, okko.rasanen@aalto.fi, 2016
% Last update: 16.2.2016
% 
% If used for research or other purposes , please cite:
% Rasanen, O., Doyle, G. & Frank, M. C. (submitted). "Pre-linguistic 
% rhythmic segmentation of speech into syllabic units".
% 
% Not explicitly protected by copyrights. Derivatives of this work
% should also cite the above paper.
 
N = 8;	% How many most energetic bands to use (default = 8)

if nargin <2
    f = 5;
elseif(isempty(f))
    f = 5;
end
if nargin <3
    Q = 0.5;
elseif(isempty(Q))
    Q = 0.5;    
end
if nargin <4
    thr = 0.025;
end

if nargin <5
    verbose = 1;
end

% Convert matrix to cell if only one signal is given as input
if(~iscell(ENVELOPE))
   tmp = ENVELOPE;   
   ENVELOPE = cell(1,1);
   ENVELOPE{1} = tmp;
end

if(N >= size(ENVELOPE{1},2))
    N = size(ENVELOPE{1},2);
    warning('Input dimensionality smaller than the N parameter. Using all frequency bands.');
end

%% Find correct delay compensation (readily tabulated)

a = [72 34 22 16 12 9 8 6 5 4 3 3 2 2 1 0 0 0 0 0;
    107 52 34 25 19 16 13 11 10 9 8 7 6 5 5 4 4 4 3 3;
    129 64 42 31 24 20 17 14 13 11 10 9 8 7 7 6 6 5 5 4;
    145 72 47 35 28 23 19 17 15 13 12 10 9 9 8 7 7 6 6 5;
    157 78 51 38 30 25 21 18 16 14 13 12 11 10 9 8 8 7 7 6;
    167 83 55 41 32 27 23 19 17 15 14 12 11 10 10 9 8 8 7 7;
    175 87 57 43 34 28 24 21 18 16 15 13 12 11 10 9 9 8 8 7;
    181 90 59 44 35 29 25 21 19 17 15 14 13 12 11 10 9 9 8 8;
    187 93 61 46 36 30 25 22 19 17 16 14 13 12 11 10 10 9 8 8;
    191 95 63 47 37 31 26 23 20 18 16 15 13 12 11 11 10 9 9 8]+1;

i1 = max(1,min(10,round(Q.*10)));
i2 = max(1,min(20,round(f)));

delay_compensation = a(i1,i2);

%% Get oscillator mass

T = 1./f;   % Oscillator period
k = 1;      % Fix spring constant k = 1, define only mass
b = 2*pi/T; 
m = k/b^2;  % Mass of the oscillator

% Get oscillator damping coefficient
c = sqrt(m*k)/Q;

if(verbose)
fprintf('Oscillator Q-value: %0.4f, center frequency: %0.1f Hz, bandwidth: %0.1f Hz.\n',Q,1/T,1/T/Q);
end

%% Run oscillator
env = cell(length(ENVELOPE),1);
bounds = cell(length(ENVELOPE),1);
bounds_t = cell(length(ENVELOPE),1);
nuclei = cell(length(ENVELOPE),1);

for signal = 1:length(ENVELOPE)
        
    % Do zero padding
    e = (ENVELOPE{signal});
    e = [e;zeros(500,size(e,2))];
    
    F = size(e,2); % Number of frequency channels
    
    % Get oscillator amplitudes as a function of time
    x = zeros(length(e),F);
    a = zeros(length(e),F);
    v = zeros(length(e),F);
    x(1,:,:) = 0;
    a(1,:,:) = 0;
                
    for t = 2:size(e,1)        
            for cf = 1:F
                
                f_up = e(t,cf); % driving positive force 
                
                f_down = -k*x(t-1,cf)-c*v(t-1,cf);
                
                f_tot = f_up+f_down; % Total force
                                
                % Get acceleration from force
                a(t,cf) = f_tot./m;
                
                % Get velocity from acceleration
                v(t,cf) = v(t-1,cf)+a(t,cf).*0.001; % assumes 1000 Hz sampling
                
                % Get position from velocity
                
                x(t,cf) = x(t-1,cf)+v(t,cf).*0.001;                
                
            end                     
    end

    % Perform group delay correction by removing samples from the
    % beginning and adding zeroes to the end    
 
     for f = 1:F
         if(delay_compensation ~= 0)
             x(:,f) = [x(delay_compensation:end,f);zeros(delay_compensation-1,1)];
         end
     end
    
    x = x(1:end-500,:,:); % Remove zero-padding
        
    
    % Combine N most energetic bands to get sonority envelope
    tmp = x;
    tmp = tmp-min(tmp(:))+0.00001;
    
    outs = x;
    
    x = zeros(size(tmp,1),1);
    
    for zz = 1:size(tmp,1)
        [~,inds] = sort(tmp(zz,:),'descend');        
        x(zz) = sum((log10(tmp(zz,inds(1:N)))));                
    end
        
    % Scale sonority envelope between 0 and 1
    
    x = x-min(x);
    x = x./max(x);
    
    env{signal} = x;
    
    [~,peaks] = peakdet(x,thr); % Valley picking
    
    if(~isempty(peaks))
        fw_bounds = peaks(:,1);
    else
        fw_bounds = [];
    end
    
    bb = fw_bounds;
           
    % Add signal onset if not detected by valley picking
    if(~isempty(bb))
        if(bb(1) > 50)
            bb = [1;bb];
        end
        % Add signal ending if not detected by valley picking
        if(bb(end)+50 < length(x))
            bb = [bb;length(x)];
        end
    else
        bb = [1;length(x)];
    end
    
    % Get nucleii as maxima between valleys (syllable boundaries)
    nuclei{signal} = zeros(length(bb)-1,1);
    
    for zz = 1:length(bb)-1
        [~,tmp] = max(x(bb(zz):bb(zz+1)));
        nuclei{signal}(zz) = bb(zz)-1+tmp;
    end
    
    % store outputs
    bounds{signal} = bb;            
    bounds_t{signal} = bounds{signal}./1000;   
end
