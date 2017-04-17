s=zeros(3, 5)
s=[1605 1575 1350 1932 0
2011 1864 1744 2487 0
2231 1982 2129 3108 0]

s(1,:)=s(1,:)/4000.0;
s(2,:)=s(2,:)/5000.0;
s(3,:)=s(3,:)/6000.0;


h=subplot(1,1,1);
hold on;
bar(s/4.0*6*100);

legend('MCF', 'EDF', 'RR', 'MSC', 2);

axis([0.3 3.5 0 100]);
set(h,'FontSize', 22, 'FontName', 'Times New Roman');    
set(gca,'XTickLabel', {'4','5','6'})
set(gca,'XTick', [1:3]);
xlabel('Different Query Numbers');
ylabel('Completeness (\times100%)');

filename = ['different_queries.eps'];
saveas(h, filename,'psc2');         
