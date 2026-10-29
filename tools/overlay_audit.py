"""Find overlays that stay on screen far longer than they should (a fade-in that starts after its own fade-out leaves
the element up for the rest of the video). Seeks the composition's GSAP timeline every STEP seconds and reports each
element in #fx that is visible (opacity > 0.05) for more than MAX seconds, or still visible in the last second.
Usage: python3 tools/overlay_audit.py path/to/index.html [MAX=12] [STEP=0.5]
"""
import sys

from playwright.sync_api import sync_playwright

path, MAX, STEP = sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 12.0, float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
JS = """([step]) => {
  const els = Array.from(document.querySelectorAll('#fx > *'));
  const dur = tl.duration(), seen = els.map(() => []);
  for (let t = 0; t <= dur; t += step) {
    tl.seek(t, false);
    els.forEach((e, i) => { const o = parseFloat(getComputedStyle(e).opacity); if (o > 0.05 && getComputedStyle(e).display !== 'none') seen[i].push(+t.toFixed(2)); });
  }
  return els.map((e, i) => ({ i, cls: e.className, text: (e.innerText || '').replace(/\\s+/g, ' ').slice(0, 60), n: seen[i].length,
                               first: seen[i][0], last: seen[i][seen[i].length - 1], dur }));
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto("file://" + __import__("os").path.abspath(path)); pg.wait_for_timeout(1500)
    rows = pg.evaluate(JS, [STEP])
    b.close()
bad = [r for r in rows if r["n"] and (r["n"] * STEP > MAX or r["last"] >= r["dur"] - 1.0)]
print(f"{len(rows)} overlays checked, {len(bad)} suspicious")
for r in bad:
    print(f"  #{r['i']} {r['cls']!r} '{r['text']}' visible {r['n'] * STEP:.1f}s between {r['first']}-{r['last']}")
