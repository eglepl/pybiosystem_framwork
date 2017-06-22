%% This block fetches the framework: do not edit
urlwrite('http://web.mit.edu/20.305/www/part_composition_setup.m', ...
    'part_composition_setup.m');
rehash;
part_composition_setup('v5');


%% The system is constructed & simulated in the block below: feel free to edit
selftiming = BioSystem();

simulation_run_time = 2500;

% Species + initial conditions
A = selftiming.AddCompositor('A', 0); 
B = selftiming.AddCompositor('B', 0); 
m_R1 = selftiming.AddCompositor('m_R1', 0);
m_R2 = selftiming.AddCompositor('m_R2', 0);
m_R3 = selftiming.AddCompositor('m_R3', 0);
m_Rtrue = selftiming.AddCompositor('m_Rtrue', 0);
m_Rfalse = selftiming.AddCompositor('m_Rfalse', 0);
m_Rstn = selftiming.AddCompositor('m_Rstn', 0);
m_Rst = selftiming.AddCompositor('m_Rst', 0);
m_OUT = selftiming.AddCompositor('m_OUT', 0);
m_OUTn = selftiming.AddCompositor('m_OUTn', 0);

R1 = selftiming.AddCompositor('R1', 0);
R2 = selftiming.AddCompositor('R2', 0);
R3 = selftiming.AddCompositor('R3', 0);
Rtrue = selftiming.AddCompositor('Rtrue', 0);
Rfalse = selftiming.AddCompositor('Rfalse', 0);
Rstn = selftiming.AddCompositor('Rstn', 0);
Rst = selftiming.AddCompositor('Rst', 0);
OUT = selftiming.AddCompositor('OUT', 0);
OUTn = selftiming.AddCompositor('OUTn', 0);

% Constants 

constants={'K_Rst','K_Rstn','K_A','K_B','K_R1','K_R2','K_R3','K_Rtrue','K_Rfalse','K_OUT','K_OUTn'};

%% Use below for random values
rng(3,'twister');
constant_values = 0.5+2*rand(size(constants));

%% Use below for all K_* set to 2
%constant_values = ones(size(constants))*2; 

for i = 1:size(constants,2)
    c = Const(constants{i}, constant_values(i));
    selftiming.AddConstant(c);
end

selftiming.AddConstant('n', 2);
selftiming.AddConstant('k_tln', 5);
selftiming.AddConstant('k_txn', 5);
selftiming.AddConstant('k_mdeg', 0.5);
selftiming.AddConstant('k_pdeg', 0.05);


% Parts
selftiming.AddPart(Part('All interactions', [m_R1 R1 m_R2 R2 m_R3 R3 m_Rtrue Rtrue m_Rfalse Rfalse m_Rstn Rstn m_Rst Rst m_OUT OUT m_OUTn OUTn  ], ...
    [... % R1
     Rate('k_txn*(K_Rst^n/(K_Rst^n+Rst^n))*(K_A^n/(K_A^n+A^n)) - k_mdeg*m_R1'), ...
     Rate('k_tln*m_R1 - k_pdeg*R1'), ...
     ... % R2
     Rate('k_txn*(K_Rst^n/(K_Rst^n+Rst^n))*(K_B^n/(K_B^n+B^n)) + k_txn*(K_Rst^n/(K_Rst^n+Rst^n))*(K_R1^n/(K_R1^n+R1^n)) - k_mdeg*m_R2'), ...
     Rate('k_tln*m_R2 - k_pdeg*R2'), ...
     ... % R3
     Rate('k_txn*(K_Rst^n/(K_Rst^n+Rst^n))*(K_R2^n/(K_R2^n+R2^n)) - k_mdeg*m_R3'), ...
     Rate('k_tln*m_R3 - k_pdeg*R3'), ...
     ... % Rtrue
     Rate('k_txn*(K_Rst^n/(K_Rst^n+Rst^n))*(K_R2^n/(K_R2^n+R2^n)) - k_mdeg*m_Rtrue'), ...
     Rate('k_tln*m_Rtrue - k_pdeg*Rtrue'), ...
     ... % Rfalse
     Rate('k_txn*(K_Rst^n/(K_Rst^n+Rst^n))*(K_R3^n/(K_R3^n+R3^n)) - k_mdeg*m_Rfalse'), ...
     Rate('k_tln*m_Rfalse - k_pdeg*Rfalse'), ...
     ... % Rstn
     Rate('k_txn*(K_Rtrue^n/(K_Rtrue^n+Rtrue^n))*(K_Rfalse^n/(K_Rfalse^n+Rfalse^n)) - k_mdeg*m_Rstn'), ...
     Rate('k_tln*m_Rstn - k_pdeg*Rstn'), ...
     ... % Rst
     Rate('k_txn*(K_Rstn^n/(K_Rstn^n+Rstn^n)) - k_mdeg*m_Rst'), ...
     Rate('k_tln*m_Rst - k_pdeg*Rst'), ...
     ... % OUT
     Rate('k_txn*(K_Rfalse^n/(K_Rfalse^n+Rfalse^n))*(K_OUTn^n/(K_OUTn^n+OUTn^n)) - k_mdeg*m_OUT'), ...
     Rate('k_tln*m_OUT - k_pdeg*OUT'), ...
     ... % OUTn
     Rate('k_txn*(K_Rtrue^n/(K_Rtrue^n+Rtrue^n))*(K_OUT^n/(K_OUT^n+OUT^n)) - k_mdeg*m_OUTn'), ...
     Rate('k_tln*m_OUTn - k_pdeg*OUTn'), ...
     ...
     ...
     ]));


%% Plotting iteration
%   TODO: Indicate which variable or parameter you would
%   like to change with each loop, plotting the changes.
%   
%   To start, we recommend looking at m_B and iterating p.
%
%   You should only iterate over one species or one 
%   parameter at a time. If you do not want to iterate
%   over one or the other, set it to false.



%% Plotting/simulation, we recommend not changing the below
%   Simulate system from 0 to simulation_run_time units

[Tpul, Ypul] = selftiming.run_pulses([...
    Pulse(0, 'B', 0), ... % initial conditions
    Pulse(500, 'B', 10), ... % inducton
    Pulse(1000, 'A', 10), ... % inducton
    Pulse(1500, 'A', 0), ... % inducton
    Pulse(2000, 'B', 0), ... % inducton
    Pulse(simulation_run_time, '', 0), ... % stop the simulation 
]);

%% To produce full 4-part plot
if 0
    figure()

    % Plot concentration of species [speciesIndex] over time
    subplot(4,1,1);
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('A')), ':', 'LineWidth',3);
    hold;
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('B')), '--', 'LineWidth',3);
    legend('A','B');
    xlabel('Time (s)');
    ylabel('Input Concentration');



    subplot(4,1,2);
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('OUT')), '-', 'LineWidth',3);
    hold;
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('OUTn')), ':', 'LineWidth',3);
    legend('OUT','OUTn');
    xlabel('Time (s)');
    ylabel('Output Concentration');

    subplot(4,1,3);
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('Rtrue')), ':', 'LineWidth',2);
    hold;
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('Rfalse')), ':', 'LineWidth',2);
    legend('Rtrue','Rfalse');
    xlabel('Time (s)');
    ylabel('Intermediate Output Concentration');


    subplot(4,1,4);
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('Rst')), '-', 'LineWidth',3);
    hold;
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('Rstn')), ':', 'LineWidth',3);
    legend('Rst','Rstn')
    xlabel('Time (s)');
    ylabel('Concentration');
end

%% to produce smaller plot with only OUT/OUTn, Rtrue/Rfalse, and K_* constants shown in a table
if 1
    f=figure();
    f.Position = [100 528 900 400]; % constant, reasonable size
    subplot(3,1,1);
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('OUT')), '-', 'LineWidth',3);
    hold;
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('OUTn')), ':', 'LineWidth',3);
    legend('OUT','OUTn');
    xlabel('Time (s)');
    ylabel('Output');

    subplot(3,1,2);
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('Rtrue')), ':', 'LineWidth',2);
    hold;
    plot(Tpul, Ypul(:, selftiming.CompositorIndex('Rfalse')), ':', 'LineWidth',2);
    legend('Rtrue','Rfalse');
    xlabel('Time (s)');
    ylabel('Intermediate');
    
    %s=subplot(3,1,3);
    uitable(f,'Units','normalized','Position',[0 0 1 0.25],'Data',constant_values,'ColumnName',constants,'RowName',[])
end
      