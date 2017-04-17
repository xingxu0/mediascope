h=subplot(1,1,1);
a=load('numstat');
x=zeros(300,1);
for (i=1:size(a))
    x(a(i)+1)=x(a(i)+1)+1;
end

aa=0;
for(i=1:size(x))
   aa=aa+x(i);
end
t=zeros(300,1)
for (i=1:size(x))
    for(j=1:i-1)
        t(i)=t(i)+x(j);
    end
end

t=t/aa*100;
p=plot(t);
set(p,'LineWidth',2)
    

set(h,'FontSize', 22, 'FontName', 'Times New Roman');    
xlabel('Availability Gap (day)');
ylabel('Percentage (\times100%)');
axis([0 300 0 102]);

filename = ['cdf.eps'];
saveas(h, filename,'psc2');         
