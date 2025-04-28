import os
import uuid
import json
from flask import Flask, jsonify, send_file, request
import google.generativeai as genai
import markdown2
import weasyprint
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

# --- Flask App ---
flask_app = Flask(__name__)

# --- Gemini AI Setup ---
def initialize_gemini():
    try:
        api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBZStWeNIXb041LngvdDKHDf-6t9DPlDQE")
        genai.configure(api_key=api_key)
        print("Gemini AI initialized successfully")
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Gemini initialization failed: {e}")
        return None

model = initialize_gemini()

# --- Prompt Templates ---
PROMPTS = {
    "tldr": "Generate a 2-sentence executive summary of this research: {input}",
    "abstract": "Generate a detailed abstract for this research paper: {input}",
    "cleanup": "Rephrase this content for academic publication: {input}",
    "structure": """Convert to markdown with these sections:
# {title}
**Authors**: {authors}
## Problem Statement
{problem}
## Methodology
{methodology}
## Key Findings
{findings}
## Insights
{insights}
## Relevance to AI Education
{relevance}
## Future Directions
{future_work}
Format using IEEE conference style guidelines."""
}

LOCAL_STORAGE = "research_data.json"

# --- Flask Endpoints ---
@flask_app.route('/')
def home():
    return '''
    <html>
        <head><title>Research Whitepaper Generator</title></head>
        <body>
            <h1>Research Whitepaper Generator API</h1>
            <p>This Proof of Concept (POC) demonstrates a multi-step whitepaper generation process using Google Gemini AI. Key concepts used include:</p>
            <ul>
                <li><strong>Prompt Chaining:</strong> We generate results in stages, starting with TLDR summaries, progressing to structured abstracts, and finally rephrased academic content.</li>
                <li><strong>AI Model:</strong> The <em>Gemini 1.5 Flash</em> model is used to generate content at each step, ensuring comprehensive and accurate results.</li>
            </ul>
            <p>Access the <a href="/dash">Dash UI</a> to generate reports and explore the features.</p>
        </body>
    </html>
    '''

@flask_app.route('/generate', methods=['POST'])
def generate_report():
    if not model:
        return jsonify({"error": "Gemini AI not initialized"}), 503

    try:
        # Step 1: Get input data
        data = request.json
        input_data = "\n".join([f"{k}: {v}" for k, v in data.items()])
        print(f"Received input data: {input_data}")

        outputs = {}

        # --- Step 2: Generate TLDR Summary ---
        print("Generating TLDR summary...")
        prompt_tldr = PROMPTS["tldr"].format(input=input_data)
        response_tldr = model.generate_content(prompt_tldr)
        outputs['tldr'] = response_tldr.text
        print(f"TLDR Summary: {outputs['tldr']}")

        # --- Step 3: Generate Abstract ---
        print("Generating Abstract based on TLDR...")
        prompt_abstract = PROMPTS["abstract"].format(input=outputs['tldr'])
        response_abstract = model.generate_content(prompt_abstract)
        outputs['abstract'] = response_abstract.text
        print(f"Abstract: {outputs['abstract']}")

        # --- Step 4: Cleanup Content ---
        print("Rephrasing content for academic publication...")
        prompt_cleanup = PROMPTS["cleanup"].format(input=outputs['abstract'])
        response_cleanup = model.generate_content(prompt_cleanup)
        outputs['cleanup'] = response_cleanup.text
        print(f"Cleaned-up content: {outputs['cleanup']}")

        # --- Step 5: Structure Content in Markdown ---
        print("Structuring content in markdown format...")
        prompt_structure = PROMPTS["structure"].format(
            title=data["title"],
            authors=data["authors"],
            problem=data["problem"],
            methodology=data["methodology"],
            findings=data["findings"],
            insights=data["insights"],
            relevance=data["relevance"],
            future_work=data["future_work"]
        )
        response_structure = model.generate_content(prompt_structure)
        outputs['structure'] = response_structure.text
        print(f"Structured Content (Markdown): {outputs['structure']}")

        # --- Step 6: Generate PDF using WeasyPrint ---
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.pdf"
        pdf_path = os.path.join(os.getcwd(), filename)

        # Convert the HTML (Markdown converted) content to PDF using WeasyPrint
        html_content = markdown2.markdown(outputs['structure'])
        weasyprint.HTML(string=html_content).write_pdf(pdf_path)

        # --- Step 7: Save Entry in Local Storage ---
        entry = {
            "id": unique_id,
            "raw": data,
            "processed": outputs,
            "pdf_filename": filename,
            "html": html_content
        }

        with open(LOCAL_STORAGE, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        print(f"Saved entry with ID: {unique_id}")

        return jsonify({
            "html": entry["html"],
            "pdf_filename": entry["pdf_filename"],
            "id": entry["id"]
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@flask_app.route('/download/<filename>')
def download_file(filename):
    if not filename.endswith('.pdf') or '..' in filename:
        return "Invalid filename", 400
    
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

# --- Dash UI Integration ---
dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dash/')

dash_app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1("AI Research Whitepaper Generator", style={'textAlign': 'center', 'color': '#365dd6'}),
    html.P("Generate detailed research papers by filling in the form below. This tool uses AI to create summaries, abstracts, and academic content based on the input you provide.", style={'textAlign': 'center', 'fontSize': '18px'}),
    
    # Input Fields
    dcc.Input(id='title', placeholder='Title', style={'width': '100%', 'marginTop': '10px'}, value='Impact of AI in Education'),
    dcc.Input(id='authors', placeholder='Authors', style={'width': '100%', 'marginTop': '10px'}, value='Dr. A. Smith, Prof. B. Johnson'),
    dcc.Textarea(id='problem', placeholder='Problem Statement', style={'width': '100%', 'marginTop': '10px'}, value="How AI can personalize learning paths and improve student outcomes."),
    dcc.Textarea(id='methodology', placeholder='Methodology', style={'width': '100%', 'marginTop': '10px'}, value="We conducted a meta-analysis of 50 AI-assisted education programs across universities."),
    dcc.Textarea(id='findings', placeholder='Key Findings', style={'width': '100%', 'marginTop': '10px'}, value="AI improves learning retention by 30% compared to traditional methods."),
    dcc.Textarea(id='insights', placeholder='Insights', style={'width': '100%', 'marginTop': '10px'}, value="Students show increased motivation and engagement with AI tools."),
    dcc.Textarea(id='relevance', placeholder='Relevance to AI Education', style={'width': '100%', 'marginTop': '10px'}, value="Demonstrates practical AI applications for scalable personalized education."),
    dcc.Textarea(id='future_work', placeholder='Future Work', style={'width': '100%', 'marginTop': '10px'}, value="Investigate AI bias mitigation techniques in education."),
    
    # Submit Button
    html.Button('Generate Report', id='submit-button', n_clicks=0, style={'marginTop': '20px', 'padding': '10px 20px', 'backgroundColor': '#365dd6', 'color': 'white', 'border': 'none', 'cursor': 'pointer'}),
    
    # Output Preview
    html.Div(id='output-preview', style={'marginTop': '20px'}),
    
    # Download Link
    html.Div(id='download-link', style={'marginTop': '20px'})
])

@dash_app.callback(
    [Output('output-preview', 'children'), Output('download-link', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('title', 'value'), State('authors', 'value'), State('problem', 'value'),
     State('methodology', 'value'), State('findings', 'value'), State('insights', 'value'),
     State('relevance', 'value'), State('future_work', 'value')]
)
def generate_callback(n_clicks, title, authors, problem, methodology, findings, insights, relevance, future_work):
    if n_clicks == 0:
        return "", ""
    
    data = {
        "title": title or "Untitled",
        "authors": authors or "Anonymous",
        "problem": problem or "",
        "methodology": methodology or "",
        "findings": findings or "",
        "insights": insights or "",
        "relevance": relevance or "",
        "future_work": future_work or ""
    }
    
    try:
        client = flask_app.test_client()
        response = client.post('/generate', json=data)

        result = json.loads(response.data.decode())
        
        if "error" in result:
            return html.Div(f"Error: {result['error']}", style={'color': 'red'}), ""

        download_link = html.A(
            'Download PDF',
            href=f'/download/{result["pdf_filename"]}',
            download=result["pdf_filename"],
            style={'color': '#365dd6', 'fontSize': '18px'}
        )

        return html.Div(f"Here is your generated report:", style={'fontSize': '18px'}), download_link

    except Exception as e:
        return html.Div(f"Error generating report: {str(e)}", style={'color': 'red'}), ""

if __name__ == '__main__':
    flask_app.run(debug=True)
