// Pages veriyi 10 dk önbellekliyor; Argon güncellemesi hemen görünsün diye her açılışta taze çek.
const { squadData } = await import(`./data/squadData.js?v=${Date.now()}`);

const $ = (sel) => document.querySelector(sel);
const root = $('#app-root');
const dots = (...xs) => xs.filter((x) => x != null && x !== '').join(' · ');
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const NAMES = Object.fromEntries(Object.entries(squadData.players).map(([k, p]) => [k, p.riotId.split('#')[0]]));

// good/bad/fix maddeleri <strong>/<em> içerebilir (şema böyle), o yüzden kaçırılmıyor.
const list = (items) => `<ul>${(items || []).map((i) => `<li>${i}</li>`).join('')}</ul>`;

function hero(title, tag, summary, kpis) {
  return `
    <section class="player-hero">
      <div class="hero-left">
        <h2>${esc(title)} ${tag ? `<span class="hero-tag">${esc(tag)}</span>` : ''}</h2>
        <p>${esc(summary)}</p>
      </div>
      <div class="kpi-grid">
        ${(kpis || []).map((k) => `<div class="kpi-box"><div class="kpi-val">${esc(k.val)}</div><div class="kpi-lbl">${esc(k.lbl)}</div></div>`).join('')}
      </div>
    </section>`;
}

function triGrid(d) {
  return `
    <div class="sec-head"><h3>🩺 Röntgen</h3></div>
    <div class="analysis-tri-grid">
      <div class="tri-card good"><h4>✅ İyi yaptıkları</h4>${list(d.good)}</div>
      <div class="tri-card bad"><h4>❌ Kötü alışkanlıklar</h4>${list(d.bad)}</div>
      <div class="tri-card fix"><h4>🔧 Çözüm reçetesi</h4>${list(d.fix)}</div>
    </div>`;
}

function builds(arr) {
  if (!arr?.length) return '';
  const variant = (v) => `
    <div class="variant-box vs-${v.kind === 'danger' ? 'danger' : 'standard'}">
      <div class="variant-title">${esc(v.title)}</div>
      <div class="variant-enemies"><strong>Rakipler:</strong> ${esc(v.enemies)}</div>
      <div class="mini-label">Rünler</div>
      <div class="chip-row">
        <span class="chip keystone">${esc(v.keystone)}</span>
        ${(v.runes || []).map((r) => `<span class="chip">${esc(r)}</span>`).join('')}
      </div>
      <div class="mini-label">Büyüler</div>
      <div class="chip-row">${(v.spells || []).map((s) => `<span class="chip spell">${esc(s)}</span>`).join('')}</div>
      <div class="mini-label">Eşya sırası</div>
      <div class="item-flow">
        ${(v.items || []).map((it, i) => `<div class="item-node">${i + 1}. ${esc(it.name)}<small>${esc(it.note)}</small></div>`).join('<span class="item-arrow">➔</span>')}
      </div>
    </div>`;
  return `
    <div class="sec-head"><h3>🎯 Rün &amp; Eşya Rehberi</h3></div>
    <div class="builds-grid">
      ${arr.map((b) => `
        <div class="build-card">
          <div class="build-card-header"><h4>${esc(b.champ)}</h4><span class="status-pill">${esc(b.note)}</span></div>
          <div class="build-variants">${(b.variants || []).map(variant).join('')}</div>
        </div>`).join('')}
    </div>`;
}

const FILTERS = { all: 'Tümü', win: 'Galibiyet', loss: 'Mağlubiyet', premade: '🤝 Premade' };

function matchesSection(matches, renderRow) {
  if (!matches?.length) {
    return `<div class="sec-head"><h3>📜 Maçlar</h3></div><p class="m-sub">Henüz maç verisi yok. Sağ üstten “Argon CLI ile Güncelle”.</p>`;
  }
  return `
    <div class="sec-head">
      <h3>📜 Son ${matches.length} Maç</h3>
      <div class="filter-bar">${Object.entries(FILTERS).map(([k, l], i) => `<button class="filter-btn${i ? '' : ' active'}" data-filter="${k}">${l}</button>`).join('')}</div>
    </div>
    <div class="matches-list">${matches.map(renderRow).join('')}</div>`;
}

const resultLabel = (r) => (r === 'win' ? '<span style="color:var(--green)">Galibiyet</span>' : '<span style="color:var(--red)">Mağlubiyet</span>');

function playerMatchRow(m) {
  const csMin = m.cs && m.duration ? (m.cs / (parseInt(m.duration, 10) + (+m.duration.split(':')[1] || 0) / 60)).toFixed(1) : null;
  return `
    <div class="match-row ${m.result === 'win' ? 'win' : 'loss'}" data-result="${esc(m.result)}" data-premade="${m.premade?.length ? 1 : 0}">
      <div class="match-top">
        <div><div class="m-champ">${esc(m.champ)}</div><div class="m-sub">${esc(dots(m.role, m.queue))}</div></div>
        <div><div class="m-kda">${esc(m.kda)}</div><div class="m-sub">${dots(resultLabel(m.result), esc(m.duration))}</div></div>
        <div class="m-cs">${m.cs ?? '—'} CS${csMin ? ` · ${csMin}/dk` : ''}<div class="m-sub">${esc(m.date)}</div></div>
        <div class="m-items">${(m.items || []).map((it) => `<span class="m-item-pill${it.flag ? ` ${it.flag}-item` : ''}">${esc(it.name)}</span>`).join('')}</div>
        <div class="premade-badges">${(m.premade || []).map((k) => `<span class="p-badge">${esc(NAMES[k] || k)}</span>`).join('')}</div>
      </div>
      ${m.verdict ? `<div class="m-verdict">${esc(m.verdict)}</div>` : ''}
    </div>`;
}

function premadeMatchRow(m) {
  return `
    <div class="match-row ${m.result === 'win' ? 'win' : 'loss'}" data-result="${esc(m.result)}" data-premade="1">
      <div class="match-top" style="grid-template-columns: 180px 1fr">
        <div><div class="m-champ">${resultLabel(m.result)}</div><div class="m-sub">${esc(dots(m.queue, m.duration, m.date))}</div></div>
        <div class="m-items">
          ${(m.players || []).map((p) => `<span class="m-item-pill"><strong>${esc(NAMES[p.key] || p.key)}</strong> ${esc(p.champ)} (${esc(p.role)}) <span class="m-kda">${esc(p.kda)}</span>${p.cs != null ? ` · ${p.cs} CS` : ''}</span>`).join('')}
        </div>
      </div>
      ${m.verdict ? `<div class="m-verdict">${esc(m.verdict)}</div>` : ''}
    </div>`;
}

function render(tab) {
  if (tab === 'premade') {
    const d = squadData.premade;
    root.innerHTML = hero('🤝 Premade Maç Analizi', 'En az 2 ekip üyesi', d.summary, d.kpis)
      + triGrid(d) + matchesSection(d.matches, premadeMatchRow);
  } else {
    const p = squadData.players[tab];
    root.innerHTML = hero(p.riotId, p.tag, p.summary, p.kpis)
      + triGrid(p) + builds(p.builds) + matchesSection(p.matches, playerMatchRow);
  }
  document.querySelectorAll('.tab-btn').forEach((b) => b.classList.toggle('active', b.dataset.tab === tab));
}

// Sekmeler (#hash ile yenilemede kalır)
const tabFromHash = () => (location.hash.slice(1) in { ...squadData.players, premade: 1 } ? location.hash.slice(1) : 'l4cg');
document.querySelectorAll('.tab-btn').forEach((b) => b.addEventListener('click', () => { location.hash = b.dataset.tab; }));
window.addEventListener('hashchange', () => render(tabFromHash()));

// Maç filtresi
root.addEventListener('click', (e) => {
  const btn = e.target.closest('.filter-btn');
  if (!btn) return;
  root.querySelectorAll('.filter-btn').forEach((b) => b.classList.toggle('active', b === btn));
  const f = btn.dataset.filter;
  root.querySelectorAll('.match-row').forEach((row) => {
    row.hidden = !(f === 'all' || (f === 'premade' ? row.dataset.premade === '1' : row.dataset.result === f));
  });
});

$('#last-updated-badge').textContent = `Son Güncelleme: ${new Date(squadData.lastUpdated).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })}`;
render(tabFromHash());

// Argon modalı
const modal = $('#argon-modal');
const status = (msg) => { const el = $('#argon-status-msg'); el.textContent = msg; el.classList.remove('hidden'); };
$('#open-argon-btn').addEventListener('click', () => modal.classList.remove('hidden'));
$('#close-argon-btn').addEventListener('click', () => modal.classList.add('hidden'));
modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.add('hidden'); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') modal.classList.add('hidden'); });

const form = () => ({ target: $('#argon-target').value, urls: $('#argon-urls').value.trim(), raw: $('#argon-raw-input').value.trim() });

$('#copy-argon-prompt-btn').addEventListener('click', async () => {
  const { target, urls, raw } = form();
  const tpl = await (await fetch('./tools/argon_prompt.md')).text();
  const prompt = tpl.replace('__TARGET__', target).replace('__URLS__', urls || '(yok)')
    .replace('__DATE__', new Date().toISOString().slice(0, 10)).replace('__RAW__', raw || '(yok)');
  await navigator.clipboard.writeText(prompt);
  status('📋 Prompt panoda. lol-squad klasöründe Argon’a yapıştır; bitince commit + push’u sen yap.');
});

$('#trigger-argon-btn').addEventListener('click', async () => {
  const { target, urls, raw } = form();
  // Ham metin URI'ye sığmayabilir; panodan okunuyor (bkz. tools/argon_bridge.py).
  if (raw) await navigator.clipboard.writeText(raw);
  const q = new URLSearchParams({ target, urls });
  if (raw) q.set('clip', '1');
  location.href = `argon-lol://update?${q}`;
  status('🚀 Argon penceresi açılıyor: orada “e” deyip onayla. Bitince site 1-2 dk içinde kendini yeniler. Pencere açılmadıysa bu bilgisayarda bir kez tools/register_protocol.ps1 çalıştır.');
});
