import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
import json
import fitz
from werkzeug.utils import secure_filename

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("A chave da API do Google não foi encontrada. Verifique seu arquivo .env")
genai.configure(api_key=api_key)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisar():
    texto_email = ""
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                if filename.lower().endswith('.pdf'):
                    with fitz.open(filepath) as doc:
                        for page in doc:
                            texto_email += page.get_text()
                elif filename.lower().endswith('.txt'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        texto_email = f.read()
            except Exception as e:
                return jsonify({'erro': f'Erro ao ler o arquivo: {e}'}), 500
            finally:
                os.remove(filepath)
        else:
            return jsonify({'erro': 'Tipo de arquivo não permitido. Use .txt ou .pdf'}), 400

    else:
        dados = request.get_json()
        if not dados or 'email_texto' not in dados:
            return jsonify({'erro': 'Nenhum texto ou arquivo enviado'}), 400
        texto_email = dados['email_texto']

    if not texto_email.strip():
        return jsonify({'erro': 'O conteúdo do e-mail está vazio.'}), 400

    try:
        classificacao, resposta_sugerida = classificar_e_responder(texto_email)
        return jsonify({
            'classificacao': classificacao,
            'resposta_sugerida': resposta_sugerida
        })
    except Exception as e:
        print(f"Ocorreu um erro na análise: {e}")
        return jsonify({'erro': 'Ocorreu um erro interno no servidor ao analisar o conteúdo'}), 500


def classificar_e_responder(texto):
    prompt_para_ia = f"""
    Você é um assistente virtual eficiente, especialista em triagem de e-mails. Sua tarefa é analisar o e-mail fornecido e executar duas ações:
    1. Classificar o e-mail como "Produtivo" ou "Improdutivo".
    2. Sugerir um rascunho de resposta curta e profissional PARA SER ENVIADA AO REMETENTE do e-mail, que seja adequada à classificação.

    Aqui estão exemplos de como você deve se comportar:
    - Exemplo 1: Se o e-mail for um simples agradecimento (Improdutivo), uma resposta sugerida apropriada seria "Ficamos felizes em ajudar! Atenciosamente.".
    - Exemplo 2: Se o e-mail for uma solicitação de status de um projeto (Produtivo), uma resposta sugerida apropriada seria "Prezado(a), recebemos sua solicitação e já estamos verificando o status. Retornaremos o mais breve possível. Atenciosamente.".

    Analise o e-mail abaixo seguindo estritamente estas regras.

    Formate sua saída final EXATAMENTE como um objeto JSON com as chaves "classificacao" e "resposta_sugerida". Não adicione nenhum texto ou formatação fora do JSON.

    E-mail para analisar:
    ---
    {texto}
    ---
    """

    model = genai.GenerativeModel('gemini-2.0-flash') 
    response = model.generate_content(prompt_para_ia)
    resultado_json_texto = response.text.replace('```json', '').replace('```', '').strip()
    resultado_dict = json.loads(resultado_json_texto)
    classificacao = resultado_dict.get('classificacao', 'Erro ao classificar')
    resposta_sugerida = resultado_dict.get('resposta_sugerida', 'Não foi possível gerar uma resposta.')
    return classificacao, resposta_sugerida

if __name__ == '__main__':
    app.run(debug=True)