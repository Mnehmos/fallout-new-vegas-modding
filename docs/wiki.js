const DATA_URL = 'data/bugs.json';

const escapeHtml = (s='') => String(s).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const statusLabel = s => ({active:'Investigating',seed:'Seed',partial:'Partially mitigated'})[s] || s;

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
  document.querySelector('#active-count').textContent=bugs.filter(b=>b.status==='active').length;
  document.querySelector('#high-count').textContent=bugs.filter(b=>b.priority===5).length;
  function render(){
    const q=search.value.trim().toLowerCase();
    const min=Number(priority.value);
    const out=bugs.filter(b=>{
      const hay=[b.id,b.title,b.summary,b.subsystem,b.platform,b.hypothesis,b.next].join(' ').toLowerCase();
      return (!q||hay.includes(q)) && (status.value==='all'||b.status===status.value) && (system.value==='all'||b.subsystem===system.value) && b.priority>=min;
    }).sort((a,b)=>b.priority-a.priority||a.id.localeCompare(b.id));
    grid.innerHTML=out.map(card).join('') || '<p>No investigations match these filters.</p>';
    document.querySelector('#visible-count').textContent=`${out.length} shown`;
  }
  [search,status,system,priority].forEach(x=>x.addEventListener('input',render));
  render();
}

async function detailPage(){
  const root=document.querySelector('#bug-detail');
  if(!root) return;
  const bugs=await loadBugs();
  const id=new URLSearchParams(location.search).get('id');
  const b=bugs.find(x=>x.id===id);
  if(!b){ root.innerHTML='<h1>Investigation not found</h1><p><a href="index.html">Return to catalog</a></p>'; return; }
  document.title=`${b.id}: ${b.title} · FNV Engine Bug Wiki`;
  const sources=(b.sources||[]).map(s=>`<li><a href="${escapeHtml(s.url)}">${escapeHtml(s.label)} ↗</a></li>`).join('');
  root.innerHTML=`<div class="detail-shell">
    <article class="detail">
      <p class="eyebrow">${escapeHtml(b.id)} · ${escapeHtml(statusLabel(b.status))}</p>
      <h1>${escapeHtml(b.title)}</h1>
      <p class="lede">${escapeHtml(b.summary)}</p>
      <h2>Current hypothesis</h2>
      <p>${escapeHtml(b.hypothesis || 'No semantic hypothesis yet. This entry remains a source-derived seed until reproduction work begins.')}</p>
      <h2>Next experiment</h2>
      <p>${escapeHtml(b.next || 'Reproduce on a clean current PC build, verify against maintained engine-fix plugins, and only then begin binary analysis.')}</p>
      <h2>Evidence / sources</h2>
      <ul class="evidence-list">${sources}</ul>
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
