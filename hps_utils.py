import re, sys

def getshortsensorname(name):
    s = name
    s = s.replace('_sensor0','')
    s = s.replace('_halfmodule','')
    s = s.replace('_module','')
    return s

def getSensorNames(includeL0=False):
    names = []
    if includeL0: r = [0,1,2,3,4,5,6]
    else: r = [1,2,3,4,5,6]    
    for l in r:
        for h in ['t', 'b']:
            #if l==0 and h=='t': #L0 is only for bottom
            #    continue
            for t in ['axial','stereo']:
                name = ''
                if l > 3:
                    for s in ['hole','slot']:
                        name = 'module_L%d%s_halfmodule_%s_%s_sensor0' % (l, h, t,s)
                        names.append(name)
                else:
                    name = 'module_L%d%s_halfmodule_%s_sensor0' % (l, h, t)
                    names.append(name)
    return names

def getSensor(name):
    m = re.match('.*_module_(.*)_sensor0.*',name)
    if m!=None:
        return m.group(1)
    else:
        print 'error get sensor from ', name

def getLayer( deName):
    m = re.search("_L(\d)\S_", deName)
    if m!=None:            
        l = m.group(1)
        il = int(l)
        return il
    else:
        print "Cannot extract layer number from deName ", deName
        sys.exit(1)

def getHalf( deName):
    m = re.search("_L\d(\S)_", deName)
    if m!=None:            
        return m.group(1)
    else:
        print "Cannot extract half from deName ", deName
        sys.exit(1)

def getAxialStereo( deName):
    l = getLayer(deName)
    if l < 4:
        m = re.search("_halfmodule_(\S+)_sensor", deName)
    else:
        m = re.search("_halfmodule_(\S+)_\S+_sensor", deName)
    if m!=None:            
        return m.group(1)
    else:
        print "Cannot extract axial or stereo from deName ", deName
        sys.exit(1)

def getHoleSlot( deName):
    l = getLayer(deName)
    if l < 4:
        return None
    else:
        m = re.search("halfmodule_\S+_(\S+)_sensor", deName)
        if m!=None:            
            return m.group(1)
        else:
            print "Cannot extract axial or stereo from deName ", deName
            sys.exit(1)
