c=zeros(1,5);
c=[1 1 8 13 45; 0 0 0 0 0 ]


h=subplot(1,1,1);
hold on;
bar(c/210*100);
legend('1632\times1224', '1280\times960', '1024\times768', '960\times720', '816\times612',2);

axis([0.5 1.5 0 25]);
set(h,'FontSize', 22, 'FontName', 'Times New Roman');    
%set(gca,'XTickLabel', {'1632x1224','1280x960','1024x768', '960x720','816x612'})
set(gca,'XTick', [0:0]);
xlabel('Different Image Resolution');
ylabel('Error Rate (\times 100%)');

filename = ['kmeans.eps'];
saveas(h, filename,'psc2');         
