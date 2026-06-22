package com.research.benchmark;

import com.research.model.Person;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.HashMap;
import java.util.concurrent.TimeUnit;

/**
 * HashMapBenchmark — mengukur 5 operasi CRUD pada HashMap<Integer, Person>.
 *
 * Konfigurasi JMH identik dengan ArrayListBenchmark untuk fairness:
 *   - Warmup    : 5 iterasi × 1 detik
 *   - Measure   : 10 iterasi × 1 detik
 *   - Forks     : 3
 *   - Mode      : AverageTime (ns/op) + Throughput (ops/sec)
 */
@BenchmarkMode({Mode.AverageTime, Mode.Throughput})
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 10, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(value = 3, jvmArgsAppend = {
    "-Xms4g", "-Xmx4g",
    "-XX:+UseG1GC",
    "-XX:+AlwaysPreTouch"
})
@State(Scope.Benchmark)
public class HashMapBenchmark {

    @Param({"1000", "10000", "100000", "1000000"})
    private int datasetSize;

    private HashMap<Integer, Person> map;
    private int[]                    searchKeys;
    private int                      keyIndex;

    private int insertCounter;

    /* ── Setup ────────────────────────────────────────────────── */
    @Setup(Level.Trial)
    public void setupTrial() {
        map        = DatasetGenerator.buildHashMap(datasetSize);
        searchKeys = DatasetGenerator.buildSearchKeys(datasetSize, 10_000);
        keyIndex   = 0;
        insertCounter = datasetSize;
    }

    @Setup(Level.Iteration)
    public void setupIteration() {
        // Trim ke ukuran asli jika ada insert tambahan
        if (map.size() > datasetSize) {
            // Hapus key tambahan (id >= datasetSize)
            map.entrySet().removeIf(e -> e.getKey() >= datasetSize);
        }
        keyIndex = 0;
    }

    /* ══════════════════════════════════════════════════════════
       1. INSERT — put entry baru (O(1) average)
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void insert(Blackhole bh) {
        Person p = Person.of(insertCounter++);
        map.put(p.getId(), p);
        bh.consume(map.size());
    }

    /* ══════════════════════════════════════════════════════════
       2. SEARCH — get by key (O(1) average)
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void search(Blackhole bh) {
        int targetId = searchKeys[keyIndex % searchKeys.length];
        keyIndex++;

        Person found = map.get(targetId);
        bh.consume(found);
    }

    /* ══════════════════════════════════════════════════════════
       3. UPDATE — get + put dengan value baru (O(1) average)
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void update(Blackhole bh) {
        int targetId = searchKeys[keyIndex % searchKeys.length];
        keyIndex++;

        Person old = map.get(targetId);
        if (old != null) {
            Person updated = new Person(old.getId(), old.getName(),
                                        old.getAge() + 1, old.getEmail());
            map.put(targetId, updated);
            bh.consume(updated);
        }
    }

    /* ══════════════════════════════════════════════════════════
       4. DELETE — remove by key lalu put kembali (O(1) average)
          Sama dengan ArrayList: elemen dikembalikan agar ukuran stabil.
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void delete(Blackhole bh) {
        int targetId = searchKeys[keyIndex % searchKeys.length];
        keyIndex++;

        Person removed = map.remove(targetId);
        if (removed != null) {
            // Kembalikan agar ukuran map tetap stabil
            map.put(removed.getId(), removed);
            bh.consume(removed);
        }
    }

    /* ══════════════════════════════════════════════════════════
       5. ITERATE — traversal seluruh values (O(n + capacity))
          Mensimulasikan use-case yang sama: sum semua age.
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public long iterate() {
        long sum = 0;
        for (Person p : map.values()) {
            sum += p.getAge();
        }
        return sum;
    }
}
