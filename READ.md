# 🛍️ Smart Price Hunter - Complete Setup Guide

Created by: **Harshit Srivastava**  
Project: **Real Web Scraping E-commerce Price Tracker**

---

## 📋 SYSTEM REQUIREMENTS

- **Windows 10/11** (or macOS/Linux)
- **Python 3.8 or higher**
- **Internet connection** (for web scraping)
- **Web browser** (Chrome, Firefox, Edge, Safari)

---

## 🚀 COMPLETE INSTALLATION GUIDE

### **STEP 1: Install Python**

#### **For Windows:**
1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Download **Python 3.11** or **Python 3.12** 
   - **IMPORTANT:** Check ✅ "Add Python to PATH" during installation

2. **Verify Python Installation:**
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x` or `Python 3.12.x`

3. **If Python command doesn't work, try:**
   ```cmd
   python3 --version
   py --version
   ```

#### **For macOS:**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Verify
python3 --version
```

#### **For Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify
python3 --version
```

---

### **STEP 2: Download Project Files**

1. **Create Project Folder:**
   ```cmd
   mkdir SmartPriceHunter
   cd SmartPriceHunter
   ```

2. **You should have these 3 files:**
   ```
   SmartPriceHunter/
   ├── enhanced_real_scraping_backend.py
   ├── enhanced_index.html  
   └── requirements.txt
   ```

---

### **STEP 3: Install Required Packages**

#### **For Windows (Command Prompt/PowerShell):**
```cmd
# Navigate to project folder
cd SmartPriceHunter

# Install packages
pip install -r requirements.txt
```

#### **If pip doesn't work, try:**
```cmd
python -m pip install -r requirements.txt
# OR
py -m pip install -r requirements.txt
# OR
python3 -m pip install -r requirements.txt
```

#### **For macOS/Linux:**
```bash
# Navigate to project folder
cd SmartPriceHunter

# Install packages
pip3 install -r requirements.txt
# OR
python3 -m pip install -r requirements.txt
```

#### **Manual Package Installation (if requirements.txt fails):**
```cmd
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install requests==2.31.0
pip install beautifulsoup4==4.12.2
pip install lxml==4.9.3
```

---

### **STEP 4: Run the Application**

#### **For Windows:**
```cmd
# Navigate to project folder
cd SmartPriceHunter

# Start the backend server
python enhanced_real_scraping_backend.py
```

#### **For macOS/Linux:**
```bash
# Navigate to project folder
cd SmartPriceHunter

# Start the backend server
python3 enhanced_real_scraping_backend.py
```

#### **Alternative Commands (if above doesn't work):**
```cmd
# Windows alternatives:
py enhanced_real_scraping_backend.py
python3 enhanced_real_scraping_backend.py

# macOS/Linux alternatives:
python enhanced_real_scraping_backend.py
```

---

### **STEP 5: Access the Web Application**

1. **After running the backend, you should see:**
   ```
   🚀 Starting ENHANCED Real Web Scraping Smart Price Hunter Backend...
   🕸️ ENHANCED FEATURES:
      ✅ Real product image extraction
      ✅ Real product link generation
      ✅ Enhanced error handling & fallbacks
   📍 Server will be available at: http://localhost:8000
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:8000
   * Running on http://localhost:8000
   ```

2. **Open your web browser and go to:**
   ```
   http://localhost:8000
   ```

3. **You should see the Smart Price Hunter interface!**

---

## 🔧 TROUBLESHOOTING

### **Problem 1: Python not found**
```cmd
# Try these commands:
python --version
python3 --version
py --version

# If none work, reinstall Python with "Add to PATH" checked
```

### **Problem 2: pip not found**
```cmd
# Try these:
python -m pip --version
python3 -m pip --version
py -m pip --version
```

### **Problem 3: Permission Error**
```cmd
# For Windows (run as Administrator):
pip install --user -r requirements.txt

# For macOS/Linux:
sudo pip3 install -r requirements.txt
```

### **Problem 4: Port 8000 already in use**
```cmd
# Kill process using port 8000:
# Windows:
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F

# macOS/Linux:
sudo lsof -i :8000
sudo kill -9 [PID_NUMBER]
```

### **Problem 5: Module not found errors**
```cmd
# Install missing modules individually:
pip install flask
pip install flask-cors  
pip install requests
pip install beautifulsoup4
pip install lxml
```

### **Problem 6: Firewall/Antivirus blocking**
- **Temporarily disable firewall/antivirus**
- **Allow Python through Windows Firewall**
- **Try different port:** Edit the backend file, change `port=8000` to `port=8080`

---

## 🎯 HOW TO USE

1. **Start the backend** (as shown above)
2. **Open http://localhost:8000** in your browser
3. **Enter a product name** (e.g., "iPhone 15", "Samsung TV", "Adidas shoes")
4. **Select sites to scrape** (Amazon India, Flipkart, Myntra, Snapdeal)
5. **Click "Start Web Scraping"**
6. **Wait for results** (shows real product images and purchase links)
7. **Click product links** to visit actual product pages

---

## 📱 FEATURES

✅ **Real Web Scraping** from Amazon India, Flipkart, Myntra, Snapdeal  
✅ **Real Product Images** extracted from websites  
✅ **Real Purchase Links** to actual product pages  
✅ **Price Comparison** across multiple sites  
✅ **Deal Score Calculation** based on price, rating, discount  
✅ **Responsive Design** works on mobile and desktop  
✅ **Error Handling** with fallback data if scraping fails  

---

## 🛑 STOPPING THE APPLICATION

**To stop the server:**
- **Press `Ctrl + C`** in the command prompt/terminal where the server is running
- **Close the command prompt/terminal window**

---

## 📞 SUPPORT

**If you encounter any issues:**
1. **Check Python version:** `python --version` (should be 3.8+)
2. **Check pip installation:** `pip --version`
3. **Verify all packages installed:** `pip list`
4. **Check firewall/antivirus settings**
5. **Try running as Administrator (Windows) or with sudo (macOS/Linux)**
6. **Contact project creator: Harshit Srivastava**

---

## 🎉 SUCCESS INDICATORS

**✅ Everything is working if:**
- Backend starts without errors
- You can access http://localhost:8000
- Web scraping returns product results
- Product images load properly
- Product links work and open actual e-commerce pages

**🎯 Enjoy using Smart Price Hunter!** 🛍️✨