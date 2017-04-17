
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
%set(gca,'XTickLabel', {'1632x1224','1280x960','1024x768', '960x720','816x612'})
p = plot(extract_30,'r-d');
set(p,'Color','red','LineWidth',2,'markers',8);
hold on;
p = plot(extract_60,'b-o');
set(p,'Color','blue','LineWidth',2,'markers',8);
p = plot(extract_120,'g-+');
set(p,'Color','green','LineWidth',2,'markers',8);
grid
% title('');
legend('Average 30s Duration','Average 60s Duration', 'Average 120s Duration', 2);
xlabel('Extraction Frequency (Hz)');
ylabel('Total Extraction Time (s)');
% set(p,'FontSize', 22, 'FontName', 'Times New Roman');    
set(gca,'XTick', [1:7]);
set(gca,'XTickLabel',{'0.125','.25','0.5','1','2','4','8'});
axis([0.5 7.5 0 350]);
pbaspect([2,1,1]);  

filename = ['frame.eps'];
saveas(h, filename,'psc2');   
