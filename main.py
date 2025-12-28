import os
import shutil
import glob
import time
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

APP_TITLE = "Hogwarts Legacy – Epic ⇄ Steam Save Manager"
SAVE_ROOT_DEFAULT = os.path.join(os.environ.get("LOCALAPPDATA", ""), "HogwartsLegacy", "Saved", "SaveGames")
BACKUP_DIR = "_Backups"

# =========================
#  UTILIDADES
# =========================

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

def human_time(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))

def get_backup_root(save_root):
    p = os.path.join(save_root, BACKUP_DIR)
    ensure_dir(p)
    return p

def list_saves(folder):
    return sorted(glob.glob(os.path.join(folder, "HL-*.sav")))

def has_valid_save(folder):
    return bool(list_saves(folder)) and os.path.exists(os.path.join(folder, "SaveGameList.sav"))

def detect_platform(folder):
    """
    Heurística:
    - Steam suele tener carpeta creada más recientemente al instalar
    - Epic suele tener saves más antiguos
    """
    mtime = os.path.getmtime(folder)
    return "Steam" if time.time() - mtime < 60 * 60 * 24 * 30 else "Epic"

# =========================
#  BACKUPS
# =========================

def create_backup(save_root, src_folder, label="AUTO"):
    if not has_valid_save(src_folder):
        raise RuntimeError("No hay saves válidos para respaldar")

    backup_root = get_backup_root(save_root)
    name = f"{timestamp()}_{label}"
    dest = os.path.join(backup_root, name)
    ensure_dir(dest)

    files = list_saves(src_folder)
    files.append(os.path.join(src_folder, "SaveGameList.sav"))

    for f in files:
        shutil.copy2(f, os.path.join(dest, os.path.basename(f)))

    return dest, len(files)

def list_backups(save_root):
    root = get_backup_root(save_root)
    return sorted(
        [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))],
        reverse=True
    )

def restore_backup(backup_path, dst_folder):
    files = glob.glob(os.path.join(backup_path, "*.sav"))
    if not files:
        raise RuntimeError("Backup vacío o inválido")

    for f in files:
        shutil.copy2(f, os.path.join(dst_folder, os.path.basename(f)))

    return len(files)

def export_backup_zip(backup_path, out_zip):
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in glob.glob(os.path.join(backup_path, "*.sav")):
            z.write(f, arcname=os.path.basename(f))

# =========================
#  CONVERSIÓN
# =========================

def convert_saves(src, dst, save_root):
    # AUTO BACKUP OBLIGATORIO
    create_backup(save_root, src, "PRE_CONVERT")

    files = list_saves(src)
    files.append(os.path.join(src, "SaveGameList.sav"))

    for f in files:
        shutil.copy2(f, os.path.join(dst, os.path.basename(f)))

# =========================
#  GUI
# =========================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("920x600")

        self.dark_mode = tk.BooleanVar(value=False)
        self.save_root = tk.StringVar(value=SAVE_ROOT_DEFAULT)
        self.src = tk.StringVar()
        self.dst = tk.StringVar()

        self.build_ui()
        self.refresh_folders()
        self.refresh_backups()

    # --------------------

    def build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="SaveGames:").pack(anchor="w")
        ttk.Entry(top, textvariable=self.save_root).pack(fill="x")
        ttk.Button(top, text="Refrescar", command=self.refresh_folders).pack(pady=4)

        ttk.Checkbutton(top, text="Modo oscuro", variable=self.dark_mode, command=self.toggle_theme).pack(anchor="e")

        mid = ttk.Frame(self, padding=10)
        mid.pack(fill="both", expand=True)

        # LEFT
        left = ttk.LabelFrame(mid, text="Carpetas detectadas", padding=8)
        left.pack(side="left", fill="both", expand=True)

        self.listbox = tk.Listbox(left, height=18)
        self.listbox.pack(fill="both", expand=True)

        ttk.Button(left, text="Usar como Origen", command=self.set_src).pack(fill="x", pady=2)
        ttk.Button(left, text="Usar como Destino", command=self.set_dst).pack(fill="x")

        # RIGHT
        right = ttk.LabelFrame(mid, text="Conversión", padding=8)
        right.pack(side="right", fill="both", expand=True, padx=10)

        ttk.Label(right, text="Origen:").pack(anchor="w")
        ttk.Entry(right, textvariable=self.src).pack(fill="x")

        ttk.Label(right, text="Destino:").pack(anchor="w", pady=(6,0))
        ttk.Entry(right, textvariable=self.dst).pack(fill="x")

        ttk.Button(
            right,
            text="Convertir Epic ⇄ Steam (con Backup automático)",
            command=self.convert
        ).pack(fill="x", pady=10)

        ttk.Label(
            right,
            text="⚠️ Desactiva Steam Cloud antes de abrir el juego",
            foreground="red"
        ).pack()

        # BACKUPS
        backup = ttk.LabelFrame(self, text="Copias de Seguridad", padding=8)
        backup.pack(fill="x", padx=10, pady=8)

        self.backup_list = tk.Listbox(backup, height=5)
        self.backup_list.pack(fill="x")

        bbtn = ttk.Frame(backup)
        bbtn.pack(fill="x", pady=4)

        ttk.Button(bbtn, text="Backup manual (Origen)", command=self.manual_backup).pack(side="left")
        ttk.Button(bbtn, text="Restaurar → Destino", command=self.restore).pack(side="left", padx=5)
        ttk.Button(bbtn, text="Exportar ZIP", command=self.export_zip).pack(side="left", padx=5)

        # LOG
        self.log = tk.Text(self, height=8)
        self.log.pack(fill="both", padx=10, pady=6)

    # --------------------

    def log_write(self, msg):
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    def refresh_folders(self):
        self.listbox.delete(0, "end")
        root = self.save_root.get()

        for d in os.listdir(root):
            p = os.path.join(root, d)
            if os.path.isdir(p) and has_valid_save(p):
                plat = detect_platform(p)
                slots = len(list_saves(p))
                self.listbox.insert("end", f"{d} | {plat} | Slots: {slots}")

    def refresh_backups(self):
        self.backup_list.delete(0, "end")
        for b in list_backups(self.save_root.get()):
            self.backup_list.insert("end", os.path.basename(b))

    def selected_folder(self):
        sel = self.listbox.curselection()
        if not sel:
            return None
        return os.path.join(self.save_root.get(), self.listbox.get(sel[0]).split(" | ")[0])

    def set_src(self):
        p = self.selected_folder()
        if p:
            self.src.set(p)

    def set_dst(self):
        p = self.selected_folder()
        if p:
            self.dst.set(p)

    def convert(self):
        try:
            convert_saves(self.src.get(), self.dst.get(), self.save_root.get())
            self.log_write("[OK] Conversión completada con backup automático")
            messagebox.showinfo("Listo", "Conversión exitosa.\nBackup creado automáticamente.")
            self.refresh_backups()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def manual_backup(self):
        try:
            path, count = create_backup(self.save_root.get(), self.src.get(), "MANUAL")
            self.log_write(f"[BACKUP] {count} archivos → {path}")
            self.refresh_backups()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def selected_backup(self):
        sel = self.backup_list.curselection()
        if not sel:
            return None
        return os.path.join(get_backup_root(self.save_root.get()), self.backup_list.get(sel[0]))

    def restore(self):
        try:
            b = self.selected_backup()
            restore_backup(b, self.dst.get())
            self.log_write("[RESTORE] Backup restaurado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_zip(self):
        b = self.selected_backup()
        if not b:
            return
        out = filedialog.asksaveasfilename(defaultextension=".zip")
        if out:
            export_backup_zip(b, out)
            self.log_write(f"[ZIP] Exportado → {out}")

    def toggle_theme(self):
        if self.dark_mode.get():
            self.configure(bg="#1e1e1e")
            self.log.configure(bg="#111", fg="white")
        else:
            self.configure(bg="")
            self.log.configure(bg="white", fg="black")


# =========================

if __name__ == "__main__":
    App().mainloop()
