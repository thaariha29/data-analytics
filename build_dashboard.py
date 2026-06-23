import pandas as pd
import json

df = pd.read_csv('/home/claude/sales_data.csv')
payload = json.dumps(df.to_dict(orient='records'), separators=(',',':'))

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sales & Revenue Analysis Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<style>
:root {
  --bg:#0d1117;--surface:#161b22;--card:#1c2128;--border:#30363d;
  --accent:#388bfd;--green:#3fb950;--orange:#d29922;--red:#f85149;
  --purple:#bc8cff;--text:#e6edf3;--sub:#8b949e;--cyan:#39c5cf;
}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh;}

.header{background:var(--surface);border-bottom:1px solid var(--border);padding:18px 28px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;}
.header h1{font-size:1.3rem;font-weight:700;letter-spacing:-.3px;}
.header h1 span{color:var(--accent);}
.header-meta{font-size:.8rem;color:var(--sub);margin-top:3px;}
.header-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap;}

.filter-bar{background:var(--surface);border-bottom:1px solid var(--border);padding:14px 28px;display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end;}
.fg{display:flex;flex-direction:column;gap:5px;}
.fg label{font-size:.72rem;font-weight:600;color:var(--sub);text-transform:uppercase;letter-spacing:.6px;}
.fg select{background:var(--card);color:var(--text);border:1px solid var(--border);border-radius:6px;padding:7px 10px;font-size:.83rem;cursor:pointer;min-width:130px;outline:none;}
.fg select:focus{border-color:var(--accent);}
.btn{background:var(--accent);color:#fff;border:none;border-radius:6px;padding:8px 18px;font-size:.83rem;font-weight:600;cursor:pointer;transition:opacity .15s;}
.btn:hover{opacity:.85;}
.btn-g{background:transparent;color:var(--sub);border:1px solid var(--border);border-radius:6px;padding:7px 14px;font-size:.8rem;cursor:pointer;}
.btn-g:hover{border-color:var(--text);color:var(--text);}
.filter-status{font-size:.78rem;color:var(--sub);align-self:flex-end;margin-left:auto;}

.main{padding:22px 28px;display:flex;flex-direction:column;gap:20px;}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px 20px;position:relative;overflow:hidden;}
.kpi::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--kc,var(--accent));border-radius:10px 10px 0 0;}
.kpi-label{font-size:.72rem;color:var(--sub);font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px;}
.kpi-value{font-size:1.85rem;font-weight:700;letter-spacing:-1px;margin-bottom:4px;}
.kpi-delta{font-size:.78rem;font-weight:600;}
.pos{color:var(--green);}.neg{color:var(--red);}.neu{color:var(--sub);}

.g2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.g3{display:grid;grid-template-columns:2fr 1fr 1fr;gap:16px;}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:18px 20px;}
.card h3{font-size:.85rem;font-weight:700;color:var(--text);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.badge{font-size:.68rem;background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:2px 8px;color:var(--sub);font-weight:500;}
.cw{position:relative;}

.table-wrap{overflow-x:auto;margin-top:4px;}
table{width:100%;border-collapse:collapse;font-size:.79rem;}
thead th{background:var(--surface);color:var(--sub);font-weight:600;text-align:left;padding:9px 12px;border-bottom:1px solid var(--border);font-size:.71rem;text-transform:uppercase;letter-spacing:.4px;cursor:pointer;user-select:none;white-space:nowrap;}
thead th:hover{color:var(--text);}
tbody tr{border-bottom:1px solid var(--border);transition:background .1s;}
tbody tr:hover{background:var(--surface);}
tbody td{padding:8px 12px;color:var(--text);}
.tag{display:inline-block;border-radius:4px;padding:2px 7px;font-size:.69rem;font-weight:600;}
.tsw{background:rgba(56,139,253,.18);color:var(--accent);}
.tsv{background:rgba(63,185,80,.18);color:var(--green);}
.tcn{background:rgba(188,140,255,.18);color:var(--purple);}
.tsp{background:rgba(210,153,34,.18);color:var(--orange);}

.import-area{display:flex;flex-direction:column;gap:4px;}
.import-hint{font-size:.73rem;color:var(--sub);}

.footer{text-align:center;color:var(--sub);font-size:.75rem;padding:20px;border-top:1px solid var(--border);margin-top:8px;}

@media(max-width:900px){
  .kpi-row{grid-template-columns:repeat(2,1fr);}
  .g2,.g3{grid-template-columns:1fr;}
  .main{padding:14px;}
  .filter-bar{padding:12px 14px;}
  .header{padding:14px;}
}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>Sales &amp; Revenue <span>Analysis Dashboard</span></h1>
    <div class="header-meta">FY 2025 &nbsp;&middot;&nbsp; Thiranex Internship Project &nbsp;&middot;&nbsp; <span id="lastUpd"></span></div>
  </div>
  <div class="header-actions">
    <button class="btn-g" onclick="exportCSV()">&#8595; Export Filtered CSV</button>
    <button class="btn" onclick="document.getElementById('fi').click()">&#8593; Import CSV</button>
    <input type="file" id="fi" accept=".csv" style="display:none" onchange="handleImport(event)">
  </div>
</div>

<div class="filter-bar">
  <div class="import-area">
    <span style="font-size:.72rem;font-weight:600;color:var(--sub);text-transform:uppercase;letter-spacing:.6px;">&#128194; Data Source</span>
    <button class="btn-g" onclick="document.getElementById('fi').click()" style="padding:6px 12px;font-size:.8rem;">Choose CSV file&hellip;</button>
    <div class="import-hint" id="fileStatus">Using built-in sample data &mdash; 500 rows</div>
  </div>

  <div class="fg"><label>Quarter</label>
    <select id="fQ" onchange="go()">
      <option value="all">All Quarters</option>
      <option>Q1</option><option>Q2</option><option>Q3</option><option>Q4</option>
    </select>
  </div>

  <div class="fg"><label>Month</label>
    <select id="fMo" onchange="go()"><option value="all">All Months</option></select>
  </div>

  <div class="fg"><label>Product</label>
    <select id="fPr" onchange="go()"><option value="all">All Products</option></select>
  </div>

  <div class="fg"><label>Region</label>
    <select id="fRg" onchange="go()"><option value="all">All Regions</option></select>
  </div>

  <div class="fg"><label>Category</label>
    <select id="fCa" onchange="go()"><option value="all">All Categories</option></select>
  </div>

  <div class="fg"><label>Sales Rep</label>
    <select id="fRp" onchange="go()"><option value="all">All Reps</option></select>
  </div>

  <div class="fg"><label>Min Revenue</label>
    <select id="fMr" onchange="go()">
      <option value="0">No minimum</option>
      <option value="5000">$5,000+</option>
      <option value="10000">$10,000+</option>
      <option value="20000">$20,000+</option>
      <option value="50000">$50,000+</option>
    </select>
  </div>

  <button class="btn-g" onclick="reset()" style="align-self:flex-end;">&#10005; Reset</button>
  <div class="filter-status" id="fstat">Showing all 500 records</div>
</div>

<div class="main">

  <!-- KPI CARDS -->
  <div class="kpi-row">
    <div class="kpi" style="--kc:var(--accent)">
      <div class="kpi-label">Total Revenue</div>
      <div class="kpi-value" id="kR">-</div>
      <div class="kpi-delta neu" id="kRd"></div>
    </div>
    <div class="kpi" style="--kc:var(--green)">
      <div class="kpi-label">Total Profit</div>
      <div class="kpi-value" id="kP">-</div>
      <div class="kpi-delta" id="kPd"></div>
    </div>
    <div class="kpi" style="--kc:var(--orange)">
      <div class="kpi-label">Profit Margin</div>
      <div class="kpi-value" id="kM">-</div>
      <div class="kpi-delta" id="kMd"></div>
    </div>
    <div class="kpi" style="--kc:var(--purple)">
      <div class="kpi-label">Transactions</div>
      <div class="kpi-value" id="kT">-</div>
      <div class="kpi-delta neu" id="kTd"></div>
    </div>
  </div>

  <!-- ROW 2: Revenue vs Cost | Margin -->
  <div class="g2">
    <div class="card">
      <h3>Monthly Revenue vs Cost &amp; Profit <span class="badge">FY 2025</span></h3>
      <div class="cw" style="height:240px"><canvas id="cRC"></canvas></div>
    </div>
    <div class="card">
      <h3>Profit Margin % by Month</h3>
      <div class="cw" style="height:240px"><canvas id="cMg"></canvas></div>
    </div>
  </div>

  <!-- ROW 3: Products | Region | Category -->
  <div class="g3">
    <div class="card">
      <h3>Top-Performing Products by Revenue</h3>
      <div class="cw" style="height:220px"><canvas id="cPr"></canvas></div>
    </div>
    <div class="card">
      <h3>Revenue by Region</h3>
      <div class="cw" style="height:220px"><canvas id="cRg"></canvas></div>
    </div>
    <div class="card">
      <h3>Category Share</h3>
      <div class="cw" style="height:220px"><canvas id="cCa"></canvas></div>
    </div>
  </div>

  <!-- ROW 4: Units by Quarter | Rep Performance -->
  <div class="g2">
    <div class="card">
      <h3>Units Sold by Product &amp; Quarter</h3>
      <div class="cw" style="height:220px"><canvas id="cUn"></canvas></div>
    </div>
    <div class="card">
      <h3>Sales Rep Revenue Performance</h3>
      <div class="cw" style="height:220px"><canvas id="cRep"></canvas></div>
    </div>
  </div>

  <!-- TRANSACTION TABLE -->
  <div class="card">
    <h3>Transaction Details <span class="badge" id="tbadge">top 50</span></h3>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th onclick="srt(0)">Date &#8597;</th>
            <th onclick="srt(1)">Product &#8597;</th>
            <th onclick="srt(2)">Category &#8597;</th>
            <th onclick="srt(3)">Region &#8597;</th>
            <th onclick="srt(4)">Sales Rep &#8597;</th>
            <th onclick="srt(5)" style="text-align:right">Units &#8597;</th>
            <th onclick="srt(6)" style="text-align:right">Revenue &#8597;</th>
            <th onclick="srt(7)" style="text-align:right">Cost &#8597;</th>
            <th onclick="srt(8)" style="text-align:right">Profit &#8597;</th>
            <th onclick="srt(9)" style="text-align:right">Margin &#8597;</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
  </div>

</div>
<div class="footer">Sales &amp; Revenue Analysis Dashboard &nbsp;&middot;&nbsp; Chart.js + PapaParse &nbsp;&middot;&nbsp; Thiranex Internship &nbsp;&middot;&nbsp; Thaariha</div>

<script>
const SAMPLE = DATA_PLACEHOLDER;

const PAL = ["#388bfd","#3fb950","#d29922","#bc8cff","#f85149","#39c5cf","#ffa657","#ff7b72"];
const MO  = ["January","February","March","April","May","June","July","August","September","October","November","December"];

let all = [...SAMPLE], fil = [...all], sc = 6, sd = -1;
const ch = {};

const $ = id => document.getElementById(id);
const fm = v => v >= 1e6 ? "$"+(v/1e6).toFixed(2)+"M" : v >= 1e3 ? "$"+(v/1e3).toFixed(1)+"K" : "$"+v.toFixed(0);
const pct = v => v.toFixed(1)+"%";

function fillSel(id, vals) {
  const s = $(id), cur = s.value;
  [...s.options].filter(o=>o.value!=="all").forEach(o=>o.remove());
  [...new Set(vals)].sort().forEach(v => {
    const o = document.createElement("option");
    o.value = o.textContent = v;
    s.appendChild(o);
  });
  if([...s.options].some(o=>o.value===cur)) s.value = cur;
}

function populateSels(data) {
  fillSel("fMo", data.map(r=>r.Month));
  fillSel("fPr", data.map(r=>r.Product));
  fillSel("fRg", data.map(r=>r.Region));
  fillSel("fCa", data.map(r=>r.Category));
  fillSel("fRp", data.map(r=>r.Sales_Rep));
}

function go() {
  const q  = $("fQ").value,  mo = $("fMo").value, pr = $("fPr").value,
        rg = $("fRg").value, ca = $("fCa").value, rp = $("fRp").value,
        mr = parseFloat($("fMr").value)||0;
  fil = all.filter(r =>
    (q==="all"||r.Quarter===q) && (mo==="all"||r.Month===mo) &&
    (pr==="all"||r.Product===pr) && (rg==="all"||r.Region===rg) &&
    (ca==="all"||r.Category===ca) && (rp==="all"||r.Sales_Rep===rp) &&
    r.Revenue>=mr
  );
  $("fstat").textContent = "Showing "+fil.length.toLocaleString()+" of "+all.length.toLocaleString()+" records";
  renderAll();
}

function reset() {
  ["fQ","fMo","fPr","fRg","fCa","fRp"].forEach(id=>$(id).value="all");
  $("fMr").value="0"; go();
}

function grpSum(data,key,val) {
  const m={};
  data.forEach(r=>{m[r[key]]=(m[r[key]]||0)+r[val];});
  return m;
}

function moAgg(data) {
  const rv={},cs={},pf={};
  data.forEach(r=>{
    rv[r.Month]=(rv[r.Month]||0)+r.Revenue;
    cs[r.Month]=(cs[r.Month]||0)+r.Cost;
    pf[r.Month]=(pf[r.Month]||0)+r.Profit;
  });
  const mo=MO.filter(m=>rv[m]);
  return {mo, rv:mo.map(m=>rv[m]), cs:mo.map(m=>cs[m]), pf:mo.map(m=>pf[m])};
}

function mkChart(id,cfg) {
  if(ch[id]) ch[id].destroy();
  ch[id] = new Chart($(id).getContext("2d"), cfg);
}

const gx = {ticks:{color:"#8b949e",font:{size:10}},grid:{color:"#21262d"}};
const gy = {ticks:{color:"#8b949e",font:{size:10},callback:v=>fm(v)},grid:{color:"#21262d"}};
const leg = {labels:{color:"#e6edf3",font:{size:10}}};

function renderKPIs() {
  const rv = fil.reduce((s,r)=>s+r.Revenue,0);
  const pf = fil.reduce((s,r)=>s+r.Profit,0);
  const mg = rv>0?pf/rv*100:0;
  const tx = fil.length;
  const un = fil.reduce((s,r)=>s+r.Units_Sold,0);
  $("kR").textContent=fm(rv);
  $("kP").textContent=fm(pf);
  $("kM").textContent=pct(mg);
  $("kT").textContent=tx.toLocaleString();
  $("kRd").textContent=un.toLocaleString()+" units sold";
  $("kPd").className="kpi-delta "+(mg>=35?"pos":"neg");
  $("kPd").textContent="Avg "+fm(pf/Math.max(tx,1))+" / txn";
  $("kMd").className="kpi-delta "+(mg>=35?"pos":"neg");
  $("kMd").textContent=mg>=35?"▲ Healthy margin":"▼ Below 35% target";
  $("kTd").textContent="Avg rev "+fm(rv/Math.max(tx,1))+" / txn";
}

function renderRC() {
  const {mo,rv,cs,pf}=moAgg(fil);
  mkChart("cRC",{type:"bar",data:{labels:mo.map(m=>m.slice(0,3)),datasets:[
    {label:"Revenue",data:rv,backgroundColor:"rgba(56,139,253,.8)",borderRadius:4,order:2},
    {label:"Cost",data:cs,backgroundColor:"rgba(248,81,73,.7)",borderRadius:4,order:3},
    {label:"Profit",data:pf,type:"line",borderColor:"#3fb950",backgroundColor:"rgba(63,185,80,.12)",
     pointBackgroundColor:"#3fb950",tension:.35,fill:true,pointRadius:3,borderWidth:2.2,order:1}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:leg},scales:{x:gx,y:gy}}});
}

function renderMg() {
  const {mo,rv,pf}=moAgg(fil);
  const mg=rv.map((r,i)=>r>0?+(pf[i]/r*100).toFixed(1):0);
  const avg=mg.length?mg.reduce((a,b)=>a+b,0)/mg.length:0;
  mkChart("cMg",{type:"line",data:{labels:mo.map(m=>m.slice(0,3)),datasets:[
    {label:"Margin %",data:mg,borderColor:"#d29922",backgroundColor:"rgba(210,153,34,.15)",
     fill:true,tension:.4,pointRadius:4,pointBackgroundColor:"#d29922",borderWidth:2.5},
    {label:"Avg "+avg.toFixed(1)+"%",data:mo.map(()=>+avg.toFixed(1)),
     borderColor:"rgba(248,81,73,.55)",borderDash:[5,3],pointRadius:0,borderWidth:1.5}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:leg},
    scales:{x:gx,y:{ticks:{color:"#8b949e",font:{size:10},callback:v=>v+"%"},grid:{color:"#21262d"}}}}});
}

function renderPr() {
  const g=grpSum(fil,"Product","Revenue");
  const s=Object.entries(g).sort((a,b)=>b[1]-a[1]);
  mkChart("cPr",{type:"bar",data:{labels:s.map(x=>x[0]),datasets:[
    {label:"Revenue",data:s.map(x=>x[1]),backgroundColor:PAL,borderRadius:5}
  ]},options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false}},
    scales:{x:{...gx,...{ticks:{color:"#8b949e",font:{size:10},callback:v=>fm(v)}}},
            y:{ticks:{color:"#e6edf3",font:{size:10}},grid:{display:false}}}}});
}

function renderRg() {
  const g=grpSum(fil,"Region","Revenue");
  const s=Object.entries(g).sort((a,b)=>b[1]-a[1]);
  mkChart("cRg",{type:"bar",data:{labels:s.map(x=>x[0]),datasets:[
    {label:"Revenue",data:s.map(x=>x[1]),backgroundColor:PAL,borderRadius:5}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
    scales:{x:gx,y:gy}}});
}

function renderCa() {
  const g=grpSum(fil,"Category","Revenue");
  const s=Object.entries(g).sort((a,b)=>b[1]-a[1]);
  mkChart("cCa",{type:"doughnut",data:{labels:s.map(x=>x[0]),datasets:[
    {data:s.map(x=>x[1]),backgroundColor:PAL,borderColor:"#1c2128",borderWidth:2,hoverOffset:6}
  ]},options:{responsive:true,maintainAspectRatio:false,cutout:"60%",
    plugins:{legend:{position:"right",labels:{color:"#e6edf3",font:{size:9.5},padding:8,
      generateLabels(c){return c.data.labels.map((l,i)=>({
        text:l+" — "+fm(c.data.datasets[0].data[i]),fillStyle:PAL[i],
        strokeStyle:"#1c2128",lineWidth:1,index:i}));}}}}}});
}

function renderUn() {
  const prods=[...new Set(fil.map(r=>r.Product))].sort();
  const qs=["Q1","Q2","Q3","Q4"].filter(q=>fil.some(r=>r.Quarter===q));
  const ds=prods.map((p,i)=>({
    label:p,data:qs.map(q=>fil.filter(r=>r.Product===p&&r.Quarter===q).reduce((s,r)=>s+r.Units_Sold,0)),
    backgroundColor:PAL[i%PAL.length],borderRadius:3
  }));
  mkChart("cUn",{type:"bar",data:{labels:qs,datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:leg},
      scales:{x:{stacked:true,...gx,grid:{display:false}},y:{stacked:true,ticks:{color:"#8b949e",font:{size:10}},grid:{color:"#21262d"}}}}});
}

function renderRep() {
  const g=grpSum(fil,"Sales_Rep","Revenue");
  const s=Object.entries(g).sort((a,b)=>b[1]-a[1]);
  mkChart("cRep",{type:"bar",data:{labels:s.map(x=>x[0].split(" ")[0]),datasets:[
    {label:"Revenue",data:s.map(x=>x[1]),backgroundColor:PAL,borderRadius:5}
  ]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},
    scales:{x:{ticks:{color:"#e6edf3",font:{size:10}},grid:{display:false}},y:gy}}});
}

function renderTable() {
  const keys=["Date","Product","Category","Region","Sales_Rep","Units_Sold","Revenue","Cost","Profit"];
  const rows=[...fil].sort((a,b)=>{
    const k=keys[sc];
    return typeof a[k]==="string"?a[k].localeCompare(b[k])*sd:(a[k]-b[k])*sd;
  }).slice(0,50);
  const ct={Software:"tsw",Services:"tsv",Consulting:"tcn",Support:"tsp",Hardware:"tsw"};
  $("tbadge").textContent="showing top "+rows.length+" of "+fil.length;
  $("tbody").innerHTML=rows.map(r=>{
    const mg=r.Revenue>0?(r.Profit/r.Revenue*100).toFixed(1)+"%":"—";
    const mc=parseFloat(mg)>=35?"color:var(--green)":"color:var(--red)";
    return "<tr><td>"+r.Date+"</td><td><b>"+r.Product+"</b></td>"+
      "<td><span class='tag "+(ct[r.Category]||"tsw")+"'>"+r.Category+"</span></td>"+
      "<td>"+r.Region+"</td><td>"+r.Sales_Rep+"</td>"+
      "<td style='text-align:right'>"+r.Units_Sold+"</td>"+
      "<td style='text-align:right;color:var(--accent)'><b>"+fm(r.Revenue)+"</b></td>"+
      "<td style='text-align:right;color:var(--sub)'>"+fm(r.Cost)+"</td>"+
      "<td style='text-align:right;color:var(--green)'>"+fm(r.Profit)+"</td>"+
      "<td style='text-align:right;"+mc+"'>"+mg+"</td></tr>";
  }).join("");
}

function srt(col){sc=col;sd*=-1;renderTable();}

function renderAll(){renderKPIs();renderRC();renderMg();renderPr();renderRg();renderCa();renderUn();renderRep();renderTable();}

function handleImport(e) {
  const file=e.target.files[0]; if(!file)return;
  $("fileStatus").textContent="Parsing "+file.name+"...";
  Papa.parse(file,{header:true,dynamicTyping:true,skipEmptyLines:true,complete(res){
    if(!res.data.length){$("fileStatus").textContent="Error: empty file.";return;}
    all=res.data.map(r=>({
      Date:r.Date||r.date||"", Month:r.Month||r.month||"",
      Quarter:r.Quarter||r.quarter||"", Product:r.Product||r.product||r.Product_Name||"",
      Category:r.Category||r.category||"", Region:r.Region||r.region||"",
      Sales_Rep:r.Sales_Rep||r.SalesRep||r.Rep||"",
      Units_Sold:+(r.Units_Sold||r.Units||r.Qty||0),
      Unit_Price:+(r.Unit_Price||r.Price||0),
      Revenue:+(r.Revenue||r.revenue||r.Sales||0),
      Cost:+(r.Cost||r.cost||0),
      Profit:+(r.Profit||r.profit||(r.Revenue-r.Cost)||0),
      Discount:+(r.Discount||r.discount||0)
    }));
    $("fileStatus").textContent="Loaded "+all.length+" rows from "+file.name;
    populateSels(all); reset();
  },error(err){$("fileStatus").textContent="Error: "+err.message;}});
}

function exportCSV() {
  const hdr=["Date","Product","Category","Region","Sales_Rep","Units_Sold","Revenue","Cost","Profit"];
  const rows=[hdr.join(",")].concat(fil.map(r=>hdr.map(h=>r[h]).join(",")));
  const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([rows.join("\\n")],{type:"text/csv"}));
  a.download="filtered_sales_data.csv"; a.click();
}

$("lastUpd").textContent="Updated "+new Date().toLocaleDateString("en-IN",{day:"2-digit",month:"short",year:"numeric"});
populateSels(all);
go();
</script>
</body>
</html>"""

# Inject data
html = html.replace("DATA_PLACEHOLDER", payload)

with open("/mnt/user-data/outputs/sales_dashboard.html","w") as f:
    f.write(html)

print("Done! Size:", len(html), "bytes")
print("Rows embedded:", len(df))
