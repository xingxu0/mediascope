c=zeros(1,5);
c=[4138 2957 1860 1522 1262; 0 0 0 0 0 ]


h=subplot(1,1,1);
hold on;
bar(c);
legend('1632\times1224', '1280\times960', '1024\times768', '960\times720', '816\times612',1);

axis([0.5 1.5 0 5000]);
set(h,'FontSize', 22, 'FontName', 'Times New Roman');    
%set(gca,'XTickLabel', {'1632x1224','1280x960','1024x768', '960x720','816x612'})
set(gca,'XTick', [0:0]);
xlabel('Different Image Resolution');
ylabel('Processing Time (ms)');

filename = ['cedd.eps'];
saveas(h, filename,'psc2');         
