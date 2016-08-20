import urllib2
import re

class Weather:

    def __init__ (self):
        """ init function """
        self.url = 'http://www.meteo-paris.com'
        self.ecart_reg = re.compile('Ecart saisonnier.*?([-0-9]+)', re.DOTALL)
        self.pluie_reg = re.compile('span class=\'pourcent\'>([0-9]+)')
        self.temp_midi_reg = re.compile('-midi</div>.*?([-0-9]+)<br', re.DOTALL)
        self.temp_matin_reg = re.compile('Matin</div>.*?([-0-9]+)<br', re.DOTALL)
        self.temp_soir_reg = re.compile('Soir.*?([-0-9]+)<br', re.DOTALL)

        self.ecart_saisonnier = -20
        self.pluie = -20
        self.temp_midi = -20
        self.temp_matin = -20
        self.temp_soir = -20

    def refresh (self):
        """ refresh weather data """
        # read data
        response = urllib2.urlopen (self.url)
        html = response.read()

        # write to file for debugging
        with open ('meteo.html','w') as fp:
            fp.write (html)

        # scan for temperature difference
        d = re.findall (self.ecart_reg, html)
        if len(d)!=1:
            print('ERROR : failed to find regexp for ecart saisonnier')
        else:
            self.ecart_saisonnier = int(d[0])

        # scan for rain prob
        d = re.findall(self.pluie_reg, html)
        if len(d)!=1:
            print('ERROR : failed to find regexp for rain')
        else:
            self.pluie = int(d[0])
        
        # scan for temperatures
        d = re.findall(self.temp_matin_reg, html)
        if len(d)!=1:
            print('ERROR : failed to find regexp for temp matin')
        else:
            self.temp_matin = int(d[0])
        # scan for temperatures
        d = re.findall(self.temp_midi_reg, html)
        if len(d)!=1:
            print('ERROR : failed to find regexp for temp midi')
        else:
            self.temp_midi = int(d[0])
        # scan for temperatures
        d = re.findall(self.temp_soir_reg, html)
        if len(d)!=1:
            print('ERROR : failed to find regexp for temp soir')
        else:
            self.temp_soir = int(d[0])


    def printout (self):
        print('Ecart saisonnier: %d deg.' % self.ecart_saisonnier) 
        print('Probabilite de pluie: %d %%' % self.pluie)
        print('Morning temp: %d deg' % self.temp_matin)
        print('Afternoon temp: %d deg' % self.temp_midi)
        print('Evening temp: %d deg' % self.temp_soir)

        pass


def main():
    w = Weather()
    w.refresh()
    w.printout()


if __name__ == "__main__":

    main()

