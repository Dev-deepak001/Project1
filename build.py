import json, os

with open('data_final.json', encoding='utf-8') as f:
    data_json = f.read()

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>60-Day FIR Compliance Calendar — Shri Muktsar Sahib</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --primary:#1d4ed8;--primary-dk:#1e3a8a;--primary-lt:#dbeafe;
  --green:#16a34a;--green-lt:#dcfce7;
  --orange:#d97706;--orange-lt:#fef3c7;
  --red:#dc2626;--red-lt:#fee2e2;
  --blue:#2563eb;--blue-lt:#eff6ff;
  --purple:#7c3aed;--purple-lt:#ede9fe;
  --gray:#64748b;--gray-lt:#f1f5f9;
  --border:#e2e8f0;--surface:#fff;--bg:#f1f5f9;--text:#0f172a;
  --text2:#475569;--text3:#94a3b8;
  --sh1:0 1px 3px rgba(0,0,0,.06);--sh2:0 4px 14px rgba(0,0,0,.09);
}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);font-size:13.5px;min-height:100vh}

/* HEADER */
.hdr{background:linear-gradient(135deg,#0f2d6e 0%,#1d4ed8 55%,#3b82f6 100%);color:#fff;padding:0 1.75rem;height:72px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 4px 20px rgba(29,78,216,.4);position:sticky;top:0;z-index:300}
.hdr-brand{display:flex;align-items:center;gap:.75rem}
.hdr-ico{font-size:2rem;line-height:1}
.hdr-title h1{font-size:1.125rem;font-weight:800;letter-spacing:-.2px;line-height:1.25}
.hdr-title p{font-size:.7rem;opacity:.75;margin-top:.15rem}
.hdr-meta{font-size:.72rem;opacity:.7;text-align:right;line-height:1.7}

/* WRAP */
.wrap{max-width:1200px;margin:1.5rem auto;padding:0 1.25rem 4rem}

/* OVERALL STATS */
.ov-stats{display:grid;grid-template-columns:repeat(5,1fr);gap:.75rem;margin-bottom:1.25rem}
@media(max-width:760px){.ov-stats{grid-template-columns:repeat(2,1fr)}}
.ov-card{background:var(--surface);border:1px solid var(--border);border-radius:.875rem;padding:1.1rem 1rem 1rem;box-shadow:var(--sh1);position:relative;overflow:hidden;cursor:pointer;transition:box-shadow .18s,transform .18s}
.ov-card:hover{box-shadow:var(--sh2);transform:translateY(-1px)}
.ov-card.af{outline:3px solid var(--primary);outline-offset:1px}
.ov-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px}
.c-all::after {background:var(--primary)}
.c-comp::after{background:var(--green)}
.c-late::after{background:var(--orange)}
.c-over::after{background:var(--red)}
.c-pend::after{background:var(--blue)}
.ov-val{font-size:2.1rem;font-weight:900;line-height:1}
.ov-lbl{font-size:.68rem;text-transform:uppercase;letter-spacing:.07em;color:var(--text3);margin-top:.3rem;font-weight:700}
.c-all  .ov-val{color:var(--primary)}
.c-comp .ov-val{color:var(--green)}
.c-late .ov-val{color:var(--orange)}
.c-over .ov-val{color:var(--red)}
.c-pend .ov-val{color:var(--blue)}
.ov-pct{font-size:.75rem;font-weight:600;margin-top:.2rem}
.c-comp .ov-pct{color:var(--green)}.c-late .ov-pct{color:var(--orange)}
.c-over .ov-pct{color:var(--red)}.c-pend .ov-pct{color:var(--blue)}

/* TOOLBAR */
.toolbar{display:flex;gap:.625rem;margin-bottom:.875rem;flex-wrap:wrap}
.tb-in,.tb-sel{padding:.55rem 1rem;border:1px solid var(--border);border-radius:.5rem;font-size:.8125rem;background:var(--surface);color:var(--text);transition:border-color .18s}
.tb-in:focus,.tb-sel:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px rgba(29,78,216,.1)}
.tb-in{flex:1;min-width:180px}.tb-sel{min-width:175px}

/* MONTH NAV */
.mnav{background:var(--surface);border:1px solid var(--border);border-radius:.875rem;padding:.875rem 1.25rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem;box-shadow:var(--sh1)}
.mnav h2{font-size:1.25rem;font-weight:800}
.mnav small{font-size:.72rem;color:var(--text3)}
.nbtn{background:var(--gray-lt);border:1px solid var(--border);border-radius:.5rem;padding:.42rem .9rem;cursor:pointer;font-weight:700;font-size:.8rem;color:var(--text);transition:all .18s}
.nbtn:hover{background:var(--primary);color:#fff;border-color:var(--primary)}
.todaybtn{background:var(--orange-lt);color:var(--orange);border:1px solid #fcd34d;border-radius:.5rem;padding:.42rem .9rem;cursor:pointer;font-weight:700;font-size:.8rem;transition:all .18s}
.todaybtn:hover{background:var(--orange);color:#fff;border-color:var(--orange)}

/* MONTH MINI STATS */
.mstats{display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-bottom:.875rem}
.mstat{background:var(--surface);border:1px solid var(--border);border-radius:.625rem;padding:.6rem .875rem;display:flex;align-items:center;gap:.625rem;box-shadow:var(--sh1)}
.ms-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.ms-body .msval{font-weight:800;font-size:1.1rem}
.ms-body .mslbl{font-size:.67rem;color:var(--text3);text-transform:uppercase;letter-spacing:.06em}

/* LEGEND */
.legend{display:flex;align-items:center;gap:1.125rem;flex-wrap:wrap;background:var(--surface);border:1px solid var(--border);border-radius:.75rem;padding:.6rem 1.25rem;margin-bottom:.875rem;font-size:.75rem;box-shadow:var(--sh1)}
.leg-it{display:flex;align-items:center;gap:.375rem;color:var(--text2);font-weight:600}
.leg-dot{width:13px;height:13px;border-radius:3px;flex-shrink:0}

/* CALENDAR */
.cal-days{display:flex;flex-direction:column;gap:.4375rem}

.day-row{background:var(--surface);border:1px solid var(--border);border-left:4px solid transparent;border-radius:.75rem;overflow:hidden;transition:box-shadow .18s}
.day-row:not(.empty):hover{box-shadow:var(--sh2)}
.t-comp  {border-left-color:var(--green)}
.t-late  {border-left-color:var(--orange)}
.t-over  {border-left-color:var(--red);background:#fff9f9}
.t-pend  {border-left-color:var(--blue)}
.t-mixed {border-left-color:var(--purple)}
.empty   {opacity:.62}
.today-r {background:#fffdf5!important}

.day-hdr{display:flex;align-items:center;padding:.75rem 1.25rem;gap:.875rem;user-select:none}
.has-cases .day-hdr{cursor:pointer}

.dcircle{width:2.2rem;height:2.2rem;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.9rem;flex-shrink:0;background:var(--gray-lt);color:var(--text2)}
.t-over  .dcircle{background:var(--red);color:#fff}
.t-comp  .dcircle{background:var(--green-lt);color:var(--green)}
.t-late  .dcircle{background:var(--orange-lt);color:var(--orange)}
.t-pend  .dcircle{background:var(--blue-lt);color:var(--blue)}
.t-mixed .dcircle{background:var(--purple-lt);color:var(--purple)}

.dmeta{flex:1;min-width:0}
.dname{font-weight:700;font-size:.875rem;display:flex;align-items:center;gap:.375rem;flex-wrap:wrap}
.t-today{font-size:.6rem;font-weight:800;text-transform:uppercase;background:var(--orange);color:#fff;padding:.1rem .45rem;border-radius:9999px}
.t-we{font-size:.6rem;font-weight:700;background:var(--purple-lt);color:var(--purple);padding:.1rem .45rem;border-radius:9999px}
.dsub{font-size:.695rem;color:var(--text3);margin-top:.1rem}

.dbadges{display:flex;gap:.35rem;flex-wrap:wrap;align-items:center}
.bx{display:inline-flex;align-items:center;padding:.17rem .55rem;border-radius:9999px;font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;white-space:nowrap}
.bx-total {background:var(--primary-lt);color:var(--primary)}
.bx-green {background:var(--green-lt);color:var(--green)}
.bx-orange{background:var(--orange-lt);color:var(--orange)}
.bx-red   {background:var(--red-lt);color:var(--red)}
.bx-blue  {background:var(--blue-lt);color:var(--blue)}

.chev{color:var(--text3);font-size:.8rem;transition:transform .25s;flex-shrink:0;margin-left:.5rem}
.day-row.expanded .chev{transform:rotate(180deg)}

/* EXPANDABLE BODY */
.day-body{display:none;border-top:1px solid var(--border);animation:sd .2s ease}
.day-row.expanded .day-body{display:block}
@keyframes sd{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}

/* TABLE */
.tw{overflow-x:auto}
table{width:100%;border-collapse:collapse;font-size:.795rem}
thead th{background:var(--gray-lt);padding:.55rem .75rem;text-align:left;font-size:.685rem;text-transform:uppercase;letter-spacing:.07em;color:var(--text3);font-weight:700;border-bottom:2px solid var(--border);white-space:nowrap}
tbody td{padding:.575rem .75rem;border-bottom:1px solid var(--border);vertical-align:middle}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:var(--gray-lt)}
.rn{color:var(--text3);font-weight:700;font-size:.7rem;white-space:nowrap}
.trunc{display:block;max-width:170px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

/* PILLS */
.pill{display:inline-flex;align-items:center;gap:.3rem;padding:.17rem .6rem;border-radius:9999px;font-size:.7rem;font-weight:700;white-space:nowrap}
.p-comp{background:var(--green-lt);color:var(--green)}
.p-late{background:var(--orange-lt);color:var(--orange)}
.p-over{background:var(--red-lt);color:var(--red)}
.p-pend{background:var(--blue-lt);color:var(--blue)}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;flex-shrink:0}
.d-g{background:var(--green)}.d-o{background:var(--orange)}.d-r{background:var(--red)}.d-b{background:var(--blue)}

.fno{font-weight:800;color:var(--primary);white-space:nowrap}
.ps-tag{display:inline-block;background:var(--purple-lt);color:var(--purple);padding:.1rem .5rem;border-radius:.3rem;font-size:.68rem;font-weight:700;white-space:nowrap}
.muted{color:var(--text3)}
.hidden{display:none!important}
</style>
</head>
<body>

<header class="hdr">
  <div class="hdr-brand">
    <span class="hdr-ico">&#9878;</span>
    <div class="hdr-title">
      <h1>60-Day FIR Compliance Calendar</h1>
      <p>District: Shri Muktsar Sahib &nbsp;&bull;&nbsp; Tracks 60-day IIF5 filing deadlines per FIR</p>
    </div>
  </div>
  <div class="hdr-meta">Data: 01 Jul 2024 &ndash; 01 Apr 2026<br>Total FIRs: 1,588</div>
</header>

<div class="wrap">
  <div class="ov-stats" id="ovStats"></div>

  <div class="toolbar">
    <input type="text" class="tb-in" id="srch" placeholder="&#128269;  Search FIR No, Police Station, IO Name, Act&hellip;" oninput="render()">
    <select class="tb-sel" id="psF" onchange="render()">
      <option value="">All Police Stations (11)</option>
    </select>
    <select class="tb-sel" id="catF" onchange="render()">
      <option value="">All Compliance Categories</option>
      <option value="compliant">&#10003; Compliant (IIF5 within 60 days)</option>
      <option value="late">&#8987; Late Filing (IIF5 &gt; 60 days)</option>
      <option value="overdue">&#10007; Overdue (IIF5 not filed)</option>
      <option value="pending">&#9679; Pending (still within 60-day window)</option>
    </select>
  </div>

  <div class="mnav">
    <button class="nbtn" onclick="chM(-1)">&#8592; Prev</button>
    <div style="text-align:center">
      <h2 id="mT"></h2><small id="mS"></small>
    </div>
    <div style="display:flex;gap:.5rem;align-items:center">
      <button class="todaybtn" onclick="goToday()">&#9679; Today</button>
      <button class="nbtn" onclick="chM(1)">Next &#8594;</button>
    </div>
  </div>

  <div class="mstats" id="mStats"></div>

  <div class="legend">
    <strong style="color:var(--text);margin-right:.25rem">Legend:</strong>
    <span class="leg-it"><span class="leg-dot" style="background:var(--green)"></span>Compliant (filed &le;60 days)</span>
    <span class="leg-it"><span class="leg-dot" style="background:var(--orange)"></span>Late Filing (filed &gt;60 days)</span>
    <span class="leg-it"><span class="leg-dot" style="background:var(--red)"></span>Overdue (IIF5 not filed, deadline passed)</span>
    <span class="leg-it"><span class="leg-dot" style="background:var(--blue)"></span>Pending (still within 60-day window)</span>
  </div>

  <div class="cal-days" id="calDays"></div>
</div>

<script>
const DATA="""

html += data_json

html += """;

const MN=['January','February','March','April','May','June','July','August','September','October','November','December'];
const DN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
let cY=new Date().getFullYear(), cM=new Date().getMonth(), EX=new Set();

(function init(){
  const ps=[...new Set(DATA.map(r=>r.ps_name).filter(Boolean))].sort();
  const s=document.getElementById('psF');
  ps.forEach(p=>{const o=document.createElement('option');o.value=p;o.textContent=p;s.appendChild(o);});
  buildOverallStats();
  render();
})();

function buildOverallStats(){
  const tot=DATA.length;
  const comp=DATA.filter(r=>r.category==='compliant').length;
  const late=DATA.filter(r=>r.category==='late').length;
  const over=DATA.filter(r=>r.category==='overdue').length;
  const pend=DATA.filter(r=>r.category==='pending').length;
  const pct=n=>((n/tot)*100).toFixed(1)+'%';
  const cards=[
    {c:'c-all', v:tot,  l:'Total FIRs',       p:''},
    {c:'c-comp',v:comp, l:'Compliant &#10003;',p:pct(comp)},
    {c:'c-late',v:late, l:'Late Filing &#8987;',p:pct(late)},
    {c:'c-over',v:over, l:'Overdue &#10007;',  p:pct(over)},
    {c:'c-pend',v:pend, l:'Pending &#9679;',   p:pct(pend)},
  ];
  document.getElementById('ovStats').innerHTML=cards.map((c,i)=>`
    <div class="ov-card ${c.c}" onclick="qf(${i})" title="Click to filter">
      <div class="ov-val">${c.v.toLocaleString()}</div>
      <div class="ov-lbl">${c.l}</div>
      ${c.p?`<div class="ov-pct">${c.p} of total</div>`:''}
    </div>`).join('');
}

const CAT_VALS=['','compliant','late','overdue','pending'];
function qf(i){
  document.getElementById('catF').value=CAT_VALS[i];
  document.querySelectorAll('.ov-card').forEach((el,j)=>el.classList.toggle('af',j===i&&i>0));
  render();
}

function gf(){
  const q=document.getElementById('srch').value.trim().toLowerCase();
  const ps=document.getElementById('psF').value;
  const cat=document.getElementById('catF').value;
  return DATA.filter(r=>{
    if(ps&&r.ps_name!==ps) return false;
    if(cat&&r.category!==cat) return false;
    if(q){
      const h=[r.fir_no,r.ps_name,r.io_name,r.act_section,r.iif5_type,r.fir_date].map(v=>(v||'').toLowerCase()).join(' ');
      if(!h.includes(q)) return false;
    }
    return true;
  });
}

function dk(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
function con(ds){return gf().filter(r=>r.deadline===ds);}

function render(){
  // month title
  document.getElementById('mT').textContent=MN[cM]+' '+cY;
  const n=new Date(cY,cM+1,0).getDate();
  document.getElementById('mS').textContent=n+' days';
  // month mini stats
  const ms=new Date(cY,cM,1), me=new Date(cY,cM+1,0); me.setHours(23,59,59);
  const fd=gf(), im=r=>{const d=new Date(r.deadline);return d>=ms&&d<=me;};
  const mc=fd.filter(r=>im(r)&&r.category==='compliant').length;
  const ml=fd.filter(r=>im(r)&&r.category==='late').length;
  const mo=fd.filter(r=>im(r)&&r.category==='overdue').length;
  const mp=fd.filter(r=>im(r)&&r.category==='pending').length;
  document.getElementById('mStats').innerHTML=`
    <div class="mstat"><span class="ms-dot" style="background:var(--green)"></span><div class="ms-body"><div class="msval" style="color:var(--green)">${mc}</div><div class="mslbl">Compliant</div></div></div>
    <div class="mstat"><span class="ms-dot" style="background:var(--orange)"></span><div class="ms-body"><div class="msval" style="color:var(--orange)">${ml}</div><div class="mslbl">Late Filing</div></div></div>
    <div class="mstat"><span class="ms-dot" style="background:var(--red)"></span><div class="ms-body"><div class="msval" style="color:var(--red)">${mo}</div><div class="mslbl">Overdue</div></div></div>
    <div class="mstat"><span class="ms-dot" style="background:var(--blue)"></span><div class="ms-body"><div class="msval" style="color:var(--blue)">${mp}</div><div class="mslbl">Pending</div></div></div>`;
  // days
  renderDays();
}

function renderDays(){
  const today=new Date(); today.setHours(0,0,0,0);
  const todayK=dk(today);
  const days=new Date(cY,cM+1,0).getDate();
  let html='';
  for(let d=1;d<=days;d++){
    const dt=new Date(cY,cM,d), dateK=dk(dt);
    const cases=con(dateK);
    const dow=dt.getDay(), isToday=dateK===todayK, isWE=dow===0||dow===6;
    const comp=cases.filter(r=>r.category==='compliant').length;
    const late=cases.filter(r=>r.category==='late').length;
    const over=cases.filter(r=>r.category==='overdue').length;
    const pend=cases.filter(r=>r.category==='pending').length;
    const total=cases.length;
    let type='';
    if(total>0){
      if(over&&!comp&&!late&&!pend)      type='t-over';
      else if(comp&&!late&&!over&&!pend) type='t-comp';
      else if(late&&!comp&&!over&&!pend) type='t-late';
      else if(pend&&!comp&&!over&&!late) type='t-pend';
      else                               type='t-mixed';
    }
    let badges='';
    if(total>0){
      badges+=`<span class="bx bx-total">${total} FIR${total>1?'s':''}</span>`;
      if(comp) badges+=`<span class="bx bx-green">&#10003; ${comp}</span>`;
      if(late) badges+=`<span class="bx bx-orange">&#8987; ${late}</span>`;
      if(over) badges+=`<span class="bx bx-red">&#10007; ${over}</span>`;
      if(pend) badges+=`<span class="bx bx-blue">&#9679; ${pend}</span>`;
    }
    const circStyle=(isToday&&!total)?'style="background:var(--orange);color:#fff"':'';
    html+=`
<div class="day-row ${type} ${isToday?'today-r':''} ${total?'has-cases':'empty'} ${EX.has(dateK)?'expanded':''}" id="dr-${dateK}">
  <div class="day-hdr" ${total?`onclick="tog('${dateK}')"`:''}>
    <div class="dcircle" ${circStyle}>${d}</div>
    <div class="dmeta">
      <div class="dname">${DN[dow]}${isToday?'<span class="t-today">Today</span>':''}${isWE&&!isToday?'<span class="t-we">Weekend</span>':''}</div>
      <div class="dsub">${MN[cM]} ${d}, ${cY}</div>
    </div>
    <div class="dbadges">${badges}</div>
    ${total?'<div class="chev">&#9660;</div>':''}
  </div>
  ${total?`<div class="day-body"><div class="tw">${bldTable(cases)}</div></div>`:''}
</div>`;
  }
  document.getElementById('calDays').innerHTML=html;
}

function bldTable(cases){
  const h=`<tr>
    <th>#</th><th>FIR No.</th><th>Police Station</th>
    <th>FIR Date</th><th>60-Day Deadline</th>
    <th>Compliance Status</th><th>IIF5 Filed On</th>
    <th>IIF5 Type</th><th>IO Name</th><th>Act &amp; Section</th>
  </tr>`;
  const rows=cases.map((r,i)=>{
    const pill={
      compliant:`<span class="pill p-comp"><span class="dot d-g"></span>Compliant</span>`,
      late:     `<span class="pill p-late"><span class="dot d-o"></span>Late Filing</span>`,
      overdue:  `<span class="pill p-over"><span class="dot d-r"></span>Overdue</span>`,
      pending:  `<span class="pill p-pend"><span class="dot d-b"></span>Pending</span>`,
    }[r.category]||'';
    return `<tr>
      <td class="rn">${i+1}</td>
      <td><span class="fno">${e(r.fir_no)}</span></td>
      <td><span class="ps-tag">${e(r.ps_name)}</span></td>
      <td class="rn">${e(r.fir_date)}</td>
      <td><strong>${e(r.deadline)}</strong></td>
      <td>${pill}</td>
      <td class="rn">${r.iif5_date?e(r.iif5_date):'<span class="muted">Not filed</span>'}</td>
      <td>${r.iif5_type?e(r.iif5_type):'<span class="muted">—</span>'}</td>
      <td><span class="trunc" title="${e(r.io_name)}">${e(r.io_name)||'—'}</span></td>
      <td><span class="trunc" title="${e(r.act_section)}">${e(r.act_section)||'—'}</span></td>
    </tr>`;
  }).join('');
  return `<table><thead>${h}</thead><tbody>${rows}</tbody></table>`;
}

function tog(dateK){
  const el=document.getElementById('dr-'+dateK);
  if(!el||!el.querySelector('.day-body')) return;
  el.classList.toggle('expanded');
  EX.has(dateK)?EX.delete(dateK):EX.add(dateK);
}
function chM(d){cM+=d;if(cM<0){cM=11;cY--;}if(cM>11){cM=0;cY++;}render();window.scrollTo({top:0,behavior:'smooth'});}
function goToday(){const t=new Date();cY=t.getFullYear();cM=t.getMonth();render();setTimeout(()=>{const el=document.getElementById('dr-'+dk(t));if(el)el.scrollIntoView({behavior:'smooth',block:'center'});},80);}
function e(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
</script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize('index.html')
print(f'Written index.html — {size/1024:.1f} KB ({size/1024/1024:.2f} MB)')
