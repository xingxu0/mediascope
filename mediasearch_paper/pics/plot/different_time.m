s=zeros(3, 5)
s=[2053 1853 1410 2398 2400 
   2856 2459 1680 3078 3080
   2427 2208 1856 2911 2930]



   

h=subplot(1,1,1);
hold on;
bar(s/4.0*6/6000*100);

legend('MCF', 'EDF', 'RR', 'MSC', 'OMNI', 2);

set(h,'FontSize', 22, 'FontName', 'Times New Roman');    
set(gca,'XTickLabel', {'Interrupted','Staggered','Complex'});
set(gca,'XTick', [1:3]);
xlabel('Different Query Settings');
ylabel('Completeness (\times100%)');
axis([0.5 3.5 0 100]);

filename = ['different_times.eps'];
saveas(h, filename,'psc2');         
