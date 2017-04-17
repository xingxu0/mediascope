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
hold on;
x=[10.5 10.5]
y=[0 55]
xx=[0 15]
yy=[50 50]
l=plot(x,y,'-.k');
hold on;
ll=plot(xx,yy,'-.k');
hold on;
xxx=10.5;yyy=50;
lll=plot(xxx,yyy,'ok', 'LineWidth', 2);
text(3, 70, '[10.5, 50%]','FontSize', 18, 'FontName', 'Times New Roman');   
a=[10.5 10.5]
b=[66 55]
hold on;
plot(a,b,'-k','LineWidth',2)
a=[10 10.5]
b=[57 55]
hold on;
plot(a,b,'-k','LineWidth',2)
a=[11 10.5]
b=[57 55]
hold on;
plot(a,b,'-k','LineWidth',2)    
set(h,'FontSize', 22, 'FontName', 'Times New Roman');    
xlabel('Availability Gap (day)');
ylabel('Percentage (\times100%)');
axis([0 60 0 102]);
hh=axes('position', [0.45, 0.2, 0.4, 0.3]);
q=plot(t,'r')
set(hh,'FontSize', 18, 'FontName', 'Times New Roman'); 
title('Entire CDF', 'FontSize', 18, 'FontName', 'Times New Roman'); 
set(q,'LineWidth',2)
grid


filename = ['cdf.eps'];
saveas(h, filename,'psc2');         
