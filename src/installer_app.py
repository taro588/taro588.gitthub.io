"""Double-click Windows installer UI for GameArt AI Toolkit."""
from __future__ import annotations
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from src.core.installer import ToolkitInstaller
from src.core.plugin_installer import PluginInstaller

PLUGINS = [
    ("texture-importer", "Maya"),
    ("totex", "3ds Max"),
    ("MayaToPainter", "Maya"),
    ("SubstancePainterToMaya", "Maya"),
    ("rename-lowhigh-proximity", "3ds Max"),
    ("fal-texture-pbr-generator", "Shared"),
    ("Procedural-PBR", "Shared"),
    ("SubstanceDesignerTools", "Shared"),
]

class InstallerApp:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("GameArt AI Toolkit Installer")
        self.root.geometry("820x620")
        self.root.minsize(760,560)
        self.install_root=Path.home()/"GameArtAI"/"Toolkit"
        self.installer=ToolkitInstaller(self.install_root)
        self.plugins=PluginInstaller(self.install_root)
        self.status=tk.StringVar(value="Ready to install")
        self._build()

    def _build(self):
        outer=ttk.Frame(self.root,padding=22); outer.pack(fill="both",expand=True)
        ttk.Label(outer,text="GameArt AI Toolkit",font=("Segoe UI",22,"bold")).pack(anchor="w")
        ttk.Label(outer,text="一键安装 / 插件管理 / Maya / 3ds Max").pack(anchor="w",pady=(2,18))
        row=ttk.Frame(outer); row.pack(fill="x")
        ttk.Label(row,text="安装位置:").pack(side="left")
        ttk.Label(row,text=str(self.install_root)).pack(side="left",padx=8)
        ttk.Button(row,text="安装 Toolkit",command=lambda:self._run(self._install)).pack(side="right")
        ttk.Label(outer,text="选择要安装的插件：").pack(anchor="w",pady=(20,6))
        self.vars={}
        grid=ttk.Frame(outer); grid.pack(fill="x")
        for i,(name,host) in enumerate(PLUGINS):
            var=tk.BooleanVar(value=False); self.vars[name]=var
            ttk.Checkbutton(grid,text=f"{name}  [{host}]",variable=var).grid(row=i//2,column=i%2,sticky="w",padx=8,pady=5)
        buttons=ttk.Frame(outer); buttons.pack(fill="x",pady=18)
        ttk.Button(buttons,text="安装选中插件",command=lambda:self._run(self._install_plugins)).pack(side="left")
        ttk.Button(buttons,text="注册 Maya",command=lambda:self._run(self._register_maya)).pack(side="left",padx=8)
        ttk.Button(buttons,text="注册 3ds Max",command=lambda:self._run(self._register_max)).pack(side="left")
        ttk.Button(buttons,text="检查环境",command=lambda:self._run(self._doctor)).pack(side="right")
        ttk.Label(outer,textvariable=self.status).pack(fill="x",pady=6)
        self.log=tk.Text(outer,height=16,wrap="word")
        self.log.pack(fill="both",expand=True)

    def _write(self,text):
        self.log.insert("end",text+"\n"); self.log.see("end")

    def _run(self,fn):
        self.status.set("正在处理…")
        threading.Thread(target=self._worker,args=(fn,),daemon=True).start()

    def _worker(self,fn):
        try:
            result=fn()
            self.root.after(0,lambda:self._done(result))
        except Exception as exc:
            self.root.after(0,lambda:self._done({"ok":False,"error":f"{type(exc).__name__}: {exc}"}))

    def _done(self,result):
        self._write(str(result))
        ok=result.get("ok",True) if isinstance(result,dict) else True
        self.status.set("完成" if ok else "失败")
        if not ok: messagebox.showerror("GameArt Toolkit",str(result))

    def _install(self):
        return self.installer.install().__dict__

    def _install_plugins(self):
        selected=[n for n,v in self.vars.items() if v.get()]
        if not selected: return {"ok":False,"error":"请至少选择一个插件"}
        return {"ok":all(self.plugins.install(n).ok for n in selected),
                "plugins":[self.plugins.install(n).__dict__ for n in []],
                "selected":selected}

    def _register_maya(self):
        from src.core.host_integration import HostIntegrator
        return HostIntegrator(self.install_root).register_maya().__dict__

    def _register_max(self):
        from src.core.host_integration import HostIntegrator
        return HostIntegrator(self.install_root).register_max().__dict__

    def _doctor(self):
        return {"ok":True,"installed":self.install_root.exists(),"plugins":self.plugins.installed()}

    def run(self): self.root.mainloop()

if __name__=="__main__": InstallerApp().run()
