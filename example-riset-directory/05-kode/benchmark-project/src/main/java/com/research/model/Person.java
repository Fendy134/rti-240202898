package com.research.model;

/**
 * POJO Person — unit data yang dipakai di semua benchmark.
 *
 * Field sesuai proposal:
 *   id    : int    — dipakai sebagai key di HashMap<Integer, Person>
 *   name  : String
 *   age   : int
 *   email : String
 *
 * Immutable by design: semua field final, tidak ada setter.
 * Equals/hashCode berbasis id saja agar konsisten dengan key HashMap.
 */
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

    /* ── Getters ─────────────────────────────────────────────── */

    public int    getId()    { return id;    }
    public String getName()  { return name;  }
    public int    getAge()   { return age;   }
    public String getEmail() { return email; }

    /* ── equals / hashCode — berbasis id ─────────────────────── */

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Person other)) return false;
        return id == other.id;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }

    /* ── toString — untuk debugging ──────────────────────────── */

    @Override
    public String toString() {
        return "Person{id=" + id + ", name='" + name + "', age=" + age
                + ", email='" + email + "'}";
    }

    /* ── Factory — buat Person dengan id tertentu ────────────── */

    /**
     * Buat Person baru dengan field yang di-derive dari id.
     * Deterministik: id yang sama selalu menghasilkan objek yang sama.
     */
    public static Person of(int id) {
        return new Person(
            id,
            "User_" + id,
            20 + (id % 50),                     // age 20–69
            "user" + id + "@research.com"
        );
    }
}
