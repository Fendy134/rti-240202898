# 05-kode — Source Code Benchmark & Analisis

Folder ini berisi dokumentasi dan referensi ke source code benchmark JMH dan analisis statistik Python.

---

## Struktur Kode

### 1. Benchmark Project (Java + Maven + JMH)

**Lokasi:** `../../benchmark-project/`

**Struktur:**
```
benchmark-project/
├── pom.xml                          ← Dependencies (JMH 1.37, JOL 0.17)
├── src/main/java/com/research/
│   ├── model/
│   │   └── Person.java              ← POJO data (id, name, age, email)
│   └── benchmark/
│       ├── DatasetGenerator.java    ← Generate dataset (seed=42)
│       ├── ArrayListBenchmark.java  ← 5 operasi CRUD ArrayList
│       ├── HashMapBenchmark.java    ← 5 operasi CRUD HashMap
│       └── MemoryProfiler.java      ← JOL memory measurement
├── run_benchmark.sh                 ← Script all-in-one
└── results/                         ← Output benchmark
```

**Komponen Utama:**

#### 1.1 Person.java — Model Data

```java
public final class Person {
    private final int    id;
    private final String name;
    private final int    age;
    private final String email;
    
    public Person(int id, String name, int age, String email) {
        this.id    = id;
        this.name  = name;
        this.age   = age;
        this.email = email;
    }
    
    public static Person of(int id) {
        return new Person(
            id,
            "User_" + id,
            20 + (id % 50),  // age 20-69
            "user" + id + "@research.com"
        );
    }
    
    // equals/hashCode berbasis id
}
```

**Karakteristik:**
- Immutable (semua field `final`)
- Factory method `Person.of(id)` untuk deterministic generation
- equals/hashCode berbasis `id` saja (konsisten dengan HashMap key)

#### 1.2 DatasetGenerator.java — Generate Dataset

```java
public class DatasetGenerator {
    private static final Random RANDOM = new Random(42); // seed tetap
    
    public static List<Person> generatePersons(int size) {
        List<Person> persons = new ArrayList<>(size);
        for (int i = 1; i <= size; i++) {
            persons.add(Person.of(i));
        }
        return persons;
    }
    
    public static Map<Integer, Person> generatePersonMap(int size) {
        Map<Integer, Person> map = new HashMap<>(size);
        for (int i = 1; i <= size; i++) {
            Person p = Person.of(i);
            map.put(p.getId(), p);
        }
        return map;
    }
}
```

**Karakteristik:**
- Seed tetap (42) untuk reproducibility
- ID sequential (1..size) untuk fairness comparison
- Pre-sizing ArrayList/HashMap untuk menghindari resize overhead saat generation

#### 1.3 ArrayListBenchmark.java — 5 Operasi CRUD

**Konfigurasi JMH:**
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Benchmark)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 10, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(value = 3)
public class ArrayListBenchmark {
    @Param({"1000", "10000", "100000", "1000000"})
    private int datasetSize;
    
    private List<Person> list;
    private Random random;
    
    @Setup(Level.Trial)
    public void setup() {
        random = new Random(42);
        list = new ArrayList<>(datasetSize);
        // Pre-populate untuk operasi search/update/delete
        for (int i = 1; i <= datasetSize; i++) {
            list.add(Person.of(i));
        }
    }
    
    @Benchmark
    public void insert(Blackhole bh) {
        Person p = Person.of(random.nextInt(1_000_000));
        list.add(p);
        bh.consume(p);
    }
    
    @Benchmark
    public void search(Blackhole bh) {
        int targetId = random.nextInt(datasetSize) + 1;
        Person result = null;
        for (Person p : list) {
            if (p.getId() == targetId) {
                result = p;
                break;
            }
        }
        bh.consume(result);
    }
    
    @Benchmark
    public void update(Blackhole bh) {
        int index = random.nextInt(datasetSize);
        Person updated = Person.of(random.nextInt(1_000_000));
        list.set(index, updated);
        bh.consume(updated);
    }
    
    @Benchmark
    public void delete(Blackhole bh) {
        int index = random.nextInt(list.size());
        Person removed = list.remove(index);
        bh.consume(removed);
    }
    
    @Benchmark
    public void iterate(Blackhole bh) {
        for (Person p : list) {
            bh.consume(p);
        }
    }
}
```

**Catatan penting:**
- `@State(Scope.Benchmark)` — state di-share antar iterations dalam satu fork
- `Blackhole.consume()` — mencegah dead-code elimination oleh JIT compiler
- `@Setup(Level.Trial)` — setup dilakukan sekali per fork (bukan per iteration)
- Random seed 42 untuk reproducibility

#### 1.4 HashMapBenchmark.java — 5 Operasi CRUD

Struktur sama dengan `ArrayListBenchmark.java`, tapi menggunakan `HashMap<Integer, Person>`:

```java
@Benchmark
public void search(Blackhole bh) {
    int targetId = random.nextInt(datasetSize) + 1;
    Person result = map.get(targetId);
    bh.consume(result);
}

@Benchmark
public void update(Blackhole bh) {
    int targetId = random.nextInt(datasetSize) + 1;
    Person updated = Person.of(random.nextInt(1_000_000));
    map.put(targetId, updated);
    bh.consume(updated);
}

@Benchmark
public void delete(Blackhole bh) {
    int targetId = random.nextInt(datasetSize) + 1;
    Person removed = map.remove(targetId);
    bh.consume(removed);
}

@Benchmark
public void iterate(Blackhole bh) {
    for (Map.Entry<Integer, Person> entry : map.entrySet()) {
        bh.consume(entry.getValue());
    }
}
```

#### 1.5 MemoryProfiler.java — JOL Memory Measurement

```java
public class MemoryProfiler {
    public static void main(String[] args) {
        int[] sizes = {1000, 10000, 100000, 1000000};
        
        System.out.println("data_structure,dataset_size,shallow_bytes,deep_bytes,bytes_per_element");
        
        for (int size : sizes) {
            // ArrayList
            List<Person> list = DatasetGenerator.generatePersons(size);
            System.out.println("ArrayList," + size + "," +
                GraphLayout.parseInstance(list).totalSize());
            
            // HashMap
            Map<Integer, Person> map = DatasetGenerator.generatePersonMap(size);
            System.out.println("HashMap," + size + "," +
                GraphLayout.parseInstance(map).totalSize());
        }
    }
}
```

---

### 2. Analysis Scripts (Python)

**Lokasi:** `../../benchmark-project/analysis/` (belum ada, referensi ke `../../analysis/`)

**Struktur:**
```
analysis/
├── 01_validate_data.py          ← Load CSV, outlier detection (Z-score)
├── 02_statistical_analysis.py   ← ANOVA, Tukey HSD, Cohen's d
├── 03_visualize.py              ← 5 figure PNG
├── requirements.txt             ← Dependencies (pandas, scipy, matplotlib)
└── README.md                    ← Dokumentasi analisis
```

**Dependencies:**
```txt
pandas>=1.5.0
scipy>=1.9.0
statsmodels>=0.13.0
matplotlib>=3.6.0
seaborn>=0.12.0
numpy>=1.23.0
```

**Workflow:**
```bash
cd analysis/
pip install -r requirements.txt

# 1. Validasi data (outlier detection)
python 01_validate_data.py ../benchmark-project/results/results.csv

# 2. Analisis statistik (ANOVA, Tukey HSD)
python 02_statistical_analysis.py ../benchmark-project/results/descriptive_stats.csv

# 3. Visualisasi
python 03_visualize.py ../benchmark-project/results/
```

---

## Cara Menjalankan Benchmark

### 1. Prerequisites

```bash
# Cek Java version
java -version  # Harus Java 17 LTS

# Cek Maven version
mvn --version  # Minimal 3.8+
```

### 2. Build

```bash
cd ../../benchmark-project/
mvn clean package
# Output: target/benchmarks.jar
```

### 3. Run Memory Profiler

```bash
java -cp target/benchmarks.jar \
    com.research.benchmark.MemoryProfiler \
    > results/memory_footprint.csv
```

### 4. Run JMH Benchmark (Full Matrix)

```bash
java -jar target/benchmarks.jar \
    -rf csv \
    -rff results/results.csv
    
# Estimasi waktu: 2-4 jam (40 kombinasi × 3 forks × ~2-3 menit)
```

### 5. Run Subset (untuk testing cepat)

```bash
# Hanya ArrayList, ukuran 1K
java -jar target/benchmarks.jar "ArrayListBenchmark" \
    -p datasetSize=1000 \
    -wi 2 -i 3 -f 1
    
# Output ke console saja (tidak ke CSV)
```

---

## Konfigurasi JVM Flags

**Default JMH flags:**
```bash
-Xms4g -Xmx4g           # Fixed heap 4GB
-XX:+UseG1GC            # G1 Garbage Collector
-XX:+AlwaysPreTouch     # Touch all memory pages saat startup
```

**Custom flags (optional):**
```bash
java -jar target/benchmarks.jar \
    -jvmArgs "-Xms4g -Xmx4g -XX:+UseParallelGC" \
    -rf csv -rff results/results_parallelgc.csv
```

---

## Troubleshooting

### Error: OutOfMemoryError

**Solusi:** Increase heap size
```bash
java -jar target/benchmarks.jar \
    -jvmArgs "-Xms8g -Xmx8g"
```

### Error: Benchmark takes too long

**Solusi:** Reduce warmup/measurement iterations
```bash
java -jar target/benchmarks.jar \
    -wi 2 -i 5 -f 1  # 2 warmup, 5 measurement, 1 fork
```

### Warning: Measurement variance too high (CV > 50%)

**Penyebab:** Background processes, GC activity, thermal throttling

**Solusi:**
- Close background applications
- Run benchmark saat sistem idle
- Increase measurement iterations (`-i 20`)

---

## Referensi

- JMH Tutorial: https://github.com/openjdk/jmh/tree/master/jmh-samples
- JOL Documentation: https://github.com/openjdk/jol
- Benchmark project: `../../benchmark-project/README.md`
