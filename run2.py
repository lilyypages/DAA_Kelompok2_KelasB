import argparse, gc, json, os, time
import pandas as pd
import sys

# Matikan Garbage Collection otomatis agar pengukuran waktu stabil
gc.disable()

# Pastikan folder results ada
os.makedirs("results", exist_ok=True)

# ALGORITMA DFS
def dfs_trans(adj_list, start, hasil, akar):
    if start in adj_list:
        for i in adj_list[start]:                
            if i not in hasil and i != akar:     
                hasil[i] = [start]                 
                dfs_trans(adj_list, i, hasil, akar)
    return hasil                              

# ALGORITMA BFS
def bfs_trans(adj_list, start, hasil, useless):
    hasil[start] = []
    qiu = [start]
    while qiu:                                
        cabang = qiu.pop(0)
        if cabang in adj_list:
            for i in adj_list[cabang]:        
                if i not in hasil:           
                    hasil[i] = [cabang]        
                    qiu.append(i)               
    return hasil                              

def run_once(algorithm, adj_list, start, hasil, akar):
    gc.collect()
    t0 = time.perf_counter()
    out = algorithm(adj_list, start, hasil, akar)
    dt = (time.perf_counter() - t0) * 1000.0
    return dt, out

def main():
    parser = argparse.ArgumentParser(
        description="Jalankan Eksperimen DFS vs BFS via Terminal (CLI)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Menambahkan argumen-argumen yg bisa diatur user
    parser.add_argument(
        "--n", 
        nargs="+", 
        type=int, 
        default=[100, 400, 700, 1000],
        help="List jumlah Node yang ingin dites (pisahkan dengan spasi)"
    )
    
    parser.add_argument(
        "--repeats", 
        type=int, 
        default=5,
        help="Jumlah pengulangan per graf"
    )
    
    parser.add_argument(
        "--start_node", 
        type=int, 
        default=5,
        help="ID Node awal penelusuran"
    )
    
    parser.add_argument(
        "--base_seed", 
        type=int, 
        default=121437,
        help="Seed dasar untuk nama file"
    )
    
    parser.add_argument(
        "--output", 
        type=str, 
        default="results/cli_result.csv",
        help="Nama file output CSV"
    )
    
    parser.add_argument(
        "--algo", 
        type=str, 
        choices=['both', 'dfs', 'bfs'], 
        default='both',
        help="Pilih algoritma yang mau dijalankan: 'both', 'dfs', atau 'bfs'"
    )

    parser.add_argument(
        "--limit", 
        type=int, 
        default=5000,
        help="Atur batas recursion limit Python (Penting buat DFS di N besar)"
    )

    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Mode hening: Jangan print detail per baris, cuma hasil akhir."
    )

    # Parsing argumen dari terminal
    args = parser.parse_args()

    # Atur Recursion Limit (Biar DFS ga crash)
    sys.setrecursionlimit(args.limit)

    if not os.path.exists("data"):
        print("[ERROR] Folder 'data/' tidak ditemukan. Jalankan generate_instances.py dulu.")
        sys.exit(1)

    print(f"\nMEMULAI EKSPERIMEN...")
    print(f"Config: N={args.n} | Repeats={args.repeats} | Start={args.start_node} | RecLimit={args.limit}")
    print("-" * 75)
    
    # Header kalau tidak quiet
    if not args.quiet:
        print(f"{'N':<6} | {'Var':<5} | {'Seed':<10} | {'Rep':<5} | {'DFS (ms)':<10} | {'BFS (ms)':<10}")
        print("-" * 75)
    
    rows = []
    
    # Loop Eksperimen
    for n in args.n:
        # Safety check start node
        curr_start = args.start_node if args.start_node < n else 0
        if curr_start != args.start_node:
            print(f"[Info] N={n}: Start Node {args.start_node} kegedean. Reset ke 0.")
        
        for r in range(args.repeats):
            seed_offset = r % 5 
            seed_idx = seed_offset + 1  # Biar kebaca Variasi 1, 2, 3..
            current_seed = args.base_seed + seed_offset
                        
            filename = f"data/social_graph_N{n}_seed{current_seed}.json"
            
            if not os.path.exists(filename):
                if not args.quiet: print(f"Skip: {filename} (File tidak ditemukan)")
                continue
            
            # Load Data
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"[ERROR] membaca file {filename}: {e}")
                continue

            # Convert keys
            adj_list = {int(k): v for k, v in data["graph_adj"].items()}
            
            dA, dB = None, None # Placeholder
            
            # Jalankan DFS jika diminta
            if args.algo in ['both', 'dfs']:
                dA, _ = run_once(dfs_trans, adj_list, curr_start, {}, curr_start)
                rows.append({'n': n, 'repeat': r, 'seed': current_seed, 'algo': 'DFS', 'time_ms': dA})

            # Jalankan BFS jika diminta
            if args.algo in ['both', 'bfs']:
                dB, _ = run_once(bfs_trans, adj_list, curr_start, {}, curr_start)
                rows.append({'n': n, 'repeat': r, 'seed': current_seed, 'algo': 'BFS', 'time_ms': dB})
            
            if not args.quiet:
                dfs_str = f"{dA:6.2f}" if dA is not None else "   -  "
                bfs_str = f"{dB:6.2f}" if dB is not None else "   -  "
                
                print(f"{n:<6} | {seed_idx:<5} | {current_seed:<10} | {r+1:<5} | {dfs_str:<10} | {bfs_str:<10}")
            
            # Eksekusi Algoritma
            # dA, _ = run_once(dfs_trans, adj_list, curr_start, {}, curr_start)
            # dB, _ = run_once(bfs_trans, adj_list, curr_start, {}, curr_start)
            
            # Simpan Data
            # rows.append({'n': n, 'repeat': r, 'algo': 'DFS', 'time_ms': dA})
            # rows.append({'n': n, 'repeat': r, 'algo': 'BFS', 'time_ms': dB})
            
            # print(f"-> N={n:<4} | Seed={current_seed} | Rep={r+1} | DFS={dA:6.2f}ms | BFS={dB:6.2f}ms")

    # Simpan Hasil
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(args.output, index=False)
        print("-" * 75)
        print(f"Selesai! Data disimpan di: {args.output}")
        
        # Menampilkan Summary
        print("\n--- Ringkasan Rata-rata Waktu (ms) ---")
        summary = df.groupby(['algo', 'n'])['time_ms'].mean().reset_index()
        print(summary.to_string(index=False))
        print("\n(Gunakan 'Analysis.ipynb' untuk visualisasi grafik)")
    else:
        print("\nTidak ada data yang berhasil diproses.")

if __name__ == "__main__":
    main()