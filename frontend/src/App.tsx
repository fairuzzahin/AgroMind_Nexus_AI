import { useEffect, useState } from "react";
import { Sprout, FlaskConical, BookOpen, History, Leaf, CloudSun, BrainCircuit, ArrowRight, LoaderCircle, CircleAlert, CheckCircle2, Menu } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
type Inputs = { N:number; P:number; K:number; temperature:number; humidity:number; ph:number; rainfall:number };
const initial: Inputs = { N:90, P:42, K:43, temperature:25, humidity:80, ph:6.5, rainfall:200 };
const fields: {key:keyof Inputs; label:string; unit:string; min:number; max:number; step:number; hint:string}[] = [
 {key:"N",label:"Nitrogen (N)",unit:"kg/ha*",min:0,max:300,step:1,hint:"Soil test value"},
 {key:"P",label:"Phosphorus (P)",unit:"kg/ha*",min:0,max:300,step:1,hint:"Soil test value"},
 {key:"K",label:"Potassium (K)",unit:"kg/ha*",min:0,max:300,step:1,hint:"Soil test value"},
 {key:"temperature",label:"Temperature",unit:"°C",min:-10,max:60,step:0.1,hint:"Typical growing conditions"},
 {key:"humidity",label:"Humidity",unit:"%",min:0,max:100,step:1,hint:"Relative humidity"},
 {key:"ph",label:"Soil pH",unit:"pH",min:0,max:14,step:0.1,hint:"Measured soil pH"},
 {key:"rainfall",label:"Rainfall",unit:"mm",min:0,max:5000,step:1,hint:"Seasonal or dataset-compatible value"}
];
type Prediction = {crop:string; model_score:number; top_alternatives:{crop:string;model_score:number}[]; feature_importance:{feature:string;importance:number}[]; explanation:string; disclaimer:string};
export default function App() {
 const [inputs,setInputs] = useState<Inputs>(initial);
 const [page,setPage] = useState("Overview");
 const [prediction,setPrediction] = useState<Prediction|null>(null);
 const [question,setQuestion] = useState("How does soil pH affect crop growth?");
 const [answer,setAnswer] = useState<any>(null);
 const [history,setHistory] = useState<any[]>([]);
 const [loading,setLoading] = useState(false);
 const [error,setError] = useState("");
 const [health,setHealth] = useState(false);
 useEffect(()=>{ fetch(`${API}/api/health`).then(r=>r.json()).then(d=>setHealth(d.model_loaded)).catch(()=>setHealth(false)); },[]);
 async function request<T>(path:string, body?:unknown):Promise<T> {
   const r=await fetch(`${API}${path}`,{method:body?"POST":"GET",headers:{"Content-Type":"application/json"},...(body?{body:JSON.stringify(body)}:{})});
   const data=await r.json(); if(!r.ok) throw new Error(data.detail||"Request failed"); return data;
 }
 async function predict() {
   setLoading(true); setError("");
   try { setPrediction(await request<Prediction>("/api/predict",inputs)); setPage("Crop Recommendation"); }
   catch(e:any){setError(e.message||"Could not connect to the backend.");}
   finally {setLoading(false);}
 }
 async function ask() {
   setLoading(true); setError("");
   try {setAnswer(await request("/api/knowledge/ask",{question}));}
   catch(e:any){setError(e.message||"Could not retrieve agricultural knowledge.");}
   finally{setLoading(false);}
 }
 async function loadHistory() {
   setLoading(true); setError("");
   try {setHistory(await request<any[]>("/api/history")); setPage("History");}
   catch(e:any){setError(e.message||"Could not load history.");}
   finally{setLoading(false);}
 }
 const nav=[{name:"Overview",icon:Sprout},{name:"Crop Recommendation",icon:FlaskConical},{name:"Knowledge Assistant",icon:BookOpen},{name:"History",icon:History}];
 return <div className="app-shell">
  <aside className="sidebar">
   <div className="brand"><div className="brand-icon"><Sprout size={23}/></div><div><b>AgroMind</b><span>NEXUS AI</span></div></div>
   <div className="workspace-label">WORKSPACE</div>
   <nav>{nav.map(n=><button key={n.name} className={`nav-item ${page===n.name?"active":""}`} onClick={()=>{setPage(n.name);setError("");if(n.name==="History")loadHistory();}}><n.icon size={18}/><span>{n.name}</span>{n.name==="Crop Recommendation"&&<ArrowRight size={15} className="nav-arrow"/>}</button>)}</nav>
   <div className="sidebar-bottom"><div className="status-dot"/><div><b>AI services</b><span>{health?"API connected":"API not connected"}</span></div></div>
   <div className="sidebar-foot">AGRICULTURE INTELLIGENCE<br/>CAPSTONE PROTOTYPE · v1.0</div>
  </aside>
  <main className="main">
   <header className="topbar"><div className="breadcrumb"><span>Workspace</span><span>/</span><b>{page}</b></div><div className="top-actions"><span className={`api-pill ${health?"online":""}`}><i/>{health?"Backend online":"Backend offline"}</span><div className="avatar">AN</div></div></header>
   <div className="content">
    {error&&<div className="error-banner"><CircleAlert size={18}/>{error}<button onClick={()=>setError("")}>Dismiss</button></div>}
    {page==="Overview"&&<><div className="hero"><div className="hero-copy"><div className="eyebrow"><span/> SMART AGRICULTURE PLATFORM</div><h1>Grow with data.<br/><em>Harvest with confidence.</em></h1><p>Bring soil insights, crop prediction and evidence-led agricultural knowledge together in one place.</p><button className="primary-btn" onClick={()=>setPage("Crop Recommendation")}>Start crop analysis <ArrowRight size={17}/></button></div><div className="hero-art"><div className="sun"/><div className="hill hill-back"/><div className="hill hill-front"/><div className="plant plant-one">♧</div><div className="plant plant-two">♧</div><div className="art-label"><Leaf size={16}/><span>Precision agriculture</span></div></div></div>
     <div className="section-heading"><div><span className="eyebrow">YOUR FARM, UNDERSTOOD</span><h2>Decision support tools</h2></div><span className="muted">Built for informed decisions</span></div>
     <div className="tool-grid"><button className="tool-card" onClick={()=>setPage("Crop Recommendation")}><div className="tool-icon green"><FlaskConical/></div><span className="tool-kicker">PREDICTIVE ML</span><h3>Crop recommendation</h3><p>Estimate a suitable crop from soil nutrients and growing conditions.</p><span className="tool-link">Analyze your field <ArrowRight size={15}/></span></button><button className="tool-card" onClick={()=>setPage("Knowledge Assistant")}><div className="tool-icon amber"><BookOpen/></div><span className="tool-kicker">RETRIEVAL-AUGMENTED AI</span><h3>Knowledge assistant</h3><p>Ask agricultural questions and review the sources behind answers.</p><span className="tool-link">Explore knowledge <ArrowRight size={15}/></span></button><button className="tool-card" onClick={loadHistory}><div className="tool-icon blue"><History/></div><span className="tool-kicker">FIELD RECORDS</span><h3>Prediction history</h3><p>Review saved predictions and their input conditions.</p><span className="tool-link">View past analyses <ArrowRight size={15}/></span></button></div>
     <div className="note-strip"><BrainCircuit size={20}/><div><b>Explainable by design</b><span>See which input features matter to the trained model. Model patterns are not guarantees of real-world yield.</span></div></div>
    </>}
    {page==="Crop Recommendation"&&<><div className="page-intro"><div className="eyebrow">PREDICTIVE INTELLIGENCE</div><h1>Crop recommendation</h1><p>Enter the soil and climate values to generate a model-based crop suggestion.</p></div><div className="analysis-layout"><section className="panel"><div className="panel-heading"><div className="panel-icon"><FlaskConical size={20}/></div><div><h2>Field conditions</h2><p>Use measured values whenever possible.</p></div><button className="text-btn" onClick={()=>setInputs(initial)}>Reset values</button></div><div className="field-grid">{fields.map(f=><label className="field" key={f.key}><span>{f.label}<small>{f.unit}</small></span><input type="number" min={f.min} max={f.max} step={f.step} value={inputs[f.key]} onChange={e=>setInputs({...inputs,[f.key]:Number(e.target.value)})}/><small className="field-hint">{f.hint}</small></label>)}</div><div className="form-note"><CircleAlert size={16}/><span>* Nutrient units in public benchmark datasets may not match your soil laboratory report. Confirm units before using field values.</span></div><button className="primary-btn full-btn" onClick={predict} disabled={loading}>{loading?<LoaderCircle className="spin" size={17}/>:<BrainCircuit size={17}/>} {loading?"Analyzing conditions":"Generate recommendation"} <ArrowRight size={17}/></button></section>
    <aside className="panel side-panel"><div className="panel-heading"><div className="panel-icon soft"><Leaf size={20}/></div><div><h2>Analysis workflow</h2><p>What happens next</p></div></div><div className="steps"><div className="step"><span>01</span><div><b>Validate inputs</b><p>Check ranges and required values.</p></div></div><div className="step"><span>02</span><div><b>Run ML model</b><p>Random Forest compares patterns learned from training data.</p></div></div><div className="step"><span>03</span><div><b>Explain the output</b><p>Review leading model features and alternatives.</p></div></div></div><div className="side-callout"><CloudSun size={19}/><p>Rainfall and temperature are inputs, not a live weather forecast.</p></div></aside></div>
    {prediction&&<section className="panel result-panel"><div className="result-top"><div><span className="eyebrow">MODEL OUTPUT</span><h2>Suggested crop: <em>{prediction.crop}</em></h2><p>{prediction.explanation}</p></div><div className="score"><b>{(prediction.model_score*100).toFixed(1)}%</b><span>model score*</span></div></div><div className="result-columns"><div><h3>Top model alternatives</h3>{prediction.top_alternatives.map((x,i)=><div className="alternative" key={x.crop}><span className="rank">{i+1}</span><b>{x.crop}</b><div className="bar-bg"><div style={{width:`${x.model_score*100}%`}}/></div><span>{(x.model_score*100).toFixed(1)}%</span></div>)}</div><div><h3>Global feature importance</h3><ResponsiveContainer width="100%" height={210}><BarChart data={prediction.feature_importance.slice(0,7)} layout="vertical" margin={{left:12,right:12}}><CartesianGrid strokeDasharray="3 3" horizontal={false}/><XAxis type="number" tickFormatter={v=>`${(v*100).toFixed(0)}%`}/><YAxis dataKey="feature" type="category" width={90}/><Tooltip formatter={(v:any)=>`${(Number(v)*100).toFixed(2)}%`}/><Bar dataKey="importance" fill="#2f7b54" radius={[0,5,5,0]}/></BarChart></ResponsiveContainer></div></div><div className="disclaimer"><CircleAlert size={17}/><span>{prediction.disclaimer}</span></div></section>}</>}
    {page==="Knowledge Assistant"&&<><div className="page-intro"><div className="eyebrow">RETRIEVAL-AUGMENTED GENERATION</div><h1>Agricultural knowledge</h1><p>Ask a question, inspect retrieved source notes, and use evidence-aware guidance.</p></div><section className="panel knowledge-panel"><div className="knowledge-head"><div className="knowledge-icon"><BookOpen size={23}/></div><div><h2>Ask AgroMind</h2><p>Answers use the current curated knowledge collection.</p></div></div><label className="question-label">Your question<textarea value={question} onChange={e=>setQuestion(e.target.value)} placeholder="e.g. How should I interpret soil pH?" rows={4}/></label><div className="suggestions"><button onClick={()=>setQuestion("How does soil pH affect crop growth?")}>Soil pH</button><button onClick={()=>setQuestion("How can I make fertilizer decisions from a soil test?")}>Soil nutrients</button><button onClick={()=>setQuestion("What should I consider when planning irrigation?")}>Water management</button></div><button className="primary-btn" onClick={ask} disabled={loading||question.trim().length<5}>{loading?<LoaderCircle className="spin" size={17}/>:<BrainCircuit size={17}/>} {loading?"Retrieving evidence":"Ask question"} <ArrowRight size={17}/></button></section>{answer&&<section className="panel answer-panel"><div className="answer-label"><CheckCircle2 size={18}/> RESPONSE</div><p className="answer-text">{answer.answer}</p><h3>Retrieved sources</h3>{answer.sources.length?answer.sources.map((s:any)=><div className="source-item" key={s.id}><div className="source-mark"><BookOpen size={17}/></div><div><b>{s.title}</b><span>Relevance score: {s.relevance}</span><a href={s.source} target="_blank" rel="noreferrer">{s.source}</a></div></div>):<p>No relevant source passages were found. Try a more specific question.</p>}<div className="disclaimer"><CircleAlert size={17}/><span>Retrieval quality depends on the small starter corpus. Sources are not a substitute for locally verified agricultural guidance.</span></div></section>}</>}
    {page==="History"&&<><div className="page-intro"><div className="eyebrow">SAVED ANALYSES</div><h1>Prediction history</h1><p>Previously generated model recommendations stored by the backend.</p></div><section className="panel"><div className="panel-heading"><div className="panel-icon"><History size={20}/></div><div><h2>Recent predictions</h2><p>Latest records first</p></div><button className="text-btn" onClick={loadHistory}>Refresh</button></div>{history.length?<div className="history-list">{history.map(r=><div className="history-row" key={r.id}><div className="history-crop"><div className="tool-icon green"><Sprout size={19}/></div><div><b>{r.crop}</b><span>{r.created_at?new Date(r.created_at).toLocaleString():"Date unavailable"}</span></div></div><div className="history-score">{(r.model_score*100).toFixed(1)}% <small>model score</small></div><button className="text-btn" onClick={()=>{setInputs(r.inputs);setPage("Crop Recommendation");}}>Reuse inputs</button></div>)}</div>:<div className="empty-state"><History size={30}/><h3>No predictions yet</h3><p>Run a crop recommendation to create your first history record.</p><button className="primary-btn" onClick={()=>setPage("Crop Recommendation")}>Start analysis</button></div>}</section></>}
    <footer className="footer"><span>© 2026 AgroMind Nexus AI</span><span>AI-assisted decisions · Human-verified farming</span></footer>
   </div>
  </main>
 </div>
}
