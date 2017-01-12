"""
stock data downloaded from Quandl:
https://www.quandl.com/tools/python

inaguration dates scraped from:
http://historyinpieces.com/research/presidential-inauguration-dates
"""
import quandl
quandl.ApiConfig.api_key = "bHAtLkvG5cEhJCSVp1zx"
import matplotlib.pyplot as plt
import numpy as np
import webinspect
import datetime

if not 'DOW' in globals().keys():
    print("downloading the dow...")
    DOW=quandl.get("BCB/UDJIAD1") # download stock data from quandl

inog="""3/4/1797, 3/4/1801, 3/4/1809, 3/4/1817, 3/4/1825, 3/4/1829, 
3/4/1837, 3/4/1841, 4/6/1841, 3/4/1845, 3/5/1849, 7/10/1850, 3/4/1853, 
3/4/1857, 3/4/1861, 4/15/1865, 3/4/1869, 3/5/1877, 3/4/1881, 9/20/1881,
3/4/1885, 3/4/1889, 3/4/1897, 9/14/1901, 3/4/1909, 3/4/1913, 3/4/1921, 
8/3/1923, 3/4/1929, 3/4/1933, 4/12/1945, 1/20/1953, 1/20/1961, 11/22/1963, 
1/20/1969, 8/9/1974, 1/20/1977, 1/20/1981, 1/20/1989, 1/20/1993, 1/20/2001,
1/20/2009""" 

if __name__=="__main__":
    dow=DOW.copy() # don't modify original downloaded data
    dates,values=list(np.array(dow.index)),dow.values
    for i,dt in enumerate(dates): # string format inog dates
        dates[i]=str(str(dt).split("T")[0])
    inogs=inog.replace("\n",'').split(',')
    for i,inog in enumerate(inogs): # string format stock price dates
        mn,dy,yr=inog.split("/")
        inogs[i]="%d-%02d-%02d"%(int(yr),int(mn),int(dy))

    padding=5 # years
    paddingDays=int(padding*365)
    Xs=(np.arange(paddingDays*2)-paddingDays)/365
    plt.figure(figsize=(15,15))
    plt.grid()
    avg=None
    for inog in [x for x in inogs if x in dates]:
        I=dates.index(inog)        
        I1,I2=I-paddingDays,I+paddingDays
        if I1<0 or I2>len(dates):
            continue
        chunk=values[I1:I2]
        chunk-=min(chunk)
        chunk=chunk/float(max(chunk))*100.0-50
        if avg is None:
            avg=np.array(chunk)
        else:
            avg=np.hstack((avg,chunk))
        #plt.plot(Xs,chunk,label=inog,alpha=.5,lw=2)
    AV=np.average(avg,axis=1)
    ER=np.std(avg,axis=1)
    plt.plot(Xs,AV,'-',lw=3,color='k',label='average')
    plt.plot(Xs,AV+ER,'-',lw=3,color='k',ls='--')
    plt.plot(Xs,AV-ER,'-',lw=3,color='k',label='stdev',ls='--')
    plt.axvline(0,color='r',lw=5,alpha=.2)
    plt.legend()
    plt.margins(0,.1)
    plt.ylabel("fractional change")
    plt.xlabel("years away from inauguration date")
    plt.title("Dow Jones Aligned to US Presidential Inaugurations")
    plt.show()
    print("DONE")