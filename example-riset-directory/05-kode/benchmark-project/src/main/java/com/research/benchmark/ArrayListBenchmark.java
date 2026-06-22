package com.research.benchmark;

import com.research.model.Person;
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

/**
 * ArrayListBenchmark — mengukur 5 operasi CRUD pada ArrayList<Person>.
 *
 * Konfigurasi JMH sesuai proposal:
 *   - Warmup    : 5 iterasi × 1 detik
 *   - Measure   : 10 iterasi × 1 detik
 *   - Forks     : 3 (JVM instance terpisah)
 *   - Mode      : AverageTime (ns/op) — primary DV
 *   - BenchmarkMode tambahan: Throughput (ops/sec) — secondary DV
 *
 * State (@State) dipisah dari benchmark method agar JMH bisa
 * mengelola lifecycle setup/teardown dengan benar.
 */
@BenchmarkMode({Mode.AverageTime, Mode.Throughput})
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, time = 1, timeUnit = TimeUnit.SECONDS)
@Measurement(iterations = 10, time = 1, timeUnit = TimeUnit.SECONDS)
@Fork(value = 3, jvmArgsAppend = {
    "-Xms4g", "-Xmx4g",
    "-XX:+UseG1GC",
    "-XX:+AlwaysPreTouch"          // pre-fault heap pages
})
@State(Scope.Benchmark)
public class ArrayListBenchmark {

    /* ── Parameter: ukuran dataset ──────────────────────────────
       JMH akan menjalankan SEMUA kombinasi secara otomatis.
       Sesuai proposal: 10³, 10⁴, 10⁵, 10⁶                      */
    @Param({"1000", "10000", "100000", "1000000"})
    private int datasetSize;

    /* ── State: data yang di-setup sebelum benchmark ─────────── */
    private ArrayList<Person> list;
    private int[]             searchKeys;   // key acak untuk search/update/delete
    private int               keyIndex;     // pointer round-robin ke searchKeys

    // Person baru untuk operasi insert (agar id tidak bentrok)
    private Person newPerson;
    private int    insertCounter;

    /* ── Setup: dipanggil SEKALI per fork, sebelum warmup ─────── */
    @Setup(Level.Trial)
    public void setupTrial() {
        list       = DatasetGenerator.buildArrayList(datasetSize);
        searchKeys = DatasetGenerator.buildSearchKeys(datasetSize, 10_000);
        keyIndex   = 0;
        insertCounter = datasetSize; // mulai dari id yang belum ada
    }

    /* ── Reset setelah setiap iterasi (bukan setiap invocation)
       Tujuan: jaga ukuran list tetap stabil antar iterasi           */
    @Setup(Level.Iteration)
    public void setupIteration() {
        // Trim ke ukuran asli jika ada insert yang menambah elemen
        if (list.size() > datasetSize) {
            list.subList(datasetSize, list.size()).clear();
        }
        // Siapkan newPerson untuk insert
        newPerson = Person.of(insertCounter++);
        keyIndex  = 0;
    }

    /* ══════════════════════════════════════════════════════════
       1. INSERT — tambah elemen di akhir list (O(1) amortized)
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void insert(Blackhole bh) {
        list.add(newPerson);
        bh.consume(list.size());   // cegah dead-code elimination
    }

    /* ══════════════════════════════════════════════════════════
       2. SEARCH — cari elemen berdasarkan id (O(n) linear scan)
          Menggunakan stream().filter() yang paling umum dipakai
          developer di production code.
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void search(Blackhole bh) {
        int targetId = searchKeys[keyIndex % searchKeys.length];
        keyIndex++;

        Person found = null;
        for (Person p : list) {
            if (p.getId() == targetId) {
                found = p;
                break;
            }
        }
        bh.consume(found);   // pastikan hasil tidak di-optimasi JIT
    }

    /* ══════════════════════════════════════════════════════════
       3. UPDATE — temukan elemen lalu ganti di index yang sama
          (O(n) untuk search + O(1) untuk set)
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void update(Blackhole bh) {
        int targetId = searchKeys[keyIndex % searchKeys.length];
        keyIndex++;

        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).getId() == targetId) {
                // Buat Person baru dengan age+1 (simulasi update field)
                Person old = list.get(i);
                list.set(i, new Person(old.getId(), old.getName(),
                                       old.getAge() + 1, old.getEmail()));
                bh.consume(i);
                break;
            }
        }
    }

    /* ══════════════════════════════════════════════════════════
       4. DELETE — hapus elemen berdasarkan id (O(n))
          Catatan: agar ukuran list stabil, elemen langsung
          ditambahkan kembali di akhir (swap strategy).
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public void delete(Blackhole bh) {
        int targetId = searchKeys[keyIndex % searchKeys.length];
        keyIndex++;

        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).getId() == targetId) {
                Person removed = list.remove(i);
                // Tambahkan kembali di akhir agar ukuran tetap stabil
                list.add(removed);
                bh.consume(removed);
                break;
            }
        }
    }

    /* ══════════════════════════════════════════════════════════
       5. ITERATE — traversal seluruh list (O(n))
          Mensimulasikan use-case: hitung sum semua age.
       ══════════════════════════════════════════════════════════ */
    @Benchmark
    public long iterate() {
        long sum = 0;
        for (Person p : list) {
            sum += p.getAge();
        }
        return sum;   // return value otomatis dikonsumsi JMH
    }
}
