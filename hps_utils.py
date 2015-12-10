import re, sys


def get_run_from_filename(name):
    m = re.match('.*/?hps_00(\d+)\..*',name)
    if m != None:
        #print 'm0 ', m.groups()
        return int(m.group(1))
    m = re.match('.*run(\d+)_.*',name)
    if m != None:
        #print 'm1 ', m.groups()
        return int(m.group(1))    
    m = re.match('.*run_(\d+)_.*',name)
    if m != None:
        #print 'm2 ', m.groups()
        return int(m.group(1))    
    else:
        print 'cannot get run number from ', name
        sys.exit(1)


def get_module_names():
    
    names = []
    for l in range(1,7):
        for h in ['t','b']:
            for t in ['axial','stereo']:
                if l < 4:
                    name = 'module_L' + str(l) + h +'_halfmodule_' + t + '_sensor0'
                    names.append(name)
                else:
                    for s in ['hole','slot']:
                        name = 'module_L' + str(l) + h +'_halfmodule_' + t + '_' + s + '_sensor0'
                        names.append(name)
    return names


def getshortsensorname(name):
    s = name
    s = s.replace('_sensor0','')
    s = s.replace('_halfmodule','')
    s = s.replace('_module_','')
    s = s.replace('module_','')
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
