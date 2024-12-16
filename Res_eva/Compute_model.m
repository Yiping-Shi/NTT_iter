clear
close all
clc

%% Parameters Definition
n = 16;             % Number of stages
m = 0 : 16;         % Number of Kernel stages
N = 2^n;           % Number of Degrees

C_add = 1;          % Cost of an adder/subtractor
C_mul = 10;         % Cost of a multiplier
C_cmp = 1;          % Cost of a comparator

%% Computation of the cost of the model
% TotalModMul = N .* (n-m+2) + 2.^(n-m) .* 3.^(m);
TotalModMul = N .* (n-m+2) + 3.^(m);
TotalModAdd = N .* (n-m) + 2.^(n-m) .* (3.^(m) - 2.^(m)) + 2^(n+1) - 2.^(n-m+1) .* (1+m);
TotalModSub = N .* (n-m) + 2.^(n+1) - 2.^(n-m+2) - 2.^(n-m+1) .* m;

TotalAddOps = 2 * (TotalModAdd + TotalModSub) + 3 * TotalModMul;
TotalMulOps = 3 * TotalModMul;
TotalCmpOps = (TotalModAdd + TotalModSub) + 2 * TotalModMul;

TotalCost = C_add * TotalAddOps + C_mul * TotalMulOps + C_cmp * TotalCmpOps;

%% Display of the results
plot(m, TotalCost, 'LineWidth', 2);
fprintf('The minimum cost is %d, when m = %d.\n', min(TotalCost), m(TotalCost == min(TotalCost)));