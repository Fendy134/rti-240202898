package com.research.benchmark;

import com.research.model.Person;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

/**
 * DatasetGenerator — generate dataset reproducible untuk benchmark.
 *
 * Seed tetap (42) sesuai proposal sehingga setiap run menghasilkan
 * data yang identik → reproducibility terjamin.
 *
 * Ukuran dataset sesuai proposal:
 *   SMALL  = 1_000      (10³)
 *   MEDIUM = 10_000     (10⁴)
 *   LARGE  = 100_000    (10⁵)
 *   XLARGE = 1_000_000  (10⁶)
 */
public final class DatasetGenerator {

    /** Seed tetap — JANGAN diubah agar data reproducible. */
    public static final long SEED = 42L;

    /** Ukuran dataset sesuai proposal */
    public static final int SMALL  = 1_000;
    public static final int MEDIUM = 10_000;
    public static final int LARGE  = 100_000;
    public static final int XLARGE = 1_000_000;

    /** Semua ukuran dalam satu array — dipakai @Param di benchmark */
    public static final int[] SIZES = { SMALL, MEDIUM, LARGE, XLARGE };

    // ── Utility class: jangan di-instantiate ──────────────────
    private DatasetGenerator() {}

    /* ── ArrayList ────────────────────────────────────────────── */

    /**
     * Buat ArrayList berisi {@code size} objek Person.
     * Index i → Person.of(i), urutan deterministik.
     */
    public static ArrayList<Person> buildArrayList(int size) {
        ArrayList<Person> list = new ArrayList<>(size);
        for (int i = 0; i < size; i++) {
            list.add(Person.of(i));
        }
        return list;
    }

    /* ── HashMap ──────────────────────────────────────────────── */

    /**
     * Buat HashMap<Integer, Person> berisi {@code size} entry.
     * Key = person.getId() (int 0..size-1).
     * Initial capacity disetel agar tidak ada resize selama benchmark.
     */
    public static HashMap<Integer, Person> buildHashMap(int size) {
        // capacity = size / loadFactor(0.75) + 1  →  tidak ada resize
        int initialCapacity = (int) (size / 0.75) + 1;
        HashMap<Integer, Person> map = new HashMap<>(initialCapacity);
        for (int i = 0; i < size; i++) {
            Person p = Person.of(i);
            map.put(p.getId(), p);
        }
        return map;
    }

    /* ── Search keys (random, reproducible) ───────────────────── */

    /**
     * Buat array key acak yang akan dicari saat benchmark search/update/delete.
     * Semua key dijamin ada di dataset (0 ≤ key < size).
     * Menggunakan SEED yang sama → reproducible.
     */
    public static int[] buildSearchKeys(int size, int count) {
        Random rng = new Random(SEED);
        int[] keys = new int[count];
        for (int i = 0; i < count; i++) {
            keys[i] = rng.nextInt(size);
        }
        return keys;
    }

    /* ── Quick sanity check (jalankan sekali sebelum benchmark) ── */

    public static void main(String[] args) {
        System.out.println("=== DatasetGenerator Sanity Check ===");
        for (int size : SIZES) {
            ArrayList<Person>       al = buildArrayList(size);
            HashMap<Integer,Person> hm = buildHashMap(size);
            System.out.printf(
                "size=%,7d | ArrayList.size=%,7d | HashMap.size=%,7d%n",
                size, al.size(), hm.size()
            );
            // Validasi: elemen pertama dan terakhir
            assert al.get(0).getId() == 0;
            assert al.get(size - 1).getId() == size - 1;
            assert hm.containsKey(0);
            assert hm.containsKey(size - 1);
        }
        System.out.println("All checks PASSED.");
    }
}
