"""Standalone one-click Windows installer UI. PyInstaller bundles Python."""
from __future__ import annotations
import os, shutil, sys, threading, tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from src.core.installer import ToolkitInstaller
from src.core.plugin_installer import PluginInstaller
PLUGINS=[("texture-importer","Maya"),("totex","3ds Max"),("MayaToPainter","Maya"),("SubstancePainterToMaya","Maya"),("rename-lowhigh-proximity","3ds Max"),("fal-texture-pbr-generator","Shared"),("Procedural-PBR","Shared"),("SubstanceDesignerTools","Shared")]
def bundled_src(): return Path(getattr(sys,"_MEIPASS",Path(__file__).resolve().parents[1]))/"src"
class InstallerApp:
 def __init__(self):
  self.root=tk.Tk(); self.root.title("GameArt AI Toolkit Installer"); self.root.geometry("860x650"); self.install_root=Path(os.environ.get("GAMEART_TOOLKIT_HOME",Path.home()/"GameArtAI"/"Toolkit")).expanduser().resolve(); self.status=tk.StringVar(value="Ready"); self._build()
 def _build(self):
  o=ttk.Frame(self.root,padding=22); o.pack(fill="both",expand=True); ttk.Label(o,text="GameArt AI Toolkit",font=("Segoe UI",22,"bold")).pack(anchor="w"); ttk.Label(o,text="一键安装版 · 无需 Python").pack(anchor="w",pady=(2,18)); ttk.Label(o,text=f"安装位置：{self.install_root}").pack(anchor="w"); ttk.Label(o,text="选择需要安装的第三方插件（可跳过）：").pack(anchor="w",pady=(18,6))
  self.vars={}; g=ttk.Frame(o); g.pack(fill="x")
  for i,(n,h) in enumerate(PLUGINS):
   v=tk.BooleanVar(); self.vars[n]=v; ttk.Checkbutton(g,text=f"{n}  [{h}]",variable=v).grid(row=i//2,column=i%2,sticky="w",padx=8,pady=4)
  b=ttk.Frame(o); b.pack(fill="x",pady=18); self.btn=ttk.Button(b,text="一键安装",command=self.start); self.btn.pack(side="left"); ttk.Button(b,text="检查环境",command=lambda:self._run(self.doctor)).pack(side="left",padx=8); ttk.Button(b,text="退出",command=self.root.destroy).pack(side="right"); self.progress=ttk.Progressbar(o,mode="indeterminate"); self.progress.pack(fill="x"); ttk.Label(o,textvariable=self.status).pack(fill="x",pady=8); self.log=tk.Text(o,height=17); self.log.pack(fill="both",expand=True)
 def write(self,s): self.log.insert("end",str(s)+"
"); self.log.see("end")
 def _run(self,fn): self.status.set("处理中…"); self.progress.start(12); threading.Thread(target=self._worker,args=(fn,),daemon=True).start()
 def _worker(self,fn):
  try:r=fn()
  except Exception as e:r={"ok":False,"error":f"{type(e).__name__}: {e}"}
  self.root.after(0,lambda:self.done(r))
 def done(self,r):
  self.progress.stop(); self.write(r); ok=r.get("ok",True); self.status.set("安装完成" if ok else "安装失败"); self.btn.configure(state="normal")
  if ok and r.get("installed"): messagebox.showinfo("GameArt AI Toolkit","安装完成。")
  elif not ok: messagebox.showerror("GameArt AI Toolkit",str(r))
 def start(self): self.btn.configure(state="disabled"); self._run(self.install_all)
 def install_all(self):
  root=self.install_root; root.mkdir(parents=True,exist_ok=True); payload=root/"current"; payload.mkdir(parents=True,exist_ok=True); src=bundled_src(); dst=payload/"src"
  if dst.exists(): shutil.rmtree(dst)
  if src.is_dir(): shutil.copytree(src,dst)
  r=ToolkitInstaller(root).install()
  if not r.ok:return {"ok":False,"error":r.error}
  results=[]; pi=PluginInstaller(root)
  for n,v in self.vars.items():
   if v.get(): self.write(f"安装插件：{n}"); results.append(pi.install(n).__dict__)
  return {"ok":all(x["ok"] for x in results),"installed":True,"root":str(root),"plugins":results}
 def doctor(self): return {"ok":self.install_root.exists(),"root":str(self.install_root)}
 def run(self): self.root.mainloop()
if __name__=="__main__": InstallerApp().run()
