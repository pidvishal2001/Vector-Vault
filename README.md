# 🛡️ Vector Vault v6.8
## High-Density Binary-to-SVG Storage

**Vector Vault** is a sophisticated data security and steganography tool that transforms *any file type* (EXE, PDF, MP3, ZIP, etc.) into encrypted, high-density SVG (Scalable Vector Graphics) segments.

> Store sensitive data in plain sight — inside valid SVG files.

It combines **AES-256 encryption**, multithreading, compression, and pixel-based binary mapping into a single powerful system.

---

# 🚀 Core Features

## ⚡ Multithreaded Processing

Large files are processed in background threads, keeping the GUI responsive and preventing ~~Not Responding~~ errors.

---

## 🧬 Recursive DNA Metadata

Every SVG segment contains an internal **DNA tag** storing:

- Original filename  
- Segment ID  
- Encryption salt  

This allows automatic reassembly even if filenames are randomized.

Example:

```xml
<desc id="VAULT_DNA">
eyJ0IjogInBob3RvLmpwZyIsICJpZCI6IDAsICJtIjogInBhc3N3b3JkIiwgInMiOiA...
</desc>
```

---

## 🔐 Dual Security Layers

### 1️⃣ AES-256 Encryption

Uses **PBKDF2HMAC** with 100,000 iterations and Fernet (AES-256 under the hood).

This makes brute-force attacks computationally expensive.

Key derivation flow:

```
Password → PBKDF2HMAC → 100,000 iterations → AES-256 Key → Fernet Encryption
```

---

### 2️⃣ Steganographic Cloaking

Encrypted data is hidden inside:

- Valid XML `<desc>` tags  
- Pixel-encoded PNG data embedded within SVG  

Each pixel stores **3 bytes** of raw binary:

| Channel | Stores |
|---------|--------|
| 🔴 Red   | Byte 1 |
| 🟢 Green | Byte 2 |
| 🔵 Blue  | Byte 3 |

---

## 📦 Lossless Compression

Choose between:

- **LZMA** (High Compression)
- **Zlib** (Fast Compression)

Ensures ***bit-perfect*** restoration after reconstruction.

---

# 🛠️ Technical Architecture

## 1️⃣ DNA Header System

Every generated SVG is a valid XML file.

Inside the `<desc>` tag, a Base64-encoded JSON manifest is embedded.

This enables:

- Segment sorting  
- Integrity validation  
- Automatic stitching  

---

## 2️⃣ Binary-to-Pixel Mapping

Raw binary is mapped directly into RGB pixel values.

This allows extremely dense storage inside image data without breaking SVG validity.

---

## 3️⃣ Encryption Details

- Algorithm: **AES-256**
- KDF: `PBKDF2HMAC`
- Iterations: 100,000
- Salt: Random per session
- Protocol: `Fernet`

Security strength increases with stronger passwords or keyfiles.

---

# 📦 Installation & Setup

## 1️⃣ Clone Repository

Use `git clone` to download the project:

```bash
git clone https://github.com/pidvishal2001/Vector-Vault.git
cd Vector-Vault
```

---

## 2️⃣ Install Dependencies

Vector Vault requires:

- Pillow
- cryptography

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Application

```bash
python v6_8.py
```

---

# 📖 How To Use

## 🔒 Locking a File

1. Click **Lock**
2. Select a file
3. Choose security mode:
   - **None** → Direct encoding  
   - **Password** → Standard protection  
   - **Keyfile** → Use an image or file as mathematical key  
4. Choose destination:
   - Source Directory  
   - Custom Location  
5. Start process  
6. Monitor real-time progress bar  

---

## 🔓 Unlocking a Folder

1. Click **Unlock**
2. Select folder containing SVG segments
3. Tool scans DNA metadata
4. Segments are validated and stitched
5. Restored file appears as:

`RECOVERED_[OriginalName]`

---

# ⚖️ License & Disclaimer

> This software is provided for educational and personal data management purposes.

The developers are **not responsible** for:

- Data loss  
- Misuse  
- Lost passwords  
- Lost keyfiles  

Always maintain backups of:

- Original files  
- Passwords  
- Keyfiles  

---

# ⭐ Why Vector Vault?

✔ Stores sensitive data inside standard SVG files  
✔ Dual-layer encryption + steganography  
✔ Lossless reconstruction  
✔ Multithreaded architecture  
✔ High-density binary mapping  

---

## 🧠 Final Note

**Vector Vault v6.8** is designed to demonstrate how cryptography, compression, and steganography can work together inside modern file formats.

<ins>Use responsibly.</ins>  
