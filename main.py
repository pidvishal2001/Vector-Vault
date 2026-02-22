import os, json, math, hashlib, base64, lzma, zlib, threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from io import BytesIO
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class VectorVaultV6_8:
    def __init__(self, root):
        self.root = root
        self.root.title("Vector Vault V6.8 [Storage Options]")
        self.root.geometry("550x700")
        self.root.configure(bg="#ffffff")
        self.dpi, self.max_dim = 300, 3000

        # UI Setup
        f = tk.Frame(root, bg="#ffffff")
        f.pack(pady=20, padx=20, fill="both", expand=True)
        
        tk.Label(f, text="🛡️ VECTOR VAULT V6.8", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#27ae60").pack(pady=10)
        
        # --- Save Options Section ---
        save_f = tk.LabelFrame(f, text=" Save To Options ", bg="#ffffff", fg="#333333", padx=10, pady=10)
        save_f.pack(fill="x", pady=10)
        
        self.save_mode = tk.StringVar(value="source")
        tk.Radiobutton(save_f, text="Source Directory", variable=self.save_mode, value="source", bg="#ffffff", command=self.toggle_save_path).pack(side="left", padx=10)
        tk.Radiobutton(save_f, text="Custom Location", variable=self.save_mode, value="custom", bg="#ffffff", command=self.toggle_save_path).pack(side="left", padx=10)
        
        self.custom_path = tk.StringVar(value="No location selected...")
        self.path_btn = tk.Button(save_f, text="Browse", command=self.pick_save_dir, state="disabled", font=("Segoe UI", 8))
        self.path_btn.pack(side="right", padx=5)
        self.path_label = tk.Label(save_f, textvariable=self.custom_path, font=("Segoe UI", 8, "italic"), bg="#ffffff", fg="#888888")
        self.path_label.pack(side="right", padx=5)

        # --- Compression & Segments ---
        opt_f = tk.Frame(f, bg="#ffffff")
        opt_f.pack(fill="x")
        
        tk.Label(opt_f, text="Compression Level:", bg="#ffffff").pack(side="left", padx=5)
        self.comp_var = tk.StringVar(value="High (Smallest)")
        ttk.Combobox(opt_f, textvariable=self.comp_var, values=["High (Smallest)", "Fast (Large)"], state="readonly", width=15).pack(side="left", pady=5)

        tk.Label(opt_f, text="Segments:", bg="#ffffff").pack(side="left", padx=10)
        self.seg_var = tk.StringVar(value="Auto")
        ttk.Combobox(opt_f, textvariable=self.seg_var, values=["Auto", "1", "3", "5", "10", "50"], state="readonly", width=8).pack(side="left", pady=5)

        # Security
        tk.Label(f, text="Security Mode:", bg="#ffffff", fg="#333333").pack(pady=(15,0))
        self.key_mode = tk.StringVar(value="none")
        mf = tk.Frame(f, bg="#ffffff")
        mf.pack()
        for m in [("None", "none"), ("Password", "password"), ("Keyfile", "keyfile")]:
            tk.Radiobutton(mf, text=m[0], variable=self.key_mode, value=m[1], bg="#ffffff").pack(side="left", padx=5)

        self.pass_entry = tk.Entry(f, show="*", width=40, bg="#f2f2f2", relief="flat", bd=2)
        self.pass_entry.pack(pady=10, ipady=3)

        # Buttons
        self.btn_lock = tk.Button(f, text="LOCK & ENCODE (SVG)", command=self.start_lock_thread, 
                  bg="#2ecc71", fg="white", font=("Segoe UI", 11, "bold"), width=30, height=2, relief="flat")
        self.btn_lock.pack(pady=15)
        
        self.btn_unlock = tk.Button(f, text="UNLOCK & RECONSTRUCT", command=self.start_unlock_thread, 
                  bg="#3498db", fg="white", font=("Segoe UI", 11, "bold"), width=30, height=2, relief="flat")
        self.btn_unlock.pack(pady=5)

        # Progress Section
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(f, textvariable=self.status_var, bg="#ffffff", fg="#666666", font=("Segoe UI", 9, "italic")).pack(pady=(20,0))
        self.progress = ttk.Progressbar(f, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

    # --- MISSING METHOD RESTORED HERE ---
    def set_status(self, text, val):
        self.status_var.set(text)
        self.progress['value'] = val
        self.root.update_idletasks()

    def toggle_save_path(self):
        if self.save_mode.get() == "custom":
            self.path_btn.config(state="normal")
            self.path_label.config(fg="#333333")
        else:
            self.path_btn.config(state="disabled")
            self.path_label.config(fg="#888888")

    def pick_save_dir(self):
        d = filedialog.askdirectory()
        if d: self.custom_path.set(d)

    def derive_key(self, salt, mode):
        if mode == "none" or not salt: return None
        if mode == "password":
            p = self.pass_entry.get().encode()
            if not p: raise ValueError("Password required.")
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
            return base64.urlsafe_b64encode(kdf.derive(p))
        else:
            kf = filedialog.askopenfilename(title="Select Keyfile")
            if not kf: raise ValueError("No Keyfile selected.")
            with open(kf, "rb") as f: h = hashlib.sha256(f.read()).digest()
            return base64.urlsafe_b64encode(h)

    def start_lock_thread(self):
        p = filedialog.askopenfilename()
        if not p: return
        self.btn_lock.config(state="disabled")
        threading.Thread(target=self.create_vault, args=(p,), daemon=True).start()

    def start_unlock_thread(self):
        fold = filedialog.askdirectory()
        if not fold: return
        self.btn_unlock.config(state="disabled")
        threading.Thread(target=self.reconstruct_vault, args=(fold,), daemon=True).start()

    def create_vault(self, p):
        try:
            if self.save_mode.get() == "custom":
                base_out = self.custom_path.get()
                if not os.path.isdir(base_out): raise ValueError("Invalid custom location.")
                od = os.path.join(base_out, os.path.basename(p) + "_vault_v6")
            else:
                od = p + "_vault_v6"

            self.set_status("Reading & Compressing...", 10)
            with open(p, "rb") as f: d = f.read()
            is_high = "High" in self.comp_var.get()
            comp = lzma.compress(d) if is_high else zlib.compress(d)
            
            self.set_status("Encrypting...", 30)
            salt = os.urandom(16)
            mode = self.key_mode.get()
            key = self.derive_key(salt, mode)
            blob = Fernet(key).encrypt(comp) if key else comp
            
            num = math.ceil(len(blob)/(self.max_dim**2*3)) if self.seg_var.get() == "Auto" else int(self.seg_var.get())
            os.makedirs(od, exist_ok=True)
            bc = math.ceil(len(blob)/num)

            for i in range(num):
                self.set_status(f"Generating Segment {i+1}/{num}...", 30 + (i/num * 60))
                c = blob[i*bc:(i+1)*bc]
                if not c: continue
                side = max(3, math.ceil(math.sqrt(math.ceil(len(c)/3))))
                img = Image.new('RGB', (side, side), (255, 255, 255))
                px, idx = img.load(), 0
                for y in range(side):
                    for x in range(side):
                        if idx < len(c):
                            r, g, b = c[idx], (c[idx+1] if idx+1 < len(c) else 0), (c[idx+2] if idx+2 < len(c) else 0)
                            px[x,y], idx = (r,g,b), idx+3
                
                buf = BytesIO(); img.save(buf, format="PNG")
                b64_img = base64.b64encode(buf.getvalue()).decode()
                meta = {"n": os.path.basename(p), "id": i, "m": mode, "s": base64.urlsafe_b64encode(salt).decode() if key else None, "c": "l" if is_high else "z", "sz": len(c), "d": side}
                m_str = base64.urlsafe_b64encode(json.dumps(meta).encode()).decode()
                
                with open(os.path.join(od, f"part_{i+1}.svg"), "w", encoding="utf-8") as f:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    f.write(f'<svg viewBox="0 0 {side} {side}" xmlns="http://www.w3.org/2000/svg">\n')
                    f.write(f'  <desc id="VAULT_DNA">{m_str}</desc>\n')
                    f.write(f'  <image width="{side}" height="{side}" href="data:image/png;base64,{b64_img}" style="image-rendering:pixelated"/>\n')
                    f.write('</svg>')
            
            self.set_status("Vault Created!", 100)
            messagebox.showinfo("Success", f"Vault created in:\n{od}")
        except Exception as e: messagebox.showerror("Error", str(e))
        finally: 
            self.btn_lock.config(state="normal")
            self.set_status("Ready", 0)

    def reconstruct_vault(self, fold):
        try:
            self.set_status("Scanning DNA...", 10)
            segs = []
            files = [f for f in os.listdir(fold) if f.lower().endswith(".svg")]
            for idx, fn in enumerate(files):
                self.set_status(f"Reading: {idx+1}/{len(files)}", 10 + (idx/len(files) * 30))
                with open(os.path.join(fold, fn), "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if 'id="VAULT_DNA"' in content:
                        m_start = content.find('VAULT_DNA">') + 11
                        m_end = content.find('</desc>', m_start)
                        meta = json.loads(base64.urlsafe_b64decode(content[m_start:m_end]).decode())
                        b_start = content.find("base64,") + 7
                        b_end = content.find('"', b_start)
                        segs.append((meta, content[b_start:b_end]))
            
            if not segs: raise ValueError("No DNA found.")
            segs.sort(key=lambda x: x[0]["id"])
            stream = bytearray()
            
            for idx, (m, b64) in enumerate(segs):
                self.set_status(f"Processing: {idx+1}/{len(segs)}", 40 + (idx/len(segs) * 40))
                px = Image.open(BytesIO(base64.b64decode(b64))).load()
                ch = bytearray()
                for y in range(m["d"]):
                    for x in range(m["d"]): ch.extend(px[x,y])
                stream.extend(ch[:m["sz"]])

            self.set_status("Finishing...", 90)
            m0 = segs[0][0]
            salt = base64.urlsafe_b64decode(m0["s"]) if m0["s"] else None
            key = self.derive_key(salt, m0["m"])
            proc = Fernet(key).decrypt(bytes(stream)) if key else bytes(stream)
            final = lzma.decompress(proc) if m0["c"] == "l" else zlib.decompress(proc)
            
            with open(os.path.join(fold, "RECOVERED_" + m0["n"]), "wb") as f: f.write(final)
            self.set_status("Complete!", 100)
            messagebox.showinfo("Success", "File Reconstructed!")
        except Exception as e: messagebox.showerror("Error", f"Failed: {str(e)}")
        finally: 
            self.btn_unlock.config(state="normal")
            self.set_status("Ready", 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = VectorVaultV6_8(root)
    root.mainloop()