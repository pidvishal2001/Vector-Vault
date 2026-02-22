**🛡️ Vector Vault v6.8: High-Density Binary-to-SVG Storage**

Vector Vault is a sophisticated data security and steganography tool that transforms any file type (EXE, PDF, MP3, etc.) into a series of encrypted, high-density SVG (Scalable Vector Graphics) segments. By leveraging the power of Python's multithreading and the AES-256 standard, it provides a unique way to store and transfer sensitive data in plain sight.



**🚀 Core Features**

Multithreaded Processing: Large files are processed in background threads, keeping the GUI responsive and eliminating "Not Responding" errors.



Recursive DNA Metadata: Every SVG segment carries an internal "DNA" tag containing the original filename, segment ID, and encryption salt for automatic reassembly.



Dual Security Layers:



AES-256 Encryption: Industry-standard protection via the Fernet protocol.



Steganographic Cloaking: Data is hidden within valid XML tags (<desc>) and pixelated PNG data inside the SVG.



Flexible Storage Options: Choose between saving to the source directory or a custom, hidden location.



Lossless Compression: Uses LZMA (High) or Zlib (Fast) to ensure bit-perfect restoration after reconstruction.



🛠️ Technical Architecture

1\. The DNA Header

Every generated SVG is a valid XML file. Within the <desc> tag, Vector Vault hides a Base64-encoded JSON manifest:



XML



<desc id="VAULT\_DNA">eyJ0IjogInBob3RvLmpwZyIsICJpZCI6IDAsICJtIjogInBhc3N3b3JkIiwgInMiOiA...</desc>

This manifest allows the Batch Unlock tool to sort and stitch segments even if filenames are randomized.



2\. Binary-to-Pixel Mapping

Data is mapped directly to RGB pixel values. Each pixel stores 3 bytes of raw binary data.



Red: Byte 1



Green: Byte 2



Blue: Byte 3



3\. Encryption Standard

The system uses PBKDF2HMAC with 100,000 iterations for key derivation, making brute-force attacks on passwords computationally expensive.



📦 Installation \& Setup

Clone the Repository:



Bash



git clone https://github.com/pidvishal2001/Vector-Vault.git

cd Vector-Vault

Install Dependencies:

Vector Vault requires Pillow for image processing and Cryptography for security.



Bash



pip install -r requirements.txt

Run the Application:



Bash



python v6_8.py

**📖 How to Use**

Locking a File

Select a File: Click the "Lock" button and choose any file.



Choose Security:



None: Direct encoding.



Password: Standard passphrase protection.



Keyfile: Use an image or any other file as a unique mathematical key.



Set Destination: Choose "Source Directory" or browse for a "Custom Location".



Process: The progress bar will track the encoding in real-time.



Unlocking a Folder

Select Folder: Click "Unlock" and select the folder containing your SVG segments.



Verification: The tool scans the "DNA" of every file to ensure the sequence is correct.



Restore: The original file is reconstructed as RECOVERED\_\[OriginalName].



**⚖️ License \& Disclaimer**

This software is provided for educational and personal data management purposes. The developers are not responsible for any data loss or misuse. Always maintain a backup of your original keys and keyfiles.

