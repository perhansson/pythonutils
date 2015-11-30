
def getshortsensorname(name):
    s = name
    s = s.replace('_sensor0','')
    s = s.replace('_halfmodule','')
    s = s.replace('_module','')
    return s
