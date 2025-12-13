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
    hasil[start] = []
    qiu = [start]
    while qiu :                                 
        cabang = qiu.pop(0)                     
        for i in adj_list[cabang] :         
            if i not in hasil :           
                hasil[i] = [cabang]        
                qiu.append(i)               
    return hasil                          

def run_once(algorithm, adj_list,start,hasil,akar):
    t0=time.perf_counter(); out=algorithm(adj_list,start,hasil,akar); dt=(time.perf_counter()-t0)*1000.0
    return dt, out

def v_graph(tree,n,seed,algo,node_data):
    tree_reverse = nx.DiGraph()

    for child, parents in tree.items():
        for parent in parents:
            tree_reverse.add_edge(node_data[parent]["nama"], node_data[child]["nama"])

    plt.figure(figsize=(20, 20))
    pos = nx.nx_pydot.graphviz_layout(tree_reverse, prog="dot")
    nx.draw(tree_reverse, pos, with_labels=False, node_size=800, arrows=True,edge_color="red")
    for node, (x, y) in pos.items():
        plt.text(
            x,
            y,
            node,
            fontsize=14,
            fontweight='bold',
            rotation=-45,
            ha='center',
            va='center',
            color='black'
        )
    plt.title(f"Footprint {algo} N({n}) Seed({seed})",fontsize=30, fontweight='bold')
    plt.show()

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

    while True :
        while True :
            os.system("cls")
            print("Mau Ngapain Bang?")
            print("A. Atur Jumlah Pengulangan Simulasi")
            print("B. Atur Mahasiswa Asal")
            print("C. Atur Jumlah Seed")
            print("D. Eksekusi Eksperimen")
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
                        file = open("data/Biodata_N100.csv","r")
                        for i in range(101) :
                            a,b,c,d,e = file.readline().split(";")
                            if i == 0 :
                                continue
                            nama.append(b)
                        file.close()
                    except FileNotFoundError :
                        print('Setidaknya Sudah Run Program 1x Untuk Membuka Fitur Ini')
                        input("Tekan Enter Untuk Lanjut...")
                        continue
                    for i in range(10) :
                        for j in range(10) :
                            print("%-15s"%(f"{i+1+j*10}.{nama[i+j*10]}"),end="")
                        else :
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
                    print("========== Atur Jumlah Seed ===========")
                    print(f"Jumlah Seed Saat Ini : {n_seed}")
                    print("--------------------------------------------------")
                    try :
                        temp = int(input("Masukan Jumlah Seed Yang Baru : "))
                        if temp > 5 or temp > repeats or temp < 1 :
                            print("Jumlah Seed Tidak Boleh Lebih Dari 5 Atau Lebih besar dari Pengulangan Atau Lebih Kecil dari 1")
                            input("Tekan Enter Untuk Lanjut...")
                            continue
                        n_seed = temp
                    except ValueError :
                        print('Input Tidak Boleh Selain Angka')
                        input("Tekan Enter Untuk Lanjut...")
                        continue
                case "d" :
                    break
                case "e" :
                    exit(0)
                case _ :
                    print("Input Tidak Valid!!!")
                    input("Tekan Enter Untuk Lanjut...")

        for n in Ns:
            for r in range(repeats):
                filename = f"data/social_graph_N{n}_seed({base_seed + r%n_seed}).json"
                with open(filename, "r") as f:
                    data = json.load(f)
                adj_list = {int(k): v for k, v in data["graph_adj"].items()}
                node_data = {int(k): v for k, v in data["node_data"].items()}
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
                filename = f"data/social_graph_N{n}_seed{base_seed + r%n_seed}.json"

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

        os.makedirs("results", exist_ok=True)
        file = open("results/experiment_raw.csv","a+")
        file.close()
        df.to_csv('results/experiment_raw.csv', index=False)
        summary=df.groupby(['algo','n']).agg(time_ms_mean=('time_ms','mean'),time_ms_median=('time_ms','median'), time_ms_sd=('time_ms','std')).reset_index() #, gap_mean=('gap','mean')).reset_index()
        summary.to_csv('results/summary.csv', index=False)
        newrun = False
        latex_table=summary.rename(columns={'time_ms_mean':'Mean (ms)','time_ms_sd':'SD (ms)','time_ms_median':'Median (ms)'}).to_latex(index=False)#,'gap_mean':'Gap'}).to_latex(index=False)

        with open('results/summary.tex','w',encoding='utf-8') as f:
            f.write(latex_table)

        print('Saved results/summary.tex')

        while True :
            os.system("cls")
            print("Mau Ngapain Bang?")
            print("A. Lihat Hasil Simulasi")
            print("B. Lihat Hasil Summary")
            print("C. Lihat Graph dan Footprint Transversal")
            print("D. Lihat Plot Tabel dan Uji Statistik")
            print("E. Keluar Program")
            print("F. Ulang Eksperimen")
            jawab = input(">> ").lower()
            os.system("cls")
            match(jawab) :
                case "a" :
                    print("========== Hasil Simulasi ==========")
                    print(df)
                    input("Tekan Enter Untuk Lanjut...")
                case "b" :
                    print("========== Hasil Summary ===========")
                    print(summary)
                    input("Tekan Enter Untuk Lanjut...")
                case "c" :
                    print("========== Graph dan Footprint Transversal ===========")
                    while True :
                        os.system("cls")
                        print("Mau Lihat Apa Bang?")
                        print("A. Graph Sosial")
                        print("B. Footprint DFS")
                        print("C. Footprint BFS")
                        print("D. Kembali")
                        jawab2 = input(">> ").lower()
                        os.system("cls")
                        match(jawab2) :
                            case "a" :
                                try :
                                    print("Pilih Jumlah Mahasiswa :")
                                    for i in range(len(Ns)) :
                                        print(f"{i+1}. {Ns[i]}")
                                    temp = int(input(">> "))
                                    if temp > len(Ns) or temp < 1 :
                                        print("Input Tidak Valid!!!")
                                        input("Tekan Enter Untuk Lanjut...")
                                        continue
                                    jumlah = Ns[temp-1]
                                    os.system("cls")
                                except ValueError :
                                    print('Input Tidak Boleh Selain Angka')
                                    input("Tekan Enter Untuk Lanjut...")
                                    continue
                                try :
                                    print("Pilih Seed :")
                                    for i in range(n_seed) :
                                        print(f"{i+1}. {121437+i}")
                                    temp = int(input(">> "))
                                    if temp > n_seed or temp < 1 :
                                        print("Input Tidak Valid!!!")
                                        input("Tekan Enter Untuk Lanjut...")
                                        continue
                                    seeds = 121437+temp-1
                                    os.system("cls")
                                except ValueError :
                                    print('Input Tidak Boleh Selain Angka')
                                    input("Tekan Enter Untuk Lanjut...")
                                    continue
                                key_graph = f"Graph N{jumlah} seed({seeds})"
                                graph_nama = {}
                                for i in graph[key_graph] :
                                    graph_nama[node_data[i]["nama"]] = []
                                    for j in graph[key_graph][i] :
                                        graph_nama[node_data[i]["nama"]].append(node_data[j]["nama"])
                                G = nx.Graph(graph_nama)
                                # pos = nx.nx_pydot.graphviz_layout(G, prog="dot")
                                pos = nx.spring_layout(G, k=2.5, iterations=200)
                                plt.figure(figsize=(15, 15))
                                nx.draw(G, pos, with_labels=True, node_size=300, font_size=7.5, font_color = "black", font_weight='bold',edge_color="red")
                                plt.title(f"Graph N({jumlah}) Seed({seeds})",fontsize=15, fontweight='bold')
                                plt.show()

                            case "b" :
                                try :
                                    print("Pilih Jumlah Mahasiswa :")
                                    for i in range(len(Ns)) :
                                        print(f"{i+1}. {Ns[i]}")
                                    temp = int(input(">> "))
                                    if temp > len(Ns) or temp < 1 :
                                        print("Input Tidak Valid!!!")
                                        input("Tekan Enter Untuk Lanjut...")
                                        continue
                                    jumlah = Ns[temp-1]
                                    os.system("cls")
                                except ValueError :
                                    print('Input Tidak Boleh Selain Angka')
                                    input("Tekan Enter Untuk Lanjut...")
                                    continue
                                try :
                                    print("Pilih Seed :")
                                    for i in range(n_seed) :
                                        print(f"{i+1}. {121437+i}")
                                    temp = int(input(">> "))
                                    if temp > n_seed or temp < 1 :
                                        print("Input Tidak Valid!!!")
                                        input("Tekan Enter Untuk Lanjut...")
                                        continue
                                    seeds = 121437+temp-1
                                    os.system("cls")
                                except ValueError :
                                    print('Input Tidak Boleh Selain Angka')
                                    input("Tekan Enter Untuk Lanjut...")
                                    continue
                                tree_reverse = nx.DiGraph()

                                for child, parents in tree_dfs[f"DFS N{jumlah} seed({seeds})"].items():
                                    for parent in parents:
                                        tree_reverse.add_edge(node_data[parent]["nama"], node_data[child]["nama"])

                                plt.figure(figsize=(15, 15))
                                pos = nx.nx_pydot.graphviz_layout(tree_reverse, prog="dot")
                                nx.draw(tree_reverse, pos, with_labels=False, node_size=400, arrows=True,edge_color="red")
                                for node, (x, y) in pos.items():
                                    plt.text(
                                        x,
                                        y,
                                        node,
                                        fontsize=7,
                                        fontweight='bold',
                                        rotation=-45,
                                        ha='center',
                                        va='center',
                                        color='black'
                                    )
                                plt.title(f"Footprint DFS N({jumlah}) Seed({seeds})",fontsize=15, fontweight='bold')
                                plt.show()

                            case "c" :
                                try :
                                    print("Pilih Jumlah Mahasiswa :")
                                    for i in range(len(Ns)) :
                                        print(f"{i+1}. {Ns[i]}")
                                    temp = int(input(">> "))
                                    if temp > len(Ns) or temp < 1 :
                                        print("Input Tidak Valid!!!")
                                        input("Tekan Enter Untuk Lanjut...")
                                        continue
                                    jumlah = Ns[temp-1]
                                    os.system("cls")
                                except ValueError :
                                    print('Input Tidak Boleh Selain Angka')
                                    input("Tekan Enter Untuk Lanjut...")
                                    continue
                                try :
                                    print("Pilih Seed :")
                                    for i in range(n_seed) :
                                        print(f"{i+1}. {121437+i}")
                                    temp = int(input(">> "))
                                    if temp > n_seed or temp < 1 :
                                        print("Input Tidak Valid!!!")
                                        input("Tekan Enter Untuk Lanjut...")
                                        continue
                                    seeds = 121437+temp-1
                                    os.system("cls")
                                except ValueError :
                                    print('Input Tidak Boleh Selain Angka')
                                    input("Tekan Enter Untuk Lanjut...")
                                    continue
                                tree_reverse = nx.DiGraph()

                                for child, parents in tree_bfs[f"BFS N{jumlah} seed({seeds})"].items():
                                    for parent in parents:
                                        tree_reverse.add_edge(node_data[parent]["nama"], node_data[child]["nama"])

                                plt.figure(figsize=(15, 15))
                                pos = nx.nx_pydot.graphviz_layout(tree_reverse, prog="dot")
                                nx.draw(tree_reverse, pos, with_labels=False, node_size=400, arrows=True,edge_color="red")
                                for node, (x, y) in pos.items():
                                    plt.text(
                                        x,
                                        y,
                                        node,
                                        fontsize=7,
                                        fontweight='bold',
                                        rotation=-45,
                                        ha='center',
                                        va='center',
                                        color='black'
                                    )
                                plt.title(f"Footprint BFS N({jumlah}) Seed({seeds})",fontsize=15, fontweight='bold')
                                plt.show()
                            
                            case "d" :
                                break

                            case _ :
                                print("Input Tidak Valid!!!")
                                input("Tekan Enter Untuk Lanjut...")
                case "d" :
                    print("========== Plot Tabel dan Uji Statistik ===========")
                    while True :
                        os.system("cls")
                        print("Mau Lihat Apa Bang?")
                        print("A. Plot N vs Mean Time by Algorithm")
                        print("B. Plot N vs Median Time by Algorithm")
                        print("C. Boxplot")
                        print("D. Uji T-Test")
                        print("E. Kembali")
                        jawab2 = input(">> ").lower()
                        os.system("cls")
                        match(jawab2) :
                            case "a" :
                                plt.figure()
                                for algo in sorted(df['algo'].unique()):
                                    xs=sorted(df['n'].unique())
                                    ys=[summary[(summary['algo']==algo)&(summary['n']==x)]['time_ms_mean'].values[0] for x in xs]
                                    plt.plot(xs, ys, marker='o', label=f'Algo {algo}')
                                plt.xlabel('n')
                                plt.ylabel('Mean time (ms)')
                                plt.title('n vs mean time by algorithm')
                                plt.legend()
                                plt.grid(True)
                                plt.tight_layout()
                                plt.savefig('results/plot_n_vs_mean_time.png', dpi=150)
                                plt.show()
                            
                            case "b" :
                                plt.figure()
                                for algo in sorted(df['algo'].unique()):
                                    xs=sorted(df['n'].unique())
                                    ys=[summary[(summary['algo']==algo)&(summary['n']==x)]['time_ms_median'].values[0] for x in xs]
                                    plt.plot(xs, ys, marker='o', label=f'Algo {algo}')

                                plt.xlabel('n')
                                plt.ylabel('Median time (ms)')
                                plt.title('n vs median time by algorithm')
                                plt.legend()
                                plt.grid(True)
                                plt.tight_layout()
                                plt.savefig('results/plot_n_vs_median_time.png', dpi=150)
                                plt.show()

                            case "c" :
                                plt.figure()
                                data=[df[df['n']==x]['time_ms'] for x in sorted(df['n'].unique())]
                                plt.boxplot(data, labels=sorted(df['n'].unique()))
                                plt.xlabel('n')
                                plt.ylabel('time (ms)')
                                plt.title('Distribusi waktu per n')
                                plt.grid(True)
                                plt.tight_layout()
                                plt.savefig('results/plot_box_time_per_n.png', dpi=150)
                                plt.show()

                            case "d" :
                                try:
                                    from scipy.stats import ttest_rel
                                    print("Hasil T-Test :")
                                    for n in sorted(df['n'].unique()):
                                        a=df[(df['n']==n)&(df['algo']=='DFS')]['time_ms'].values
                                        b=df[(df['n']==n)&(df['algo']=='BFS')]['time_ms'].values
                                        t,p=ttest_rel(a,b)
                                        print(f'n={n}: t={t:.3f}, p={p*100:.2f}%')
                                    input("Tekan Enter Untuk Lanjut...")

                                except Exception as e:
                                    print('SciPy tidak tersedia; lewati uji t berpasangan.', e)

                            case "e" :
                                break

                            case _ :
                                print("Input Tidak Valid!!!")
                                input("Tekan Enter Untuk Lanjut...")

                case "e" :
                    exit(0)
                case "f" :
                    break
                case _ :
                    print("Input Tidak Valid!!!")
                    input("Tekan Enter Untuk Lanjut...")

if __name__ == "__main__":
    if not(os.path.exists("data/Biodata_N100.csv")):
        print("Silahkan Run generate_instance.py terlebih dahulu")
        exit(0)
    main()