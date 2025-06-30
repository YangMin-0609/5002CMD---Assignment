import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor


def generate_random_numbers(count=100):
    """Generate list of random numbers between 0-10000"""
    return [random.randint(0, 10000) for _ in range(count)]


def threaded_execution():
    #Generate 3 sets of random numbers using multithreading
    threads = []
    results = [[] for _ in range(3)]  # Store results from each thread

    def worker(thread_id):
        #Thread worker function
        results[thread_id] = generate_random_numbers()

    # Record start time before creating threads
    start_time = time.time_ns()

    # Create and start threads
    for i in range(3):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Get end time after last thread finishes
    end_time = time.time_ns()

    return results, end_time - start_time


def sequential_execution():
    """Generate 3 sets of random numbers sequentially"""
    start_time = time.time_ns()

    results = [
        generate_random_numbers(),
        generate_random_numbers(),
        generate_random_numbers()
    ]

    end_time = time.time_ns()

    return results, end_time - start_time


def run_comparison(rounds=10):
    """Run multithreaded vs sequential comparison for specified rounds"""
    print("+--------+----------------------+--------------------------+-----------------+")
    print("| Round  | Multithreading Time  | Non-Multithreading Time  | Difference      |")
    print("|        | (ns)                 | (ns)                     | (ns)            |")
    print("+--------+----------------------+--------------------------+-----------------+")

    mt_times = []
    st_times = []

    for round_num in range(1, rounds + 1):
        # Multithreaded execution
        _, mt_time = threaded_execution()
        mt_times.append(mt_time)

        # Sequential execution
        _, st_time = sequential_execution()
        st_times.append(st_time)

        # Calculate difference
        difference = mt_time - st_time

        print(f"| {round_num:<6} | {mt_time:<20} | {st_time:<24} | {difference:<15} |")

    print("+--------+----------------------+--------------------------+-----------------+")

    # Calculate summary statistics
    total_mt = sum(mt_times)
    total_st = sum(st_times)
    avg_mt = total_mt / rounds
    avg_st = total_st / rounds
    total_diff = total_mt - total_st
    avg_diff = avg_mt - avg_st

    print("\nSummary of Results:")
    print("+------------------+----------------------+--------------------------+-----------------+")
    print("| Metric           | Multithreading (ns)  | Non-Multithreading (ns)  | Difference (ns) |")
    print("+------------------+----------------------+--------------------------+-----------------+")
    print(f"| Total Time       | {total_mt:<20} | {total_st:<24} | {total_diff:<15} |")
    print(f"| Average Time     | {avg_mt:<20.1f} | {avg_st:<24.1f} | {avg_diff:<15.1f} |")
    print("+------------------+----------------------+--------------------------+-----------------+")

    return mt_times, st_times


if __name__ == "__main__":
    print("=== Multithreading Performance Comparison ===")
    print("Generating 3 sets of 100 random numbers (0-10000)")
    print("Testing with 10 rounds each for multithreaded and sequential approaches\n")

    mt_results, st_results = run_comparison()