# DDIA Transactions

Transactions are an abtraction layer that allows an application to pretend that certain concurrency problems and certain kinds of hardware and software faults dont' exit. A large class of errors is reduced down to a simple *transaction abort*, and the application just need to try again.

## Examples of Race Conditions

### Dirty reads
One client reads another clients' writes before they have been committed. The read committed isolation level and stronger levels prevent dirty reads.

### Dirty writes
One client overwrites data that another client has written, but not yet committed. Almost all transaction implementations prevent dirty writes.

### Read skew
A client sees different parts of the database at different points in time. Some cases of read skew are also know as nonrepeatable reads. This issues is most commonly prevented with snapshot isolation, which allows a transaction to read from a consistent snapshot corresponding to one particular point in time. It is usually implemented with multi-version concurrency control (MVCC).

### Lost updates
Two clients concurrently perform a read-modify-write cycle. One overwiretes the other's write without incorporating its changes, so data is lost. Some implementations of snapshot isolation prevent this anomaly automatically, while others require a manual lock (`SELECT FOR UPDATE`).

### Write skew
A transactions reads something, makes a decision based on the value it saw, and writes the decision to the database. However by the time the write is made, the premise of the decision is no longer true. Only serializable isolation prevents this anomaly.

### Phantom reads
A transaction reads objects that match some search condition. Another client makes a write that affects the results of that search. Snapshot isolation prevents straighforward phantom reads, but phantoms in the context of write skew required special treatment, such as index-range locks.