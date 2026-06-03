import pandas as pd
import bcrypt
import sys
import random

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode('utf-8')

def migrate():
    try:
        print("Iniciando Migração Massiva (Padrão E-commerce 3NF)...")
        
        # 1. Carregar Clientes Brutos
        csv_path = 'data/clientes_bruto.csv'
        df_bruto = pd.read_csv(csv_path)
        
        # 2. Tabela: Clientes
        print("Migrando Tabela: clientes...")
        df_clientes = df_bruto[['id', 'nome', 'email', 'telefone']].copy()
        df_clientes['senha_hash'] = df_bruto['senha'].apply(hash_password)
        df_clientes['data_cadastro'] = df_bruto['data_cadastro']
        
        # 3. Tabela: Endereços (Parsing do campo único para múltiplas colunas)
        print("Migrando Tabela: enderecos (Normalizando strings)...")
        enderecos_data = []
        for index, row in df_bruto.iterrows():
            # Exemplo de parsing simples: "Rua A Luanda" -> ["Rua A", "Luanda"]
            partes = str(row['endereco']).split(' ')
            cidade = partes[-1] if len(partes) > 1 else "Luanda"
            rua = ' '.join(partes[:-1]) if len(partes) > 1 else partes[0]
            
            enderecos_data.append({
                'id': index + 1,
                'cliente_id': row['id'],
                'rua': rua,
                'cidade': cidade,
                'provincia': cidade, # Simplificação para o exemplo
                'tipo': 'Entrega'
            })
        df_enderecos = pd.DataFrame(enderecos_data)

        # 4. Tabela: Categorias (Sintético)
        print("Gerando Tabela: categorias...")
        categorias = ['Eletrônicos', 'Moda', 'Casa', 'Livros']
        df_categorias = pd.DataFrame([{'id': i+1, 'nome': c, 'descricao': f'Produtos de {c}'} for i, c in enumerate(categorias)])

        # 5. Tabela: Produtos (Sintético)
        print("Gerando Tabela: produtos...")
        produtos_sinteticos = [
            {'id': 1, 'categoria_id': 1, 'nome': 'Smartphone X', 'preco_base': 2500.00, 'estoque': 50},
            {'id': 2, 'categoria_id': 1, 'nome': 'Laptop Pro', 'preco_base': 7500.00, 'estoque': 20},
            {'id': 3, 'categoria_id': 2, 'nome': 'Camiseta Algodão', 'preco_base': 80.00, 'estoque': 200},
            {'id': 4, 'categoria_id': 3, 'nome': 'Cafeteira Express', 'preco_base': 450.00, 'estoque': 15},
        ]
        df_produtos = pd.DataFrame(produtos_sinteticos)

        # 6. Tabela: Pedidos e Itens (Sintético baseado no histórico do CSV)
        print("Gerando Tabelas: pedidos e pedido_itens...")
        pedidos_data = []
        itens_data = []
        
        for index, row in df_bruto.iterrows():
            if row['valor_ultima_compra'] > 0:
                pedido_id = index + 1
                pedidos_data.append({
                    'id': pedido_id,
                    'cliente_id': row['id'],
                    'endereco_id': index + 1, # Vinculado ao endereço criado acima
                    'total_pedido': row['valor_ultima_compra'],
                    'status': 'Entregue'
                })
                # Criar um item de pedido aleatório para justificar o valor
                itens_data.append({
                    'id': index + 1,
                    'pedido_id': pedido_id,
                    'produto_id': random.choice([1, 2, 3, 4]),
                    'quantidade': 1,
                    'preco_unitario': row['valor_ultima_compra']
                })
        
        df_pedidos = pd.DataFrame(pedidos_data)
        df_itens = pd.DataFrame(itens_data)

        # Salvar todos os arquivos normalizados
        print("Salvando arquivos CSV normalizados...")
        df_clientes.to_csv('data/normalizado_clientes.csv', index=False)
        df_enderecos.to_csv('data/normalizado_enderecos.csv', index=False)
        df_categorias.to_csv('data/normalizado_categorias.csv', index=False)
        df_produtos.to_csv('data/normalizado_produtos.csv', index=False)
        df_pedidos.to_csv('data/normalizado_pedidos.csv', index=False)
        df_itens.to_csv('data/normalizado_pedido_itens.csv', index=False)
        
        print("Migração concluída com sucesso! 6 tabelas geradas em data/normalizado_*.csv")

    except Exception as e:
        print(f"Erro fatal na migração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
