package com.research.benchmark;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;

import org.openjdk.jol.info.ClassLayout;
import org.openjdk.jol.info.GraphLayout;

import com.research.model.Person;

public class MemoryProfiler {

    private static final int[] SIZES = DatasetGenerator.SIZES;

    public static void main(String[] args) throws IOException {
        System.out.println("=== Memory Profiler (JOL) ===");
        System.out.println("Timestamp: " + LocalDateTime.now());
        System.out.println();

        String csvPath = "results/memory_footprint.csv";

        new java.io.File("results").mkdirs();

        try (PrintWriter csv = new PrintWriter(new FileWriter(csvPath))) {

            csv.println("timestamp,data_structure,dataset_size,shallow_bytes,deep_bytes,bytes_per_element");
            System.out.printf("%-12s | %-10s | %14s | %14s | %18s%n",
                "Structure", "Size", "Shallow(bytes)", "Deep(bytes)", "Bytes/Element");
            System.out.println("-".repeat(75));

            for (int size : SIZES) {

                // ArrayList
                ArrayList<Person> list = DatasetGenerator.buildArrayList(size);
                System.gc();
                Thread.yield();

                long listShallow = ClassLayout.parseInstance(list).instanceSize();
                long listDeep    = GraphLayout.parseInstance(list).totalSize();
                double listPerElem = (double) listDeep / size;

                String now = LocalDateTime.now().toString();
                csv.printf("%s,ArrayList,%d,%d,%d,%.2f%n",
                    now, size, listShallow, listDeep, listPerElem);
                System.out.printf("%-12s | %,10d | %,14d | %,14d | %,18.2f%n",
                    "ArrayList", size, listShallow, listDeep, listPerElem);

                list = null;
                System.gc();
                Thread.yield();

                // HashMap
                HashMap<Integer, Person> map = DatasetGenerator.buildHashMap(size);
                System.gc();
                Thread.yield();

                long mapShallow = ClassLayout.parseInstance(map).instanceSize();
                long mapDeep    = GraphLayout.parseInstance(map).totalSize();
                double mapPerElem = (double) mapDeep / size;

                csv.printf("%s,HashMap,%d,%d,%d,%.2f%n",
                    now, size, mapShallow, mapDeep, mapPerElem);
                System.out.printf("%-12s | %,10d | %,14d | %,14d | %,18.2f%n",
                    "HashMap", size, mapShallow, mapDeep, mapPerElem);

                System.out.println();
                map = null;
            }
        }

        System.out.println("CSV tersimpan di: " + csvPath);
    }
}