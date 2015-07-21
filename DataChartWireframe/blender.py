

class Appliance(object):

    def __init__(self, name):
        """
        Constructor
        """
        self.name = name

    def run_appliance(self, heat_level=1):

        if heat_level > 5:
            print "it's burnt!"
        else:
            print "it's toasted!"


    def get_dict_for_web(self):

        d = {}
        for k, v in self.__dict__.items():
            d[k] = v
        return d

'''
class Blender(Appliance):

    def __init__(self):
        """
        Constructor
        """
        pass
'''

if __name__=='__main__':
    a = Appliance('toaster')
    print a.name
    a.run_appliance()

    b = Appliance('toaster2')
    b.run_appliance(7)

    print a.get_dict_for_web()