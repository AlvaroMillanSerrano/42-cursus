(Ctrl + Shift + V)

# 📘 Docstrings en Python
## 🧠 ¿Qué son?
Los **docstrings** son cadenas de documentación definidas entre triples comillas:

    """Docstring"""

Se utilizan para documentar módulos, funciones, clases y métodos.

👉 Se colocan justo después de la línea de definición.


## ⚠️ Nota importante

Si usas barras invertidas (\) dentro del docstring, utiliza:

    r"""raw triple double quotes"""


## 📦 Contenido de un docstring

Un buen docstring debe incluir:
	•	Una descripción concisa
	•	Los argumentos de entrada (parámetros)
	•	Los valores de retorno


## 📍 Dónde se colocan

Los docstrings se colocan al inicio de:
	•	Módulos
	•	Funciones
	•	Clases
	•	Métodos

Sirven para explicar:
	•	Propósito
	•	Parámetros
	•	Retorno
	•	Uso


## 🔍 Acceso en tiempo de ejecución

Los docstrings se almacenan en el atributo:

    __doc__

Y se pueden consultar de dos formas:

    1. Usando__doc__
        import math
        print(math.__doc__)

    1. Usando help()
        import math
        help(math)



## 🛠️ Generar documentación automáticamente

### 📄 pydoc

Genera documentación en texto:

    python -m pydoc nombre_archivo

Para generar HTML:

    python -m pydoc -w nombre_archivo


### 🌐 Sphinx

Genera documentación profesional en:
	•	HTML
	•	PDF


## 🆚 Diferencia entre comentarios y docstrings

#### 💬 Comentarios (#)
	•	Explican lógica del código o desactivan código
	•	No son accesibles en tiempo de ejecución
	•	Pueden aparecer en cualquier parte del código
	•	Se escriben con #

#### 📘 Docstrings (""" """)
	•	Documentan módulos, clases y funciones
	•	Son accesibles en tiempo de ejecución (help(), __doc__)
	•	Van justo después de la definición
	•	Se escriben con triples comillas

⸻

🧩 Resumen rápido
	•	# → para explicar cómo funciona el código
	•	""" """ → para explicar qué hace y cómo se usa



definidos entre triples comillas (""")
Use r"""raw triple double quotes""" if you use any backslashes in your docstrings.

Contenido: Deben incluir una descripción concisa, los argumentos de entrada (parámetros), y los valores de retorno.

Se colocan al inicio de módulos, funciones, clases o métodos en Python para explicar su propósito, parámetros, retorno y uso. 
Se almacenan en el atributo __doc__ y son accesibles mediante funciones como help()

Python provides two built-in ways to access docstrings: the .__doc__ attribute and the help() function.
>>> import math
>>> print(math.__doc__)

>>> import math
>>> help(math)

Generate Documentation from Python Docstrings
pydoc: Generates text-based documentation. python -m pydoc (add -w to view in html) file_name_without.py. 
Sphinx: Generates professional-looking documentation in HTML or PDF format.

Comments (#):
Explain code logic or disable code.
Not accessible at runtime.
Can appear anywhere in the code.
Use the # symbol before the text.
Docstrings (""" """):
Document modules, classes, and functions.
Are accessible at runtime through help().
Go right after the definition line of a function, class, or module.
Use triple quotes to enclose the text.

para alberto: https://realpython.com/how-to-write-docstrings-in-python/ (Ways to Access Docstrings in Python)