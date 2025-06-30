import random


def generate_IC():
    year = random.randint(0, 99)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    birthday = f"{year:02d}{month:02d}{day:02d}"

    state = random.randint(1, 14)
    state_code = f"{state:02d}"

    serial = random.randint(0, 9999)
    serial_num = f"{serial:04d}"

    return birthday + state_code + serial_num


def folding_hash(ic, table_size):
    part1 = int(ic[0:4])
    part2 = int(ic[4:8])
    part3 = int(ic[8:12])
    return (part1 + part2 + part3) % table_size


def build_hash_table(size, ic_list):
    table = [[] for _ in range(size)]
    collisions = 0

    for ic in ic_list:
        index = folding_hash(ic, size)
        if table[index]:
            collisions += 1
        table[index].append(ic)

    return table, collisions


def print_full_table(table):
    print(f"\nHash Table with size {len(table)}:")
    for i in range(len(table)):
        if table[i]:
            chain = " --> ".join(table[i])
            print(f"table[{i}] --> {chain}")
        else:
            print(f"table[{i}]")


def main():
    rounds = 10
    entries = 1000
    sizes = [1009, 2003]  # Or [1009, 3001] to match sample

    for size in sizes:
        total_collisions = 0

        for round_num in range(rounds):
            ic_list = [generate_IC() for _ in range(entries)]
            table, collisions = build_hash_table(size, ic_list)
            total_collisions += collisions

        print_full_table(table)

        avg_collisions = total_collisions / rounds
        collision_rate = (avg_collisions / entries) * 100

        print(f"\nCollision Rate for {'Smaller' if size == 1009 else 'Bigger'} Hash Table: {collision_rate:.2f} %")


if __name__ == "__main__":
    main()