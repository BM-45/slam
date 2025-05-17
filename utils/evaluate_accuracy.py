#!/usr/bin/env python3
import argparse, os, sys, numpy as np
from pykitti import raw

def load_gt(p, d, r):
    ds = raw(p, d, r)
    Rs, ts = [], []
    for o in ds.oxts:
        T = o.T_w_imu
        Rs.append(T[:3,:3]); ts.append(T[:3,3])
    if not ts: sys.exit("no ground truth")
    return Rs, ts

def load_est(f):
    if not os.path.isfile(f): sys.exit("no est file")
    v = np.fromfile(f, sep=' ')
    n = len(v)//12
    if n==0: sys.exit("no data in est file")
    b = v[:n*12].reshape(n,12)
    Rs = [x[:9].reshape(3,3) for x in b]
    ts = [np.array([x[3],x[7],x[11]]) for x in b]
    return Rs, ts

def align(A, B):
    cA, cB = A.mean(0), B.mean(0)
    H = (A-cA).T@(B-cB)
    U,_,Vt = np.linalg.svd(H)
    R = Vt.T@U.T
    if np.linalg.det(R)<0: Vt[2]*=-1; R=Vt.T@U.T
    return R, cB-R@cA

def ate(Rg, tg, Re, te):
    A = np.stack(te)
    B = np.stack(tg)
    R,t = align(A,B)
    Ae = (R@A.T).T + t
    e = np.linalg.norm(Ae-B,axis=1)
    return np.sqrt((e**2).mean())

def rpe(Rg, tg, Re, te, d):
    T = lambda x: (align(np.vstack(te),np.vstack(tg)) and None)
    A = np.stack(te)
    B = np.stack(tg)
    R,t = align(A,B)
    P = [R@x+t for x in te]
    errs=[]
    for i in range(len(tg)-d):
        dtg = np.linalg.norm((np.linalg.inv(Rg[i])@Rg[i+d])[:3,3])
        dte = abs(np.linalg.norm(P[i+d]-P[i]) - dtg)
        errs.append(dte)
    e=np.array(errs)
    return np.sqrt((e**2).mean())

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--base_path',required=True)
    p.add_argument('--date',required=True)
    p.add_argument('--drive',required=True)
    p.add_argument('--est_file',required=True)
    p.add_argument('--delta',type=int,default=1)
    a=p.parse_args()
    Rg,tg=load_gt(a.base_path,a.date,a.drive)
    Re,te=load_est(a.est_file)
    n=min(len(tg),len(te))
    print("ATE RMSE:",ate(Rg[:n],tg[:n],Re[:n],te[:n]))
    print("RPE RMSE:",rpe(Rg[:n],tg[:n],Re[:n],te[:n],a.delta))

if __name__=='__main__':
    main()
