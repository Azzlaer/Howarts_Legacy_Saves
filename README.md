# 🧙‍♂️ Hogwarts Legacy – Epic ⇄ Steam Save Manager

✨ **Sistema avanzado con GUI en Python para convertir partidas guardadas entre Epic Games y Steam, con copias de seguridad automáticas** ✨

---

## 📌 ¿Qué es este proyecto?

![Descripci?n de la imagen](https://github.com/Azzlaer/Howarts_Legacy_Saves/blob/main/pantalla.jpeg?raw=true)

Este programa te permite gestionar de forma **segura y visual** las partidas guardadas de **Hogwarts Legacy**, permitiéndote:

- ✅ Convertir partidas de **Epic Games → Steam**
- ✅ Convertir partidas de **Steam → Epic Games**
- 💾 Crear **copias de seguridad automáticas** antes de cada conversión
- 💾 Crear **backups manuales**
- ♻️ Restaurar backups fácilmente
- 📦 Exportar backups en **ZIP**
- 🎮 Visualizar cantidad de slots (`HL-00`, `HL-01`, etc.)
- ⚠️ Evitar sobrescrituras por **Steam Cloud**
- 🌙 Modo oscuro integrado
- 🖥️ Interfaz gráfica (GUI), sin comandos complicados

Todo funciona **100% local**, sin modificar archivos del juego ni usar internet.

---

## 📂 Ubicación de los guardados

El sistema trabaja directamente con la carpeta oficial de Windows:

```txt
C:\Users\TU_USUARIO\AppData\Local\HogwartsLegacy\Saved\SaveGames
```

Dentro encontrarás carpetas distintas para Epic y Steam.

---

## 🖥️ Requisitos

- Windows 10 / 11  
- Python **3.9 o superior**
- Hogwarts Legacy instalado (Epic Games o Steam)

📌 **No requiere librerías externas** (Tkinter viene incluido en Python).

---

## ▶️ Ejecución

1. Descarga o clona este repositorio
2. Ejecuta el archivo:

```bash
py hogwarts_save_converter.py
```

O simplemente doble clic si Python está asociado correctamente.

---

## 🧭 Interfaz – ¿Qué hace cada sección?

### 🗂️ Carpetas detectadas
- Detecta automáticamente las carpetas de guardado
- Muestra:
  - Plataforma estimada (Epic / Steam)
  - Cantidad de slots disponibles

### 🔁 Conversión
- **Origen** → Carpeta que contiene tu partida actual
- **Destino** → Carpeta donde se copiará la partida

Al convertir:
- ✔ Se crea un **backup obligatorio**
- ✔ Se copian todos los archivos `.sav`

### 💾 Copias de Seguridad
- Backups automáticos antes de convertir
- Backups manuales a demanda
- Restauración de backups
- Exportación a ZIP

### 🧾 Registro (Log)
- Muestra en tiempo real todas las acciones realizadas

---

## 🧪 Tutorial – Epic Games → Steam

1. Abre el programa
2. Selecciona la carpeta de Epic
3. Pulsa **“Usar como Origen”**
4. Selecciona la carpeta de Steam
5. Pulsa **“Usar como Destino”**
6. Haz clic en:

```txt
Convertir Epic ⇄ Steam
```

🎉 Listo. Tu partida aparecerá en Steam.

---

## ⚠️ IMPORTANTE – Steam Cloud

Antes de abrir el juego en Steam:

1. Steam → Biblioteca
2. Hogwarts Legacy → Propiedades
3. Steam Cloud → **DESACTIVAR**

Esto evita que Steam sobrescriba tu partida convertida.

---

## 💾 Backups – Información técnica

Los backups se guardan automáticamente en:

```txt
SaveGames/_Backups/
```

Cada backup contiene:
- Fecha y hora
- Tipo (`AUTO`, `MANUAL`, `PRE_CONVERT`)
- Todos los archivos `.sav`

### Acciones disponibles
- Crear backup manual
- Restaurar backup
- Exportar backup en ZIP
- Volver atrás si algo falla

---

## ♻️ Restaurar una partida

1. Selecciona un backup en la lista
2. Selecciona una carpeta destino
3. Pulsa **“Restaurar → Destino”**

Tu progreso se restaurará exactamente a ese punto.

---

## 🌙 Modo Oscuro

Incluye **modo oscuro** para uso nocturno 🌑  
Se puede activar directamente desde la interfaz.

---

## 🔐 Seguridad

- ❌ No modifica archivos del juego
- ❌ No altera cuentas Epic ni Steam
- ❌ No requiere conexión a internet
- ✅ Todo es reversible gracias a los backups

---

## 🎯 Conclusión

Si quieres cambiar de Epic a Steam (o viceversa) sin perder tu progreso:

👉 **Este sistema es seguro, rápido y pensado para jugadores.**

🧙‍♀️ ¡Disfruta Hogwarts Legacy sin perder tu magia! ✨

---

## 📜 Licencia

Proyecto creado con fines educativos y comunitarios.  
No afiliado a Warner Bros, Portkey Games, Epic Games ni Valve.

---

## ❤️ Créditos

Desarrollado por la comunidad, con ayuda de **ChatGPT (OpenAI)**  
Inspirado en la necesidad real de jugadores que migran entre plataformas.
