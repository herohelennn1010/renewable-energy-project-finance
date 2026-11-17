"""Build the static portfolio from the published model snapshots; no model recalculation."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
cases = json.loads((ROOT / 'model/scenario_results.json').read_text())
grid = json.loads((ROOT / 'model/formula_map.json').read_text())['grids']['Assumptions']
data = []
for c, col in zip(cases, 'FGHI'):
    data.append({
        'name': c['case'],
        'debt': c['Actual debt drawn at COD'],
        'dscr': c['Minimum quarterly organic DSCR'],
        'ordinary': c['Minimum DSCR excluding replacement'],
        'arrears': c['Peak unpaid debt service'],
        'gap': c['Peak construction funding gap'],
        'support': c['Completion support drawn'],
        'conditional': bool(c['COD beyond construction longstop'] or c['Peak construction funding gap'] > .01),
        'drivers': {name: grid[col + str(row)] for name, row in [
            ('merchant', 90), ('yield', 91), ('rate', 92), ('opex', 93), ('epc', 94), ('delay', 95)]},
    })
template = (ROOT / 'site/index.template.html').read_text()
assert template.count('__SCENARIO_DATA__') == 1
(ROOT / 'index.html').write_text(template.replace('__SCENARIO_DATA__', json.dumps(data, separators=(',', ':')).replace('<', '\\u003c')))
(ROOT / '.nojekyll').touch()
print('Built static portfolio from four published model scenarios.')
