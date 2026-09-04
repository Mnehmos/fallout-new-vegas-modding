const DATA_URL = 'data/bugs.json';

const escapeHtml = (s='') => String(s).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

// Machine-readable status vocabulary (see docs/bug-kanban.md columns).
const STATUS_LABELS = {
  seed: 'Seed',
  active: 'Investigating',
  partial: 'Partially mitigated',
  remapped: 'Static mapping',
  'root-caused': 'Root cause confirmed',
  'fix-shipped': 'Fix shipped',
  'verified-closed': 'Verified & closed',
};
const statusLabel = s => STATUS_LABELS[s] || s;
const isFixed = s => s === 'fix-shipped' || s === 'verified-closed';

async function loadBugs(){
  const r = await fetch(DATA_URL);
  if(!r.ok) throw new Error(`Could not load ${DATA_URL}`);
  return r.json();
}

function priorityText(p){ return '★'.repeat(p) + '☆'.repeat(5-p); }

function card(b){
  const tags=[b.subsystem,b.platform].filter(Boolean).map(x=>`<span class="tag">${escapeHtml(x)}</span>`).join('');
  return `<article class="bug-card">
    <div class="bug-top"><span class="bug-id">${escapeHtml(b.id)}</span><span class="badge ${escapeHtml(b.status)}">${escapeHtml(statusLabel(b.status))}</span></div>
    <h3>${escapeHtml(b.title)}</h3>
    <p>${escapeHtml(b.summary)}</p>
    <div class="tags">${tags}</div>
    <div class="bug-meta"><span class="priority" title="Priority ${b.priority}/5">${priorityText(b.priority)}</span><a class="more" href="bug.html?id=${encodeURIComponent(b.id)}">Open investigation →</a></div>
  </article>`;
}

async function catalogPage(){
  const grid=document.querySelector('#bug-grid');
  if(!grid) return;
  const bugs=await loadBugs();
  const search=document.querySelector('#search');
  const status=document.querySelector('#status-filter');
  const system=document.querySelector('#system-filter');
  const priority=document.querySelector('#priority-filter');
  [...new Set(bugs.map(b=>b.status))].sort().forEach(v=>status.insertAdjacentHTML('beforeend',`<option value="${escapeHtml(v)}">${escapeHtml(statusLabel(v))}</option>`));
  [...new Set(bugs.map(b=>b.subsystem))].sort().forEach(v=>system.insertAdjacentHTML('beforeend',`<option value="${escapeHtml(v)}">${escapeHtml(v)}</option>`));
  document.querySelector('#total-count').textContent=bugs.length;
  document.querySelector('#active-count').textContent=bugs.filter(b=>b.status==='active'||b.status==='remapped').length;
  document.querySelector('#high-count').textContent=bugs.filter(b=>b.priority===5).length;
  const fixed=document.querySelector('#fixed-count');
  if(fixed) fixed.textContent=bugs.filter(b=>isFixed(b.status)).length;
  function render(){
    const q=search.value.trim().toLowerCase();
    const min=Number(priority.value);
    const out=bugs.filter(b=>{
      const hay=[b.id,b.title,b.summary,b.subsystem,b.platform,b.hypothesis,b.re_findings,b.root_cause,b.next].join(' ').toLowerCase();
      return (!q||hay.includes(q)) && (status.value==='all'||b.status===status.value) && (system.value==='all'||b.subsystem===system.value) && b.priority>=min;
    }).sort((a,b)=>b.priority-a.priority||a.id.localeCompare(b.id));
    grid.innerHTML=out.map(card).join('') || '<p>No investigations match these filters.</p>';
    document.querySelector('#visible-count').textContent=`${out.length} shown`;
  }
  [search,status,system,priority].forEach(x=>x.addEventListener('input',render));
  render();
}

// --- detail page rendering -------------------------------------------------

function section(title, text){
  if(!text || (typeof text === 'string' && !text.trim())) return '';
  const body = typeof text === 'string'
    ? `<p>${escapeHtml(text)}</p>`
    : `<pre class="record">${escapeHtml(JSON.stringify(text, null, 2))}</pre>`;
  return `<h2>${escapeHtml(title)}</h2>${body}`;
}

function falsificationTrail(trail){
  if(!Array.isArray(trail) || !trail.length) return '';
  const items = trail.map(t=>`<li>
    <strong>${escapeHtml(t.hypothesis||'Hypothesis')}</strong>
    <p>Result: ${escapeHtml(t.result||'—')}</p>
    ${t.lesson?`<p>Lesson: ${escapeHtml(t.lesson)}</p>`:''}
  </li>`).join('');
  return `<h2>Falsification trail</h2><ul class="evidence-list trail">${items}</ul>`;
}

function sourcesList(sources){
  if(!Array.isArray(sources) || !sources.length) return '';
  const items = sources.map(s=>{
    const link = s.url
      ? `<a href="${escapeHtml(s.url)}">${escapeHtml(s.label)} ↗</a>`
      : `<strong>${escapeHtml(s.label||'Evidence')}</strong>`;
    const detail = s.detail ? `<p class="src-detail">${escapeHtml(s.detail)}</p>` : '';
    return `<li>${link}${detail}</li>`;
  }).join('');
  return `<h2>Evidence / sources</h2><ul class="evidence-list">${items}</ul>`;
}

const RENDERED_KEYS = new Set(['id','title','status','status_note','subsystem','priority','platform','summary','hypothesis','measured','root_cause','fix_direction','next','sources','falsification_trail','shipped_fix','re_findings','atlas_findings','dead_code_finding','fix_verified','remaining','v3_design','superseded_thrown_weapon_analysis']);

async function detailPage(){
  const root=document.querySelector('#bug-detail');
  if(!root) return;
  const bugs=await loadBugs();
  const id=new URLSearchParams(location.search).get('id');
  const b=bugs.find(x=>x.id===id);
  if(!b){ root.innerHTML='<h1>Investigation not found</h1><p><a href="index.html">Return to catalog</a></p>'; return; }
  document.title=`${b.id}: ${b.title} · FNV Engine Bug Wiki`;
  const extraKeys=Object.keys(b).filter(k=>!RENDERED_KEYS.has(k));
  root.innerHTML=`<div class="detail-shell">
    <article class="detail">
      <p class="eyebrow">${escapeHtml(b.id)} · ${escapeHtml(statusLabel(b.status))}</p>
      <h1>${escapeHtml(b.title)}</h1>
      <p class="lede">${escapeHtml(b.summary)}</p>
      ${b.status_note?`<p class="status-note">${escapeHtml(b.status_note)}</p>`:''}
      ${section('Hypothesis / findings so far', b.hypothesis)}
      ${section('Measured evidence', b.measured)}
      ${section('Reverse-engineering findings', b.re_findings)}
      ${section('Root cause', b.root_cause)}
      ${section('Fix direction', b.fix_direction)}
      ${section('Shipped fix', b.shipped_fix)}
      ${section('Fix verification', b.fix_verified)}
      ${section('Outstanding', b.remaining)}
      ${falsificationTrail(b.falsification_trail)}
      ${section('Next experiment', b.next || 'Reproduce on a clean current PC build, verify against maintained engine-fix plugins, and only then begin binary analysis.')}
      ${sourcesList(b.sources)}
      ${extraKeys.length?`<details class="raw"><summary>Additional record fields (${extraKeys.length})</summary><pre class="record">${escapeHtml(JSON.stringify(Object.fromEntries(extraKeys.map(k=>[k,b[k]])), null, 2))}</pre></details>`:''}
      <h2>Evidence status</h2>
      <p>No community source can promote an engine symbol by itself. Static names remain candidates until our own PC analysis concurs; high-confidence behavioral claims require runtime artifacts under the <code>mnehmos.re</code> confidence policy.</p>
    </article>
    <aside class="sidebox"><a href="index.html">← Bug catalog</a><dl>
      <dt>Status</dt><dd>${escapeHtml(statusLabel(b.status))}</dd>
      <dt>Priority</dt><dd class="priority">${priorityText(b.priority)} (${b.priority}/5)</dd>
      <dt>Subsystem</dt><dd>${escapeHtml(b.subsystem)}</dd>
      <dt>Platforms</dt><dd>${escapeHtml(b.platform)}</dd>
    </dl></aside>
  </div>`;
}

catalogPage().catch(console.error);
detailPage().catch(console.error);
