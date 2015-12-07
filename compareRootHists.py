#!/usr/bin/python

import sys, os
import argparse
from ROOT import TFile, gDirectory, TIter, TCanvas, TF1
from plotutils import myText, getLegend, getLegendList, getHistograms, getHistMaxBinValue




def compareHists(histos,legends=None,normalize=None,fitName=None, t='',pad=None,myTextSize=0.05):
    print 'compareHists:'
    if fitName != None: print 'fitName: ', fitName
    c = None
    cName = 'c_'
    if pad == None:
        for h in histos:
            print h.GetName(), ' ', h.GetEntries()
            cName += h.GetName()
        c = TCanvas(cName, cName ,10 ,10 ,700 ,500)
    else:
        pad.cd()
    fillColors = [33,45,20,4,4,4,4,4,4,4,4]
    lineColors = [1,2,3,4,5,6,7,8,9,10]
    #lineColors = [1,2,3,4,5,6,7,8,9,10]
    lineWidth = 2
    n = 0
    nm = 0
    maxBC = -1.
    hFirst = None
    for ih in range(len(histos)):
        h = histos[ih]
        if ih == 0:
            hFirst = h
        h.SetLineColor(lineColors[ih])
        h.SetLineWidth(lineWidth)
        h.Sumw2()
        if normalize != None:
            if h.Integral() == 0:
                print 'warning: histogram ', h.GetName(), ' cannot be normalized with no integral!'
            else:
                h.Scale(1.0/h.Integral())
        if h.GetMaximum() > maxBC:
            maxBC = h.GetMaximum()
        f = None
        if fitName != None:
            if fitName['name'] == 'gaus':
                print 'Fitting ', h.GetName()
                fitFuncName = 'fg_' + h.GetName()
                fitOpt = '0R'
                fg = TF1(fitFuncName,'gaus')
                if h.GetRMS() < 1e-10 or h.GetRMS() < h.GetBinWidth(1):
                    print 'WARNING: histogram ', h.GetName(), ' has small RMS', h.GetRMS(), ' dont fit but use that RMS and mean ', h.GetMean() 
                    fg.SetParameter(0,0) 
                    fg.SetParameter(1, h.GetMean() )
                    fg.SetParameter(2, h.GetRMS() )
                    listOfFunctions = h.GetListOfFunctions()
                    print 'got ', len(listOfFunctions), ' function'
                    for func in listOfFunctions: print func.GetName()
                    listOfFunctions.append(fg)
                    print 'now got ', len(listOfFunctions), ' function'
                    for func in listOfFunctions: print func.GetName()
                else:
                    if 'xmin' and 'xmax' in fitName:
                        fg.SetRange(fitName['xmin'],fitName['xmax'])
                    else:
                        fg.SetRange(h.GetBinCenter(1),h.GetBinCenter(h.GetNbinsX()+1))
                    if 'peakbin' in fitName:
                        bc = getHistMaxBinValue(h)    
                        fg.SetParameter(1,bc)                
                    if 'rms' in fitName:
                        bc = getHistMaxBinValue(h)    
                        rms = h.GetRMS()
                        fg.SetParameter(1,bc)                
                        fg.SetParameter(2,rms)                
                        fg.SetRange( bc - rms*fitName['rms'], bc + rms*fitName['rms'] )
                    h.Fit(fg,fitOpt)
                f = fg #h.GetFunction(fitFuncName)
                if f != None:
                    f.SetLineColor(lineColors[ih])
                    f.SetLineWidth(lineWidth)
        if ih != -1:
            h.SetFillColor(fillColors[ih])
            h.SetFillStyle(3002)
        if ih == 0:
            h.Draw('hist')
        else:
            h.Draw('hist,same')

        if f != None:
            f.Draw('same')
            if fitName['name'] == 'gaus':
                myText(0.13,0.2+ih*myTextSize,'<m>=%.2e #sigma=%.2e'%(f.GetParameter(1),f.GetParameter(2)),myTextSize,lineColors[ih])
        n=n+1
        #ans = raw_input('press anywhere to continue')
    
    hFirst.SetMaximum(maxBC)
    if legends:
        styles = ['FL' for x in range(len(histos))] 
        l = getLegendList(0.13,0.75,0.25,0.85,histos,legends,styles)
        l.Draw()

    if c != None:
        name = cName
        if t != '':
            name += '_' + t
        c.SaveAs(name + '.png')
    #ans = raw_input('press anywhere to continue')



def main(file1,file2,legend=None,skip=None,only=None,skipempty=True,pause=False):
    print 'GO'

    f1 = TFile(file1)
    f1name = os.path.splitext(os.path.basename(file1))[0]
    histos1 = getHistograms(gDirectory)

    f2 = TFile(file2)
    f2name = os.path.splitext(os.path.basename(file2))[0]
    histos2 = getHistograms(gDirectory)

    n = 0
    nm = 0
    c = TCanvas('c_'+f1name+'_'+f2name,'c_'+f1name+'_'+f2name,10,10,700,500)
    #open file
    c.Print('cmp_' + f1name + '_' + f2name + '.ps[')
    for h1 in histos1:
        if skip != None:
            if skip in h1.GetName():
                continue
        if only != None:
            if only not in h1.GetName():
                continue
        print 'Look for ', h1.GetName()
        for h2 in histos2:
            if h1.GetName()==h2.GetName():            
                if skipempty:
                    if h1.GetEntries()==0.0 or h2.GetEntries()==0.0 or h1.Integral()==0.0 or h2.Integral()==0.0:
                        continue
                print 'match ', h1.GetName(), ' ',  h1.GetEntries(), ' ', h2.GetEntries()
                c = TCanvas('c_'+h1.GetName()+'_'+h2.GetName(),'c_'+h1.GetName()+'_'+h2.GetName(),10,10,700,500)
                h1.SetLineColor(4)
                h1.SetFillColor(4)
                h1.SetFillStyle(3004)
                h2.SetFillStyle(3005)
                h2.SetFillColor(2)
                h2.SetLineColor(2)
                h2.Scale(1.0/h2.Integral())
                h1.Scale(1.0/h1.Integral())
                if h1.GetMaximum()>h2.GetMaximum():
                    h1.Draw("hist")
                    h2.Draw("hist,same")
                else:
                    h2.Draw("hist")                    
                    h1.Draw("hist,same")
                #h1.DrawNormalized("hist",1.0/h1.Integral())
                #h2.DrawNormalized("same,hist",1.0/h2.Integral())
                n=n+1
                if legend:
                    l = getLegend(0.13,0.75,0.25,0.85,h1,h2,legend[0],legend[1],'FL','FL')
                    l.Draw()
                #c.SaveAs(c.GetName()+'.png')
                c.Print('cmp_' + f1name + '_' + f2name + '.ps')
                
                if pause:
                    ans = raw_input('press anywhere to continue')
            else:
                #print 'NO match ', h1.GetName()
                nm=nm+1
    print 'compared ', n, ' missed ', nm
    c.Print('cmp_' + f1name + '_' + f2name + '.ps]')
    

    f1.Close()
    f2.Close()
    return 0






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run comparison.')
    parser.add_argument('--files',nargs=2, required=True, help='Input files.')
    parser.add_argument('--skipempty',action='store_true', help='Input files.')
    parser.add_argument('--skip', help='Skip histogram containing this text.')
    parser.add_argument('--only', help='Use only histograms containing this text..')
    parser.add_argument('--pause', action='store_true',help='Pause b/w histograms')
    parser.add_argument('--legend',nargs=2,help='Legends to be used on plots.')
    args = parser.parse_args();
    print args
    
    #main(args)
    main(args.files[0],args.files[1],args.legend,args.skip,args.only,args.skipempty,args.pause)

