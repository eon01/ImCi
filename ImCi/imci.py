import os
import tempfile
import urllib2
from urlparse import urlparse
import ConfigParser
import logging
import logging.config
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

class Check(object):

    """ if a single image has a bigger size than the fixed size limit  """

    def __init__(self):
        """ init """
        config = {}
        logging.config.fileConfig('logging.ini')
        self.logger = logging.getLogger(__name__)

        execfile("settings.py", config)

        self.header = config["HEADER"]
        self.source = config["SOURCE"]
        self.max_img_size = config["MAX_IMG_SIZE"]
        self.domain = self.source.split('/')[2]


    def download(self):
        """ using wget to crawl all the wesbite for images """
        f = tempfile.NamedTemporaryFile(delete=False)
        self.destination = f.name
        command = "wget -D {} --spider -r --header='{}' {}  --delete-after 2>&1 | grep '^--' | awk '{{ print $3 }}' | grep '\.\(png\|gif\|jpg\|JPG\|jpeg\|bmp\|png\|svg\)$' > {}".format(self.domain, self.header, self.source, self.destination)
        os.system(command)
        return self.destination

    def check_size(self, tempfile):
        """ return the size in OCTETs / Byte of an image """
        self.tempfile = tempfile
        print tempfile
        imci_size = {}
        with open(tempfile) as f:
                for line in f:
                    try:
                        res = urllib2.urlopen(line)
                    except urllib2.HTTPError:
                        self.logger.error(line + ' : http error - ignoring')
                        pass

                    if int(res.info().getheaders("Content-Length")[0]) > int(self.max_img_size):
                        imci_size[line] = res.info().getheaders("Content-Length")[0]
                        self.logger.info(line + '- size check ok')
                    else:
                        self.logger.info(line + '- size check ko')
                        pass

        return imci_size

    def validate(self, imci_size):
        """ return true or false in fuction of the test """
        self.imci_size = imci_size
        if (len(imci_size) != 0):
            exit(1)
        elif (imci_size == 0):
            exit(0)




