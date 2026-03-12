import time


class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


def color(text, code):
    return f"{code}{text}{C.RESET}"


def measure(func, *args, repeats=3):
    best = float("inf")
    result = None

    for _ in range(repeats):
        start = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)

    return result, best


def progress_bar(progress, width=30):
    progress = max(0.0, min(progress, 1.0))
    filled = int(progress * width)
    empty = width - filled
    return "[" + "#" * filled + "-" * empty + "]"


def evaluate_performance_static_speedup(
    problem_name,
    baseline_func,
    student_func,
    args,
    target_speedup,
    repeats=3,
    enforce_correctness=True,
):
    baseline_result, baseline_time = measure(baseline_func, *args, repeats=repeats)
    student_result, student_time = measure(student_func, *args, repeats=repeats)

    if baseline_result != student_result and enforce_correctness:
        print(color("\n❌ CORRECTNESS FAILURE: Optimized result differs from baseline.", C.RED))
        print(color("Your optimization changed the observable behavior of the system.", C.YELLOW))
        print()
        print(color("Baseline result:", C.CYAN), baseline_result)
        print(color("Your result   :", C.CYAN), student_result)
        print()
        print(color("⚠️  Even small numeric differences are considered incorrect.", C.YELLOW))
        print(color("Common causes:", C.YELLOW))
        print("  - Reusing computation across requests when state changes")
        print("  - Caching without proper invalidation")
        print("  - Changing tie-breaking behavior in shortest path")
        print("  - Mutating shared state in a different order")
        print()
        print(color("Performance will NOT be evaluated until correctness matches baseline.", C.RED))
        return

   

    student_speedup = baseline_time / student_time if student_time > 0 else float("inf")
    progress = min(student_speedup / target_speedup, 1.0) if target_speedup > 0 else 1.0

    print("\n" + color("=" * 74, C.BLUE))
    print(color(problem_name, C.BOLD + C.CYAN))
    print(color("=" * 74, C.BLUE))

    print(f"{color('Baseline time', C.WHITE):<30}: {baseline_time:.6f}s")
    print(f"{color('Your time', C.WHITE):<30}: {student_time:.6f}s")
    print()

    print(f"{color('Your speedup', C.WHITE):<30}: {student_speedup:.2f}x")
    print(f"{color('Target speedup', C.WHITE):<30}: {target_speedup:.2f}x")
    print(f"{color('Progress toward target', C.WHITE):<30}: {progress * 100:.2f}%")

    if progress >= 1.0:
        progress_color = C.GREEN
    elif progress >= 0.5:
        progress_color = C.YELLOW
    else:
        progress_color = C.RED

    print(f"{color('Progress bar', C.WHITE):<30}: {color(progress_bar(progress), progress_color)}")
    print()

    improved = student_time < baseline_time
    reached_target = student_speedup >= target_speedup

    print(color("Status", C.BOLD + C.WHITE))
    print("  " + (color("✓ Improved over original", C.GREEN) if improved else color("✗ Not faster than original", C.RED)))
    print("  " + (color("✓ Reached target speedup", C.GREEN) if reached_target else color("✗ Target speedup not reached", C.YELLOW)))