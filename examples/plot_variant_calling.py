#!/usr/bin/env python3
"""Plot the measured tiny SV and official repeat examples, with distinct units."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
def plot(sv,repeat,output):
    s=json.loads(sv.read_text());r=json.loads(repeat.read_text());output.mkdir(parents=True,exist_ok=True)
    fig,(a,b)=plt.subplots(2,1,figsize=(10,6.2),layout='constrained')
    a.plot([0,100000],[1,1],color='#576b79',lw=2)
    a.plot([30000,30500],[1,1],color='#a63254',lw=7)
    a.scatter([70000],[1],marker='v',s=90,color='#187ca8',zorder=4)
    a.annotate('DEL 500 bp\nanchor 30,000',xy=(30250,1),xytext=(30000,1.28),ha='center',arrowprops={'arrowstyle':'->','color':'#a63254'})
    a.annotate('INS 300 bp\nanchor 70,000',xy=(70000,1),xytext=(70000,1.28),ha='center',arrowprops={'arrowstyle':'->','color':'#187ca8'})
    a.text(50000,.62,'Actual Sniffles / Truvari: TP-base = 2, TP-comp = 2, FP = FN = 0\nTwo artificial events only; cohort R01 stays missing',ha='center',fontsize=10)
    a.set(xlim=(-2000,102000),ylim=(.4,1.6),yticks=[],xlabel='chrToySV coordinate (bp)',title='Artificial SV case: perfect reads, actual mapping and calling')
    a.spines[['top','right','left']].set_visible(False)
    sample=next(iter(r['variants'][0]['samples'].values()));lengths=[60,*sample['AL']]
    b.barh(['Reference repeat span','Called allele 1','Called allele 2'],lengths,color=['#6c7a89','#187ca8','#187ca8'])
    for i,n in enumerate(lengths):b.text(n+.8,i,str(n)+' bp',va='center')
    b.invert_yaxis();b.set(xlim=(0,72),xlabel='Repeat length, excluding VCF padding (bp)',title='Official TRGT chrA / TR1: CAG motif counts 11, 11')
    b.spines[['top','right']].set_visible(False)
    fig.savefig(output/'calling-and-repeat.png',dpi=180);plt.close(fig)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sv',type=Path,default=ROOT/'examples/output/calling-sv/summary.json')
    p.add_argument('--repeat',type=Path,default=ROOT/'examples/output/trgt-official/summary.json')
    p.add_argument('--output',type=Path,default=ROOT/'examples/output/variant-calling-plots')
    args=p.parse_args();plot(args.sv,args.repeat,args.output)
