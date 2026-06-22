# Tahap 1: Setup Environment & Implementasi Benchmark Harness

**Periode:** Minggu 6-7  
**Status:** ✅ Selesai  

---

## Tujuan Tahap

1. Setup development environment (Java 17 LTS, Maven, IDE)
2. Implementasi model data `Person.java` (POJO)
3. Implementasi dataset generator dengan seed tetap (reproducibility)
4. Implementasi benchmark harness JMH untuk ArrayList dan HashMap (5 operasi CRUD)
5. Implementasi memory profiler JOL untuk measurement memory footprint
6. Verifikasi build success dan test run

---

## Aktivitas & Deliverable

### 1.1 Setup Environment

**Prerequisites:**
```bash
# Java 17 LTS
java -version
# Output: openjdk version "17.0.x"

# Maven 3.8+
mvn --version
# Output: Apache Maven 3.8.x
```

**Project setup:**
```bash
cd ../../benchmark-project/
mvn archetype:generate \
    -DarchetypeGroupId=org.openjdk.jmh \
    -DarchetypeArtifactId=jmh-java-benchmark-archetype \
    -DgroupId=com.research \
    -DartifactId=benchmark-project \
    -Dversion=1.0-SNAPSHOT
```

**Dependencies (`pom.xml`):**
```xml
<dependencies>
    <!-- JMH -->
    <dependency>
        <groupId>org.openjdk.jmh</groupId>
        <artifactId>jmh-core</artifactId>
        <version>1.37</version>
    </dependency>
    <dependency>
        <groupId>org.openjdk.jmh</groupId>
        <artifactId>jmh-generator-annprocess</artifactId>
        <version>1.37</version>
    </dependency>
    
    <!-- JOL -->
    <dependency>
        <groupId>org.openjdk.jol</groupId>
        <artifactId>jol-core</artifactId>
        <version>0.17</version>
    </dependency>
</dependencies>
```

**Build:**
```bash
mvn clean package
# Output: target/benchmarks.jar
```

---

### 1.2 Model Data — Person.java

**File:** `src/main/java/com/research/model/Person.java`

**Karakteristik:**
- Immutable (semua field `final`)
- 4 field: `id` (int), `name` (String), `age` (int), `email` (String)
- Factory method `Person.of(id)` untuk deterministic generation
- equals/hashCode berbasis `id` saja (konsisten dengan HashMap key)

**Rationale:**
- POJO sederhana untuk fokus pada performa struktur data (bukan kompleksitas objek)
- Immutable untuk thread-safety (future work: multithreading)
- equals/hashCode berbasis id untuk fairness comparison (ArrayList.search vs HashMap.get)

**Kode lengkap:** Lihat [../../benchmark-project/src/main/java/com/research/model/Person.java](../../benchmark-project/src/main/java/com/research/model/Person.java)

---

### 1.3 Dataset Generator — DatasetGenerator.java

**File:** `src/main/java/com/research/benchmark/DatasetGenerator.java`

**Karakteristik:**
- Seed tetap (42) untuk reproducibility
- ID sequential (1..size) untuk fairness comparison
- Pre-sizing ArrayList/HashMap untuk menghindari resize overhead saat generation

**Rationale:**
- Seed tetap → dataset identik di setiap run → reproducible benchmark
- Pre-sizing → avoid resize overhead pada setup phase (hanya ukur resize overhead saat benchmark insert)

**Methods:**
```java
public static List<Person> generatePersons(int size);
public static Map<Integer, Person> generatePersonMap(int size);
```

---

### 1.4 Benchmark Harness — ArrayListBenchmark.java

**File:** `src/main/java/com/research/benchmark/ArrayListBenchmark.java`

**Konfigurasi JMH:**
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Benchmark)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 10, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(value = 3)
@Param({"1000", "10000", "100000", "1000000"})
private int datasetSize;
```

**5 Benchmark Methods:**
1. `insert()` — append ke ArrayList
2. `search()` — linear scan by id
3. `update()` — set by random index
4. `delete()` — remove by random index
5. `iterate()` — foreach loop

**Catatan penting:**
- `Blackhole.consume()` — mencegah dead-code elimination oleh JIT compiler
- `@Setup(Level.Trial)` — setup dilakukan sekali per fork (bukan per iteration)
- Random seed 42 untuk reproducibility

---

### 1.5 Benchmark Harness — HashMapBenchmark.java

**File:** `src/main/java/com/research/benchmark/HashMapBenchmark.java`

**Struktur sama dengan ArrayListBenchmark, tapi:**
- Menggunakan `HashMap<Integer, Person>`
- Search/update/delete by key (id) bukan by index/linear scan

**5 Benchmark Methods:**
1. `insert()` — put(key, value)
2. `search()` — get(key)
3. `update()` — put(existing_key, new_value)
4. `delete()` — remove(key)
5. `iterate()` — foreach entrySet()

---

### 1.6 Memory Profiler — MemoryProfiler.java

**File:** `src/main/java/com/research/benchmark/MemoryProfiler.java`

**Fungsi:**
- Mengukur memory footprint (shallow size + deep size) menggunakan JOL
- Output CSV: `data_structure,dataset_size,shallow_bytes,deep_bytes,bytes_per_element`

**Rationale:**
- JOL mengukur footprint presisi (termasuk object header, alignment padding)
- Alternatif `Runtime.getRuntime().freeMemory()` tidak akurat (terpengaruh GC)

**Command:**
```bash
java -cp target/benchmarks.jar \
    com.research.benchmark.MemoryProfiler \
    > results/memory_footprint.csv
```

---

## Verifikasi

### Test Run (Subset Kecil)

```bash
# Hanya ArrayList.search, ukuran 1K, 2 warmup, 3 measurement, 1 fork
java -jar target/benchmarks.jar "ArrayListBenchmark.search" \
    -p datasetSize=1000 \
    -wi 2 -i 3 -f 1
```

**Expected output:**
```
Benchmark                             (datasetSize)  Mode  Cnt    Score   Error  Units
ArrayListBenchmark.search                      1000  avgt    3  1088.87 ± 45.23  ns/op
```

**Verification checklist:**
- [x] Build success (`mvn clean package`)
- [x] JMH annotations valid (no compilation error)
- [x] Test run sukses (no exception)
- [x] Score reasonable (tidak 0 atau inf)
- [x] Dataset generation deterministik (run 2× menghasilkan score sama)

---

## Konfigurasi JVM Flags

**Default JMH flags:**
```bash
-Xms4g -Xmx4g           # Fixed heap 4GB
-XX:+UseG1GC            # G1 Garbage Collector
-XX:+AlwaysPreTouch     # Touch all memory pages saat startup
```

**Rationale:**
- Fixed heap → reduce GC variability
- G1GC → default Java 17, pause time target <200ms
- AlwaysPreTouch → avoid page fault overhead saat benchmark

---

## Output Tahap 1

| File | Deskripsi |
|---|---|
| `Person.java` | Model data POJO (immutable, 4 field) |
| `DatasetGenerator.java` | Dataset generator (seed=42, pre-sizing) |
| `ArrayListBenchmark.java` | 5 operasi CRUD ArrayList |
| `HashMapBenchmark.java` | 5 operasi CRUD HashMap |
| `MemoryProfiler.java` | JOL memory measurement |
| `target/benchmarks.jar` | Executable JAR untuk run benchmark |

---

## Kendala & Solusi

| Kendala | Solusi |
|---|---|
| Maven build error: JMH annotation processor not found | Add `jmh-generator-annprocess` dependency |
| JVM OutOfMemoryError saat build | Increase Maven heap: `export MAVEN_OPTS="-Xmx2g"` |
| Test run terlalu lama (>5 menit untuk 1 kombinasi) | Reduce iterations: `-wi 1 -i 2 -f 1` untuk testing |

---

## Status

✅ **Tahap 1 selesai** — benchmark harness ready untuk eksekusi penuh.

**Next:** [Tahap 2 — Eksekusi Benchmark Penuh](tahap-2-eksekusi-benchmark.md)
