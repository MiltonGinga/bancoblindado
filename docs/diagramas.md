# Diagramas do Banco Blindado (Evolução 3NF)

## 1. Modelo Entidade-Relacionamento (ER)

O diagrama abaixo representa a estrutura profissional de e-commerce implementada em 3NF.

```mermaid
erDiagram
    CLIENTES ||--o{ ENDERECOS : "possui"
    CLIENTES ||--o{ PEDIDOS : "realiza"
    CATEGORIAS ||--o{ PRODUTOS : "contem"
    PEDIDOS ||--o{ PEDIDO_ITENS : "inclui"
    PRODUTOS ||--o{ PEDIDO_ITENS : "vendido_em"
    ENDERECOS ||--o{ PEDIDOS : "entrega_em"

    CLIENTES {
        int id PK
        string nome
        string email UK
        string senha_hash
        string telefone
        timestamp data_cadastro
    }

    ENDERECOS {
        int id PK
        int cliente_id FK
        string rua
        string bairro
        string cidade
        string provincia
        string tipo
    }

    CATEGORIAS {
        int id PK
        string nome
        string descricao
    }

    PRODUTOS {
        int id PK
        int categoria_id FK
        string nome
        decimal preco_base
        int estoque
    }

    PEDIDOS {
        int id PK
        int cliente_id FK
        int endereco_id FK
        timestamp data_pedido
        string status
        decimal total_pedido
    }

    PEDIDO_ITENS {
        int id PK
        int pedido_id FK
        int produto_id FK
        int quantidade
        decimal preco_unitario
    }
```

## 2. Justificativa da Normalização

- **1ª Forma Normal (1FN):** Atributos compostos como "Endereço" foram decompostos em campos atômicos (Rua, Cidade, Província).
- **2ª Forma Normal (2FN):** Todos os campos não-chave dependem totalmente da Chave Primária (ex: dados do produto não estão na tabela de itens, apenas o FK).
- **3ª Forma Normal (3NF):** Eliminamos dependências transitivas. O endereço de entrega é uma referência (FK), evitando repetir dados geográficos em cada pedido.
