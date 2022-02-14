import csv
import json
import os
from urllib.request import urlopen
import contextlib
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def getfile(url,filename,timeout=1800):
    with contextlib.closing(urlopen(url,timeout=timeout, context=ctx)) as fp:
        block_size = 1024 * 8
        block = fp.read(block_size)
        if block:
            with open(filename,'wb') as out_file:
                out_file.write(block)
                while True:
                    block = fp.read(block_size)
                    if not block:
                        break
                    out_file.write(block)
        else:
            raise Exception ('nonexisting file or connection error')


def parseCsv(csvFilePath,pkey):
	data = {}
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for rows in csvReader:
			key = rows[pkey]
			data[key] = rows
	return data
		
csvFilePath = r'video-list.csv'
pkey = r'sequence'
dict = parseCsv(csvFilePath, pkey)

try:
    os.mkdir('1080P')
except OSError as error:
    pass
try:
    os.mkdir('4K')
except OSError as error:
    pass
try:
    os.mkdir('4K-HDR')
except OSError as error:
    pass

for sequence in list(dict.keys()):
    location = dict[sequence]['location']
    try:
        os.mkdir(os.path.join('1080P', location))
    except OSError as error:
        pass
    try:
        os.mkdir(os.path.join('4K', location))
    except OSError as error:
        pass
    try:
        os.mkdir(os.path.join('4K-HDR', location))
    except OSError as error:
        pass

    try:getfile(dict[sequence]['1080p'], "1080P/%s/%s" % (location, dict[sequence]['1080p'].split("/")[-1]))
    except:pass
    try:getfile(dict[sequence]['4k'], "4K/%s/%s" % (location, dict[sequence]['4k'].split("/")[-1]))
    except:pass
    try:getfile(dict[sequence]['4k-hdr'], "4K-HDR/%s/%s" % (location, dict[sequence]['4k-hdr'].split("/")[-1]))
    except:pass

        