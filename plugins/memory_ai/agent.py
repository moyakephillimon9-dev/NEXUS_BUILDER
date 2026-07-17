"""
NEXUS Builder
Memory AI — Enterprise Knowledge Engine

Module ID : MEMORY-001
Version   : 4.0.0
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import shutil
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Optional performance upgrade
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("NEXUS.MemoryAI")


# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------

DATABASE_VERSION = "4.0.0"


# ---------------------------------------------------------
# MEMORY CATEGORIES
# ---------------------------------------------------------

class MemoryCategory(str, Enum):

    PROJECT = "projects"

    ARCHITECTURE = "architectures"

    CODE_PATTERN = "patterns"

    FAILURE = "failures"

    SUCCESS = "best_practices"

    SECURITY = "security"

    PERFORMANCE = "performance"

    DOCUMENTATION = "documentation"

    DEPLOYMENT = "deployment"


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

@dataclass(slots=True)
class MemoryConfig:

    database_path: str = "memory/nexus_memory.json"

    backup_directory: str = "memory/backups"

    snapshot_directory: str = "memory/snapshots"

    backup_retention_days: int = 7

    autosave_interval: int = 60

    maximum_backups: int = 100

    enable_compression: bool = False

    enable_integrity_check: bool = True


# ---------------------------------------------------------
# MEMORY RECORD
# ---------------------------------------------------------

@dataclass(slots=True)
class MemoryRecord:

    record_id: str

    category: MemoryCategory

    title: str

    payload: Dict[str, Any]

    tags: List[str] = field(default_factory=list)

    author: str = "SYSTEM"

    created_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    modified_at: str = field(
        default_factory=lambda:
        datetime.now(timezone.utc).isoformat()
    )

    checksum: Optional[str] = None

    embedding: Optional[List[float]] = None


# ---------------------------------------------------------
# MEMORY AI
# ---------------------------------------------------------

class MemoryAI:

    """
    Enterprise Knowledge Engine

    Responsibilities

    • Persistent Knowledge

    • Learning

    • Search

    • Snapshots

    • Backups

    • Metrics

    • Atomic Transactions

    • High-speed Cache
    """

    def __init__(

        self,

        shared_memory,

        config: MemoryConfig | None = None

    ):

        self.shared_memory = shared_memory

        self.config = config or MemoryConfig()

        self.database = Path(self.config.database_path)

        self.backups = Path(self.config.backup_directory)

        self.snapshots = Path(self.config.snapshot_directory)

        self._lock = asyncio.Lock()

        self._cache: Dict[str, Any] = {}

        self.metrics = {

            "reads": 0,

            "writes": 0,

            "queries": 0,

            "cache_hits": 0,

            "cache_misses": 0,

            "rollbacks": 0,

            "snapshots": 0,

            "uptime_started": time.time()
        }

        self.indexes = {

            "tags": {},

            "categories": {},

            "titles": {}
        }

        self._bootstrap()

        logger.info("Memory AI initialized successfully.")

    # ---------------------------------------------------------
    # BOOTSTRAP
    # ---------------------------------------------------------

    def _bootstrap(self):

        """
        Creates required folders, initializes the database,
        loads cache, rebuilds indexes and verifies integrity.
        """

        self.database.parent.mkdir(parents=True, exist_ok=True)

        self.backups.mkdir(parents=True, exist_ok=True)

        self.snapshots.mkdir(parents=True, exist_ok=True)

        if not self.database.exists():

            logger.info("Creating new enterprise memory database...")

            initial_database = {

                "system": {

                    "database_version": DATABASE_VERSION,

                    "created_at": datetime.now(
                        timezone.utc
                    ).isoformat(),

                    "last_checkpoint": datetime.now(
                        timezone.utc
                    ).isoformat(),

                    "checksum": None

                },

                "records": {

                    category.value: {}

                    for category in MemoryCategory

                }

            }

            initial_database["system"]["checksum"] = \
                self._calculate_checksum(initial_database)

            with open(
                self.database,
                "w",
                encoding="utf-8"
            ) as fp:

                json.dump(
                    initial_database,
                    fp,
                    indent=4
                )

        self._load_database()

        self._rebuild_indexes()

        logger.info("Enterprise Memory Database Ready.")


    # ---------------------------------------------------------
    # DATABASE LOADER
    # ---------------------------------------------------------

    def _load_database(self):

        with open(

            self.database,

            "r",

            encoding="utf-8"

        ) as fp:

            self._cache = json.load(fp)

        if self.config.enable_integrity_check:

            self._verify_integrity()


    # ---------------------------------------------------------
    # CHECKSUM
    # ---------------------------------------------------------

    def _verify_integrity(self):

        expected = self._cache["system"].get("checksum")

        tmp = json.loads(json.dumps(self._cache))

        tmp["system"]["checksum"] = None

        actual = self._calculate_checksum(tmp)

        if expected != actual:

            logger.warning(

                "Database checksum mismatch detected."

            )

        else:

            logger.info(

                "Database integrity verified."

            )


    def _calculate_checksum(

        self,

        data

    ):

        serialized = json.dumps(

            data,

            sort_keys=True

        ).encode()

        return hashlib.sha256(

            serialized

        ).hexdigest()


    # ---------------------------------------------------------
    # INDEX ENGINE
    # ---------------------------------------------------------

    def _rebuild_indexes(self):

        self.indexes = {

            "tags": {},

            "categories": {},

            "titles": {}

        }

        for category_name, bucket in \

                self._cache["records"].items():

            for record_id, record in bucket.items():

                self.indexes["categories"] \
                    .setdefault(

                        category_name,

                        set()

                    ).add(record_id)

                self.indexes["titles"][

                    record["title"].lower()

                ] = record_id

                for tag in record.get(

                    "tags",

                    []

                ):

                    self.indexes["tags"] \
                        .setdefault(

                            tag.lower(),

                            set()

                        ).add(record_id)

        logger.info(

            "Indexes rebuilt successfully."

        )

    # ---------------------------------------------------------
    # ATOMIC WRITE ENGINE
    # ---------------------------------------------------------

    async def _atomic_commit(self):
        """
        Enterprise ACID-style commit.

        Workflow
        --------
        1. Update checkpoint
        2. Recalculate checksum
        3. Write temporary database
        4. Backup current database
        5. Atomically replace database
        6. Rollback automatically on failure
        """

        async with self._lock:

            temporary_database = self.database.with_suffix(".tmp")

            try:

                self._cache["system"]["last_checkpoint"] = (
                    datetime.now(timezone.utc).isoformat()
                )

                # Refresh checksum
                working_copy = json.loads(json.dumps(self._cache))
                working_copy["system"]["checksum"] = None

                checksum = self._calculate_checksum(working_copy)

                self._cache["system"]["checksum"] = checksum

                loop = asyncio.get_running_loop()

                await loop.run_in_executor(

                    None,

                    self._write_database,

                    temporary_database,

                    self._cache

                )

                self._create_backup()

                os.replace(
                    temporary_database,
                    self.database
                )

                self.metrics["writes"] += 1

                logger.info("Atomic commit successful.")

            except Exception as exc:

                self.metrics["rollbacks"] += 1

                logger.error(
                    "Atomic commit failed. Restoring database."
                )

                if temporary_database.exists():
                    temporary_database.unlink()

                self._restore_latest_backup()

                raise RuntimeError(
                    f"Commit failure: {exc}"
                )


    # ---------------------------------------------------------
    # LOW LEVEL WRITER
    # ---------------------------------------------------------

    @staticmethod
    def _write_database(path: Path, payload: dict):

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                payload,
                file,
                indent=4,
                ensure_ascii=False
            )


    # ---------------------------------------------------------
    # BACKUP ENGINE
    # ---------------------------------------------------------

    def _create_backup(self):

        if not self.database.exists():
            return

        backup_name = (
            f"backup_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        destination = self.backups / backup_name

        shutil.copy2(
            self.database,
            destination
        )

        logger.info(
            f"Backup created -> {destination.name}"
        )

        self._cleanup_old_backups()


    # ---------------------------------------------------------
    # BACKUP RETENTION
    # ---------------------------------------------------------

    def _cleanup_old_backups(self):

        backups = sorted(

            self.backups.glob("*.json"),

            key=lambda x: x.stat().st_mtime,

            reverse=True

        )

        if len(backups) <= self.config.maximum_backups:
            return

        for file in backups[self.config.maximum_backups:]:

            try:

                file.unlink()

                logger.info(
                    f"Old backup removed -> {file.name}"
                )

            except Exception:

                pass


    # ---------------------------------------------------------
    # RESTORE
    # ---------------------------------------------------------

    def _restore_latest_backup(self):

        backups = sorted(

            self.backups.glob("*.json"),

            key=lambda x: x.stat().st_mtime,

            reverse=True

        )

        if not backups:

            logger.critical(
                "No backup available for restoration."
            )

            return

        shutil.copy2(
            backups[0],
            self.database
        )

        self._load_database()

        logger.info(
            "Latest backup restored successfully."
        )


    # ---------------------------------------------------------
    # SNAPSHOT ENGINE
    # ---------------------------------------------------------

    async def create_snapshot(self):

        snapshot_name = (
            f"snapshot_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        snapshot_path = self.snapshots / snapshot_name

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(

            None,

            self._write_database,

            snapshot_path,

            self._cache

        )

        self.metrics["snapshots"] += 1

        logger.info(
            f"Snapshot saved -> {snapshot_name}"
        )

    # ---------------------------------------------------------
    # RECORD VALIDATION
    # ---------------------------------------------------------

    def _validate_record(self, record: MemoryRecord):

        if not record.record_id:
            raise ValueError("record_id cannot be empty.")

        if not record.title:
            raise ValueError("title cannot be empty.")

        if not isinstance(record.payload, dict):
            raise TypeError("payload must be a dictionary.")

        if not isinstance(record.tags, list):
            raise TypeError("tags must be a list.")

        return True


    # ---------------------------------------------------------
    # STORE RECORD
    # ---------------------------------------------------------

    async def commit_record(self, record: MemoryRecord):

        self._validate_record(record)

        record.modified_at = datetime.now(
            timezone.utc
        ).isoformat()

        record.checksum = hashlib.sha256(

            json.dumps(
                record.payload,
                sort_keys=True
            ).encode()

        ).hexdigest()

        category = record.category.value

        self._cache["records"][category][
            record.record_id
        ] = asdict(record)

        self._index_record(record)

        await self._atomic_commit()

        logger.info(
            f"Record stored -> {record.record_id}"
        )


    # ---------------------------------------------------------
    # UPDATE RECORD
    # ---------------------------------------------------------

    async def update_record(

        self,

        record_id: str,

        category: MemoryCategory,

        updates: Dict[str, Any]

    ):

        bucket = self._cache["records"][
            category.value
        ]

        if record_id not in bucket:
            raise KeyError(record_id)

        bucket[record_id].update(updates)

        bucket[record_id]["modified_at"] = (

            datetime.now(timezone.utc).isoformat()

        )

        await self._atomic_commit()

        self._rebuild_indexes()

        logger.info(
            f"Record updated -> {record_id}"
        )


    # ---------------------------------------------------------
    # DELETE RECORD
    # ---------------------------------------------------------

    async def delete_record(

        self,

        record_id: str,

        category: MemoryCategory

    ):

        bucket = self._cache["records"][
            category.value
        ]

        if record_id not in bucket:
            return

        del bucket[record_id]

        await self._atomic_commit()

        self._rebuild_indexes()

        logger.info(
            f"Record deleted -> {record_id}"
        )


    # ---------------------------------------------------------
    # INDEX RECORD
    # ---------------------------------------------------------

    def _index_record(self, record: MemoryRecord):

        category = record.category.value

        self.indexes["categories"] \
            .setdefault(category, set()) \
            .add(record.record_id)

        self.indexes["titles"][
            record.title.lower()
        ] = record.record_id

        for tag in record.tags:

            self.indexes["tags"] \
                .setdefault(
                    tag.lower(),
                    set()
                ) \
                .add(record.record_id)


    # ---------------------------------------------------------
    # FETCH RECORD
    # ---------------------------------------------------------

    async def get_record(

        self,

        category: MemoryCategory,

        record_id: str

    ) -> Optional[dict]:

        self.metrics["reads"] += 1

        bucket = self._cache["records"][
            category.value
        ]

        if record_id in bucket:

            self.metrics["cache_hits"] += 1

            return bucket[record_id]

        self.metrics["cache_misses"] += 1

        return None


    # ---------------------------------------------------------
    # RECORD EXISTS
    # ---------------------------------------------------------

    async def exists(

        self,

        category: MemoryCategory,

        record_id: str

    ) -> bool:

        return record_id in self._cache[
            "records"
        ][
            category.value
        ]

    # ---------------------------------------------------------
    # SEARCH BY TAG
    # ---------------------------------------------------------

    async def query_by_tag(

        self,

        tag: str

    ) -> List[dict]:

        self.metrics["queries"] += 1

        tag = tag.lower()

        results = []

        record_ids = self.indexes["tags"].get(tag, set())

        for category in self._cache["records"].values():

            for record_id in record_ids:

                if record_id in category:

                    results.append(category[record_id])

        return results


    # ---------------------------------------------------------
    # SEARCH BY CATEGORY
    # ---------------------------------------------------------

    async def query_category(

        self,

        category: MemoryCategory

    ) -> List[dict]:

        self.metrics["queries"] += 1

        return list(

            self._cache["records"][

                category.value

            ].values()

        )


    # ---------------------------------------------------------
    # SEARCH TITLE
    # ---------------------------------------------------------

    async def search_title(

        self,

        keyword: str

    ) -> List[dict]:

        self.metrics["queries"] += 1

        keyword = keyword.lower()

        results = []

        for bucket in self._cache["records"].values():

            for record in bucket.values():

                if keyword in record["title"].lower():

                    results.append(record)

        return results


    # ---------------------------------------------------------
    # FULL TEXT SEARCH
    # ---------------------------------------------------------

    async def search(

        self,

        text: str

    ) -> List[dict]:

        self.metrics["queries"] += 1

        text = text.lower()

        results = []

        for bucket in self._cache["records"].values():

            for record in bucket.values():

                searchable = json.dumps(

                    record,

                    ensure_ascii=False

                ).lower()

                if text in searchable:

                    results.append(record)

        return results


    # ---------------------------------------------------------
    # FILTER RECORDS
    # ---------------------------------------------------------

    async def filter(

        self,

        category: MemoryCategory | None = None,

        author: str | None = None,

        tag: str | None = None

    ) -> List[dict]:

        self.metrics["queries"] += 1

        results = []

        buckets = []

        if category:

            buckets.append(

                self._cache["records"][

                    category.value

                ]

            )

        else:

            buckets = self._cache["records"].values()

        for bucket in buckets:

            for record in bucket.values():

                if author:

                    if record["author"] != author:

                        continue

                if tag:

                    if tag not in record["tags"]:

                        continue

                results.append(record)

        return results


    # ---------------------------------------------------------
    # DATABASE STATISTICS
    # ---------------------------------------------------------

    async def statistics(self):

        total_records = 0

        category_breakdown = {}

        for category in MemoryCategory:

            count = len(

                self._cache["records"][

                    category.value

                ]

            )

            category_breakdown[category.value] = count

            total_records += count

        return {

            "database_version": DATABASE_VERSION,

            "total_records": total_records,

            "categories": category_breakdown,

            "reads": self.metrics["reads"],

            "writes": self.metrics["writes"],

            "queries": self.metrics["queries"],

            "cache_hits": self.metrics["cache_hits"],

            "cache_misses": self.metrics["cache_misses"],

            "rollbacks": self.metrics["rollbacks"],

            "snapshots": self.metrics["snapshots"]

        }


    # ---------------------------------------------------------
    # HEALTH REPORT
    # ---------------------------------------------------------

    async def health(self):

        uptime = int(

            time.time()

            -

            self.metrics["uptime_started"]

        )

        stats = await self.statistics()

        stats["uptime_seconds"] = uptime

        stats["database_file"] = str(self.database)

        stats["backup_directory"] = str(self.backups)

        stats["snapshot_directory"] = str(self.snapshots)

        stats["status"] = "HEALTHY"

        return stats

    # ---------------------------------------------------------
    # BACKGROUND MAINTENANCE
    # ---------------------------------------------------------

    async def start(self):
        """
        Starts all enterprise background services.
        """

        logger.info("Enterprise Memory Engine Online.")

        asyncio.create_task(self._autosave_loop())
        asyncio.create_task(self._snapshot_loop())
        asyncio.create_task(self._maintenance_loop())


    # ---------------------------------------------------------
    # AUTOSAVE LOOP
    # ---------------------------------------------------------

    async def _autosave_loop(self):

        while True:

            try:

                await asyncio.sleep(
                    self.config.autosave_interval
                )

                await self._atomic_commit()

                logger.info(
                    "Automatic checkpoint completed."
                )

            except Exception as exc:

                logger.error(
                    f"Autosave failed: {exc}"
                )


    # ---------------------------------------------------------
    # SNAPSHOT LOOP
    # ---------------------------------------------------------

    async def _snapshot_loop(self):

        while True:

            try:

                await asyncio.sleep(3600)

                await self.create_snapshot()

            except Exception as exc:

                logger.error(
                    f"Snapshot creation failed: {exc}"
                )


    # ---------------------------------------------------------
    # MAINTENANCE LOOP
    # ---------------------------------------------------------

    async def _maintenance_loop(self):

        while True:

            try:

                await asyncio.sleep(86400)

                self._cleanup_old_backups()

                self._optimize_indexes()

                logger.info(
                    "Daily maintenance completed."
                )

            except Exception as exc:

                logger.error(
                    f"Maintenance failed: {exc}"
                )


    # ---------------------------------------------------------
    # INDEX OPTIMIZATION
    # ---------------------------------------------------------

    def _optimize_indexes(self):

        self._rebuild_indexes()

        logger.info(
            "Indexes optimized."
        )


    # ---------------------------------------------------------
    # DATABASE EXPORT
    # ---------------------------------------------------------

    async def export_database(
        self,
        destination: str
    ):

        destination = Path(destination)

        shutil.copy2(
            self.database,
            destination
        )

        logger.info(
            f"Database exported -> {destination}"
        )


    # ---------------------------------------------------------
    # DATABASE IMPORT
    # ---------------------------------------------------------

    async def import_database(
        self,
        source: str
    ):

        source = Path(source)

        if not source.exists():

            raise FileNotFoundError(source)

        shutil.copy2(
            source,
            self.database
        )

        self._load_database()

        self._rebuild_indexes()

        logger.info(
            "Database imported successfully."
        )


    # ---------------------------------------------------------
    # RESET CACHE
    # ---------------------------------------------------------

    async def clear_cache(self):

        self._cache.clear()

        self.indexes = {
            "tags": {},
            "categories": {},
            "titles": {}
        }

        self._load_database()

        self._rebuild_indexes()

        logger.info(
            "Memory cache refreshed."
        )


    # ---------------------------------------------------------
    # SHUTDOWN
    # ---------------------------------------------------------

    async def shutdown(self):

        logger.info(
            "Saving final checkpoint..."
        )

        await self._atomic_commit()

        logger.info(
            "Enterprise Memory Engine Offline."
        )


# ==========================================================
# END OF ENTERPRISE MEMORY AI v4.0
# ==========================================================
