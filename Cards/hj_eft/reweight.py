#!/usr/bin/env python
##Spin 1
#2=>gDMV
#3=>gDMA
# 4, 5, 6, 7, 8, 9=>gV
#10,11,12,13,14,15=>gA


def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])

def printsetg(gt,cgt,cyr,cyi,mtp):
    weight_id = 'gt_%s_cgt_%s_cyr_%s_cyi_%s_mtp_%s' % (str(gt), str(cgt), str(cyr), str(cyi),str(mtp))
    print 'launch --rwgt_name=%s' % (weight_id.replace('.','p'))
    #Scalar
    print 'set param_card DIM6  1  %s' % str(gt)
    print 'set param_card DIM6  2  %s' % str(cgt)
    print 'set param_card DIM6  3  %s' % str(cyr)
    print 'set param_card DIM6  4  %s' % str(cyi)
    print 'set param_card mass  6000006 %s' % str(mtp)
    print 'set param_card decay 25 AUTO'
    print 'set param_card decay 6000006 AUTO'

print 'change mode LO'
print 'change helicity False'
print 'change rwgt_dir rwgt'
weight_counter = 0

print '#' + str(weight_counter) + ' start of scalar'

#pure scalar
for mtp in [10000]:
    for gt in [0.5,1.0,2.0]:
        for cgt in [0.0,0.5,1.0,2.0,5.0]:
            for cyr in [-0.3,0,0.3]:
                for cyi in [0.]:
                    tCyr=cgt+cyr
                    printsetg(gt,cgt,tCyr,cyi,mtp)
                    weight_counter += 1
