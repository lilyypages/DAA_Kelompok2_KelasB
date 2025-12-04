import networkx as nx
import json
import random
import os

# Buat folder data jika belum ada
os.makedirs("data", exist_ok=True)

def generate_bem_graph(n_total, seed):
    """
    Membuat graf sosial BEM dengan 3 divisi dan DATA DUMMY di setiap node.
    """
    random.seed(seed)
    
    # 1. Bagi populasi (supaya tidak rata)
    n_a = int(n_total * 0.4)
    n_b = int(n_total * 0.35)
    n_c = n_total - n_a - n_b
    
    # 2. Generate Struktur Graf (Barabasi-Albert)
    # Node 0 di setiap sub-graf biasanya adalah 'Hub' (paling populer)
    G_A = nx.barabasi_albert_graph(n=n_a, m=1, seed=seed)
    G_B = nx.barabasi_albert_graph(n=n_b, m=1, seed=seed+1)
    G_C = nx.barabasi_albert_graph(n=n_c, m=1, seed=seed+2)
    
    # 3. Gabungkan jadi satu (Disjoint Union)
    # disjoint_union_all otomatis mengubah ID node jadi urut (0, 1, 2... n)
    # Urutannya: Semua node A dulu, lalu B, lalu C.
    G_total = nx.disjoint_union_all([G_A, G_B, G_C])
    
    # 4. GENERATE DATA DUMMY (Sesuai permintaan Dosen)
    # Kita buat dictionary untuk menyimpan data tiap node
    node_data = {}
    
    for node_id in G_total.nodes():
        # Tentukan Divisi berdasarkan rentang ID
        if node_id < n_a:
            divisi = "Divisi Acara"
            # Node 0 di Divisi A kita jadikan Ketua
            jabatan = "Ketua Divisi" if node_id == 0 else "Staff"
        elif node_id < (n_a + n_b):
            divisi = "Divisi Humas"
            # Node awal di Divisi B jadi Ketua
            jabatan = "Ketua Divisi" if node_id == n_a else "Staff"
        else:
            divisi = "Divisi Logistik"
            # Node awal di Divisi C jadi Ketua
            jabatan = "Ketua Divisi" if node_id == (n_a + n_b) else "Staff"
        
        # Simpan data
        node_data[str(node_id)] = {
            "nama": f"Mahasiswa_{node_id}",
            "divisi": divisi,
            "jabatan": jabatan,
            "ipk": round(random.uniform(2.5, 4.0), 2)  # Tambahan biar terlihat 'real'
        }

    # 5. Ambil Adjacency List (Struktur Teman)
    adj_list = nx.to_dict_of_lists(G_total)
    
    return adj_list, node_data

def main():
    n = 375 # Ukuran graf yang diinginkan
    my_seed = 121437  # Seed unik kamu
    
    
    adj_list, node_data = generate_bem_graph(n, my_seed)
        
    output_content = {
        "project": "connected_components_social_graph",
        "description": f"Graf BEM {n} nodes dengan Data Atribut",
        "n_nodes": n,
        "graph_adj": adj_list,   # <--- Ini untuk algoritma BFS/DFS (Jalan)
        "node_data": node_data   # <--- Ini untuk data mahasiswa
    }
        
    filename = f"data/social_graph_N{n}.json"
    with open(filename, "w") as f:
        json.dump(output_content, f, indent=2)
            
    print(f"[OK] Berhasil membuat: {filename} (Lengkap dengan data mahasiswa)")

if __name__ == "__main__":
    main()