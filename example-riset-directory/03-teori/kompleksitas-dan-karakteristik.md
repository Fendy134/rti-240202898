# Teori Kompleksitas & Karakteristik Struktur Data

Landasan teoretis untuk ArrayList dan HashMap pada Java Collections Framework.

---

## 1. ArrayList\<T\>

### 1.1 Definisi

`ArrayList<T>` adalah implementasi **dynamic array** (array dinamis) dari interface `List<T>` pada Java Collections Framework. Secara internal menggunakan `Object[]` array yang otomatis di-resize (grow) saat kapasitas penuh.

### 1.2 Karakteristik Internal

```java
public class ArrayList<E> {
    transient Object[] elementData; // backing array
    private int size;               // jumlah elemen aktif
    
    private static final int DEFAULT_CAPACITY = 10;
}
```

**Resize strategy:**
- Initial capacity: 10 elemen
- Growth factor: 1.5× (kapasitas baru = kapasitas lama × 1.5)
- Operasi resize memerlukan alokasi array baru + copy semua elemen (O(n))

### 1.3 Kompleksitas Waktu (Big-O Notation)

| Operasi | Average Case | Worst Case | Keterangan |
|---|---|---|---|
| **insert** (append) | O(1)* | O(n) | *Amortized O(1), worst case saat resize |
| **insert** (at index) | O(n) | O(n) | Shift elemen dari index ke kanan |
| **search** (by value) | O(n) | O(n) | Linear scan (sequential search) |
| **get** (by index) | O(1) | O(1) | Direct array access |
| **update** (by index) | O(1) | O(1) | Direct array access + assignment |
| **delete** (by index) | O(n) | O(n) | Shift elemen dari index+1 ke kiri |
| **iterate** | O(n) | O(n) | Sequential traversal |

### 1.4 Kompleksitas Memori

```
Memory overhead = 16 bytes (object header) + 
                  4 bytes (size field) + 
                  8 bytes (reference to array) +
                  (capacity × 8 bytes for references) +
                  (n × size of Person object)
```

**Keuntungan:**
- Cache locality — elemen disimpan contiguous di memory (friendly untuk CPU cache L1/L2)
- Memory overhead rendah untuk dataset kecil
- No hash overhead

**Kerugian:**
- Resize overhead saat kapasitas penuh
- Search O(n) — tidak efisien untuk lookup by value

---

## 2. HashMap<K, V>

### 2.1 Definisi

`HashMap<K,V>` adalah implementasi **hash table** dari interface `Map<K,V>` pada Java Collections Framework. Secara internal menggunakan array of buckets (linked list atau tree) dengan hash function untuk distribusi key.

### 2.2 Karakteristik Internal

```java
public class HashMap<K,V> {
    transient Node<K,V>[] table;  // array of buckets
    transient int size;            // jumlah entries
    int threshold;                 // rehash threshold = capacity × loadFactor
    final float loadFactor;        // default 0.75
    
    static final int DEFAULT_INITIAL_CAPACITY = 16;
    static final int TREEIFY_THRESHOLD = 8;  // switch to tree saat collision > 8
}
```

**Collision resolution:**
- Bucket < 8 entries: Linked list (O(n) traversal)
- Bucket ≥ 8 entries: Red-black tree (O(log n) traversal) — optimization sejak Java 8

**Rehashing:**
- Terjadi saat `size > capacity × loadFactor`
- Kapasitas baru = 2× kapasitas lama
- Semua entries di-rehash ke bucket baru (O(n))

### 2.3 Kompleksitas Waktu (Big-O Notation)

| Operasi | Average Case | Worst Case | Keterangan |
|---|---|---|---|
| **insert** (put) | O(1) | O(n) | Worst case saat rehash |
| **search** (get by key) | O(1) | O(log n) | O(log n) saat collision → tree |
| **update** (put existing key) | O(1) | O(log n) | Same as search |
| **delete** (remove by key) | O(1) | O(log n) | Same as search |
| **iterate** (entrySet) | O(n + capacity) | O(n + capacity) | Traverse all buckets (termasuk bucket kosong) |

**Catatan:** Average case O(1) mengasumsikan hash function distribusi uniform dan load factor < 0.75.

### 2.4 Kompleksitas Memori

```
Memory overhead = 16 bytes (object header) +
                  8 bytes (reference to table array) +
                  4 bytes (size field) +
                  4 bytes (threshold field) +
                  4 bytes (loadFactor field) +
                  (capacity × 8 bytes for bucket references) +
                  (n × (32 bytes Node overhead + size of K + size of V))
```

**Node structure:**
```java
static class Node<K,V> {
    final int hash;     // 4 bytes
    final K key;        // 8 bytes (reference)
    V value;            // 8 bytes (reference)
    Node<K,V> next;     // 8 bytes (reference)
    // + 16 bytes object header
    // Total: 44 bytes overhead per entry
}
```

**Keuntungan:**
- Search/update/delete O(1) rata-rata — sangat efisien untuk lookup by key
- No shift overhead seperti ArrayList

**Kerugian:**
- Memory overhead tinggi (Node wrapper + bucket array)
- Rehashing overhead saat size > threshold
- Cache locality buruk — entries tersebar di memory (cache miss)
- Iterate lebih lambat karena harus traverse all buckets (termasuk kosong)

---

## 3. Perbandingan Teoretis

| Aspek | ArrayList | HashMap |
|---|---|---|
| **Search by value** | O(n) — linear scan | N/A (HashMap search by key, bukan value) |
| **Search by key** | N/A (ArrayList tidak punya key) | O(1) — hash lookup |
| **Insert (append)** | O(1) amortized | O(1) amortized (jika tidak rehash) |
| **Update by index** | O(1) | N/A (HashMap update by key) |
| **Update by key** | O(n) — search + update | O(1) — hash lookup + update |
| **Delete** | O(n) — shift elemen | O(1) — hash lookup + delete |
| **Iterate** | O(n) — cache friendly | O(n + capacity) — cache unfriendly |
| **Memory overhead** | Rendah (array + references) | Tinggi (Node + bucket array + hash) |

---

## 4. Hipotesis Performa Empiris

Berdasarkan teori kompleksitas di atas, **hipotesis performa empiris**:

1. **HashMap lebih cepat pada operasi search** (O(1) vs O(n)) — hipotesis: speedup >100× pada dataset 10⁶

2. **HashMap lebih cepat pada operasi update** (O(1) vs O(n)) — hipotesis: speedup >100× pada dataset 10⁶

3. **HashMap lebih cepat pada operasi delete** (O(1) vs O(n)) — hipotesis: speedup >1000× pada dataset 10⁶

4. **ArrayList lebih cepat pada operasi insert** (append) — hipotesis: speedup 2–5× karena no hash overhead

5. **ArrayList lebih cepat pada operasi iterate** — hipotesis: speedup 2–10× karena cache locality (CPU cache L1/L2 hit rate tinggi)

6. **ArrayList lebih hemat memori pada dataset kecil** (<10⁴) — hipotesis: perbedaan >50% karena HashMap Node overhead

7. **Boundary condition: iterate pada dataset 1M** — hipotesis: perbedaan menjadi tidak signifikan (TIE) karena ArrayList cache miss pada dataset besar

---

## 5. Faktor Runtime JVM yang Mempengaruhi Performa

### 5.1 JIT Compiler (Just-In-Time Compilation)

- **Tiered Compilation** — Java 17 LTS menggunakan C1 (client compiler) untuk warm-up, C2 (server compiler) untuk hot methods
- **Inlining** — JIT dapat inline method call kecil (seperti `ArrayList.get(index)`) untuk eliminasi overhead
- **Escape Analysis** — objek yang tidak escape method dapat dialokasikan di stack (bukan heap) untuk mengurangi GC overhead

**Implikasi:** Benchmark harus melakukan **warmup** (5+ iterations) untuk memastikan JIT compiler sudah mengoptimasi hot path.

### 5.2 Garbage Collection (GC)

- **G1GC** (default Java 17) — generational GC dengan pause time target (<200ms)
- **Eden space** — tempat alokasi objek baru (young generation)
- **Survivor space** — objek yang survive 1+ GC cycle
- **Old generation** — objek yang survive banyak GC cycle

**Implikasi:** Benchmark harus menggunakan **fixed heap size** (`-Xms4g -Xmx4g`) untuk mengurangi variabilitas GC.

### 5.3 CPU Cache Locality

- **L1 cache** — 32 KB, latency ~4 cycles (~1 ns)
- **L2 cache** — 256 KB, latency ~12 cycles (~3 ns)
- **L3 cache** — 8 MB, latency ~40 cycles (~10 ns)
- **Main memory** — latency ~200 cycles (~60 ns)

**Implikasi:** ArrayList (contiguous memory) lebih cache-friendly dibanding HashMap (pointer chasing) pada operasi iterate.

---

## Referensi

1. Naftalin, Maurice, and Philip Wadler. *Java Generics and Collections*. O'Reilly Media, 2006.
2. Bloch, Joshua. *Effective Java*. 3rd ed. Addison-Wesley, 2018.
3. Evans, Benjamin J. *Optimizing Java: Practical Techniques for Improving JVM Application Performance*. O'Reilly Media, 2018.
4. Oracle. *Java Platform, Standard Edition 17 API Specification*. 2023. https://docs.oracle.com/en/java/javase/17/
