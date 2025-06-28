# 🧠 Research Whitepaper Generator

> **Generate branded whitepapers and blog posts from employee research using Gemini AI. Export as PDF or HTML. Modular, embeddable across existing tools/sites.**

---

## 📚 Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
  - [Flask API](#flask-api)
  - [Dash UI](#dash-ui)
- [Endpoints](#endpoints)
- [Folder Structure](#folder-structure)
- [Workflow](#workflow)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 📖 About the Project

This project transforms raw research input into professional, structured whitepapers and blog posts. Powered by Google's **Gemini 1.5 Flash** AI model, it automates:
- Executive summaries (TLDRs)
- Academic abstracts
- Full-fledged whitepapers
- SEO-optimized blogs
- Exporting in PDF and HTML formats

Built using:
- **Python** (Flask + Dash)
- **Gemini AI** (Generative AI API)

---

## ✨ Features
- 🧠 Summarization and Expansion with Gemini
- 📄 Automatic Whitepaper and Blog Structuring
- 📥 Upload and Store Research
- 🌐 Exportable Outputs (PDF / HTML)
- 📊 Modular Design (can be integrated into websites, internal portals)
- 🔒 Secure API Key Handling

---

## 🛠️ Tech Stack
- **Backend:** Flask
- **Frontend:** Dash (Plotly)
- **AI Engine:** Google Gemini 1.5 Flash
- **Storage:** Local filesystem (`outputs/`)
- **Deployment Ready:** Dockerfile (optional)

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/research-whitepaper-generator.git
cd research-whitepaper-generator
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory and add:

```bash
GOOGLE_API_KEY=your_gemini_api_key
```

---

## 🚀 Usage

### 1. Flask API

```bash
python main.py
```

The API will start at `http://localhost:8000/`.

### 2. Dash UI

Visit `http://localhost:8000/ui` in your browser.

Upload your research text, choose output format (PDF/HTML), and generate.

---

## 📬 Endpoints

| Method | Endpoint         | Description                           |
|:------:|:----------------- |:------------------------------------- |
| POST   | `/generate_paper` | Generates a whitepaper/blog          |
| GET    | `/download/<type>/<filename>` | Downloads the generated PDF/HTML |
| GET    | `/ui`             | Opens Dash-based UI                  |

---

## 🗂️ Folder Structure

```
research-whitepaper-generator/
├── main.py
├── requirements.txt
├── outputs/
│   ├── pdf/
│   └── html/
├── templates/
│   └── whitepaper_template.html
├── static/
│   └── (optional css/js files)
├── .env
└── README.md
```

---
## steps to run the code base given in howtorun.txt

## 🔄 Workflow

1. Employee uploads their research notes.
2. Gemini AI generates:
   - Short TLDR
   - Academic abstract
   - Detailed whitepaper structure
   - SEO blog post
3. File saved in `/outputs/pdf/` or `/outputs/html/`.
4. Option to download directly.

---

## 🚀 Future Enhancements

- [ ] Multi-language whitepaper generation
- [ ] Email sharing directly from UI
- [ ] Integration with Notion, Confluence, SharePoint
- [ ] Version history for documents
- [ ] Admin dashboard for managing submissions

---

## 📝 License

This project is licensed under the MIT License.

---
