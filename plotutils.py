import sys
import math
from ROOT import TLatex, TLegend, gDirectory, TIter, TCanvas, Double, TH2F, TGraphErrors
from ROOT import Double as ROOTDouble


def divideTGraphs(gr_num, gr_den, checkNumPoints=False):
    ''' Assumes Poission errors. '''

    debug = False
    n = gr_num.GetN()
    
    if gr_den.GetN() != n and checkNumPoints:
        print 'graphs need the same nr of points'
        sys.exit(1)
    xn = ROOTDouble(0)
    yn = ROOTDouble(0)
    xd = ROOTDouble(0)
    yd = ROOTDouble(0)

    grR = TGraphErrors()
    grR.SetName(gr_num.GetName() + '_ratio')
    for i in range(n):
        gr_num.GetPoint(i,xn,yn)
        dy_num = gr_num.GetErrorY(i)
        # find the same point for the other graph
        for j in range(n):
            gr_den.GetPoint(j,xd,yd)
            dy_den = gr_den.GetErrorY(i)
            if xd != xn:
                continue
            else:
                # found it, do the ratio
                if yd == 0.:
                    print 'den is zero for point ', i, ' at x ', x
                    continue
                else:
                    point = grR.GetN()
                    r = yn/yd
                    if debug: print 'point ', point,' r ', r, ' yn ', yn, ' yd ', yd, ' x ', xn, ' dy_num ', dy_num, ' dy_den ', dy_den
                    dr = math.sqrt( (1/(yd**2)) * (dy_num**2) + ((yn/(yd**2))**2) * (dy_den**2) )
                    if dr/math.fabs(r) > 2.:
                        continue
                    grR.SetPoint(point,xn,r)
                    grR.SetPointError(point,0.,dr)
                    if debug: print 'point ', point,' r ', r, ' dr ', dr, ' x ', xn
    return grR


def setGraphXLabels(gr,idToName):
    h = gr.GetHistogram()
    for i,name in idToName.iteritems():
        b = h.FindBin(i)
        h.GetXaxis().SetBinLabel(b, name )

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

def getLegendList(x1,y1,x2,y2,histos,texts,styles):
    l = TLegend(x1,y1,x2,y2)
    l.SetFillColor(0)
    l.SetFillStyle(0)
    l.SetBorderSize(0)
    for i in range(len(histos)):
        h = histos[i]
        txt = texts[i]
        style = styles[i]
        l.AddEntry(h,txt,style)
    return l

def setGraphStyle(gr,color=1):
    gr.SetMarkerStyle(20)
    gr.SetMarkerSize(1.0)
    gr.SetMarkerColor(color)
    gr.SetLineColor(color)


def setBinLabels(gr,names):
    h = gr.GetHistogram()
    print h.GetNbinsX(), ' vs ', gr.GetN()
    i = 0
    for p in names:
        b = h.FindBin(i)
        h.GetXaxis().SetBinLabel(b, p )
        i = i + 1

def fixSaveName(name):
    save_name = name.replace(' ','_').replace(')','_').replace('(','_').replace('>=','')
    return save_name
    

def getTemplate(gr,names):
    n = gr.GetN()
    n_names = len(names)
    if n != n_names:
        print 'npoints ', n, ' n_names ', n_names, ' doesnt match'
        sys.exit(1)
    hgr = gr.GetHistogram()
    n_hgr = hgr.GetNbinsX()
    h = TH2F('h_' + gr.GetName(), gr.GetTitle(), n, hgr.GetXaxis().GetBinLowEdge(1),hgr.GetXaxis().GetBinUpEdge(n_hgr),10,hgr.GetMinimum(), hgr.GetMaximum())
    print h.GetNbinsX(), ' vs ', gr.GetN()
    i = 0
    for p in names:
        x , y =  ROOTDouble(0), ROOTDouble(0)
        gr.GetPoint(i,x,y)        
        b = h.GetXaxis().FindBin(x)
        print  'x ', x, ' y ', y, ' binlabel ', p, ' i ', i, ' b ', b, ' low ', hgr.GetXaxis().GetBinLowEdge(1), ' high ', hgr.GetXaxis().GetBinUpEdge(n_hgr)
        h.GetXaxis().SetBinLabel(b, p )
        i = i + 1
    return h


def setBinLabelsDict(gr,namePoints):
    h = gr.GetHistogram()
    print h.GetNbinsX(), ' vs ', gr.GetN()
    for i,p in namePoints.iteritems():
        b = h.FindBin(i)
        h.GetXaxis().SetBinLabel(b, p )

def getHistograms(direc):
    histos = []
    print direc.GetList().GetSize()
    iter = TIter(direc.GetListOfKeys())
    print iter.GetCollection().GetSize(), ' items in collection'
    while True:
        key = iter.Next()
        if not key:
            break
        obj = key.ReadObj()
        if obj.InheritsFrom('TH1') and not obj.InheritsFrom('TH2') and not obj.InheritsFrom('TH3'):
            print 'Getting TH1 %s' % obj.GetName()
            histos.append(obj)
    print 'Got ', len(histos), ' TH1s'
    return histos


def getGraphMaxMinVal(gr):
    ymax = -999999.9
    ymin = 999999.9
    for ipoint in range(gr.GetN()):
        x = Double(0.0)
        y = Double(0.0)
        gr.GetPoint(ipoint,x,y)
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y
    return [ymin, ymax]

def getHistMaxBinValue(h):    
    ymax = -999999.9
    for i in range(1,h.GetNbinsX()+1):
        y = h.GetBinContent(i)
        x = h.GetBinCenter(i)
        if y > ymax:
            ymax = y
            xmax = x
    return xmax


        
