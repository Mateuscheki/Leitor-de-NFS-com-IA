import json
from openai import OpenAI
from app.core.settings import settings
from app.db.schemas import NotaFiscalIAExtract

# Inicializa o cliente OpenAI
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_json_prompt(texto_bruto: str) -> str:
    """
    Monta o prompt estruturado para forçar uma resposta JSON da IA.
    """
    # Escapa quebras de linha e aspas no texto bruto para não quebrar o JSON/prompt
    texto_bruto_escapado = texto_bruto.replace('"', '\\"').replace('\n', '\\n')

    prompt = f"""
    Você é um assistente especialista em contabilidade e extração de dados de Notas Fiscais de Serviço brasileiras (NFS-e).
    Analise o texto extraído de uma NFS-e abaixo e retorne APENAS um objeto JSON válido com a seguinte estrutura.
    Se uma informação não for encontrada, retorne null para o campo. 
    Para 'tem_retencao_impostos', retorne true se houver menção clara a ISS retido, IRRF, PIS, COFINS, CSLL na fonte; caso contrário, false.

    Estrutura JSON esperada:
    {{
      "nome_prestador": "Nome da Empresa Prestadora",
      "cnpj_prestador": "00.000.000/0001-00",
      "valor_total": 1500.50,
      "codigo_servico": "14.01",
      "cnae": "6201-5/01",
      "tem_retencao_impostos": true,
      "detalhes_retencao": "Retenção de IRRF (1.5%) e PIS/COFINS/CSLL (4.65%)",
      "data_emissao": "YYYY-MM-DDTHH:MM:SS"
    }}

    Texto da Nota Fiscal:
    "{texto_bruto_escapado}"
    """
    return prompt


async def analisar_texto_nf(texto_bruto: str) -> NotaFiscalIAExtract:
    """
    Envia o texto bruto para a OpenAI e parseia a resposta JSON.
    """
    if not texto_bruto or texto_bruto.strip() == "":
        raise ValueError("Texto bruto está vazio. Impossível analisar.")

    prompt = get_json_prompt(texto_bruto)

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # Ou "gpt-3.5-turbo-1106" que é bom com JSON
            messages=[
                {"role": "system", "content": "Você é um extrator de dados que SÓ responde em JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}  # Força o modo JSON (modelos recentes)
        )

        response_content = completion.choices[0].message.content

        # Ocasionalmente, o modelo pode incluir ```json ... ```. Vamos limpar.
        if response_content.startswith("```json"):
            response_content = response_content.strip("```json\n").strip("```")

        # Parseia o JSON recebido
        dados_json = json.loads(response_content)

        # Valida com o Pydantic
        dados_validados = NotaFiscalIAExtract(**dados_json)
        return dados_validados

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON da IA: {e}")
        print(f"Resposta recebida: {response_content}")
        raise ValueError("A IA não retornou um JSON válido.")
    except Exception as e:
        print(f"Erro na chamada da API OpenAI: {e}")
        raise