## This is a simplified, multithreaded Redis-like key-value store server built in Python. It uses the RESP (REdis Serialization Protocol) format to handle common Redis commands like `PING`, `ECHO`, `SET`, and `GET`, and supports key expiration using the `PX` flag.

## 🚀 Features

- RESP protocol parsing (compatible with Redis CLI)
- In-memory key-value storage with optional TTL expiration
- Supports basic Redis commands:
  - `PING`: Responds with `PONG`
  - `ECHO <message>`: Returns the message
  - `SET <key> <value> [PX <ms>]`: Stores key with optional expiration (in milliseconds)
  - `GET <key>`: Retrieves value or returns null if expired/missing
- Multithreaded handling of multiple client connections
- Socket server running on `localhost:6379` (default Redis port)

---

## ⚙️ How It Works

### RESP Parsing

The server accepts input in RESP format (used by the Redis CLI and drivers):

\*2\r\n$4\r\nECHO\r\n$6\r\norange\r\n

This would be parsed and interpreted as:

ECHO orange

### Key Expiration

Keys set with the `PX` option are stored with:

- Expiration time (in ms)
- Timestamp of insertion

On every `GET`, the server checks whether the key has expired before returning a value.

---

## 🏗️ Architecture

- `main()`: Starts the server and listens for new connections.
- `handle_client()`: Handles client commands in a new thread.
- `parse_resp()`: Parses RESP-formatted data into commands.
- `Value`: A simple class to track value, expiration time, and timestamp.
- `set_key()`, `get_val()`, `echo()`, `pong()`: Command implementations.

---

## 📦 Requirements

- Python 3.8+
- No external dependencies

---

## 🧪 Example Usage

Once running, you can connect to your server via netcat or the Redis CLI:

### With netcat:

```bash
nc localhost 6379


This is a simplified version of Redis and is not optimized for production use.

All data is stored in-memory and is lost on shutdown.

Key expiration is checked only on access, not through background cleanup.
```
