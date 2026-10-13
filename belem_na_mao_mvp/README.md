# BelémNaMão — MVP desktop

Protótipo funcional em Python + CustomTkinter para demonstração em computador.

## O que já funciona
- Tela inicial com categorias.
- Catálogo local de pontos turísticos e experiências.
- Busca por nome/descrição e filtros por categoria e faixa de preço.
- Janela de detalhes de cada local.
- Adicionar/remover locais do roteiro.
- Persistência do roteiro em `data/roteiro.json`.
- Interface desktop com menu lateral.

## O que é simulado ou ficou para depois
- O botão de entrada não autentica usuários.
- Recomendações usam filtros simples, não IA.
- Os dados de exemplo são demonstrativos: confirme endereços, preços, horários e informações antes de uma apresentação pública.
- Não há mapas integrados, avaliações reais, contas, Premium ou sincronização online.

## Requisitos
- Python 3.10+
- Windows, macOS ou Linux com ambiente gráfico.

## Instalação (Windows)
Abra o terminal na pasta do projeto e execute:

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Se `py` não funcionar, tente `python` no lugar.

## Estrutura
```text
belem_na_mao_mvp/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── locais.json
│   └── roteiro.json  # criado automaticamente quando salvar
├── services/
│   ├── catalogo.py
│   └── roteiro.py
├── views/
│   └── main_window.py
└── assets/
    └── README.txt
```

## Próximos passos sugeridos
1. Substituir os dados de exemplo por informações verificadas.
2. Adicionar fotos licenciadas em `assets/` e ligar cada imagem ao cadastro do local.
3. Ajustar cores, tipografia e identidade visual.
4. Só depois avaliar SQLite, autenticação e publicação mobile/web.
