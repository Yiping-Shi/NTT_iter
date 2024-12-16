clear
close all
clc

m = 0 : 12;

%% NTT
ntt_num_mod_mult = 3*m .* (2.^m) /2 + 2.^m;
ntt_num_mod_add  = 3*m .* (2.^m);

ntt = ntt_num_mod_mult * 200 + ntt_num_mod_add * 3;


%% Iter conv
iter_num_mult    = 3.^m;
iter_num_mod_add = 2 * 2.^(m-1) .* ((3/2).^m-1) + 12 * (2.^m-1) - 8*m;

iter = iter_num_mult * 64 + iter_num_mod_add * 3;
 
%% 



%% 
hold on;
plot(m, ntt, "b");
plot(m, iter, "r");
legend("ntt", "iter");
fprintf("ntt(8),%d\n", ntt(8));
fprintf("iter(8),%d\n", iter(8));
fprintf("ntt(7),%d\n", ntt(7));
fprintf("ntt(9),%d\n", ntt(9));
fprintf("iter(7),%d\n", iter(7));
hold off;