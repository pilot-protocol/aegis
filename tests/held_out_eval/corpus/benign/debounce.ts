// Generic debounce + throttle utilities used across the dashboard UI.

export function debounce<A extends unknown[]>(
  fn: (...args: A) => void,
  waitMs: number,
): (...args: A) => void {
  let timer: ReturnType<typeof setTimeout> | undefined;
  return (...args: A) => {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => fn(...args), waitMs);
  };
}

export function throttle<A extends unknown[]>(
  fn: (...args: A) => void,
  intervalMs: number,
): (...args: A) => void {
  let last = 0;
  return (...args: A) => {
    const now = Date.now();
    if (now - last >= intervalMs) {
      last = now;
      fn(...args);
    }
  };
}
