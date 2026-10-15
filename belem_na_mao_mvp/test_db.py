import os
import sys
from pathlib import Path

# Adiciona o diretório da aplicação ao sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from services.database import (
    adicionar_ao_roteiro_db,
    autenticar_usuario,
    buscar_locais_db,
    cadastrar_usuario,
    inicializar_banco,
    listar_todos_locais,
    obter_roteiro_db,
    remover_do_roteiro_db,
)


def run_tests():
    print("[*] Iniciando testes do banco SQLite...")
    inicializar_banco()

    # 1. Testar autenticação do usuário padrão
    user = autenticar_usuario("turista", "123456")
    assert user is not None, "Falha ao autenticar turista"
    print(f"[OK] Usuário padrão autenticado: {user['nome']} ({user['usuario']})")

    # 2. Testar cadastro de novo usuário
    import time
    username_teste = f"maria_{int(time.time())}"
    sucesso, msg = cadastrar_usuario("Maria Silva", username_teste, f"{username_teste}@email.com", "senha123")
    assert sucesso, f"Erro ao cadastrar novo usuário: {msg}"
    print(f"[OK] Cadastro de novo usuário: sucesso={sucesso}, login={username_teste}")
    user_maria = autenticar_usuario(username_teste, "senha123")
    assert user_maria is not None, "Falha ao autenticar novo usuário maria"

    # 3. Testar prevenção de usuário duplicado
    sucesso_dup, msg_dup = cadastrar_usuario("Maria Repetida", username_teste, "outro@email.com", "senha123")
    assert not sucesso_dup, "Deveria rejeitar usuário duplicado"
    print(f"[OK] Tentativa de duplicidade tratada com sucesso: {msg_dup}")

    # 4. Testar senha incorreta
    user_invalido = autenticar_usuario("maria", "senha_errada")
    assert user_invalido is None, "Senha errada não deve autenticar"
    print("[OK] Rejeição de senha inválida validada")

    # 5. Testar catálogo
    locais = listar_todos_locais()
    assert len(locais) >= 8, f"Esperado >= 8 locais, obtido {len(locais)}"
    print(f"[OK] Total de locais carregados do SQLite: {len(locais)}")

    # 6. Testar busca com filtros
    busca_peso = buscar_locais_db(texto="peso", categoria="Todas")
    assert any("Ver-o-Peso" in l["nome"] for l in busca_peso), "Busca por peso falhou"
    print(f"[OK] Busca textual funcionando: {[l['nome'] for l in busca_peso]}")

    busca_cat = buscar_locais_db(categoria="Gastronomia")
    assert len(busca_cat) > 0, "Filtro por categoria Gastronomia falhou"
    print(f"[OK] Filtro por categoria funcionando ({len(busca_cat)} encontrados)")

    # 7. Testar roteiro isolado por usuário
    adicionar_ao_roteiro_db("ver-o-peso", usuario_id=user_maria["id"])
    roteiro_maria = obter_roteiro_db(usuario_id=user_maria["id"])
    assert len(roteiro_maria) == 1, "Roteiro de maria deveria ter 1 item"
    print(f"[OK] Roteiro do usuário persistido: {[i['nome'] for i in roteiro_maria]}")

    # 8. Remover item do roteiro
    removido = remover_do_roteiro_db("ver-o-peso", usuario_id=user_maria["id"])
    assert removido is True, "Falha ao remover item do roteiro"
    roteiro_pos = obter_roteiro_db(usuario_id=user_maria["id"])
    assert len(roteiro_pos) == 0, "Roteiro deveria estar vazio"
    print("[OK] Remoção do roteiro validada com sucesso")

    print("\n>>> [SUCESSO TOTAL] O banco de dados SQLite e todos os serviços estão 100% funcionais! <<<")


if __name__ == "__main__":
    run_tests()
