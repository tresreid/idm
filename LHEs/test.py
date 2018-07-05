import random
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Input LHE, which is to be replaced')
args = parser.parse_args()
inFn = args.input

inf = open(inFn,'r')
eventBegin = False
eventEnd = True
for line in inf:
	if line.startswith('<event>'):
		eventBegin = True
		eventEnd = False
	if line.startswith('</event>'):
		eventBegin = False
		eventEnd = True
	if not (eventBegin==True and eventEnd==False):
		#print line
		continue
	if line.split()[0] != str(32):
		continue
	else:
		assert(len(line.split())==13)
		togo = line.split()
		print togo[11]

