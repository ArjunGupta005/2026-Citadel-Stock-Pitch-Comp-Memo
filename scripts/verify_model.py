"""Recalculate model/TeamName.xlsx with the `formulas` engine and compare to the Python reference outputs."""
import formulas
import scenario_engine as se
import cprt_framework_b as fb
from common import ROOT

path = str(ROOT / "model" / "TeamName.xlsx")
sol = formulas.ExcelModel().loads(path).finish().calculate()
def get(sheet, cell):
    for k, v in sol.items():
        if k.upper().endswith(f"[TEAMNAME.XLSX]{sheet.upper()}'!{cell}"):
            return float(v.value[0][0])
    raise KeyError(sheet + cell)
ok = True
for j, w in enumerate([se.CPRT_WORLDS["bear"], se.CPRT_WORLDS["base"], se.CPRT_WORLDS["bull"], fb.W4]):
    col = "BCDE"[j]
    ref = sum(q["eps"] for q in se.cprt_quarters(w))
    xl = get("VALUATION", f"{col}5")
    print(f"W{j+1} FY27 EPS excel {xl:.4f} python {ref:.4f}")
    ok &= abs(xl - ref) < 1e-6
print("Summary: short EV", round(get("SUMMARY", "B8"), 4), "| EPS-only", round(get("SUMMARY", "B9"), 4),
      "| base PT", round(get("SUMMARY", "B6"), 2), "| max loss", round(get("SUMMARY", "B10"), 4),
      "| FY27 gap", round(get("SUMMARY", "B11"), 4), "| Q1 gap", round(get("SUMMARY", "B12"), 4))
print("Sensitivity:", [round(get("SENSITIVITY", f"B{r}"), 4) for r in range(4, 9)])
print("ALL WORLD EPS MATCH" if ok else "MISMATCH")
