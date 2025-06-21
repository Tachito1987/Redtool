#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[94m=== Instalador de RedTool para Termux ===\033[0m"

# 1. Clonar repositorio desde GitHub
echo "📥 Clonando repositorio desde GitHub..."
git clone https://github.com/Tachito1987/redtool.git $HOME/.redtool || {
    echo "❌ Error al clonar el repositorio."
    exit 1
}

# 2. Copiar el script principal al HOME
cp $HOME/.redtool/suite_red_termux.py $HOME/

# 3. Crear el comando redtool
echo "⚙️ Creando comando redtool..."
cat > $PREFIX/bin/redtool <<EOF
#!/data/data/com.termux/files/usr/bin/bash
python \$HOME/suite_red_termux.py
EOF

chmod +x $PREFIX/bin/redtool

# 4. Instalar dependencias sin romper pip
echo "📦 Instalando dependencias..."
pip install --no-cache-dir ipwhois python-whois requests

echo -e "\n✅ Instalación completada."
echo -e "Ejecuta tu herramienta con: \033[92mredtool\033[0m"
