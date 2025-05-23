from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Iterable, List


def run_tasks(func: Callable[[any], any], items: Iterable[any], max_workers: int = 4) -> List[any]:
    """Execute func(item) for each item asynchronously."""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as exc:
        futures = {exc.submit(func, item): item for item in items}
        for future in as_completed(futures):
            results.append(future.result())
    return results
