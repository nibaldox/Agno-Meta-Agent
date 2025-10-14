"""
Script de verificación del proyecto Meta-Agente.

Verifica que todos los archivos necesarios existen y tienen la estructura correcta.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> bool:
    """Verifica que un archivo existe."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} faltante: {filepath}")
        return False

def check_python_syntax(filepath: str) -> bool:
    """Verifica la sintaxis de un archivo Python."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        return True
    except SyntaxError as e:
        print(f"  ⚠ Error de sintaxis en {filepath}: {e}")
        return False

def main():
    """Ejecuta todas las verificaciones."""
    print("🔍 Verificando estructura del proyecto Meta-Agente\n")

    all_ok = True

    # Verificar archivos principales
    print("📄 Archivos principales:")
    files = [
        ("src/application/services/meta_agent.py", "Lógica principal del meta-agente"),
        ("src/infrastructure/templates/agent_templates.py", "Sistema de plantillas"),
        ("src/presentation/cli/main.py", "Punto de entrada CLI"),
        ("requirements.txt", "Dependencias del proyecto"),
        (".env.example", "Ejemplo de configuración"),
        ("README.md", "Documentación principal"),
        (".gitignore", "Configuración de Git"),
    ]

    for filepath, description in files:
        if not check_file_exists(filepath, description):
            all_ok = False

    print("\n📝 Archivos de documentación:")
    doc_files = [
        ("proyect_context.md", "Contexto del proyecto"),
        ("cursor_prompts.md", "Biblioteca de prompts"),
        ("readme_cursor.md", "Guía de Cursor"),
        (".cursorrules", "Reglas de Cursor"),
    ]

    for filepath, description in doc_files:
        check_file_exists(filepath, description)

    # Verificar sintaxis de archivos Python
    print("\n🐍 Verificando sintaxis Python:")
    python_files = [
        "src/application/services/meta_agent.py",
        "src/infrastructure/templates/agent_templates.py",
        "src/presentation/cli/main.py",
    ]

    for filepath in python_files:
        if os.path.exists(filepath):
            if check_python_syntax(filepath):
                print(f"  ✓ {filepath}: sintaxis correcta")
            else:
                all_ok = False

    # Verificar contenido de archivos clave
    print("\n📦 Verificando contenido:")

    # Verificar imports en meta_agent.py
    with open("src/application/services/meta_agent.py", 'r', encoding='utf-8') as f:
        content = f.read()
        if "class AgentPlan" in content and "class MetaAgent" in content:
            print("  ✓ meta_agent.py: clases principales presentes")
        else:
            print("  ✗ meta_agent.py: faltan clases principales")
            all_ok = False

    # Verificar templates en agent_templates.py
    with open("src/infrastructure/templates/agent_templates.py", 'r', encoding='utf-8') as f:
        content = f.read()
        if "generate_basic_agent" in content and "generate_agent_with_memory" in content:
            print("  ✓ agent_templates.py: templates principales presentes")
        else:
            print("  ✗ agent_templates.py: faltan templates")
            all_ok = False

    # Verificar requirements.txt
    with open("requirements.txt", 'r', encoding='utf-8') as f:
        content = f.read()
        required_packages = ["agno", "anthropic", "pydantic", "rich", "python-dotenv"]
        missing = [pkg for pkg in required_packages if pkg not in content]
        if not missing:
            print("  ✓ requirements.txt: todas las dependencias presentes")
        else:
            print(f"  ⚠ requirements.txt: faltan dependencias: {', '.join(missing)}")

    # Resumen final
    print("\n" + "="*60)
    if all_ok:
        print("✅ Proyecto verificado exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Instalar dependencias: pip install -r requirements.txt")
        print("2. Configurar .env con tu DEEPSEEK_API_KEY")
        print("3. Ejecutar: python -m src.presentation.cli.main")
    else:
        print("⚠️  Se encontraron algunos problemas. Revisa los mensajes arriba.")
        sys.exit(1)
    print("="*60)

if __name__ == "__main__":
    main()
