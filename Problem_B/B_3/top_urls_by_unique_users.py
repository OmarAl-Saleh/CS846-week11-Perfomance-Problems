from __future__ import annotations

import argparse
import random
import tempfile
import time
import tracemalloc
from collections import defaultdict
from pathlib import Path


def generate_log_file(path: Path, num_events: int = 2_000_000) -> None:
    rng = random.Random(42)
    urls = [f"/product/{i}" for i in range(5000)]

    with path.open("w", encoding="utf-8") as f:
        for _ in range(num_events):
            user_id = rng.randint(1, 400_000)
            url = urls[rng.randint(0, len(urls) - 1)]
            f.write(f"{user_id},{url}\n")


def top_urls_by_unique_users(path: Path, top_k: int = 100) -> list[tuple[str, int]]:
    users_per_url: dict[str, set[int]] = defaultdict(set)

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            user_id_text, url = line.rstrip("\n").split(",", 1)
            users_per_url[url].add(int(user_id_text))

    counts = [(url, len(users)) for url, users in users_per_url.items()]
    counts.sort(key=lambda item: item[1], reverse=True)
    return counts[:top_k]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-events", type=int, default=2_000_000)
    parser.add_argument("--top-k", type=int, default=100)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "events.csv"
        generate_log_file(path, num_events=args.num_events)

        tracemalloc.start()
        t0_wall = time.perf_counter()
        t0_cpu = time.process_time()
        result = top_urls_by_unique_users(path, top_k=args.top_k)
        t1_cpu = time.process_time()
        t1_wall = time.perf_counter()
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed_wall = t1_wall - t0_wall
        elapsed_cpu = t1_cpu - t0_cpu
        events_per_sec = (args.num_events / elapsed_wall) if elapsed_wall > 0 else float("inf")
        peak_mb = peak / (1024 * 1024)

        print(f"Computed top {len(result)} URLs in {elapsed_wall:.3f}s")
        print(result[:5])
        print(f"cpu_seconds={elapsed_cpu:.3f}")
        print(f"events_per_sec={events_per_sec:.1f}")
        print(f"tracemalloc_peak_mb={peak_mb:.1f}")


if __name__ == "__main__":
    main()
