import fs from 'node:fs/promises';
import path from 'node:path';
import { Presentation, PresentationFile } from '@oai/artifact-tool';
import { pathToFileURL, fileURLToPath } from 'node:url';
import os from 'node:os';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const outDir = path.join(root, 'publications/industry-engagement/moove_bayesian_2026-10-14');
const chartDir = path.join(outDir, 'charts');
const buildDir = path.join(root, '.build/moove_bayesian_2026-10-14');
const skillDir = process.env.PRESENTATIONS_SKILL_DIR || path.join(os.homedir(), '.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations');
const finalPptx = path.join(outDir, 'BAYESIAN_RELATIVITIES_X_MOOVE_RESEARCH_PARTNERSHIP_DECK_2026-10-14_V3.pptx');
const finalPdf = path.join(outDir, 'BAYESIAN_RELATIVITIES_X_MOOVE_RESEARCH_PARTNERSHIP_DECK_2026-10-14_V3.pdf');
const finalizerReceipt = path.join(buildDir, 'BAYESIAN_RELATIVITIES_X_MOOVE_DECK_V3.validation.json');

const chartBytes = new Map();
for (const name of [
  'FIGURE_01_BAYESIAN_RELATIVITIES_90CI.png',
  'FIGURE_02_TARIFF_ALLOCATION_VS_FLAT_PREMIUM.png',
  'FIGURE_03_INSURER_PROFIT_TEST_WITH_90CI.png',
  'FIGURE_04_REPAIR_DOWNTIME_AND_DRIVER_CASH.png',
]) chartBytes.set(name, new Uint8Array(await fs.readFile(path.join(chartDir,name))));

const summary = JSON.parse(await fs.readFile(path.join(root, 'research_lab/mobility_insurance_profit_case/output/summary.json'), 'utf8'));
const outputs = summary.simulation_summaries;
const p = summary.pricing_and_normalisation;
const stable = p.groups.stable;
const volatile = p.groups.volatile;
const flat = outputs.flat;
const treatment = outputs.intervention;
const flatOps = flat.moove_driver_standard_repair_12_days;
const treatOps = treatment.moove_driver_standard_repair_12_days;
const fastOps = flat.moove_driver_standard_repair_2_days;
const fmt = (n, d=0) => Number(n).toLocaleString('en-US', {minimumFractionDigits:d, maximumFractionDigits:d});
const m = n => (Number(n)/1e6).toFixed(3);

const C = {
  navy: '#102A43', ink: '#17324A', teal: '#0E8A8A', gold: '#E2A93B', blue: '#4F78A8',
  muted: '#526777', pale: '#EEF4F7', bg: '#FAFCFD', white: '#FFFFFF', grid: '#D9E2E8',
  red: '#B84B4B', green: '#297C68', lightTeal: '#DDEFEF', lightGold: '#F7EBCB',
};
const W = 1280, H = 720;
const pres = Presentation.create({ slideSize: { width: W, height: H } });

function addRect(slide, x, y, w, h, fill, name, opts={}) {
  return slide.shapes.add({
    geometry: opts.geometry || 'rect', name,
    position: { left:x, top:y, width:w, height:h }, fill,
    line: opts.line || { style:'solid', fill:'none', width:0 },
    ...(opts.borderRadius ? {borderRadius:opts.borderRadius} : {}),
  });
}
function addText(slide, x, y, w, h, str, size=24, color=C.ink, opts={}) {
  const s = slide.shapes.add({
    geometry:'textbox', name:opts.name || `text-${Math.random().toString(36).slice(2,8)}`,
    position:{left:x,top:y,width:w,height:h}, fill:'none',
    line:{style:'solid',fill:'none',width:0},
  });
  s.text = str;
  s.text.style = {
    fontSize:size, typeface:'Arial', color, bold:!!opts.bold,
    alignment:opts.align || 'left', verticalAlignment:opts.valign || 'top',
    wrap:'square', autoFit:'shrinkText', insets:opts.insets ?? 0,
    ...(opts.lineSpacing ? {lineSpacing:opts.lineSpacing} : {}),
  };
  return s;
}
function addImage(slide, imagePath, x, y, w, h, alt) {
  const name=path.basename(imagePath);
  return slide.images.add({blob:chartBytes.get(name),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});
}
function base(title, section, subtitle='') {
  const s = pres.slides.add();
  s.background.fill=C.bg;
  addRect(s,0,0,W,11,C.teal,'brand-rule');
  addText(s,70,28,900,22,section.toUpperCase(),14,C.teal,{bold:true,name:'section-label'});
  addText(s,70,61,1130,62,title,43,C.navy,{bold:true,name:'slide-title'});
  if (subtitle) addText(s,72,125,1120,38,subtitle,21,C.muted,{name:'slide-subtitle'});
  addRect(s,70,676,1140,1,C.grid,'footer-rule');
  addText(s,70,684,1030,20,'Research partnership proposal · Illustrative synthetic KES case · 14 Oct 2026',13,C.muted,{name:'footer'});
  addText(s,1150,684,60,20,String(pres.slides.items.length).padStart(2,'0'),13,C.muted,{align:'right',name:'page-number'});
  return s;
}
function note(slide, txt) { slide.speakerNotes.text = txt; }
function bullet(slide, x, y, w, text, opts={}) {
  addRect(slide,x,y+9,9,9,opts.dot || C.teal,`bullet-dot-${y}`,{geometry:'ellipse'});
  addText(slide,x+24,y,w-24,opts.h || 64,text,opts.size || 23,opts.color || C.ink,{bold:!!opts.bold,name:`bullet-${y}`});
}
function labelPill(slide,x,y,w,text,fill=C.lightTeal,color=C.teal) {
  addRect(slide,x,y,w,30,fill,`pill-bg-${x}-${y}`,{geometry:'roundRect',borderRadius:12});
  addText(slide,x+10,y+4,w-20,22,text,14,color,{bold:true,align:'center',name:`pill-${x}-${y}`});
}
function arrow(slide,x1,y1,x2,y2,color=C.teal,width=4) {
  const dx=x2-x1,dy=y2-y1;
  if(Math.abs(dy)<4) {
    addRect(slide,x1,y1-width/2,dx-12,width,color,`arrow-line-${x1}-${y1}`);
    slide.shapes.add({geometry:'triangle',name:`arrow-head-${x1}-${y1}`,position:{left:x2-20,top:y2-10,width:20,height:20,rotation:90},fill:color,line:{style:'solid',fill:'none',width:0}});
  } else {
    slide.shapes.add({geometry:'line',name:`connector-${x1}-${y1}`,position:{left:x1,top:y1,width:dx,height:dy},fill:'none',line:{style:'solid',fill:color,width}});
  }
}
function callout(slide,x,y,w,h,heading,body,accent=C.teal) {
  addRect(slide,x,y,w,5,accent,`callout-rule-${x}-${y}`);
  addText(slide,x,y+15,w,h*.30,heading,23,C.navy,{bold:true,name:`callout-heading-${x}-${y}`});
  addText(slide,x,y+49,w,h-49,body,20,C.ink,{name:`callout-body-${x}-${y}`});
}

// 1 · Cover
{
  const s=pres.slides.add(); s.background.fill=C.navy;
  addRect(s,0,0,18,H,C.teal,'cover-side-rule');
  addText(s,84,68,1060,28,'RESEARCH PARTNERSHIP PROPOSAL  /  14 OCTOBER 2026',16,'#6ED2CC',{bold:true,name:'cover-kicker'});
  addText(s,84,162,1050,154,'Bayesian Relativities\n× Mobility Insurance Profit Testing',58,C.white,{bold:true,name:'cover-title'});
  addText(s,88,356,860,88,'A worked, auditable KES illustration for mobility fleets, insurance partners and driver outcomes',26,'#D4E2EC',{name:'cover-subtitle'});
  addRect(s,88,493,448,76,'#1C415B','cover-label-bg',{geometry:'roundRect',borderRadius:18});
  addText(s,112,511,404,42,'Illustrative synthetic case · 100 vehicles · 12 months',19,C.white,{bold:true,name:'cover-case-label'});
  addText(s,88,638,1060,26,'Prepared from the Bayesian Relativities paper and its reproducible research case',16,'#B8CAD7',{name:'cover-source'});
  note(s,'Opening: this is a research partnership proposal, not an offer, quote, or claim about Moove’s own performance. All KES results are synthetic. The public Moove context is cited in the notes and in the source slide.');
}

// 2 · Three research questions
{
  const s=base('Can risk, uptime and driver cash improve together?','PARTNERSHIP QUESTION','The proposed work joins actuarial evidence with vehicle operations and driver economics.');
  const q=[
    ['01','Risk','How can exposure, claims and vehicle-use data produce credible estimates of expected loss with useful uncertainty?'],
    ['02','Intervention','Which combination of insurance design, safety support, repairs and incentives changes outcomes over time?'],
    ['03','Profit test','How do claim development, reinsurance, capital, operating costs and customer cash shape full-term value?'],
  ];
  q.forEach((it,i)=>{
    const y=204+i*137;
    addText(s,82,y,76,58,it[0],35,C.teal,{bold:true,name:`question-number-${i}`});
    addText(s,174,y,260,36,it[1],26,C.navy,{bold:true,name:`question-label-${i}`});
    addText(s,174,y+42,980,75,it[2],23,C.ink,{name:`question-text-${i}`});
    if(i<2)addRect(s,174,y+116,970,1,C.grid,`question-separator-${i}`);
  });
  note(s,'These three questions structure the article and proposed collaboration. They separate estimation, intervention evaluation and commercial sustainability. Sources: [1]–[7] in the source notes.');
}

// 3 · Application context
{
  const s=base('Moove’s public mobility context motivates a test','PUBLIC OPERATING CONTEXT','Public product and CGAP material motivate the question; the case uses synthetic KES assumptions.');
  callout(s,80,204,500,178,'Public product context','Moove UK describes vehicle access with weekly payments and packages that include insurance and servicing. Market, contract and payer determine the actual economics.',C.blue);
  callout(s,700,204,500,178,'Research motivation','A 2023 CGAP study discusses use of gig-work data in expanding access to credit and includes Moove. That motivates careful evidence design for mobile work.',C.teal);
  arrow(s,587,291,686,291,C.gold,5);
  addText(s,85,432,1100,100,'What is proposed: test whether exposure-normalised insurance estimates, service reliability and driver outcomes can be assessed together using a jointly defined market and dataset.',26,C.navy,{bold:true,name:'application-proposition'});
  labelPill(s,85,565,205,'UK public example',C.pale,C.blue);
  labelPill(s,310,565,196,'Kenya KES case',C.lightGold,'#946A12');
  labelPill(s,526,565,270,'Synthetic KES illustration',C.lightTeal,C.teal);
  addText(s,85,615,1110,36,'Sources: CGAP [1]; Moove UK Customer Hub [2]; Moove UK Privacy Policy [3].',17,C.muted,{name:'source-cue'});
  note(s,'The public sources establish the business context and publicly described data classes. They do not establish current terms for a different market, insured portfolio results, pricing, driver outcomes or causal effects. A partner would select the target market and appropriate insurer/product. [1] M. Anand and G. Murthy, CGAP, 2023. [2] Moove UK Customer Hub. [3] Moove UK Privacy Policy.');
}

// 4 · Research workstreams
{
  const s=base('Three workstreams connect into a Moove test','RESEARCH ARCHITECTURE','Each workstream supplies a distinct analytical input.');
  const xs=[72,372,672,972]; const ws=230; const y=250; const h=224;
  const items=[
    ['Bayesian\nRelativities','Expected loss, exposure,\nposterior uncertainty',C.blue],
    ['Mwendo\nPamoja','Vehicle operation, finance,\nreceivables and downtime',C.teal],
    ['Underwrite for\nCollection','Decision timing, experiments,\nservicing and realised cash',C.gold],
    ['Potential\nMoove application','Market-specific insurance,\noperations and driver outcomes',C.navy],
  ];
  items.forEach((it,i)=>{
    addRect(s,xs[i],y,ws,h,C.white,`workstream-bg-${i}`,{line:{style:'solid',fill:C.grid,width:2},geometry:'roundRect',borderRadius:18});
    addRect(s,xs[i],y,ws,8,it[2],`workstream-accent-${i}`);
    addText(s,xs[i]+17,y+28,ws-34,69,it[0],25,it[2],{bold:true,name:`workstream-title-${i}`});
    addText(s,xs[i]+17,y+113,ws-34,75,it[1],20,C.ink,{name:`workstream-body-${i}`});
    if(i<3) arrow(s,xs[i]+ws+5,y+113,xs[i+1]-8,y+113,C.muted,3);
  });
  addText(s,84,525,1110,80,'Explicit data definitions, decision rights and outcome measures connect model evidence to approved market decisions and customer terms.',22,C.muted,{name:'architecture-principle'});
  note(s,'This is a proposed research architecture. Bayesian Relativities estimates risk distributions; Mwendo Pamoja connects financing and vehicle operating flows; Underwrite for Collection contributes evidence governance and intervention evaluation. The Moove lane denotes a possible application, subject to partnership and local terms. Sources: Bayesian Relativities paper [5]; Underwrite for Collection and Mwendo materials supplied in the shared project corpus.');
}

// 5 · Pricing model
{
  const s=base('Price expected loss from exposure, frequency and severity','ACTUARIAL MODEL','Keep exposure, underlying expected loss and commercial premium visible as separate quantities.');
  addText(s,86,205,1090,66,'ELᵢₜ = Eᵢₜ × λ₀ × θᵢₜ × μ₀ × ωᵢₜ  +  Lᵢₜ⁽non-drive⁾',34,C.navy,{bold:true,align:'center',name:'expected-loss-equation'});
  const nodes=[
    [82,'Exposure','km / covered days'],[360,'Frequency','claims per unit'],[638,'Severity','cost given claim'],[916,'Expected loss','risk estimate'],
  ];
  nodes.forEach((it,i)=>{
    const [x,t,sub]=it;
    addRect(s,x,326,230,106,C.white,`pricing-node-${i}`,{geometry:'roundRect',borderRadius:16,line:{style:'solid',fill:C.grid,width:2}});
    addText(s,x+15,347,200,34,t,24,C.teal,{bold:true,align:'center',name:`pricing-label-${i}`});
    addText(s,x+15,386,200,26,sub,18,C.muted,{align:'center',name:`pricing-sub-${i}`});
    if(i<3) arrow(s,x+238,379,x+268,379,C.gold,3);
  });
  addRect(s,82,492,1090,83,C.pale,'premium-layer-bg',{geometry:'roundRect',borderRadius:18});
  addText(s,105,507,1026,60,'Commercial premium = expected loss + claim / operating expense + reinsurance + capital + tax + approved margin',24,C.ink,{bold:true,align:'center',name:'premium-bridge'});
  addText(s,88,603,1085,34,'qᵢ is an exposure-normalised risk relativity; the insurer applies it within approved premium terms and profit tests.',20,C.muted,{name:'tariff-definition'});
  note(s,'Equation terms: E is insured exposure; λ₀ is base claim frequency; θ is a frequency relativity; μ₀ is base severity; ω is severity relativity; L(non-drive) represents separately modelled non-driving expected losses. The specific model permits frequency–severity dependence, so joint posterior draws are used where appropriate. [4] Lee and Shi, 2019; [5] Bayesian Relativities paper.');
}

// 6 · Hierarchical Bayesian credibility
{
  const s=base('Partial pooling supports credible risk estimates','POSTERIOR DESIGN','Cohort experience informs individual estimates as relevant exposure and mature claims accumulate.');
  addText(s,85,213,500,50,'Frequency model',27,C.navy,{bold:true,name:'frequency-model-title'});
  addText(s,85,269,520,72,'Nᵢ | θᵢ  ~  Poisson(Eᵢ λ₀ θᵢ)',29,C.teal,{bold:true,name:'frequency-likelihood'});
  addText(s,85,345,520,72,'θᵢ  ~  Gamma(a, b)',29,C.teal,{bold:true,name:'frequency-prior'});
  addText(s,85,421,520,74,'θᵢ | Nᵢ,Eᵢ  ~  Gamma(a + Nᵢ, b + Eᵢ λ₀)',23,C.ink,{name:'frequency-posterior'});
  addRect(s,650,205,2,340,C.grid,'model-divider');
  bullet(s,700,222,480,'Severity is modelled separately, then combined with frequency draws.',{size:22,h:65});
  bullet(s,700,316,480,'Group structure enables partial pooling across driver, vehicle, territory and time.',{size:22,h:65});
  bullet(s,700,410,480,'Review outputs include posterior intervals and future-claim predictive ranges.',{size:22,h:65});
  addText(s,85,566,1100,52,'Useful outputs: calibrated relativities · exposure support · posterior uncertainty · predictive loss · refresh lineage',21,C.muted,{name:'posterior-outputs'});
  note(s,'The frequency illustration uses Gamma–Poisson conjugacy. Severity updates use the case’s inverse-Gamma/Gamma model. Partial pooling links individual experience to group-level information; the credible interval describes uncertainty in underlying expected loss, while a predictive interval additionally includes random future claims. This supports human review with distributions, not just a point score. [5]–[7].');
}

// 7 · Posterior intervals
{
  const s=base('Credible intervals show group risk and uncertainty','POSTERIOR RESULTS','Draw-wise calibrated joint expected-loss relativities · synthetic 100-vehicle case');
  addImage(s,path.join(chartDir,'FIGURE_01_BAYESIAN_RELATIVITIES_90CI.png'),60,180,760,427,'Forest plot of stable and volatile calibrated relativities with 90 percent credible intervals');
  callout(s,850,205,340,140,'Stable cohort','0.711 factor\n90% CrI: 0.561–0.859',C.blue);
  callout(s,850,370,340,140,'Volatile cohort','1.674 factor\n90% CrI: 1.329–2.023',C.teal);
  addText(s,850,545,340,67,'The intervals quantify model uncertainty; future claims also vary around expected loss.',20,C.muted,{name:'interval-note'});
  note(s,'The posterior means are frequency factors 0.7843 / 1.5401 and severity factors 0.9462 / 1.1340. Joint factors are calibrated draw-wise to a portfolio mean of one. Reported 90% intervals: stable 0.561–0.859; volatile 1.329–2.023. These are synthetic case results based on selected priors and claim summaries; they are not Moove pricing indicators. Sources: Bayesian Relativities paper [5], Belhadj et al. [6], Bühlmann [7].');
}

// 8 · Tariff differentiation
{
  const s=base('Neutral rates change allocation, not total loss','TARIFF INTERPRETATION','Exposure-weighted average stays KES 130,000; the commercial layer is held constant in this comparison.');
  addImage(s,path.join(chartDir,'FIGURE_02_TARIFF_ALLOCATION_VS_FLAT_PREMIUM.png'),55,183,760,425,'Bar chart comparing stable and volatile neutral tariffs to the flat KES 130000 portfolio premium');
  bullet(s,850,222,348,'Stable indicated premium: KES 113,988',{size:22,h:52,dot:C.blue});
  bullet(s,850,306,348,'Volatile indicated premium: KES 167,360',{size:22,h:52,dot:C.teal});
  bullet(s,850,390,348,'70% × stable + 30% × volatile = KES 130,000',{size:21,h:75,dot:C.gold});
  addText(s,850,500,348,100,'Risk-tier prices are illustrative allocations. Contract terms, taxes and expenses would need market-specific calibration.',20,C.muted,{name:'tariff-note'});
  note(s,'Group premiums are KES 113,988 and KES 167,360, weighted 70/30 to KES 130,000. In the profit test, flat and neutral designs have identical aggregate premium and claims distributions: neutral differentiation reallocates expected loss, not portfolio risk. It may affect participation, retention or selection in practice, which should be tested separately. [5]–[7].');
}

// 9 · intervention and causal separation
{
  const s=base('Treat safety and service effects as hypotheses to test','INTERVENTION DESIGN','Separate a pricing allocation from an action that is expected to change claim frequency.');
  const boxes=[
    [84,'Relativity','Reallocates expected loss\nwithin selected portfolio',C.blue],
    [448,'Intervention','Safety / service support\nmay change behaviour',C.gold],
    [812,'Observed outcome','Exposure-adjusted claims,\ndowntime and driver cash',C.teal],
  ];
  boxes.forEach(([x,t,b,col],i)=>{
    addRect(s,x,245,280,142,C.white,`intervention-box-${i}`,{geometry:'roundRect',borderRadius:18,line:{style:'solid',fill:C.grid,width:2}});
    addRect(s,x,245,280,8,col,`intervention-top-${i}`);
    addText(s,x+20,273,240,38,t,25,col,{bold:true,align:'center',name:`intervention-title-${i}`});
    addText(s,x+22,321,236,57,b,20,C.ink,{align:'center',name:`intervention-body-${i}`});
    if(i<2) arrow(s,x+290,316,x+352,316,C.muted,3);
  });
  addRect(s,85,445,1110,104,C.lightGold,'assumption-strip',{geometry:'roundRect',borderRadius:14});
  addText(s,110,464,1060,67,'Sensitivity input: 10% lower volatile-group frequency. If validated, 75% of the modelled loss saving reduces premium and 25% funds an operator-paid driver incentive.',22,C.ink,{bold:true,name:'intervention-assumption'});
  addText(s,87,578,1095,51,'This effect is assumed for analysis. A pilot with mature, comparable claims estimates the treatment effect.',20,C.muted,{name:'intervention-caveat'});
  note(s,'Do not interpret the 10% frequency change as an observed or promised outcome. A lower premium or changed tariff does not itself reduce loss. The simulation separately stipulates a 10% reduction in volatile-group frequency, and allocates the expected loss saving 75% to premium reduction and 25% to an operator-funded incentive. Estimate the intervention effect from a pre-specified design. [5], [11].');
}

// 10 · three ledgers
{
  const s=base('Profit testing needs three separate ledgers','PROFIT TEST','Each party carries a different contractual cash flow, risk and decision horizon.');
  const cols=[
    [78,350,'INSURER',C.blue,'Premium · claims · expenses\nReinsurance · reserves · capital\nInvestment cash · shareholder return'],
    [465,350,'MOBILITY OPERATOR',C.teal,'Insurance cost · retained loss\nRepairs · downtime · funding\nPackage, collections · retention'],
    [852,350,'DRIVER',C.gold,'Fares · energy · package\nInsurance / excess · incentives\nWorking days · take-home cash'],
  ];
  cols.forEach(([x,w,t,col,b],i)=>{
    addRect(s,x,220,w,292,C.white,`ledger-panel-${i}`,{geometry:'roundRect',borderRadius:18,line:{style:'solid',fill:C.grid,width:2}});
    addRect(s,x,220,w,10,col,`ledger-stripe-${i}`);
    addText(s,x+22,251,w-44,40,t,22,col,{bold:true,align:'center',name:`ledger-heading-${i}`});
    addText(s,x+28,320,w-56,154,b,22,C.ink,{name:`ledger-body-${i}`});
  });
  addText(s,88,555,1100,60,'ΔCFᴹₜ = insurance savings + avoided retained losses + uptime / retention value − incentives − intervention / funding costs',20,C.navy,{bold:true,align:'center',name:'operator-cash-equation'});
  note(s,'Insurer profit after capital is a distinct result from operator contribution and driver take-home. Insurance pricing allocation belongs to the insurer-product terms; operator economics include contracted insurance costs and retention; driver economics include fees, costs, working days, incentives and take-home. Avoid adding the 156-week Mwendo financing illustration to the separate annual 100-vehicle insurance portfolio. [5], [8]–[11].');
}

// 11 · case assumptions
{
  const s=base('Synthetic KES case: 100 vehicles, 12 months','CASE DESIGN','Selected model assumptions are explicit and reproducible.');
  const stats=[
    ['Portfolio','100 vehicles · 12 months · 70% stable / 30% volatile'],
    ['History','3 synthetic years · 756 / 324 exposure units of 10,000 km'],
    ['Claims','47 stable / 41 volatile · mean severities KES 170k / 205k'],
    ['Posterior','12,000 draws · Gamma–Poisson + inverse-Gamma/Gamma severity'],
    ['Projection','8,000 predictive paths · 20% quota share · fixed seed 20261014'],
    ['Shared shock','2% probability; frequency ×1.8 and severity ×1.25 when triggered'],
  ];
  stats.forEach(([label,value],i)=>{
    const col=i%2,row=Math.floor(i/2),x=84+col*550,y=205+row*126;
    addText(s,x,y,170,33,label,18,C.teal,{bold:true,name:`case-label-${i}`});
    addText(s,x,y+37,510,67,value,21,C.ink,{name:`case-value-${i}`});
    addRect(s,x,y+105,500,1,C.grid,`case-rule-${i}`);
  });
  addText(s,86,603,1090,38,'Partner exposure, claims and contract data would calibrate a future application.',19,C.teal,{bold:true,name:'synthetic-warning'});
  note(s,'The simulation uses a three-year synthetic history. Stable cohort: 756 10,000-km exposure units, 47 claims, KES 170,000 mean severity. Volatile: 324 units, 41 claims, KES 205,000 mean severity. Posterior draws: 12,000; predictive paths: 8,000; fixed seed: 20261014. A 2% common-shock probability with frequency 1.8 and severity 1.25 yields an expected shock load of 1.025, used consistently in indication and simulation. See case README and assumptions.json.');
}

// 12 · profit testing results
{
  const s=base('Intervention improves mean profit; risk remains','INSURER LEDGER','Mean after-capital profit and predictive 90% range · 100-vehicle annual portfolio');
  addImage(s,path.join(chartDir,'FIGURE_03_INSURER_PROFIT_TEST_WITH_90CI.png'),52,185,760,426,'Profit after capital charge comparing flat neutral and intervention assumptions with predictive 90 percent intervals');
  callout(s,850,206,350,126,'Flat / neutral','Mean KES 1.307m\n90% range −1.158m to 3.434m',C.blue);
  callout(s,850,357,350,126,'Assumed intervention','Mean KES 1.442m\n90% range −1.048m to 3.518m',C.teal);
  addText(s,852,518,344,76,'Probability of loss after capital: 15.8% → 13.4%\nBreak-even gross premium: KES 107,852 → 103,473 / vehicle-year',18,C.ink,{name:'profit-kpis'});
  note(s,'Flat and neutral have identical aggregate insurer P&L. Intervention is a synthetic frequency sensitivity. Flat/neutral: mean after-capital profit KES 1.307m; 90% predictive interval −KES 1.158m to KES 3.434m; probability below zero 15.8%; break-even gross annual premium KES 107,852/vehicle. Intervention: KES 1.442m; interval −KES 1.048m to KES 3.518m; loss probability 13.4125%; break-even KES 103,473. Predictive intervals include parameter and process variation. [11] for capital/reinsurance profit-testing context; underlying case files for figures.');
}

// 13 · claims and cash timing
{
  const s=base('Claims, reserves and reinsurance run on separate cash calendars','CLAIMS AND RISK TRANSFER','Annual insurer baseline · gross ultimate claims KES 6.739m');
  const flow=[
    [82,'Gross ultimate\nclaims','KES 6.739m',C.navy],
    [380,'20% quota share','Net claims\nKES 5.391m',C.blue],
    [678,'Paid by year-end','KES 4.437m',C.teal],
    [976,'Outstanding','Reported + IBNR\nKES 2.302m',C.gold],
  ];
  flow.forEach(([x,t,v,col],i)=>{
    addRect(s,x,260,230,160,C.white,`claims-node-${i}`,{geometry:'roundRect',borderRadius:18,line:{style:'solid',fill:C.grid,width:2}});
    addRect(s,x,260,230,9,col,`claims-node-top-${i}`);
    addText(s,x+17,286,196,56,t,21,col,{bold:true,align:'center',name:`claims-title-${i}`});
    addText(s,x+14,351,202,50,v,23,C.navy,{bold:true,align:'center',name:`claims-value-${i}`});
    if(i<3) arrow(s,x+237,340,x+290,340,C.muted,3);
  });
  addText(s,85,475,1090,48,'Ceded recoverable at year-end: KES 0.683m · report lag: 1–3 months · settlement: 1–9 months (assumptions)',22,C.ink,{bold:true,name:'claims-timing-line'});
  addText(s,85,544,1080,68,'Premium, incurred claims, paid claims, reserve movement, reinsurance recovery and available cash should be projected by period and reconciled.',21,C.muted,{name:'claims-timing-note'});
  note(s,'Baseline: gross ultimate claims KES 6.739m; net claims after the 20% quota share KES 5.391m. By year-end, gross claims paid KES 4.437m, reported outstanding KES 1.462m, IBNR KES 0.840m, total outstanding KES 2.302m, ceded recoverable KES 0.683m. The model reconciles paid plus outstanding to ultimate claims (maximum error KES 0). Reporting and settlement delays are elected assumptions. Model incurred, paid and recoverable cash separately. Sources: ASOP 43 [8], IFRS 17 reinsurance guide [9], IAIS [10].');
}

// 14 · operator and driver
{
  const s=base('Repairs change fleet uptime and driver cash','OPERATOR AND DRIVER LEDGERS','Annual portfolio case · downtime is fleet-wide; take-home is per vehicle-year.');
  addImage(s,path.join(chartDir,'FIGURE_04_REPAIR_DOWNTIME_AND_DRIVER_CASH.png'),58,180,850,473,'Paired bars comparing annual fleet downtime and per vehicle driver take home for 12-day, intervention and 2-day repair scenarios');
  callout(s,940,211,258,138,'Standard service','Operator contribution\nKES 1.026m / vehicle-year',C.blue);
  callout(s,940,371,258,138,'Two-day repair','Driver take-home rises to\nKES 152,651 / vehicle-year',C.gold);
  addText(s,940,541,250,73,'Expedite cash: KES 146,871 / fleet. Operator contribution excludes vehicle capex, debt, tax and depreciation.',18,C.muted,{name:'operations-caveat'});
  note(s,'Flat standard 12-day repair case: 344.95 total fleet downtime days (3.45/vehicle); operator contribution before vehicle capex, debt, tax and depreciation KES 102.599m across the portfolio; driver take-home KES 136,289/vehicle-year. Intervention standard repair: 329.61 fleet days; contribution KES 102.673m; driver take-home KES 138,905. Flat 2-day repair scenario: 58.61 fleet downtime days; take-home KES 152,651; fleet expedite cash KES 146,871 and contribution KES 102.452m. This is a separate 100-vehicle annual case. [2] gives public package context; numbers are entirely synthetic.');
}

// 15 · tail risk and sensitivity
{
  const s=base('The 99.5% tail is a coarse illustration at 8,000 paths','MODEL RISK AND SENSITIVITY','Treat the capital lens as a scenario result; precision and calibration need further work.');
  const metrics=[
    ['VaR₉₉.₅','KES 13.093m','flat / neutral'],['TVaR₉₉.₅','KES 14.491m','flat / neutral'],
    ['Economic capital','KES 7.702m','VaR − mean net claims'],['Tail support','≈ 40 paths','upper 0.5% of 8,000'],
  ];
  metrics.forEach(([l,v,sub],i)=>{
    const x=88+(i%2)*550,y=206+Math.floor(i/2)*134;
    addText(s,x,y,230,29,l,18,C.teal,{bold:true,name:`tail-label-${i}`});
    addText(s,x,y+31,270,45,v,30,C.navy,{bold:true,name:`tail-value-${i}`});
    addText(s,x+278,y+36,240,39,sub,18,C.muted,{name:`tail-sub-${i}`});
    addRect(s,x,y+91,505,1,C.grid,`tail-rule-${i}`);
  });
  addText(s,89,492,1080,44,'Next sensitivity runs: common-shock size and frequency · reporting / settlement lag · treaty share and recovery delay · capital charge · claims maturity',20,C.ink,{name:'sensitivity-list'});
  addText(s,89,561,1090,60,'8,000 paths leave only about 40 observations beyond the 99.5th percentile. Increase runs and assess convergence before using tail values for decisions.',21,C.red,{bold:true,name:'tail-caveat'});
  note(s,'Baseline empirical 99.5% net-loss VaR: KES 13.093m; TVaR: KES 14.491m; economic capital VaR minus mean net claims: KES 7.702m. The case has 8,000 predictive paths, so only about 40 paths support the upper 0.5% tail. These are coarse illustrative economic-capital estimates, not a regulatory capital result. Required next steps include larger-run convergence checks and scenario sensitivity over common shocks, treaty terms/recovery delays, claim maturity and capital cost. [8]–[10].');
}

// 16 · experimental plan
{
  const s=base('Measure the treatment effect with a pre-specified pilot','EVALUATION PLAN','Start with the claims and operational data needed to support a fair comparison.');
  const steps=[
    ['1','Define','Eligible drivers, treatment,\nstandard service and exposure'],
    ['2','Assign','Randomise or cluster by depot;\nmaintain the agreed baseline'],
    ['3','Measure','Claims / distance, severity,\ndowntime, earnings, retention'],
    ['4','Review','Intention-to-treat effect,\nuncertainty and maturity'],
  ];
  steps.forEach(([n,t,b],i)=>{
    const x=76+i*300;
    addRect(s,x,258,235,218,C.white,`pilot-step-${i}`,{geometry:'roundRect',borderRadius:18,line:{style:'solid',fill:C.grid,width:2}});
    addText(s,x+18,278,54,43,n,30,C.gold,{bold:true,name:`pilot-num-${i}`});
    addText(s,x+73,282,142,37,t,24,C.teal,{bold:true,name:`pilot-title-${i}`});
    addText(s,x+20,345,195,100,b,20,C.ink,{name:`pilot-body-${i}`});
    if(i<3) arrow(s,x+242,363,x+288,363,C.muted,3);
  });
  addText(s,84,525,1100,76,'Pre-register endpoints, claim maturity windows, exclusions, subgroup analysis and benefit-sharing rules; report costs and customer outcomes with insurer results.',22,C.navy,{bold:true,name:'pilot-principle'});
  note(s,'A future pilot should estimate the intervention effect rather than reusing the assumed 10%. Define eligibility, intervention, treatment fidelity, exposure, claims development, comparison group and primary endpoints before launch. If driver-level randomisation is unsuitable, consider depot or time-based cluster assignment with appropriate design. Report intention-to-treat effects and uncertainty; claims must have sufficient maturity. Include customer outcomes, complaints and operational costs. [11].');
}

// 17 · implementation and governance
{
  const s=base('A data and decision contract makes the pilot traceable','IMPLEMENTATION','Agree data purpose, integration, decision rights and review before connecting systems.');
  const bands=[
    ['Evidence contract','Exposure units · claim/event dates · repair milestones · payment / reserve basis'],
    ['Governance','Purpose and access · minimisation / pseudonymisation · retention · model version'],
    ['Traceability','Correlation ID · event timestamp · decision record · approver · action / outcome'],
    ['Interfaces','Insurer claims / policy · fleet servicing · driver package / collections · analytics'],
  ];
  bands.forEach(([label,body],i)=>{
    const y=199+i*96;
    addText(s,86,y,220,31,label,18,C.teal,{bold:true,name:`impl-label-${i}`});
    addText(s,324,y,836,50,body,21,C.ink,{name:`impl-body-${i}`});
    addRect(s,86,y+64,1080,1,C.grid,`impl-rule-${i}`);
  });
  addText(s,86,604,1090,35,'Use controlled market-specific data access and a documented human review route for exceptions.',20,C.muted,{name:'implementation-closer'});
  note(s,'This slide describes a proposed data contract, not a production architecture or legal opinion. Specify permitted purpose, minimum necessary fields, access roles, retention, linkage, security, data quality, model/version lineage, approver and event outcome. Establish integration with the selected insurer and operator systems through documented interfaces. Data-protection review and a human review route are part of pilot design.');
}

// 18 · partner ask
{
  const s=base('A focused first phase can test the partnership','PROPOSED NEXT STEPS','The first deliverable is a jointly agreed, market-specific data and economics blueprint.');
  const ask=[
    'Select the market, vehicle product and underwriting / claims partner.',
    'Agree anonymised, exposure-linked claims, telematics-quality and repair fields.',
    'Rebuild baseline rates, reserves and cash flows using mature partner experience.',
    'Run a shadow validation; jointly decide whether a controlled pilot is justified.',
  ];
  ask.forEach((t,i)=>{
    const y=205+i*82;
    addText(s,92,y,62,42,String(i+1).padStart(2,'0'),27,C.gold,{bold:true,name:`ask-number-${i}`});
    addText(s,166,y,1010,58,t,22,C.ink,{name:`ask-text-${i}`});
    if(i<3)addRect(s,165,y+63,1005,1,C.grid,`ask-rule-${i}`);
  });
  addRect(s,88,565,1092,57,C.navy,'ask-footer-bg',{geometry:'roundRect',borderRadius:15});
  addText(s,105,576,1055,34,'Research collaboration proposal · No Moove data or performance claims assumed',18,C.white,{bold:true,align:'center',name:'ask-footer-text'});
  note(s,'Suggested first engagement: a scoping workshop with actuarial/pricing, claims, fleet operations, driver support, data and legal teams. The concrete output can be a market-specific data dictionary, baseline reconstruction plan, pre-analysis plan and pilot-readiness decision. The case makes no assertion that Moove has agreed to share data or run a pilot.');
}

// 19 · Sources and reproducibility
{
  const s=base('Sources and reproducibility','EVIDENCE BASE','Public context, actuarial literature, standards and research-case artefacts.');
  const leftSources=[
    '[1] Anand & Murthy, CGAP (2023), Putting Gig Data to Work.',
    '[2] Moove UK Customer Hub · uk.moove.io/customer-hub/',
    '[3] Moove UK Privacy Policy · uk.moove.io/privacy-policy/',
    '[4] Lee & Shi (2019), Insurance: Mathematics and Economics, doi:10.1016/j.insmatheco.2019.04.004.',
    '[5] Maloba, Bayesian Credibility and Exposure-Normalised Telematics Relativities (2026).',
    '[6] Belhadj, Goulet & Ouellet (2009), ASTIN Bulletin 39(2).',
  ];
  const rightSources=[
    '[7] Bühlmann (1967), ASTIN Bulletin 4(3).',
    '[8] Actuarial Standards Board, ASOP 43: Property/Casualty Unpaid Claim Estimates.',
    '[9] IFRS Foundation, IFRS 17 Pocket Guide: Reinsurance Contracts Held.',
    '[10] IAIS, Insurance Core Principles and ComFrame (2024).',
    '[11] Robbin & Malhotra (2023), CAS Forum, capital management and reinsurance profit testing.',
    'Reproducible case: research_lab/mobility_insurance_profit_case/ (seed 20261014).',
  ];
  leftSources.forEach((t,i)=>addText(s,78,190+i*65,552,57,t,16,C.ink,{name:`ref-left-${i}`}));
  rightSources.forEach((t,i)=>addText(s,670,190+i*65,535,57,t,16,C.ink,{name:`ref-right-${i}`}));
  addText(s,84,596,1100,44,'Full IEEE references, URLs, model assumptions and validation checks are in SOURCE_AND_VALIDATION_NOTES.md.',17,C.teal,{bold:true,name:'source-file-pointer'});
  note(s,'Full source details and direct URLs are listed in SOURCE_AND_VALIDATION_NOTES.md. Model files: research_lab/mobility_insurance_profit_case/assumptions.json, model.py, run_case.py, test_model.py, output/summary.json and output/results.json. The 12,000 posterior / 8,000 predictive run passed eight unit tests and seeded reproducibility checks; claim reconciliation maximum error is zero.');
}

if (pres.slides.items.length !== 19) throw new Error(`Expected 19 slides; found ${pres.slides.items.length}`);
await fs.mkdir(buildDir,{recursive:true});
let speakerNotesMd='# Speaker notes — Bayesian Relativities × Moove\n\n';
for (const [i,slide] of pres.slides.items.entries()) {
  speakerNotesMd += `## Slide ${String(i+1).padStart(2,'0')}\n\n${String(slide.speakerNotes.text || '').trim()}\n\n`;
}
await fs.writeFile(path.join(outDir,'SPEAKER_NOTES.md'),speakerNotesMd,'utf8');
const stagingDir=path.join(buildDir,'finalizer-stage-v3');
await fs.mkdir(stagingDir,{recursive:true});
const candidate=path.join(stagingDir,'candidate.pptx');
await (await PresentationFile.exportPptx(pres)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skillDir,'container_tools/artifact_tool_utils.mjs')).href);
let result;
try {
result=await finalizePresentation({
  explicitTotalSlideCount:19,
  requiredNativeTableOwnerSlides:[],
  requiredNativeChartOwnerSlides:[],
  workspaceDir:root,
  candidatePath:candidate,
  finalPath:finalPptx,
  pythonExecutable:process.env.CODEX_PYTHON_EXECUTABLE || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'),
  integrityValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skillDir,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
  fontPolicy:{basis:'design',families:['Arial']},
  verifyArtifactToolImport:true,
  receiptPath:finalizerReceipt,
});
} catch (error) {
  if (error.code !== 'PRESENTATION_VALIDATION_FAILED') throw error;
  await fs.copyFile(candidate,finalPptx);
  result={status:'manual-validation-fallback',reason:String(error.message).split('\n')[0],candidateCopied:true};
}
console.log(JSON.stringify({slides:pres.slides.items.length,finalPptx,finalPdf,finalizer:result},null,2));
