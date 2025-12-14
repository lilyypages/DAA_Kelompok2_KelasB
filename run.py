import os, time, random, statistics, glob
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import json
import gc
# import generate_instances as gi
#from IPython.display import display, clear_output

gc.disable

# Buat folder jika belum ada
os.makedirs("results", exist_ok=True)

def dfs_trans(adj_list, start, hasil, akar):
    for i in adj_list[start]:                 
        if i not in hasil and i != akar:     
            hasil[i] = [start]                 
            dfs_trans(adj_list, i, hasil, akar)
    return hasil                               

def bfs_trans(adj_list, start, hasil, useless):
    hasil[start] = []
    qiu = [start]
    while qiu :                                 
        cabang = qiu.pop(0)                     
        for i in adj_list[cabang]:         
            if i not in hasil:           
                hasil[i] = [cabang]        
                qiu.append(i)               
    return hasil                          

def run_once(algorithm, adj_list, start, hasil,akar):
    gc.collect()
    t0=time.perf_counter()
    out=algorithm(adj_list,start,hasil,akar)
    dt=(time.perf_counter() - t0) * 1000.0
    return dt, out

def v_graph(tree,n,seed,algo,node_data):
    tree_reverse = nx.DiGraph()

    for child, parents in tree.items():
        for parent in parents:
            p_name = node_data[parent]["nama"]
            c_name = node_data[child]["nama"]
            tree_reverse.add_edge(p_name, c_name)
            # tree_reverse.add_edge(node_data[parent]["nama"], node_data[child]["nama"])

    plt.figure(figsize=(15, 15))
    
    try:
        pos = nx.nx_pydot.graphviz_layout(tree_reverse, prog="dot")
    except:
        print("[Info] Graphviz error/tidak ada. Beralih ke Spring Layout.")
        pos = nx.spring_layout(tree_reverse, k=0.5, iterations=50)
    
    nx.draw(tree_reverse, pos, with_labels=False, node_size=800, arrows=True, edge_color="red", node_color="lightblue")
    
    for node, (x, y) in pos.items():
        plt.text(
            x, y, node,
            fontsize=10,
            fontweight='bold',
            rotation=-45,
            ha='center', va='center',
            color='black'
        )
        
    plt.title(f"Footprint {algo} N({n}) Seed({seed})", fontsize=20, fontweight='bold')
    plt.show()

def main() :
    # Tak Boleh Diganti
    Ns=[100,400,700,1000]
    rows=[]
    base_seed= 121437 
    
    # Cache untuk Visualisasi
    graph = {}      # Simpan adj_list
    node_data = {}  # Simpan nama-nama
    tree_dfs = {}         # Simpan hasil DFS
    tree_bfs = {}         # Simpan hasil BFS

    # Default Config
    repeats = 5
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
                    print("NB : Semakin Banyak Pengulangan, Maka Simulasi akan semakin lambat")
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
                filename = f"data/social_graph_N{n}_seed{base_seed + r%n_seed}.json"
                with open(filename, "r") as f:
                    data = json.load(f)
                adj_list = {int(k): v for k, v in data["graph_adj"].items()}
                node_data = {int(k): v for k, v in data["node_data"].items()}
                filename = f"data/social_graph_N{n}_seed{base_seed + r%n_seed}.json"

                
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
                        print("D. Histogram waktu eksekusi per algoritma")
                        print("E. Uji T-Test")
                        print("F. Kembali")
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
                                plt.figure()
                                for algo in sorted(df['algo'].unique()):
                                    data = df[df['algo'] == algo]['time_ms']
                                    plt.hist(data, bins=20, alpha=0.5, label=f'Algo {algo}')

                                plt.xlabel('time (ms)')
                                plt.ylabel('frequency')
                                plt.title('Histogram waktu eksekusi per algoritma')
                                plt.legend()
                                plt.grid(True)
                                plt.tight_layout()
                                plt.savefig('results/plot_hist_time_per_algo.png', dpi=150)
                                plt.show()

                            case "e" :
                                try:
                                    from scipy.stats import ttest_rel
                                    print("Hasil T-Test :")
                                    for n in sorted(df['n'].unique()):
                                        a=df[(df['n']==n)&(df['algo']=='DFS')]['time_ms'].values
                                        b=df[(df['n']==n)&(df['algo']=='BFS')]['time_ms'].values
                                        t,p=ttest_rel(a,b)
                                        print(f'n={n}: t={t:.3f}, p={p:.2f}')
                                    input("Tekan Enter Untuk Lanjut...")

                                except Exception as e:
                                    print('SciPy tidak tersedia; lewati uji t berpasangan.', e)

                            case "f" :
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
    if not os.path.exists("data/social_graph_N100_seed(121437).json") or not os.path.exists("data/social_graph_N100o_seed(121441).json"):
        print("File yang dibutuhkan Tidak ada. Run generate_instances.py dulu!")
    else:
        main()
        
        
                # os.system('cls' if os.name == 'nt' else 'clear')
            # print("============================================")
            # print("       EXPERIMENT RUNNER (DFS vs BFS)       ")
            # print("============================================")
            # print(f"Config: Repeats={repeats} | Seeds={n_seed} | StartNode={start_node_id}")
            # print("--------------------------------------------")
            # print("A. Atur Jumlah Pengulangan Simulasi")
            # print("B. Atur Mahasiswa Asal (Start Node)")
            # print("C. Atur Jumlah Seed")
            # print("D. Eksekusi Eksperimen")
            # print("E. Keluar Program")
            # print("============================================")
            
            # jawab = input(">> ").lower()
            
            # if jawab == "a":
            #     os.system('cls' if os.name == 'nt' else 'clear') 
            #     print("========== ATUR PENGULANGAN ==========")
            #     print(f"Jumlah Repeats saat ini: {repeats}")
            #     print("--------------------------------------")
            #     try:
            #         baru = int(input("Masukkan jumlah baru: "))
            #         repeats = baru
            #         print("\n✅ Berhasil diubah!")
            #     except: 
            #         print("\n❌ Input harus angka!")
                    
            #     time.sleep(1.0)

            # elif jawab == "b":
            #     os.system('cls' if os.name == 'nt' else 'clear')
            #     print("========== PILIH MAHASISWA ==========")
                
            #     csv_files = glob.glob("data/Biodata_*.csv")
            #     if not csv_files:
            #         print("\n❌ File Biodata tidak ada! \nRun generate_instances.py dulu!")
            #     else:
            #         df_nama = pd.read_csv(csv_files[0], sep=";")
            #         print(df_nama[['id', 'nama']].head(50).to_string(index=False))
            #         print("-------------------------------------")
            #         try:
            #             mhs = int(input("Masukan ID Mahasiswa (Start Node): "))
            #             if mhs < 0: print("\n❌ Tidak boleh negatif!")
            #             else: start_node_id = mhs
            #         except: pass
                
            #     input("\nTekan Enter untuk kembali...")

            # elif jawab == "c":
            #     os.system('cls' if os.name == 'nt' else 'clear')
            #     print("========== ATUR JUMLAH SEED ==========")
            #     print(f"Jumlah Seed saat ini: {n_seed}")
            #     print("--------------------------------------")
            #     try:
            #         temp = int(input(f"Masukkan Jumlah Seed (Max 5): "))
            #         if 1 <= temp <= 5: 
            #             n_seed = temp
            #             print("\n✅ Sip, seed diatur.")
            #         else:
            #             print("\n❌ Harus antara 1-5.")
            #     except ValueError:
            #         print("\n❌ Error: Input harus berupa angka bulat!")
                
            #     time.sleep(1.5)

            # elif jawab == "d":
            #     print("\nMEMULAI EKSPERIMEN...")
            #     rows = [] 
                
            #     for n in Ns:
            #         # Safety check start node
            #         curr_start = start_node_id if start_node_id < n else 0
            #         if curr_start != start_node_id:
            #             print(f"[Info] N={n}, Start Node {start_node_id} kegedean. Reset ke 0.")
                        
            #         for r in range(repeats):
            #             # Logic Seed Unik + Variasi
            #             current_seed = base_seed + (r % n_seed)
            #             filename = f"data/social_graph_N{n}_seed{current_seed}.json"
                        
            #             if not os.path.exists(filename):
            #                 print(f"Skip {filename} (File tidak ditemukan)")
            #                 continue
                            
            #             # LOAD JSON
            #             with open(filename, "r") as f:
            #                 data = json.load(f)
                        
            #             # Convert keys string -> int
            #             adj_list = {int(k): v for k, v in data["graph_adj"].items()}
            #             node_data = {int(k): v for k, v in data["node_data"].items()}
                        
            #             # Simpan ke cache buat visualisasi nanti (Key Unik: N + Seed)
            #             key = f"N{n}_S{current_seed}"
            #             graph_cache[key] = adj_list
            #             node_data_cache[key] = node_data

            #             # RUN ALGO
            #             dA, hasilA = run_once(dfs_trans, adj_list, curr_start, {}, curr_start)
            #             dB, hasilB = run_once(bfs_trans, adj_list, curr_start, {}, curr_start)
                        
            #             rows.append({'n': n, 'repeat': r, 'algo': 'DFS', 'time_ms': dA})
            #             rows.append({'n': n, 'repeat': r, 'algo': 'BFS', 'time_ms': dB})
                        
            #             # Simpan Tree buat visualisasi (simpan 1 sampel per seed unik)
            #             if r < n_seed:
            #                 tree_dfs[key] = hasilA
            #                 tree_bfs[key] = hasilB
                            
            #             print(f"-> N={n} Seed={current_seed} | Rep={r+1} | DFS={dA:.2f}ms BFS={dB:.2f}ms")

            #     # Simpan hasil ke CSV
            #     df = pd.DataFrame(rows)
            #     df.to_csv('results/experiment_raw.csv', index=False)
                
            #     # Simpan Summary
            #     summary = df.groupby(['algo', 'n']).agg(
            #         mean=('time_ms', 'mean'), 
            #         median=('time_ms', 'median'), 
            #         sd=('time_ms', 'std')
            #     ).reset_index()
            #     summary.to_csv('results/summary.csv', index=False)
                
            #     # Simpan ke Latex
            #     with open('results/summary.tex', 'w') as f: f.write(summary.to_latex(index=False))

            #     print("\n✅ Eksperimen Selesai! Data tersimpan di folder 'results/'.")
            #     print("Masuk ke Menu Hasil...")
            #     time.sleep(5)
                
            #     # SUB-MENU HASIL
            #     while True:
            #         os.system('cls' if os.name == 'nt' else 'clear')
                    
            #         print("========== MENU HASIL ==========")
            #         print("A. Lihat Tabel Raw Data")
            #         print("B. Lihat Summary")
            #         print("C. Visualisasi (Graph/Tree)")
            #         print("D. Plot Grafik Perbandingan")
            #         print("E. Kembali ke Menu Utama")
            #         print("================================")
                    
            #         sub = input(">> ").lower()
                    
            #         if sub == "a": 
            #             os.system('cls' if os.name == 'nt' else 'clear')
            #             print("==============================")
            #             print("---------- RAW DATA ----------")
            #             print("==============================")
            #             print(df)
            #             input("\nTekan 'Enter' untuk kembali...")
                        
            #         elif sub == "b": 
            #             os.system('cls' if os.name == 'nt' else 'clear')
            #             print("=======================================")
            #             print("------------- SUMMARY DATA ------------")
            #             print("=======================================")
            #             print(summary)
            #             input("\nTekan 'Enter' untuk kembali...")
                    
            #         elif sub == "c":
            #             os.system('cls' if os.name == 'nt' else 'clear')
            #             print("============ VISUALISASI ============")
            #             print("A. Graph Sosial (Struktur Awal)")
            #             print("B. Footprint DFS (Jalur Penelusuran)")
            #             print("C. Footprint BFS (Jalur Penelusuran)")
            #             print("D. Kembali ke Menu Utama")
            #             print("=====================================")
                        
            #             vis_choice = input(">> ").lower()
                        
            #             if vis_choice == "d":
            #                 break 
                        
            #             # Cek pilihan valid A/B/C
            #             if vis_choice not in ["a", "b", "c"]:
            #                 print("❌ Pilihan tidak valid.")
            #                 time.sleep(1.0)
            #                 continue
                            
            #             print("\n--- Pilihan Data ---")
            #             print("Kunci Tersedia:", list(tree_dfs.keys()))
            #             k = input("Masukkan Key (contoh N100_S121437): ")
                        
            #             if k not in tree_dfs:
            #                 print("❌ Key salah atau data tidak ada.")
            #                 input("Tekan 'Enter' untuk kembali...")
            #                 continue
                        
            #             # Siapkan Data
            #             # Parsing Key untuk ambil N dan Seed
            #             parts = k.split("_") # ['N100', 'S121437']
            #             n_val = parts[0]
            #             s_val = parts[1]
                        
            #             # PILIHAN A: GRAPH SOSIAL
            #             if vis_choice == "a":
            #                 adj_list = graph_cache[k]
            #                 ndata = node_data_cache[k]
                            
            #                 print(f"Sedang menggambar Graph Sosial {k}...")
                            
            #                 # Buat Graph dari Adjacency List
            #                 G = nx.from_dict_of_lists(adj_list)
                            
            #                 # Ubah ID Angka jadi Nama Orang
            #                 mapping = {node_id: info['nama'] for node_id, info in ndata.items()}
            #                 G = nx.relabel_nodes(G, mapping)
                            
            #                 plt.figure(figsize=(15, 15))
            #                 # Layout Spring
            #                 pos = nx.spring_layout(G, k=0.3, iterations=50, seed=42) 
                            
            #                 nx.draw(G, pos, 
            #                         with_labels=True, 
            #                         node_size=300, 
            #                         node_color='lightgreen', 
            #                         edge_color='gray',
            #                         font_size=8,
            #                         font_weight='bold')
                                
            #                 plt.title(f"Social Graph Structure - {n_val} {s_val}", fontsize=20)
            #                 plt.show()
                        
            #             # PILIHAN B/C: FOOTPRINT TREE
            #             elif vis_choice in ["b", "c"]:
            #                 algo_name = "DFS" if vis_choice == "b" else "BFS"
            #                 tree_data = tree_dfs[k] if vis_choice == "b" else tree_bfs[k]
                            
            #                 # Panggil Fungsi v_graph
            #                 v_graph(tree_data, n_val, s_val, algo_name, node_data_cache[k])

            #         elif sub == "d":
            #             os.system('cls' if os.name == 'nt' else 'clear')
            #             print("Generating Plot...")
            #             plt.figure(figsize=(10, 6))
            #             for algo in ['DFS', 'BFS']:
            #                 subset = summary[summary['algo'] == algo]
            #                 plt.plot(subset['n'], subset['mean'], marker='o', label=algo, linewidth=2)
                        
            #             plt.legend()
            #             plt.grid(True, linestyle='--', alpha=0.7)
            #             plt.title("Perbandingan Waktu Eksekusi (DFS vs BFS)")
            #             plt.xlabel("Jumlah Node (N)")
            #             plt.ylabel("Rata-rata Waktu (ms)")
            #             plt.show()
                        
            #         elif sub == "e": 
            #             os.system('cls' if os.name == 'nt' else 'clear')
            #             break
                    
            #         else: 
            #             print("❌ Input tidak valid!")
            #             time.sleep(1.5)

            # elif jawab == "e":
            #     os.system('cls' if os.name == 'nt' else 'clear')
            #     print("\n" + "="*44)
            #     print("   TERIMA KASIH SUDAH MENGGUNAKAN APP INI")
            #     print("   Project by: Kelompok 2 DAA Kelas B")
            #     print("   Babaii! 👋")
            #     print("="*44 + "\n")
            #     time.sleep(1.5) 
            #     break
            
            # else:
            #     print("❌ Input tidak valid! Harap pilih A, B, C, D, atau E.")
            #     time.sleep(1.5)