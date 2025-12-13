import os, time, random, statistics
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

import generate_instances as gi
import networkx as nx
import json
#from IPython.display import display, clear_output
import gc

gc.disable
# Buat folder data jika belum ada
os.makedirs("data", exist_ok=True)

def dfs_trans(adj_list,start,hasil,akar) :
    for i in adj_list[start] :                 
        if i not in hasil and i != akar :     
            hasil[i] = [start]                 
            dfs_trans(adj_list,i,hasil,akar)
    return hasil                               

def bfs_trans(adj_list,start,hasil,useless) :
    hasil[start] = []                           # 1
    qiu = [start]                               # 1
    while qiu :                                 # n
        cabang = qiu.pop(0)                     # n   t n(n)
        for i in adj_list[cabang] :             # n_e   t e
            if i not in hasil :                 # 1
                hasil[i] = [cabang]             # 1     t n-1
                qiu.append(i)                   # 1     t n-1
    return hasil                                # 1

def run_once(algorithm, adj_list,start,hasil,akar):
    t0=time.perf_counter(); out=algorithm(adj_list,start,hasil,akar); dt=(time.perf_counter()-t0)*1000.0
    return dt, out

def main() :
    # Tak Boleh Diganti
    Ns=[100,400,700,1000]
    rows=[]
    base_seed= 121437 
    graph = {}
    tree_dfs = {}
    tree_bfs = {}

    # Boleh Diganti
    repeats=5
    start = 5
    n_seed = 1
    newrun = True

    while True :
        os.system("cls")
        print("Mau Ngapain Bang?")
        print("A. Atur Jumlah Pengulangan Simulasi")
        print("B. Atur Mahasiswa Asal")
        print("C. Atur Jumlah Seed")
        print("D. Eksekusi  Eksperimen")
        print("E. Keluar Program")
        jawab = input(">> ").lower()
        os.system("cls")
        match(jawab) :
            case "a" :
                print("========== Atur Jumlah Pengulangan Simulasi ===========")
                print(f"Jumlah Pengulangan Simulasi Saat Ini : {repeats}")
                print("--------------------------------------------------")
                try :
                    temp = int(input("Masukan Jumlah Pengulangan Simulasi Yang Baru : "))
                    repeats = temp
                except ValueError :
                    print('Input Tidak Boleh Selain Angka')
                    input("Tekan Enter Untuk Lanjut...")
                    continue
            case "b" :
                print("========== Atur Mahasiswa Asal ===========")
                print("Daftar Nama Mahasiswa :")
                nama = []
                try : 
                    file = open("Biodata N100 seed(121437).csv","r")
                    for i in range(101) :
                        if i == 0 :
                            continue
                        a,b,c,d,e = file.readlines().split(";")
                        nama.append(b)
                except FileNotFoundError :
                    print('Setidaknya Sudah Run Program 1x Untuk Membuka Fitur Ini')
                    input("Tekan Enter Untuk Lanjut...")
                    continue
                for i in range(10) :
                    for j in range(10) :
                        print("%-13s"%(f"{i+1+j*10}.{nama[i+j*10]}"),end="")
                    else :
                        if i < 9 :
                            print("\n")
                print("--------------------------------------------------")
                try :
                    mhs = int(input("Masukan Nomor Mahasiswwa : "))
                    if mhs < 1 or mhs > 100 :
                        print('Input Tidak Valid')
                        input("Tekan Enter Untuk Lanjut...")
                        continue
                    start = mhs - 1
                except ValueError :
                    print('Input Tidak Boleh Selain Angka')
                    input("Tekan Enter Untuk Lanjut...")
                    continue
            case "c" :
                print("========== C. Atur Jumlah Seed ===========")
                print(f"Jumlah Seed Saat Ini : {n_seed}")
                print("--------------------------------------------------")
                try :
                    temp = int(input("Masukan Jumlah Seed Yang Baru : "))
                    if temp > 5 :
                        print("Jumlah Seed Tidak Boleh Lebih Dari 5")
                        input("Tekan Enter Untuk Lanjut...")
                        continue
                    repeats = temp
                    newrun = True
                except ValueError :
                    print('Input Tidak Boleh Selain Angka')
                    input("Tekan Enter Untuk Lanjut...")
                    continue
            case "d" :
                break
            case "e" :
                exit(0)

    for n in Ns:
        for r in range(repeats):
            if newrun :
                if r < n_seed :
                    adj_list, node_data = gi.generate_bem_graph(n, base_seed + r)
                    output_content = {
                        "project": "connected_components_social_graph",
                        "description": f"Graf BEM {n} nodes dengan Data Atribut",
                        "n_nodes": n,
                        "graph_adj": adj_list,
                        "node_data": node_data
                    }       
            filename = f"data/social_graph_N{n} seed({base_seed + r%n_seed}).json"

            if newrun and r < n_seed :
                with open(filename, "w") as f:
                    json.dump(output_content, f, indent=2)
                
            else :
                with open(filename, "r") as f:
                    data = json.load(f)
                adj_list = {int(k): v for k, v in data["graph_adj"].items()}
                node_data = {int(k): v for k, v in data["node_data"].items()}

            gc.collect
            dA, hasilA = run_once(dfs_trans, adj_list,start,{},start)
            gc.collect
            dB, hasilB = run_once(bfs_trans, adj_list,start,{},start)
            
            rows.append({'n':n,'repeat':r,'algo':'DFS','time_ms':dA})#,'gap':gA})
            rows.append({'n':n,'repeat':r,'algo':'BFS','time_ms':dB})#,'gap':gB})

            if r < n_seed :
                graph[f"Graph N{n} seed({base_seed + r})"] = adj_list
                tree_dfs[f"DFS N{n} seed({base_seed + r})"] = hasilA
                tree_bfs[f"BFS N{n} seed({base_seed + r})"] = hasilB

    df=pd.DataFrame(rows)
    os.system("cls")
    print("Hasil Simulasi :")
    print(df)

    os.makedirs("results", exist_ok=True)
    file = open("results/experiment_raw.csv","a+")
    file.close()
    df.to_csv('results/experiment_raw.csv', index=False)
    summary=df.groupby(['algo','n']).agg(time_ms_mean=('time_ms','mean'),time_ms_median=('time_ms','median'), time_ms_sd=('time_ms','std')).reset_index() #, gap_mean=('gap','mean')).reset_index()
    summary.to_csv('results/summary.csv', index=False)
    newrun = False

    print(summary)

if __name__ == "__main__":
    main()