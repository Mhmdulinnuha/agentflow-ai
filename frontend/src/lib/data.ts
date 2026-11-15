export const navGroups = [
  { label: "WORKSPACE", items: [{label:"Overview",href:"/",icon:"LayoutDashboard"},{label:"AI Playground",href:"/playground",icon:"MessageSquare"},{label:"Agents",href:"/agents",icon:"Bot"}]},
  { label: "KNOWLEDGE & TOOLS", items: [{label:"Knowledge Base",href:"/knowledge",icon:"Database"},{label:"MCP Servers",href:"/mcp",icon:"Plug"},{label:"Workflows",href:"/workflows",icon:"Workflow"}]},
  { label: "OBSERVABILITY", items: [{label:"Executions",href:"/executions",icon:"Activity"},{label:"Settings",href:"/settings",icon:"Settings"}]}
];
export const agents = [
 {name:"Research Assistant",description:"Researches topics and synthesizes trusted sources.",model:"qwen3:4b",status:"Active",runs:"1,284",updated:"2 min ago",initials:"RA"},
 {name:"Knowledge Assistant",description:"Answers questions using your internal knowledge base.",model:"qwen3:4b",status:"Active",runs:"856",updated:"18 min ago",initials:"KA"},
 {name:"Workflow Planner",description:"Breaks down goals and coordinates connected tools.",model:"qwen3:4b",status:"Draft",runs:"42",updated:"Yesterday",initials:"WP"}
];
export const documents = [
 {name:"Product documentation.pdf",type:"PDF",size:"2.4 MB",chunks:124,status:"Indexed",date:"Today, 10:42"},
 {name:"Engineering handbook.docx",type:"DOCX",size:"840 KB",chunks:86,status:"Indexed",date:"Yesterday"},
 {name:"Customer FAQ.txt",type:"TXT",size:"32 KB",chunks:18,status:"Processing",date:"Yesterday"}
];
export const executions = [
 {id:"EX-2481",name:"Research Assistant",trigger:"Chat",status:"Success",duration:"4.2s",time:"2 min ago"},
 {id:"EX-2480",name:"Knowledge Assistant",trigger:"Chat",status:"Success",duration:"1.8s",time:"18 min ago"},
 {id:"EX-2479",name:"Daily summary",trigger:"Schedule",status:"Failed",duration:"0.6s",time:"1 hour ago"},
 {id:"EX-2478",name:"Research Assistant",trigger:"API",status:"Success",duration:"6.1s",time:"3 hours ago"}
];
