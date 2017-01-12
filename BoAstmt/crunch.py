"""
python script to analyze a checking account statement.
On the BoA Accounts screen, click on "Download" and it will
let you download a custom date range (up to 18 months) as a
stmt.csv file (which it calls Excel format, doh!)

The purpose of this script is to estimate large-scale
spending habits over the last year and a half.
"""
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np

def monthlyStmt(fname,transfers={}):
    with open(fname, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for i,line in enumerate(spamreader):
            if not len(line)==4 or not line[0].count("/")==2:
                continue
            if line[2]=="":
                continue
            dt,desc,val,tot=line
            desc,val,tot=str(desc).upper(),float(val),float(tot)
            
            # exclude paychecks, deposits, and transfers
            if val>0 and "UNIVERSITY OF FL" in desc:
                continue
            if "TRANSFER TO SAV" in desc:
                continue
            if "IRS DES" in desc:
                print("SKIPPING IRS PAYMENT:",dt,val)
                continue                
            
            # eyeball check
            if val<-500 and not "BILL PAYMENT" in desc:
                print("Large spending:",dt,desc,val)
                
            # add this transaction to this month's balance
            month=dt.split("/")[2]+"-"+dt.split("/")[0]
            if not month in transfers.keys():
                transfers[month]=0
            transfers[month]=round(transfers[month]+val,2)
            
    return transfers

if __name__=="__main__":
    data=monthlyStmt(r"C:\Users\scott\Downloads\stmt.csv")
    Xs,Ys=[],[]
    for item in sorted(data.keys()):
        Ys.append(data[item])
        item=item.split("-")
        Xs.append(datetime.date(int(item[0]),int(item[1]),1))
    plt.figure(figsize=(7,5))
    msg="%d months of transactions (avg %d/mo)"%(len(Ys)-2,np.average(Ys[1:-1]))
    msg+="\n(paycheck income and taxes are excluded)"
    plt.title(msg)
    plt.ylabel("net transaction value (USD)")
    plt.grid()
    plt.plot(Xs,Ys,'.-',ms=10,color='k',alpha=.5)
    Xs,Ys=Xs[1:-1],Ys[1:-1] # skip first and last month (incomplete data)
    plt.plot(Xs,Ys,'.-',ms=10)
    plt.axhline(np.average(Ys),color='r',ls='--',lw=3,alpha=.3)
    plt.margins(.1,.1)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.show()
    print("DONE")