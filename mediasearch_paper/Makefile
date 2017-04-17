#Jerry's Makefile for latex

TARGET = main.pdf
SOURCES =  main.tex abstract.tex Introduction.tex motivation.tex implementation.tex evaluation.tex

LATEX = latex
BIBTEX = bibtex
GREP = egrep
DVIPS = dvips
DVIPSFLAGS = -t Letter -Ppdf -G0 
PS2PDF = ps2pdf
PS2PDFFLAGS = -dAutoFilterColorImages=false \
	      -dColorImageFilter=/FlateEncode \
	      -dAutoFilterGrayImages=false \
	      -dGrayImageFilter=/FlateEncode \
	      -sPAPERSIZE=letter -dCompatibilityLevel=1.3

all: $(TARGET)

$(TARGET): $(SOURCES)

%.pdf: %.ps 
		#cp paper.ps paper2.ps
		$(PS2PDF) $(PS2PDFFLAGS) $*.ps
#		rm -f $*.ps
		#acroread $*.pdf &

%.ps: %.dvi 
		$(DVIPS) -o $*.ps $(DVIPSFLAGS) $*.dvi

%.dvi: %.tex 
		$(LATEX) $*
		$(GREP) -c "No file.*\.bbl|Citation.*undefined" $*.log && $(BIBTEX) $* ; true
		$(LATEX) $*  
		$(LATEX) $*

clean:
		-rm -f *~ *.log *.aux *.bbl *.blg *.idx *.dvi *.lof
		-rm -f *.lot *.ilg *.ind *.toc *.out
		-rm -f $(TARGET) 

cleanall: clean
		-rm -f $(TARGET) 

#compatible with older version
ps: root.pdf 
	gv root.pdf 

pdf: root.pdf 
	gv root.pdf 


