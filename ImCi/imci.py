import os
import tempfile
import urllib2

class Check(object):

    """ ImCi """

    def __init__(self, source):
        """init """
        self.source = source


    def download(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        self.destination = f.name
        command = "wget --spider -r {} 2>&1 | grep '^--' | awk '{{ print $3 }}' | grep '\.\(png\|gif\|jpg\|JPG\|jpeg\|bmp\|png\|svg\)$' > {}".format(self.source, self.destination)
        os.system(command)
        return self.destination


    def check_size(self):
        tempfile = self.download()
        with open(tempfile) as f:
                for line in f:
                    res = urllib2.urlopen(line)
                    size = res.getheaders("Content-Length")


