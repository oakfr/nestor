import urllib2
import re

class BusChecker:

    def __init__ (self):
        self.urls = {\
                'B_72':'http://www.ratp.fr/horaires/fr/ratp/bus/prochains_passages/PP/B72/72_94_107/A',\
                'B_22':'http://www.ratp.fr/horaires/fr/ratp/bus/prochains_passages/PP/B22/22_31/A',\
                'B_PC1':'http://www.ratp.fr/horaires/fr/ratp/bus/prochains_passages/PP/BPC1/PC1_4042_4074/A',\
                'M_10':'http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/chardon+lagache/10/A',\
                'M_9' :'http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/exelmans/9/A'}
        self.re_search = re.compile ('[0-9]+ mn')
        self.next_bus = {}


    def to_string (self):
        s = ''
        for k,v in self.urls.iteritems():
            s += '%s: ' % (k)
            if k in self.next_bus:
                for v in self.next_bus[k]:
                    s += '%d ' % v
            s += '\n'
        return s


    def __str__ (self):
        s = ''
        for k,v in self.urls.iteritems():
            s += '%s: ' % (k)
            if k in self.next_bus:
                for v in self.next_bus[k]:
                    s += '%d ' % v
            s += '\n'
        return s


    def refresh (self):
        self.next_bus = {}
        for k,v in self.urls.iteritems():
            response = urllib2.urlopen (v)
            html = response.read()
            times = re.findall (self.re_search,html)
            self.next_bus[k] = []
            count=0
            for mtime in times:
                stime = int(mtime.split(' ')[0])
                self.next_bus[k].append (stime)
                count += 1
                if count == 2:
                    break

    def lines_names_sorted (self):
        return sorted(self.next_bus.keys())


    def lines_times_sorted (self):
        return [self.next_bus[x] for x in self.lines_names_sorted()]


def main():
    b = BusChecker()
    b.refresh()
    print(b.to_string())

if __name__ == "__main__":

    main()


