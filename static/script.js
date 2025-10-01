document.addEventListener('DOMContentLoaded', () => {

    const analisadorForm = document.getElementById('analisador-form');
    const emailInput = document.getElementById('email-input');
    const fileInput = document.getElementById('file-input');
    const resultadoSection = document.getElementById('resultado');
    const classificacaoOutput = document.getElementById('classificacao-output');
    const respostaOutput = document.getElementById('resposta-output');
    const loader = document.getElementById('loader');

    analisadorForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        loader.classList.remove('hidden');
        resultadoSection.classList.add('hidden');

        let bodyContent;
        let headers = {};

        const file = fileInput.files[0];

        if (file) {
            bodyContent = new FormData();
            bodyContent.append('file', file);
        } else {
            const textoEmail = emailInput.value;
            if (textoEmail.trim() === "") {
                alert("Por favor, insira o texto do e-mail ou selecione um arquivo.");
                loader.classList.add('hidden');
                return;
            }
            headers['Content-Type'] = 'application/json';
            bodyContent = JSON.stringify({ email_texto: textoEmail });
        }

        try {
            const response = await fetch('/analisar', {
                method: 'POST',
                headers: headers,
                body: bodyContent
            });

            const data = await response.json();

            if (data.erro) {
                throw new Error(data.erro);
            }

            classificacaoOutput.textContent = data.classificacao;
            respostaOutput.textContent = data.resposta_sugerida;
            
            resultadoSection.classList.remove('hidden');

        } catch (error) {
            console.error('Erro ao analisar:', error);
            alert(`Ocorreu um erro: ${error.message}`);
        } finally {
            loader.classList.add('hidden');
        }
    });
});