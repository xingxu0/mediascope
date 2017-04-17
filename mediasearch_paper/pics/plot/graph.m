clear
close
extract_30 = [73327
41153
20236
9642
4687
2257
1122];

extract_60 = [141994
74977
41048
18357
9028
4539
2316];

extract_120 = [311985
161176
79473
39862
19170
9168
4690];

extract_30 = sort(extract_30/1000);
extract_60 = sort(extract_60/1000);
extract_120 = sort(extract_120/1000);

h=subplot(1,1,1);
hold on;
set(h,'FontSize', 22, 'FontName', 'Times New Roman'); 
% sim_30 = [3.2642276422764227, 6.528455284552845,10.51612903225806, 19.741935483870968, 33.1875, 37.75, 40.75];
% sim_60 = [3.0510204081632653, 6.0653061224489795, 10.08130081300813,19.967741935483872, 33.70967741935484,38.6875, 39.5  ];
% sim_120 = [3.060416666666667, 6.120833333333334, 10.241666666666667, 20.075, 33.35, 40.266666666666666, 42.0];
sim_30 = [2.0410625364722274, 4.182125072944455, 8.49195780600271, 16.006621514597246, 26.080984622240067, 33.6422803401947, 37.50462245941162];
sim_60 = [1.8907825703523597, 3.8647599473291513, 7.6989120902084725, 14.876873985413582, 23.954314824073546, 32.58059448003769, 34.160579681396484];
sim_120 = [2.1572850154091915, 4.414570030818383, 8.329140061636766, 15.41074840327104, 24.875755294164023, 34.175501775741576, 36.63161284128825];
sim_30 = sort(sim_30,'descend');
sim_60 = sort(sim_60,'descend');
sim_120 = sort(sim_120,'descend');
p = plot(sim_30,'r-d');
set(p,'Color','red','LineWidth',2,'markers',8);
hold on;
p = plot(sim_60,'b-o');
set(p,'Color','blue','LineWidth',2,'markers',8);
p = plot(sim_120,'g-+');
set(p,'Color','green','LineWidth',2,'markers',8);
grid
% title('');
legend('Average 30s Duration','Average 60s Duration', 'Average 120s Duration');
xlabel('Extraction Frequency (Hz)');
ylabel('Total Extraction Time (s)');
% set(p,'FontSize', 22, 'FontName', 'Times New Roman');    

set(gca,'XTickLabel',{'0.125','.25','0.5','1','2','4','8'});

set(gca,'XTick', [1:7]);
set(gcf, 'PaperSize', [4, 2]);
axis([0.5 7.5 0 40]);
pbaspect([2,1,1]);   
filename = ['similarity.eps'];
saveas(h, filename,'psc2');   
