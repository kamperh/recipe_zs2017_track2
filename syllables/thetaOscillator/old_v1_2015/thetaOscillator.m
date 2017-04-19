function [bounds,bounds_t,osc_env,nuclei] = thetaOscillator(envelopes,f,Q,thr)
%function [bounds,bounds_t,osc_env,nuclei] = thetaOscillator(envelopes,f,Q,thr)
%
% Performs syllabification for the input gammatone-filterbank envelopes.
%
%  Inputs:
%       envelopes   : gammatone-filterbank envelopes sampeld at 1000 Hz
%                     (a vector or cell array of vectors, one cell per signal) 
%       f           : center frequency of the oscillator (default = 5 Hz)
%       Q           : Q-value of the oscillator (~bandwidth; default = 0.5)
%       thr         : peak detection threshold (default: 0.01)
%
%   Outputs:
%       bounds      : syllable boundaries in samples (cell array)
%       bounds_t    : syllable boundaries in seconds (cell array)
%       osc_env     : oscillator envelopes used for bound/nuclei detection
%       nuclei      : oscillator nuclei locations (maxima of osc_env)
%
%  Note: uses MATLAB parallel loops by default. Change row 70 from "parfor"
% to "for" if parallel computing toolbox is not enabled. 
%
% (c) Okko Rasanen, okko.rasanen@aalto.fi , v0.1 (date: 5.10.2015)
%
% If you use this algorithm in publications, please cite: 
% 
% Räsänen O., Doyle G. & Frank M. C. (2015). "Unsupervised word discovery 
% from speech using automatic segmentation into syllable-like units". 
% Proc. Interspeech'2015, Dresden, Germany.
%
% (note that the paper has an outdated version of the segmenter, a better
% reference for the present version will appear soon, hopefully). 

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
    thr = 0.01;
end

if(~iscell(envelopes))
   tmp = envelopes;   
   envelopes = cell(1,1);
   envelopes{1} = tmp;
end

T = 1./f; % Oscillator period

% Set time-shift compensation based on the center frequency (empirical values)

a = [-115  -100   -95   -75   -75   -60   -55   -55   -55   -50];
lag_correction = abs(a(min(10,ceil(f))));


k = 1;   % Fix spring constant to k = 1 and define only mass

% Get oscillator mass

b = 2*pi/T;
m = k/b^2;

% Get oscillator damping coefficient
c = sqrt(m*k)/Q;

fprintf('Oscillator Q-value: %0.4f, center frequency: %0.1f Hz, bandwidth: %0.1f Hz.\n',Q,1/T,1/T/Q);

% Run oscillator for each input signal
osc_env = cell(length(envelopes),1);
bounds = cell(length(envelopes),1);
bounds_t = cell(length(envelopes),1);
nuclei = cell(length(envelopes),1);

parfor signal = 1:length(envelopes) % <-- change to normal "for" if needed
        

    % Pick current signal and zero padding
    e = (envelopes{signal});    
    e = [e;zeros(500,size(e,2))];
    
    % Number of frequency channels
    F = size(e,2);
                    
    x = zeros(length(e),F);     % position
    a = zeros(length(e),F);     % acceleration
    v = zeros(length(e),F);     % velocity
    x(1,:,:) = 0;
    a(1,:,:) = 0;
                
    for t = 2:length(e)         
            for cf = 1:F   % Run a parallel oscillator for each frequency band
                
                f_up = e(t,cf);     % force up
                
                f_down = -k*x(t-1,cf)-c*v(t-1,cf);  % force down
                
                f_tot = f_up+f_down;
                                
                % Get acceleration from force
                a(t,cf) = f_tot./m;
                
                % Get velocity from acceleration
                v(t,cf) = v(t-1,cf)+a(t,cf).*0.001;
                
                % Get position from velocity                
                x(t,cf) = x(t-1,cf)+v(t,cf).*0.001;                
                
            end                     
    end

    % Do phase shift correction 
 
     for f = 1:F
         if(lag_correction ~= 0)
             x(:,f) = [x(lag_correction:end,f);zeros(lag_correction-1,1)];
         end
     end
    
    x = x(1:end-500,:,:); % Remove zero-padding
 
    tmp = x+0.00001;        % Add a small noise floor to avoid log(0).
    
    % Compute sonority curve as a log-sum across the N most energetic bands
    x = zeros(size(tmp,1),1);
    N = 8;
    for zz = 1:size(tmp,1)
        [~,inds] = sort(tmp(zz,:),'descend');        
        x(zz) = sum(log10(tmp(zz,inds(1:N))));        
    end
        
    % Scale sonority curve between 0 and 1
    
    x = x-min(x);
    x = x./max(x);
    
    osc_env{signal} = x;
    
    [~,minima] = peakdet(x,thr); % Find minima
    
    if(~isempty(minima))
        seg_bounds = minima(:,1);
    else
        seg_bounds = [];
    end
           
    % Add onset boundary if it's not detected within 50 ms from start 
    if(~isempty(seg_bounds))
        if(seg_bounds(1) > 50)
            seg_bounds = [1;seg_bounds];
        end
        % Add offset if offset not detected within 50 ms from signal end
        if(seg_bounds(end)+50 < length(x))
            seg_bounds = [seg_bounds;length(x)];
        end
    else
        seg_bounds = [1;length(x)];
    end
    
    % Get nuclei positions as envelope maxima between the detected bounds
    nuclei{signal} = zeros(length(seg_bounds)-1,1);
    
    for zz = 1:length(seg_bounds)-1
        [~,tmp] = max(x(seg_bounds(zz):seg_bounds(zz+1)));
        nuclei{signal}(zz) = seg_bounds(zz)-1+tmp;
    end
    
    % Add to output cells
    bounds{signal} = seg_bounds;            
    bounds_t{signal} = bounds{signal}./1000;   
end
