# Record Queue

`record_queue` is the finished reference artifact for the Library Forge. It is a fixed-capacity, allocation-free FIFO for timestamped integer records. Its public object provides aligned private storage, so consumers can allocate deterministically without coupling to ring indices or record layout.

The queue rejects new records when full, preserves FIFO order across index wrap, returns explicit status values, and is usable from C or C++. Build with `make test`, or install with CMake and consume the exported `Learn::record_queue` target.
