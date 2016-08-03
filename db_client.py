import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(
        "postgres://coxqszruxmxpxl:wYLXsDdRyZHsugy6fnYVMyc_xl@ec2-23-21-179-195.compute-1.amazonaws.com:5432/d74vv6iktq05gk")

select_query = 'SELECT bits FROM FishBucket ORDER BY timestamp ASC LIMIT 1;'
delete_query = 'DELETE FROM FishBucket WHERE bits IN (SELECT bits FROM FishBucket ORDER BY timestamp ASC LIMIT 1);'

try:
    connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
    )
    # print connection
    current = connection.cursor()

    current.execute(select_query)
    row = current.fetchone()
    if row is not None:
        gotcha = row[0]
        current.execute(delete_query)
        print gotcha
    else:
        print 'empty db'

    # for row in rows:
    #     print row[0]

    connection.commit()
    connection.close()
except:
    print "I am unable to connect to the database"


# FIFO Queue structure, for postGreSQL db management

# query for retrieval / removal (reads/removes from the head)
"""
select bits from FishBucket order by timestamp asc limit 1;
delete from FishBucket where bits in (select bits from FishBucket order by timestamp asc limit 1);
"""

# query for insert (inserts at the tail)
"""
INSERT INTO FishBucket (bits) VALUES('1111');
"""

# table schema
"""
Create table FishBucket(bits varbit(83886080), time timestamp default now);
"""