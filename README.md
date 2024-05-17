# Logging-System

This Logging system has 2 components 

### Ingesting logs:

  Choice of DataBase and why?
  I chose to use a NoSQL database such as MongoDB due to the following reasons
  #### Schema Flexibility: 
Logs don't necessarily follow a specific schema in all cases. The structure of log entries can vary depending on factors such as the logging framework being used, the preferences of the developers, and the specific requirements of the application, which makes schema-independent databases the best choice for use cases like these.
  #### Scalibility: 
MongoDB can scale horizontally, making them well-suited for handling large volumes of log data in distributed environments. MongoDB, in particular, supports sharding, which enables data partitioning across multiple servers to handle increasing data volumes and read/write operations.
to facilitate efficient search and distribute the data 
  #### Performance:
 MongoDb is optimized for high performance and can efficiently handle write-heavy workloads, which are typical in logging scenarios where large volumes of log entries are generated continuously.
  #### Fault tolerance:
 Mechanisms such as replication and automatic failover helps the MongoDB database system to automatically recover and ensure data availability, which is critical for preserving log data integrity and continuity.


### Query Interface

For efficient and quicker search based on log levels, I have stored logs of different levels in different MongoDB collections, reducing the search space significantly

