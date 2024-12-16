clear
clc
close all

%% Para def
n = 16;
m = 0:10;
N = 2^n;

%% Partial-NTT
% n-m stages
NTT_MM = 3 * (n-m) * N/2;
NTT_MM(1) = NTT_MM(1) + N;
NTT_MA = 3 * (n-m) * N;
NTT_com = NTT_MM * 240 + NTT_MA * 3;

%% Partial-Kara
% m stages
Kara_M = 2.^(n-m) .* (3.^m);
Kara_MA = 2.^(n-m) .* (2.^(m+1).*((3/2).^m-1) + 6*(2.^m-1) - 4*m);
Kara_com = Kara_M * 64 + Kara_MA * 3;

%% Results
All_com = NTT_com + Kara_com;

% Find global minimum and baseline
[min_val, min_idx] = min(All_com);
x_min = m(min_idx);
baseline_val = All_com(1); % corresponding to x=0

%% Plot
figure('Color','w'); % White background
plot(m, All_com, 'k-', 'LineWidth', 2); % main line
hold on;

% Mark the global minimum point
plot(x_min, min_val, 'ro', 'MarkerFaceColor','r', 'MarkerSize',8);

% Add a baseline reference marker at x=0
plot(m(1), baseline_val, 'bs', 'MarkerFaceColor','b', 'MarkerSize',8);

% Draw a horizontal line at the baseline for visual comparison
yline(baseline_val, '--b', 'LineWidth', 1.5);
yline(min_val, '--r', 'LineWidth', 1.5);

% % Annotations for minimum point
% text(x_min, min_val, ...
%     sprintf('  Global Min (x=%d)\nValue = %.2e', x_min, min_val), ...
%     'FontSize', 12, 'Color', 'r', 'VerticalAlignment', 'bottom');
% 
% % Annotation for difference from baseline
% diff_percent = (min_val - baseline_val)/baseline_val * 100;
% text(0, baseline_val, ...
%     sprintf('Baseline (x=0)\nValue = %.2e\nReduction = %.2f%%', baseline_val, diff_percent), ...
%     'FontSize', 12, 'Color', 'b', 'VerticalAlignment', 'top', 'HorizontalAlignment','left');

% Adjust axis labels, title and grid
xlabel('\textbf{Partial Stage}', 'FontSize', 14, 'Interpreter','latex');
ylabel('\textbf{Computational Cost}', 'FontSize',14, 'Interpreter','latex');
% title('Comparison of Computational Cost vs. m', 'FontSize',16, 'Interpreter','latex');
grid on;
xticks(m);

% Set font
set(gca, 'Box', 'off', ...            % 去掉上、右边框
         'XAxisLocation', 'bottom', ...% x轴在底部
         'YAxisLocation', 'left', ...  % y轴在左侧
         'TickDir','out', ...          % 刻度线向外
         'LineWidth',1.5, ...
         'FontSize', 12);

hold off;