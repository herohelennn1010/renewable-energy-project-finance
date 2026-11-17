'use strict';
(() => {
  const cases = JSON.parse(document.getElementById('scenario-data').textContent);
  const buttons = [...document.querySelectorAll('[data-case]')];
  const el = id => document.getElementById(id);
  const ratio = x => (x < 0 ? '−' : '') + Math.abs(x).toFixed(2) + 'x';
  const money = x => 'S$' + (Math.abs(x) < .01 ? 0 : x / 1e6).toFixed(2) + 'm';
  const change = x => Math.abs(x - 1) < 1e-8 ? 'Unchanged' : (x > 1 ? '+' : '−') + Math.round(Math.abs(x - 1) * 100) + '%';
  const descriptions = [
    'The baseline pays scheduled debt service from retained cash, but year-12 replacement causes an organic DSCR covenant breach.',
    'Improved operating assumptions increase ordinary-quarter coverage. The planned replacement quarter still breaches the full covenant.',
    'Combined operating and construction stresses require completion support and create temporary debt-service arrears. Eventual repayment does not erase that failure.',
    'Construction exhausts the assumed completion support and retains an unfunded gap. COD also misses the fixed longstop; operating results assume completion.'
  ];
  const statuses = ['Covenant breach', 'Covenant breach remains', 'Payment shortfall', 'Completion not funded'];
  function render(index) {
    const c = cases[index];
    buttons.forEach((button, i) => {
      button.classList.toggle('active', i === index);
      button.setAttribute('aria-pressed', String(i === index));
    });
    el('case-name').textContent = c.name + ' case';
    el('case-status').textContent = statuses[index];
    el('case-description').textContent = descriptions[index];
    el('case-dscr').textContent = ratio(c.dscr) + (c.conditional ? '*' : '');
    el('case-ordinary').textContent = ratio(c.ordinary) + (c.conditional ? '*' : '');
    el('case-debt').textContent = money(c.debt);
    el('case-support').textContent = money(c.support);
    el('case-arrears').textContent = c.conditional ? 'Conditional*' : money(c.arrears);
    el('case-gap').textContent = money(c.gap);
    el('case-caveat').textContent = c.conditional
      ? '* Severe operating outputs assume completion despite the funding gap and missed longstop. Conditional zero arrears reflect retained cash under distribution lockup, and do not establish lower risk or bankability.'
      : 'Reserve draws and sponsor cash never increase CFADS. A covenant breach and a cash payment failure are different outcomes.';
    const drivers = [
      ['Merchant price', change(c.drivers.merchant)], ['Generation', change(c.drivers.yield)],
      ['Benchmark rate', c.drivers.rate === 0 ? 'Unchanged' : (c.drivers.rate > 0 ? '+' : '−') + Math.round(Math.abs(c.drivers.rate) * 1e4) + ' bp'],
      ['Recurring opex', change(c.drivers.opex)], ['EPC cost', change(c.drivers.epc)], ['COD delay', c.drivers.delay + ' months']
    ];
    el('case-drivers').replaceChildren(...drivers.map(([name, value]) => {
      const row = document.createElement('div');
      const dt = document.createElement('dt'); dt.textContent = name;
      const dd = document.createElement('dd'); dd.textContent = value;
      row.append(dt, dd); return row;
    }));
    el('coverage-rows').replaceChildren(...cases.map((item, i) => {
      const row = document.createElement('div'); row.className = 'chart-row' + (i === index ? ' selected' : '');
      const label = document.createElement('span'); label.textContent = item.name + (item.conditional ? '*' : '');
      const track = document.createElement('div'); track.className = 'bar-track'; track.setAttribute('aria-hidden', 'true');
      const bar = document.createElement('div'); bar.className = 'bar' + (item.ordinary < 1.2 ? ' below' : '');
      bar.style.width = Math.min(100, Math.max(0, item.ordinary / 2 * 100)) + '%'; track.append(bar);
      const value = document.createElement('span'); value.className = 'chart-value'; value.textContent = ratio(item.ordinary);
      row.append(label, track, value); return row;
    }));
  }
  buttons.forEach((button, index) => button.addEventListener('click', () => render(index)));
  render(0);
})();
