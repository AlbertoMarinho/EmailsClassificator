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
    Você é um assistente virtual especializado em triagem de e-mails.
    Sua tarefa é analisar o e-mail fornecido e executar duas ações obrigatórias:

    Classificação → Determine se o e-mail é:
    "Produtivo" (quando exige ação, decisão, resposta ou envolve trabalho/negócio relevante).
    "Improdutivo" (quando é apenas agradecimento, confirmação simples, mensagem social ou sem necessidade de ação).

    Resposta sugerida → Redija um rascunho de resposta curto, direto e profissional, adequado à classificação:
    Para e-mails Produtivos: uma resposta que reconheça a solicitação e indique próximos passos.
    Para e-mails Improdutivos: uma resposta educada e breve de encerramento.

    Regras obrigatórias:
    A saída DEVE ser formatada exatamente como um objeto JSON com as chaves "classificacao" e "resposta_sugerida".
    Não adicione nenhum texto fora do JSON.
    A resposta sugerida sempre deve estar pronta para ser enviada ao remetente.
    Seja conciso (1 a 2 frases no máximo).

    Exemplos:
    E-mail: "Obrigado pela ajuda!"
    Saída:
    {"classificacao": "Improdutivo","resposta_sugerida": "Ficamos felizes em ajudar! Atenciosamente."}

    E-mail: "Qual o status do projeto X?"
    Saída:
    {"classificacao": "Produtivo","resposta_sugerida": "Prezado(a), recebemos sua solicitação e já estamos verificando o status. Retornaremos o mais breve possível. Atenciosamente."}

    ---

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