import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Example preprocessed wiki documents keyed by repo URL.
# In production this would live in a database or cache layer populated by
# offline analysis jobs.
PREPROCESSED_WIKIS = {
    "https://github.com/facebook/rocksdb": {
        "meta": {
            "name": "RocksDB",
            "repo_url": "https://github.com/facebook/rocksdb",
            "language": ["C++", "C"],
            "last_indexed_iso": "2024-02-01T12:00:00Z",
            "maintainers": [
                {"name": "Storage Team", "contact": "storage@example.com"}
            ],
        },
        "summary": {
            "one_liner": "Embedded persistent key-value store optimized for fast storage.",
            "problem_solved": [
                "Low-latency reads/writes on fast storage hardware",
                "Configurable trade-offs between throughput, latency, and space",
                "Pluggable compaction and IO primitives for specialized workloads",
            ],
            "architecture_overview": (
                "Log-structured merge-tree (LSM) engine with layered caches and pluggable "
                "filesystems. Core abstractions: Env (IO), Table Formats (SST), "
                "MemTable (in-memory), VersionSet (manifest), and Compaction."
            ),
        },
        "architecture": {
            "components": [
                {
                    "id": "api",
                    "label": "Public API",
                    "description": "DB, ColumnFamilyHandle, Options; entrypoint for users.",
                },
                {
                    "id": "write_path",
                    "label": "Write Path",
                    "description": "WriteBatch -> MemTable -> WAL; optional two-phase write.",
                },
                {
                    "id": "read_path",
                    "label": "Read Path",
                    "description": "MemTable + BlockCache + SSTables resolved via VersionSet.",
                },
                {
                    "id": "storage",
                    "label": "Storage",
                    "description": "SST files, MANIFEST, WAL on Env (posix, HDFS, custom).",
                },
                {
                    "id": "compaction",
                    "label": "Compaction",
                    "description": "Level, universal, FIFO strategies merge sorted runs.",
                },
                {
                    "id": "services",
                    "label": "Background Services",
                    "description": "Flush, compaction, rate limiting, IO throttling.",
                },
            ],
            "edges": [
                {"source": "api", "target": "write_path", "label": "writes"},
                {"source": "api", "target": "read_path", "label": "reads"},
                {"source": "write_path", "target": "storage", "label": "persists"},
                {"source": "read_path", "target": "storage", "label": "fetches"},
                {"source": "storage", "target": "compaction", "label": "inputs"},
                {"source": "compaction", "target": "storage", "label": "rewrites"},
                {"source": "services", "target": "compaction", "label": "schedules"},
            ],
            "callouts": [
                {
                    "title": "Performance levers",
                    "bullets": [
                        "Block cache size and bloom filters",
                        "Compaction strategy per column family",
                        "MemTable type (skiplist vs hash) and size",
                    ],
                }
            ],
        },
        "workflows": [
            {
                "name": "Write flow",
                "steps": [
                    "Client issues WriteBatch via DB::Write with options.",
                    "Batch appended to WAL (Env) then inserted into active MemTable.",
                    "MemTable marked immutable when full and queued for flush.",
                    "Flush job writes SSTable (table builder) and updates MANIFEST.",
                ],
            },
            {
                "name": "Read flow",
                "steps": [
                    "Lookup hits MemTable/Immutable MemTables first.",
                    "Block cache checked; on miss, table reader loads SST block.",
                    "Iterators merge multiple table levels via VersionSet.",
                ],
            },
            {
                "name": "Compaction flow",
                "steps": [
                    "Background trigger based on level size or manual request.",
                    "Input SSTables read, merged, filtered (tombstones), rewritten.",
                    "Manifest updated; old files scheduled for deletion.",
                ],
            },
        ],
        "modules": [
            {
                "path": "db/db_impl.cc",
                "role": "Core DB implementation; coordinates reads/writes and background jobs.",
                "owner": "storage-runtime",
                "risky_changes": [
                    "Threading and mutex ordering",
                    "WAL durability guarantees",
                    "Interactions with flush/compaction scheduling",
                ],
            },
            {
                "path": "db/version_set.cc",
                "role": "Tracks live SSTables and manifests; surfaces iterators per level.",
                "owner": "storage-runtime",
                "risky_changes": ["Manifest corruption", "Iterator invalidation"],
            },
            {
                "path": "table/block_based_table_reader.cc",
                "role": "Reads SSTable blocks, handles caching and bloom filters.",
                "owner": "storage-io",
                "risky_changes": ["Cache interaction", "Bloom filter correctness"],
            },
            {
                "path": "compaction/compaction_job.cc",
                "role": "Executes compaction strategies and file rewrites.",
                "owner": "storage-runtime",
                "risky_changes": ["File lifecycle", "Performance regressions"],
            },
        ],
        "operational_readiness": {
            "metrics": [
                {"name": "rocksdb_compaction_pending", "why": "Backlog signals IO pressure"},
                {"name": "rocksdb_memtable_flush_pending", "why": "Write stall predictor"},
                {"name": "rocksdb_block_cache_hit", "why": "Read efficiency"},
            ],
            "runbooks": [
                {
                    "title": "Write stalls",
                    "summary": "Reduce ingest rate; increase memtable/level size; tune compaction.",
                },
                {
                    "title": "High read latency",
                    "summary": "Increase block cache; enable bloom filters; verify Env IO latency.",
                },
            ],
        },
        "getting_started": {
            "dev_setup": [
                "Install dependencies: snappy/zlib/bzip2/lz4/zstd",
                "Build: `cmake -S . -B build && cmake --build build`",
                "Tests: `ctest --test-dir build`",
            ],
            "sample_usage": (
                "DB* db; Options opts; opts.create_if_missing = true; "
                'Status s = DB::Open(opts, "/tmp/testdb", &db);'
            ),
        },
        "faq": [
            {
                "q": "When to use universal compaction?",
                "a": "Use for high-update or time-series workloads needing low read amp.",
            },
            {
                "q": "How to limit write stalls?",
                "a": "Tune level sizes and compaction threads; monitor L0 file count.",
            },
        ],
    }
}


@app.get("/api/getCodeBaseSummary")
def get_code_base_summary():
    codebase_url = request.args.get("codebase_url")
    if not codebase_url:
        return jsonify({"error": "missing codebase_url"}), 400

    wiki = PREPROCESSED_WIKIS.get(codebase_url)
    if not wiki:
        return jsonify({"error": "codebase not indexed"}), 404

    return jsonify({"wiki": wiki})


@app.get("/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
