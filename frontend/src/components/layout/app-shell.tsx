"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, Bell, Bot, ChevronDown, Command, Database, LayoutDashboard, MessageSquare, Plug, Search, Settings, Workflow, Zap } from "lucide-react";
import { navGroups } from "@/lib/data";
const icons: Record<string, React.ElementType> = {LayoutDashboard,MessageSquare,Bot,Database,Plug,Workflow,Activity,Settings};
export function AppShell({children}:{children:React.ReactNode}) {
 const path=usePathname();
 return <div className="app-shell">
  <aside className="sidebar">
   <Link href="/" className="flex items-center gap-3 px-2 mb-8"><div className="brand-mark"><Command size={19}/></div><div className="brand-text"><div className="font-bold tracking-tight text-[15px]">AgentFlow <span className="text-violet-300">AI</span></div><div className="text-[10px] text-slate-500 mt-0.5">AGENT WORKSPACE</div></div></Link>
   <div className="card-soft p-2.5 flex items-center gap-2 mb-5"><div className="avatar">AF</div><div className="workspace-text flex-1 min-w-0"><div className="text-xs font-semibold">Acme Workspace</div><div className="text-[10px] text-slate-500">Free plan</div></div><ChevronDown size={14} className="text-slate-500"/></div>
   {navGroups.map(group=><div key={group.label}><div className="nav-label">{group.label}</div>{group.items.map(item=>{const Icon=icons[item.icon];const active=path===item.href || (item.href!=="/" && path.startsWith(item.href));return <Link key={item.href} href={item.href} className={`nav-link ${active?"active":""}`}><Icon size={17}/><span className="nav-text text-[12px] font-medium">{item.label}</span>{item.href==="/agents"&&<span className="nav-text ml-auto text-[10px] text-slate-500">3</span>}</Link>})}</div>)}
   <div className="mt-auto sidebar-footer"><div className="card-soft p-3"><div className="flex items-center gap-2 text-xs font-semibold"><Zap size={14} className="text-violet-300"/> Local runtime</div><div className="text-[10px] text-slate-500 mt-2">Ollama connection is not configured</div><div className="mt-3 h-1.5 rounded-full bg-slate-800"><div className="h-1.5 w-1/3 rounded-full bg-violet-400"/></div></div><div className="flex items-center gap-2 mt-4 px-2"><div className="avatar">UN</div><div className="workspace-text flex-1"><div className="text-xs font-medium">Workspace owner</div><div className="text-[10px] text-slate-500">Local development</div></div><Settings size={15} className="text-slate-500"/></div></div>
  </aside>
  <main className="main-area"><header className="topbar"><div className="flex items-center gap-2 text-xs text-slate-500"><span className="mobile-hide">Workspace</span><span className="mobile-hide">/</span><span className="text-slate-200">{navGroups.flatMap(g=>g.items).find(i=>i.href===path)?.label || "Overview"}</span></div><div className="flex items-center gap-3"><button className="btn mobile-hide"><Search size={14}/> <span>Search</span><kbd className="text-[10px] text-slate-500 ml-2">⌘ K</kbd></button><button className="relative p-2 text-slate-400 hover:text-white"><Bell size={17}/><span className="absolute top-1 right-1 w-1.5 h-1.5 bg-violet-400 rounded-full"/></button><div className="w-7 h-7 rounded-full bg-gradient-to-br from-violet-400 to-indigo-700"/></div></header><div className="page-wrap">{children}</div></main>
 </div>;
}
