# Analisis Algoritma DFS vs BFS pada Social Network Graph

**Project DAA Kelas B - Kelompok 2**

Paket proyek ini berisi implementasi dan kerangka eksperimen untuk membandingkan performa algoritma *Depth First Search (DFS)* dan *Breadth First Search (BFS)* dalam melakukan penelusuran (traversal) pada graf jaringan sosial mahasiswa (BEM).

## 📂 Struktur Folder

* **`data/`**: Direktori penyimpanan *instance* graf (JSON) dan biodata (CSV). (Otomatis dibuat oleh generator).
* **`results/`**: Direktori penyimpanan hasil benchmark (CSV, Summary, LaTeX).
* **`generate_instances.py`**: Generator dataset graf menggunakan model *Barabasi-Albert* dan atribut mahasiswa.
* **`run.py`**: Program utama (Menu Interaktif) untuk eksekusi eksperimen, pengukuran waktu, dan visualisasi.
* **`Analysis.ipynb`**: Jupyter Notebook untuk analisis statistik lanjutan, uji T-Test, dan dashboard interaktif.

## ⚙️ Persiapan (Requirements)

Install library Python yang dibutuhkan:

```bash
pip install networkx matplotlib pandas numpy scipy seaborn ipywidgets jupyter pydot
```
> **Note:** Untuk visualisasi graf yang optimal, pastikan **Graphviz** terinstall di sistem. Jika tidak, program akan otomatis menggunakan layout alternatif (Spring Layout).

## Cara Penggunaan

Jalankan program secara berurutan:

### 1. Pembangkitan Data
Jalankan script ini untuk membuat variasi graf dan data mahasiswa.

```bash
python generate_instances.py
```

### 2. Eksekusi Eksperimen & Visualisasi
```bash
python run.py
```

### 3. Analisis Lanjutan (Opsional)
```bash
jupyter notebook Analysis.ipynb
```

