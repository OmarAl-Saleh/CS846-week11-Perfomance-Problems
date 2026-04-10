"""Simulated async scraper.

Fetches a fixed set of URLs (simulated latency) and extracts the <title> text.
"""

from __future__ import annotations

import argparse
import asyncio
import time
import tracemalloc


URLS = [f"https://example.com/page/{i}" for i in range(2000)]


async def fetch(url: str, *, simulated_latency_s: float) -> str:
    await asyncio.sleep(simulated_latency_s)
    return f"<html><title>{url}</title></html>"


def parse_title(html: str) -> str:
    start = html.find("<title>")
    end = html.find("</title>")
    if start == -1 or end == -1 or end <= start:
        return ""
    return html[start + 7 : end]


async def run(*, simulated_latency_s: float) -> list[str]:
    titles: list[str] = []
    for url in URLS:
        html = await fetch(url, simulated_latency_s=simulated_latency_s)
        titles.append(parse_title(html))
    return titles


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulated-latency-s", type=float, default=0.01)
    args = parser.parse_args()

    tracemalloc.start()
    t0_wall = time.perf_counter()
    t0_cpu = time.process_time()

    titles = asyncio.run(run(simulated_latency_s=args.simulated_latency_s))

    t1_cpu = time.process_time()
    t1_wall = time.perf_counter()
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    elapsed_wall = t1_wall - t0_wall
    elapsed_cpu = t1_cpu - t0_cpu
    req_per_sec = (len(URLS) / elapsed_wall) if elapsed_wall > 0 else float("inf")
    peak_mb = peak / (1024 * 1024)

    print("got", len(titles), "titles")
    print(f"wall_seconds={elapsed_wall:.3f}")
    print(f"cpu_seconds={elapsed_cpu:.3f}")
    print(f"throughput_requests_per_sec={req_per_sec:.1f}")
    print(f"tracemalloc_peak_mb={peak_mb:.1f}")


if __name__ == "__main__":
    main()
