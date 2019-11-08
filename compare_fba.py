#!/bin/python3
import pandas as pd
from optparse import OptionParser
import sys
import numpy as np

def main():
    parser = OptionParser()
    parser.add_option("-m","--file1",dest="filename1",help="FBA input file 1 in tsv format",metavar="FILE")
    parser.add_option("-n","--file2",dest="filename2",help="FBA input file 2 in tsv format",metavar="FILE")
    parser.add_option("-o","--outfile",dest="outfile",help="Output FBA comparison filename in csv format",metavar="FILE")
    (options, args) = parser.parse_args()
    try:
      data1 = pd.read_csv(options.filename1,sep="\t");
      data2 = pd.read_csv(options.filename2,sep="\t");
    except IOError:
        print("files not found")
        sys.exit(2)
    data = data1.append(data2)
    grouped = data.groupby(['id'])
    # for the reactions that appear in both FBA solutions
    flux1 = []
    flux2 = []
    comi = [] # common reaction id
    com_name = [] # common reaction names
    diffi = [] # different reaction id
    for i in grouped:
        # i[0] = id, i[1] = dataframes of list of data1 and data2
        content = i[1] # dataframe
        fluxes = content['flux'].values
        if( len(fluxes) == 2 ): # the reaction is common in data1 and data2
            comi.append(i[0]) # id
            com_name.append(content['name'].values[0]) # name
            flux1.append(fluxes[0])
            flux2.append(fluxes[1])
        elif ( len(fluxes) == 1): # the reaction exists in only one data
            diffi.append([i[0],content['name'].values[0]]) # [id, name]
            if (data1[data1['id'].values==i[0]].empty): # the reaction doesn't exist in data1
                print('Only #2 has: '+i[0]+', '+content['name'].values[0])
            else:
                print('Only #1 has: '+i[0]+', '+content['name'].values[0])
    # compute the similarity of two fluxes
    print(np.corrcoef(flux1,flux2))
    df = pd.DataFrame(list(zip(comi,com_name,flux1,flux2,np.abs(np.subtract(flux1,flux2)))),columns=['id','name','flux1','flux2','diff'])
    df = df.sort_values(by=['diff'],ascending=False)
    df.to_csv(options.outfile)

if __name__ == "__main__":
    main()
