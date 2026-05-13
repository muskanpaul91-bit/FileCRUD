import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from pathlib import Path


# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#0f1117"
SIDEBAR_BG  = "#161b27"
CARD_BG     = "#1c2333"
CARD_BORDER = "#2a3349"
INPUT_BG    = "#111827"
INPUT_FOCUS = "#2563eb"

TEXT_PRI    = "#f0f4ff"
TEXT_SEC    = "#8b9abf"
TEXT_HINT   = "#4a5578"

ACCENT      = "#3b82f6"       # blue
ACCENT_HOV  = "#2563eb"
SUCCESS_BG  = "#0d2818"
SUCCESS_FG  = "#4ade80"
ERROR_BG    = "#2d0e0e"
ERROR_FG    = "#f87171"
INFO_BG     = "#0c1d3a"
INFO_FG     = "#60a5fa"
WARN_BG     = "#2a1a00"
WARN_FG     = "#fbbf24"

NAV_ITEMS = [
    ("✦  Create",  "create"),
    ("◎  Read",    "read"),
    ("⟳  Update",  "update"),
    ("⊗  Delete",  "delete"),
    ("⊞  Browse",  "browse"),
]


class StyledEntry(tk.Frame):
    """Custom entry with animated bottom-border focus effect."""
    def __init__(self, parent, textvariable=None, **kwargs):
        super().__init__(parent, bg=CARD_BG)
        self.var = textvariable or tk.StringVar()
        self.entry = tk.Entry(
            self, textvariable=self.var,
            font=("Consolas", 11), bg=INPUT_BG, fg=TEXT_PRI,
            insertbackground=ACCENT, relief="flat", bd=0,
            highlightthickness=2, highlightbackground=CARD_BORDER,
            highlightcolor=ACCENT
        )
        self.entry.pack(fill="x", ipady=8, padx=0)

    def get(self):  return self.var.get()
    def set(self, v): self.var.set(v)


class StyledText(tk.Frame):
    def __init__(self, parent, height=7, **kwargs):
        super().__init__(parent, bg=CARD_BG)
        self.text = tk.Text(
            self, font=("Consolas", 10), bg=INPUT_BG, fg=TEXT_PRI,
            insertbackground=ACCENT, relief="flat", bd=0,
            highlightthickness=2, highlightbackground=CARD_BORDER,
            highlightcolor=ACCENT, height=height, wrap="word",
            selectbackground=ACCENT, selectforeground="#fff", padx=10, pady=8
        )
        self.text.pack(fill="both", expand=True)

    def get(self): return self.text.get("1.0", "end-1c")
    def delete(self): self.text.delete("1.0", "end")
    def insert(self, content): self.text.insert("end", content)
    def configure_state(self, s): self.text.config(state=s)


def nav_button(parent, label, cmd, active=False):
    bg = "#1e3a5f" if active else SIDEBAR_BG
    fg = TEXT_PRI  if active else TEXT_SEC
    lft = tk.Frame(parent, bg="#3b82f6" if active else SIDEBAR_BG, width=3)
    lft.pack(side="left", fill="y")
    btn = tk.Button(
        parent, text=label, command=cmd,
        font=("Segoe UI", 10, "bold" if active else "normal"),
        bg=bg, fg=fg, relief="flat", bd=0,
        activebackground="#1e3a5f", activeforeground=TEXT_PRI,
        anchor="w", padx=18, pady=10, cursor="hand2"
    )
    btn.pack(side="left", fill="both", expand=True)
    return btn, lft


def accent_btn(parent, text, cmd, color=ACCENT, hover=ACCENT_HOV, fg="#fff"):
    f = tk.Frame(parent, bg=color, bd=0)
    btn = tk.Button(
        f, text=text, command=cmd,
        font=("Segoe UI", 10, "bold"), bg=color, fg=fg,
        relief="flat", bd=0, padx=20, pady=9,
        activebackground=hover, activeforeground=fg, cursor="hand2"
    )
    btn.pack(padx=1, pady=1)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return f


def section_label(parent, text):
    tk.Label(parent, text=text, font=("Segoe UI", 9),
             bg=CARD_BG, fg=TEXT_SEC).pack(anchor="w", pady=(14, 4))


def card_title(parent, icon, title, subtitle=""):
    row = tk.Frame(parent, bg=CARD_BG)
    row.pack(fill="x", pady=(0, 18))
    tk.Label(row, text=icon, font=("Segoe UI", 22),
             bg=CARD_BG, fg=ACCENT).pack(side="left", padx=(0, 12))
    col = tk.Frame(row, bg=CARD_BG)
    col.pack(side="left")
    tk.Label(col, text=title, font=("Segoe UI", 14, "bold"),
             bg=CARD_BG, fg=TEXT_PRI).pack(anchor="w")
    if subtitle:
        tk.Label(col, text=subtitle, font=("Segoe UI", 9),
                 bg=CARD_BG, fg=TEXT_SEC).pack(anchor="w")


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FileVault — File Manager")
        self.root.geometry("820x580")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self._active_tab = None
        self._nav_refs = {}
        self._panels = {}
        self._build()

    # ── Shell ─────────────────────────────────────────────────────────────
    def _build(self):
        # Top bar
        topbar = tk.Frame(self.root, bg=SIDEBAR_BG, height=48)
        topbar.pack(fill="x")
        topbar.pack_propagate(False)
        tk.Label(topbar, text="  ◈ FileVault", font=("Segoe UI", 12, "bold"),
                 bg=SIDEBAR_BG, fg=TEXT_PRI).pack(side="left", padx=8, pady=12)
        tk.Label(topbar, text="workspace file manager",
                 font=("Segoe UI", 9), bg=SIDEBAR_BG, fg=TEXT_HINT).pack(side="left", pady=14)

        sep = tk.Frame(self.root, bg=CARD_BORDER, height=1)
        sep.pack(fill="x")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(body, bg=SIDEBAR_BG, width=190)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Frame(self.sidebar, bg=CARD_BORDER, height=1).pack(fill="x")
        tk.Label(self.sidebar, text="OPERATIONS", font=("Segoe UI", 7, "bold"),
                 bg=SIDEBAR_BG, fg=TEXT_HINT).pack(anchor="w", padx=22, pady=(16, 6))

        for label, key in NAV_ITEMS:
            row = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
            row.pack(fill="x", pady=1)
            btn, lft = nav_button(row, label, lambda k=key: self.switch(k))
            self._nav_refs[key] = (row, btn, lft)

        # Divider + footer
        tk.Frame(self.sidebar, bg=CARD_BORDER, height=1).pack(fill="x", pady=(20, 0))
        tk.Label(self.sidebar, text="v2.0  •  tkinter", font=("Consolas", 8),
                 bg=SIDEBAR_BG, fg=TEXT_HINT).pack(anchor="w", padx=22, pady=10)

        # Main content
        self.main = tk.Frame(body, bg=BG)
        self.main.pack(side="left", fill="both", expand=True, padx=24, pady=20)

        self._build_create()
        self._build_read()
        self._build_update()
        self._build_delete()
        self._build_browse()

        self.switch("create")

    def _card(self):
        outer = tk.Frame(self.main, bg=CARD_BORDER, bd=0)
        inner = tk.Frame(outer, bg=CARD_BG, padx=28, pady=22)
        inner.pack(fill="both", expand=True, padx=1, pady=1)
        return outer, inner

    def _msg_label(self, parent):
        lbl = tk.Label(parent, text="", bg=CARD_BG,
                       font=("Segoe UI", 9), anchor="w", wraplength=520)
        lbl.pack(fill="x", pady=(10, 0))
        return lbl

    def _show_msg(self, lbl, text, kind="success"):
        palette = {
            "success": (SUCCESS_BG, SUCCESS_FG),
            "error":   (ERROR_BG,   ERROR_FG),
            "info":    (INFO_BG,    INFO_FG),
            "warn":    (WARN_BG,    WARN_FG),
        }
        bg, fg = palette.get(kind, (CARD_BG, TEXT_PRI))
        lbl.config(text=f"  {text}", bg=bg, fg=fg, padx=10, pady=7,
                   relief="flat", font=("Segoe UI", 9))
        lbl.after(3500, lambda: lbl.config(text="", bg=CARD_BG, padx=0, pady=0))

    # ── Panels ────────────────────────────────────────────────────────────
    def _build_create(self):
        outer, card = self._card()
        self._panels["create"] = outer

        card_title(card, "✦", "Create File", "Write a new file to your workspace")

        section_label(card, "FILE NAME")
        self.c_name = StyledEntry(card)
        self.c_name.pack(fill="x")

        section_label(card, "CONTENT")
        self.c_body = StyledText(card, height=7)
        self.c_body.pack(fill="x")

        row = tk.Frame(card, bg=CARD_BG)
        row.pack(anchor="w", pady=(16, 0))
        accent_btn(row, "✦  Create File", self._create).pack(side="left")

        self.c_msg = self._msg_label(card)

    def _build_read(self):
        outer, card = self._card()
        self._panels["read"] = outer

        card_title(card, "◎", "Read File", "View the contents of any file")

        section_label(card, "FILE NAME")
        self.r_name = StyledEntry(card)
        self.r_name.pack(fill="x")

        row = tk.Frame(card, bg=CARD_BG)
        row.pack(anchor="w", pady=(14, 0))
        accent_btn(row, "◎  Read File", self._read,
                   color="#0f4c75", hover="#1b6ca8").pack(side="left")

        self.r_msg = self._msg_label(card)

        section_label(card, "OUTPUT")
        self.r_out = tk.Text(
            card, font=("Consolas", 10), bg=INPUT_BG, fg=SUCCESS_FG,
            insertbackground=ACCENT, relief="flat", bd=0,
            highlightthickness=2, highlightbackground=CARD_BORDER,
            height=8, state="disabled", wrap="word", padx=10, pady=8
        )
        self.r_out.pack(fill="x")

    def _build_update(self):
        outer, card = self._card()
        self._panels["update"] = outer

        card_title(card, "⟳", "Update File", "Overwrite or append to an existing file")

        section_label(card, "FILE NAME")
        self.u_name = StyledEntry(card)
        self.u_name.pack(fill="x")

        self.u_mode = tk.StringVar(value="overwrite")
        mode_row = tk.Frame(card, bg=CARD_BG)
        mode_row.pack(anchor="w", pady=(12, 0))
        for lbl, val in [("⬤  Overwrite", "overwrite"), ("⊕  Append", "append")]:
            tk.Radiobutton(
                mode_row, text=lbl, variable=self.u_mode, value=val,
                font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_SEC,
                selectcolor=INPUT_BG, activebackground=CARD_BG,
                activeforeground=TEXT_PRI
            ).pack(side="left", padx=(0, 24))

        section_label(card, "NEW CONTENT")
        self.u_body = StyledText(card, height=6)
        self.u_body.pack(fill="x")

        row = tk.Frame(card, bg=CARD_BG)
        row.pack(anchor="w", pady=(14, 0))
        accent_btn(row, "⟳  Update File", self._update,
                   color="#1a3a2a", hover="#1f5c3a", fg=SUCCESS_FG).pack(side="left")

        self.u_msg = self._msg_label(card)

    def _build_delete(self):
        outer, card = self._card()
        self._panels["delete"] = outer

        card_title(card, "⊗", "Delete File", "Permanently remove a file from disk")

        section_label(card, "FILE NAME")
        self.d_name = StyledEntry(card)
        self.d_name.pack(fill="x")

        # Warning banner
        warn = tk.Frame(card, bg=WARN_BG)
        warn.pack(fill="x", pady=(14, 0))
        tk.Label(warn, text="  ⚠  This action is irreversible. The file will be permanently deleted.",
                 font=("Segoe UI", 9), bg=WARN_BG, fg=WARN_FG,
                 anchor="w", padx=10, pady=8).pack(fill="x")

        row = tk.Frame(card, bg=CARD_BG)
        row.pack(anchor="w", pady=(14, 0))
        accent_btn(row, "⊗  Delete File", self._delete,
                   color=ERROR_BG, hover="#4a1515", fg=ERROR_FG).pack(side="left")

        self.del_msg = self._msg_label(card)

    def _build_browse(self):
        outer, card = self._card()
        self._panels["browse"] = outer

        top = tk.Frame(card, bg=CARD_BG)
        top.pack(fill="x", pady=(0, 12))
        card_title(top, "⊞", "Browse Files", "All files in the current workspace")
        accent_btn(top, "↺ Refresh", self._refresh_browse,
                   color="#1c2a3a", hover="#1e3a5f", fg=INFO_FG).pack(side="right", pady=4)

        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=INPUT_BG, fieldbackground=INPUT_BG,
                        foreground=TEXT_PRI, font=("Consolas", 10),
                        rowheight=30, borderwidth=0)
        style.configure("Dark.Treeview.Heading",
                        background=CARD_BORDER, foreground=TEXT_SEC,
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", "#1e3a5f")],
                  foreground=[("selected", INFO_FG)])

        tree_frame = tk.Frame(card, bg=CARD_BORDER)
        tree_frame.pack(fill="both", expand=True)
        inner_frame = tk.Frame(tree_frame, bg=INPUT_BG)
        inner_frame.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree = ttk.Treeview(inner_frame, columns=("name", "size", "ext"),
                                 show="headings", height=10, style="Dark.Treeview")
        self.tree.heading("name", text="  File Name")
        self.tree.heading("size", text="Size")
        self.tree.heading("ext", text="Type")
        self.tree.column("name", width=350, anchor="w")
        self.tree.column("size", width=90, anchor="e")
        self.tree.column("ext", width=80, anchor="w")

        sb = ttk.Scrollbar(inner_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        act = tk.Frame(card, bg=CARD_BG)
        act.pack(fill="x", pady=(12, 0))
        accent_btn(act, "◎ Read Selected", self._browse_read,
                   color=INFO_BG, hover="#0c2d5a", fg=INFO_FG).pack(side="left", padx=(0, 10))
        accent_btn(act, "⊗ Delete Selected", self._browse_delete,
                   color=ERROR_BG, hover="#4a1515", fg=ERROR_FG).pack(side="left")

    # ── Tab switching ─────────────────────────────────────────────────────
    def switch(self, key):
        for k, panel in self._panels.items():
            panel.pack_forget()
        for k, (row, btn, lft) in self._nav_refs.items():
            active = (k == key)
            lft.config(bg=ACCENT if active else SIDEBAR_BG)
            btn.config(bg="#1e3a5f" if active else SIDEBAR_BG,
                       fg=TEXT_PRI if active else TEXT_SEC,
                       font=("Segoe UI", 10, "bold" if active else "normal"))
        self._panels[key].pack(fill="both", expand=True)
        self._active_tab = key
        if key == "browse":
            self._refresh_browse()

    # ── Actions ───────────────────────────────────────────────────────────
    def _create(self):
        name = self.c_name.get().strip()
        content = self.c_body.get()
        if not name:
            return self._show_msg(self.c_msg, "Please enter a file name.", "error")
        if Path(name).exists():
            return self._show_msg(self.c_msg, f'"{name}" already exists.', "warn")
        try:
            with open(name, "w") as f:
                f.write(content)
            self.c_name.set("")
            self.c_body.delete()
            self._show_msg(self.c_msg, f'"{name}" created successfully.', "success")
        except Exception as e:
            self._show_msg(self.c_msg, str(e), "error")

    def _read(self):
        name = self.r_name.get().strip()
        if not name:
            return self._show_msg(self.r_msg, "Please enter a file name.", "error")
        if not Path(name).exists():
            return self._show_msg(self.r_msg, f'"{name}" does not exist.', "error")
        try:
            with open(name, "r") as f:
                data = f.read()
            self.r_out.config(state="normal")
            self.r_out.delete("1.0", "end")
            self.r_out.insert("end", data or "(empty file)")
            self.r_out.config(state="disabled")
            self._show_msg(self.r_msg, f'Loaded "{name}"', "info")
        except Exception as e:
            self._show_msg(self.r_msg, str(e), "error")

    def _update(self):
        name = self.u_name.get().strip()
        content = self.u_body.get()
        mode = self.u_mode.get()
        if not name:
            return self._show_msg(self.u_msg, "Please enter a file name.", "error")
        if not Path(name).exists():
            return self._show_msg(self.u_msg, f'"{name}" does not exist.', "error")
        try:
            with open(name, "a" if mode == "append" else "w") as f:
                f.write(content)
            self.u_body.delete()
            self._show_msg(self.u_msg, f'"{name}" updated ({mode}).', "success")
        except Exception as e:
            self._show_msg(self.u_msg, str(e), "error")

    def _delete(self):
        name = self.d_name.get().strip()
        if not name:
            return self._show_msg(self.del_msg, "Please enter a file name.", "error")
        if not Path(name).exists():
            return self._show_msg(self.del_msg, f'"{name}" does not exist.', "error")
        if not messagebox.askyesno("Confirm Delete",
                                   f'Permanently delete "{name}"?\nThis cannot be undone.',
                                   icon="warning"):
            return
        try:
            os.remove(name)
            self.d_name.set("")
            self._show_msg(self.del_msg, f'"{name}" deleted.', "success")
        except Exception as e:
            self._show_msg(self.del_msg, str(e), "error")

    def _refresh_browse(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in sorted(Path(".").rglob("*")):
            if item.is_file():
                sz = item.stat().st_size
                sz_str = f"{sz:,} B" if sz < 1024 else f"{sz/1024:.1f} KB"
                self.tree.insert("", "end", values=(str(item), sz_str, item.suffix or "—"))

    def _browse_read(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showinfo("No selection", "Please select a file first.")
        self.r_name.set(self.tree.item(sel[0])["values"][0])
        self.switch("read")
        self._read()

    def _browse_delete(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showinfo("No selection", "Please select a file first.")
        self.d_name.set(self.tree.item(sel[0])["values"][0])
        self.switch("delete")
        self._delete()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()