import sys
from ROOT import TLatex, TLegend


def myText(x,y,text, tsize,color):
    l = TLatex()
    l.SetTextSize(tsize); 
    l.SetNDC();
    l.SetTextColor(color);
    l.DrawLatex(x,y,text);


def getLegend(x1,y1,x2,y2,h1,h2,txt1,txt2,style1,style2):
    l = TLegend(x1,y1,x2,y2)
    l.SetFillColor(0)
    l.SetFillStyle(0)
    l.SetBorderSize(0)
    l.AddEntry(h1,txt1,style1)
    l.AddEntry(h2,txt2,style2)
    return l

def setGraphStyle(gr):
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(1.0)


def setBinLabels(gr,names):
    h = gr.GetHistogram()
    print h.GetNbinsX(), ' vs ', gr.GetN()
    i = 0
    for p in names:
        b = h.FindBin(i)
        h.GetXaxis().SetBinLabel(b, p )
        i = i + 1
