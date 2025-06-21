#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[94m=== Instalador de RedTool para Termux ===\033[0m"

# 1. Clonar repositorio
echo "📥 Clonando repositorio desde GitHub..."
git clone https://github.com/Tachito1987/redtool.git $HOME/.redtool || {
    echo "❌ Error al clonar el repositorio."
    exit 1
}

# 2. Copiar script al home
cp $HOME/.redtool/suite_red_termux.py $HOME/

# 3. Crear comando redtool
cat > $PREFIX/bin/redtool <<EOF
#!/data/data/com.termux/files/usr/bin/bash
python \$HOME/suite_red_termux.py
EOF

chmod +x $PREFIX/bin/redtool

# 4. Instalar dependencias de Python
echo "📦 Instalando dependencias..."
pip install --upgrade pip > /dev/null
pip install ipwhois python-whois requests > /dev/null

echo -e "\n✅ Instalación completada."
echo -e "Ejecuta tu herramienta con: \033[92mredtool\033[0m"
