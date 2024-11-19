
# PostgreSQL Connection Pooling vs No Pooling: Benchmark Analysis

This repository provides a detailed benchmark analysis comparing PostgreSQL performance using **connection pooling** versus **no pooling** under various workloads. The benchmarking script evaluates common database operations—**INSERT**, **READ**, and **UPDATE**—across different connection pool sizes and row counts.


## **Table of Contents**
- [Introduction](#introduction)
- [Setup Instructions](#setup-instructions)
- [Benchmark Script Overview](#benchmark-script-overview)
- [Conclusion](#conclusion)
- [License](#license)


## **Introduction**

Connection pooling is a technique to optimize database performance by reusing connections, reducing the overhead of creating new connections for every query. This project benchmarks the performance impact of connection pooling versus no pooling using PostgreSQL under different scenarios:

- **Row Counts**: 100, 1000, and 10000 rows.
- **Connection Pool Sizes**: 5, 10, 20, 50.
- **Operations**: INSERT, READ, and UPDATE.



## **Setup Instructions**

1. **Install Dependencies**:
   Ensure you have Python and PostgreSQL installed. Install the required Python packages:
   ```bash
   pip install psycopg2-binary matplotlib
   ```

2. **Configure PostgreSQL**:
   - Create a database and user for the benchmark:
     ```sql
     CREATE DATABASE benchmark_db;
     CREATE USER benchmark_user WITH PASSWORD 'password';
     GRANT ALL PRIVILEGES ON DATABASE benchmark_db TO benchmark_user;
     ```

3. **Set Database Configuration**:
   Update the `DB_CONFIG` dictionary in the script with your database credentials:
   ```python
   DB_CONFIG = {
       'database': 'benchmark_db',
       'user': 'benchmark_user',
       'password': 'password',
       'host': 'localhost',
       'port': '5432'
   }
   ```

4. **Run the Benchmark**:
   Execute the script to generate results and graphs:
   ```bash
   python benchmark_script.py
   ```


## **Benchmark Script Overview**

The script simulates concurrency with threads and evaluates the performance of three common database operations:
- **INSERT**: Adding new rows to the database.
- **READ**: Fetching rows from the database.
- **UPDATE**: Modifying existing rows in the database.

### Script Features:
- Measures execution time for operations with and without connection pooling.
- Benchmarks different connection pool sizes and row counts.
- Generates performance graphs for each scenario.


## **Conclusion**

- Connection pooling is highly beneficial, significantly reducing connection overhead.
- For larger workloads, careful tuning of the connection pool size is essential to avoid contention and maximize performance.
- **Recommendation**: Use connection pooling for most workloads, but monitor and optimize pool settings for high-concurrency environments.


## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.


Complete article can be found here: [Postgres Connection Pooling vs No Pooling: Benchmark Analysis]()

