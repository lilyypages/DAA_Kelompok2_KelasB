import networkx as nx
import json
import random
import os

# Folder data untuk menyimpan file JSON
os.makedirs("data", exist_ok=True)

def generate_bem_graph(n_total, seed):
    """
    Membuat graf sosial (BEM) dengan 3 divisi terpisah (komponen).
    Setiap divisi menggunakan model Barabasi-Albert (Scale-Free Network).
    """
    random.seed(seed)
    
    # 1. Bagi populasi menjadi 3 divisi (Komponen A, B, C)
    # Supaya tidak rata, acak sedikit ukurannya
    n_a = int(n_total * 0.4)
    n_b = int(n_total * 0.35)
    n_c = n_total - n_a - n_b
    
    # 2. Generate masing-masing divisi (Barabasi-Albert)
    # m=1 artinya setiap anggota baru kenal 1 orang lama (membentuk hub/ketua)
    G_A = nx.barabasi_albert_graph(n=n_a, m=1, seed=seed)
    G_B = nx.barabasi_albert_graph(n=n_b, m=1, seed=seed+1)
    G_C = nx.barabasi_albert_graph(n=n_c, m=1, seed=seed+2)
    
    # 3. Gabungkan jadi satu graf besar (tanpa menyambungkan antar divisi)
    # Kita harus relabel node supaya ID-nya tidak tabrakan (0..n)
    G_total = nx.disjoint_union_all([G_A, G_B, G_C])
    
    # 4. Konversi ke format Adjacency List (Dictionary) untuk disimpan
    adj_list = nx.to_dict_of_lists(G_total)
    
    return adj_list

def main():
    # KITA BUAT 4 UKURAN DATA (Kecil -> Besar)
    sizes = [100, 500, 1000, 2000]
    my_seed = 121437
    
    for i, n in enumerate(sizes):
        # Generate graf
        instance_data = generate_bem_graph(n, my_seed + i)
        
        # Siapkan isi file JSON
        output_content = {
            "project": "connected_components_social_graph",
            "description": f"Graf BEM {n} nodes, 3 disconnected components (Barabasi-Albert)",
            "n_nodes": n,
            "graph_adj": instance_data 
        }
        
        # Simpan ke file
        filename = f"data/social_graph_N{n}.json"
        with open(filename, "w") as f:
            json.dump(output_content, f, indent=2)
            
        print(f"[OK] Berhasil membuat: {filename}")

if __name__ == "__main__":
    main()