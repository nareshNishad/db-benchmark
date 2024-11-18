import psycopg2
from psycopg2 import pool
import time
import matplotlib.pyplot as plt
import threading

# Database configuration
DB_CONFIG = {
    'database': 'benchmark_db',
    'user': 'benchmark_user',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Benchmark configurations
THREADS = 5  # Number of threads to simulate concurrent operations

# Ensure pool sizes are greater than or equal to THREADS
POOL_SIZES = [5, 10, 20, 50]  # Adjust as needed
OPERATIONS = ['insert', 'update', 'read']
NUM_RECORDS = 1000  # Number of records to process

# Results storage
results = {
    'insert': {'pooling': [], 'no_pooling': []},
    'update': {'pooling': [], 'no_pooling': []},
    'read': {'pooling': [], 'no_pooling': []}
}

def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        DROP TABLE IF EXISTS benchmark_table;
        CREATE TABLE benchmark_table (
            id SERIAL PRIMARY KEY,
            data TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_records(conn_pool, num_records):
    def worker():
        if conn_pool:
            conn = conn_pool.getconn()
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for _ in range(num_records):
            cur.execute("INSERT INTO benchmark_table (data) VALUES ('Test data');")
        conn.commit()
        cur.close()
        if conn_pool:
            conn_pool.putconn(conn)
        else:
            conn.close()
    threads = []
    start_time = time.time()
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return time.time() - start_time

def update_records(conn_pool, num_records):
    def worker():
        if conn_pool:
            conn = conn_pool.getconn()
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for i in range(1, num_records + 1):
            cur.execute("UPDATE benchmark_table SET data = 'Updated data' WHERE id = %s;", (i,))
        conn.commit()
        cur.close()
        if conn_pool:
            conn_pool.putconn(conn)
        else:
            conn.close()
    threads = []
    start_time = time.time()
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return time.time() - start_time

def read_records(conn_pool, num_records):
    def worker():
        if conn_pool:
            conn = conn_pool.getconn()
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for i in range(1, num_records + 1):
            cur.execute("SELECT * FROM benchmark_table WHERE id = %s;", (i,))
            cur.fetchone()
        cur.close()
        if conn_pool:
            conn_pool.putconn(conn)
        else:
            conn.close()
    threads = []
    start_time = time.time()
    for _ in range(THREADS):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return time.time() - start_time

def benchmark():
    for pool_size in POOL_SIZES:
        print(f"\nBenchmarking with pool size: {pool_size}")
        
        # Connection Pooling
        print("Testing with connection pooling...")
        benchmark_with_pooling(pool_size)
        
        # No Connection Pooling
        print("Testing without connection pooling...")
        benchmark_without_pooling()

def benchmark_with_pooling(pool_size):
    conn_pool = psycopg2.pool.ThreadedConnectionPool(THREADS, pool_size, **DB_CONFIG)
    run_benchmark(conn_pool, 'pooling')
    conn_pool.closeall()

def benchmark_without_pooling():
    # We won't use a connection pool here
    run_benchmark(None, 'no_pooling')

def run_benchmark(conn_pool, scenario):
    create_table()
    
    # Insert Benchmark
    insert_time = insert_records(conn_pool, NUM_RECORDS)
    results['insert'][scenario].append(insert_time)
    print(f"{scenario.capitalize()} Insert Time: {insert_time:.2f}s")
    
    # Update Benchmark
    update_time = update_records(conn_pool, NUM_RECORDS)
    results['update'][scenario].append(update_time)
    print(f"{scenario.capitalize()} Update Time: {update_time:.2f}s")
    
    # Read Benchmark
    read_time = read_records(conn_pool, NUM_RECORDS)
    results['read'][scenario].append(read_time)
    print(f"{scenario.capitalize()} Read Time: {read_time:.2f}s")

def visualize():
    for op in OPERATIONS:
        plt.figure()
        for scenario in ['pooling', 'no_pooling']:
            plt.plot(POOL_SIZES, results[op][scenario], marker='o', label=scenario.capitalize())
        plt.title(f'{NUM_RECORDS} rows {op.capitalize()} Performance')
        plt.xlabel('Connection Pool Size')
        plt.ylabel('Time (seconds)')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    benchmark()
    visualize()
