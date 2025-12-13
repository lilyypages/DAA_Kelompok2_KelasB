import networkx as nx
import random
import os
import json
import itertools

# Buat folder data jika belum ada
os.makedirs("data", exist_ok=True)

def generate_bem_graph(n_total, seed):
    random.seed(seed)
    
    n_a = int(n_total * 0.2)
    n_b = int(n_total * 0.15)
    n_c = int(n_total * 0.25)
    n_d = int(n_total * 0.15)
    n_e = n_total - (n_a + n_b + n_c + n_d)
    
    # Generate Sub-Graf
    G_A = nx.barabasi_albert_graph(n=n_a, m=10, seed=seed)
    G_B = nx.barabasi_albert_graph(n=n_b, m=10, seed=seed+1)
    G_C = nx.barabasi_albert_graph(n=n_c, m=10, seed=seed+2)
    G_D = nx.barabasi_albert_graph(n=n_d, m=10, seed=seed+3)
    G_E = nx.barabasi_albert_graph(n=n_e, m=10, seed=seed+4)
    
    G_total = nx.disjoint_union_all([G_A, G_B, G_C, G_D, G_E])
    
    # Koneksi Antar Ketua
    ketua_a = 0
    ketua_b = n_a
    ketua_c = n_a + n_b
    ketua_d = n_a + n_b + n_c
    ketua_e = n_a + n_b + n_c + n_d
    
    list_ketua = [ketua_a, ketua_b, ketua_c, ketua_d, ketua_e]
    
    for k1, k2 in itertools.combinations(list_ketua, 2):
        G_total.add_edge(k1, k2)
    
    node_data = {}
    
    # Load Nama
    nama = []
    if os.path.exists("data/nama.csv"):
        with open("data/nama.csv", "r") as file:
            nama = [line.strip() for line in file.readlines()]
    
    random.seed(121437)
    random.shuffle(nama)
    
    for node_id in G_total.nodes():
        if node_id < n_a:
            divisi = "Bidang Pergerakan"
            jabatan = "Ketua Divisi" if node_id == 0 else "Staff"
        elif node_id < n_a+n_b :
            divisi = "Bidang Analisis"
            jabatan = "Ketua Divisi" if node_id == n_a else "Staff"
        elif node_id < n_a+n_b+n_c :
            divisi = "Bidang Kemasyarakatan"
            jabatan = "Ketua Divisi" if node_id == n_a+n_b else "Staff"
        elif node_id < n_a+n_b+n_c+n_d :
            divisi = "Bidang Relasi"
            jabatan = "Ketua Divisi" if node_id == n_a+n_b+n_c else "Staff"
        else:
            divisi = "Bidang Kemahasiswaan"
            jabatan = "Ketua Divisi" if node_id == n_a+n_b+n_c+n_d else "Staff"
        
        # Ambil nama
        if len(nama) > 0:
            nama1 = nama.pop()
        else:
            nama1 = f"Mahasiswa_{node_id}"
        node_data[node_id] = {
            "nama": nama1,
            "divisi": divisi,
            "jabatan": jabatan,
            "ipk": round(random.uniform(2.5, 4.0), 2)
        }
        
    adj_list = nx.to_dict_of_lists(G_total)
    
    # Simpan Biodata ke CSV
    file = open(f"data/Biodata_N{n_total}.csv", "w")
    file.write("id;nama;divisi;jabatan;ipk\n")
    for i in range(n_total) :
        file.write(f"{i};{node_data[i]['nama']};{node_data[i]['divisi']};{node_data[i]['jabatan']};{node_data[i]['ipk']}\n")
    file.close()
    
    return adj_list, node_data

if __name__ == "__main__":
    Ns = [100, 400, 700, 1000]
    base_seed = 121437

    for n in Ns:
        for r in range(5):
            current_seed = base_seed + r
            
            adj_list, node_data = generate_bem_graph(n, current_seed)
            
            output_content = {
                "project": "connected_components_social_graph",
                "description": f"Graf BEM {n} nodes dengan Data Atribut",
                "n_nodes": n,
                "graph_adj": adj_list,
                "node_data": node_data
            }       
            
            filename = f"data/social_graph_N{n}_seed{current_seed}.json"
            
            with open(filename, "w") as f:
                json.dump(output_content, f, indent=2)
                
            print(f"[OK] Generated: {filename}")
            
    print(">> Selesai, data sudah siap! Silahkan jalankan run.py")