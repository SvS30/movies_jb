# Movies JB
Web de peliculas con **Django** y **Django Rest Framework**.

### ✔ Checklist of features
- [X] Listado de peliculas por genero.
- [X] Los usuarios pueden asignar un rating personal a las peliculas.
- [X] Los usuarios pueden marcar películas como favoritas.
- [X] Los usuarios pueden agregar reviews.

### 🚧 Configuración
Luego de clonar el proyecto, necesitara:
1. Instalar las dependencias del proyecto
    ```bash
    pip install -r requirements.txt
    ```

2. Modificar variables de entorno
    - Duplicar `.env.example` y renombrar copia a `.env`.
    - Establecer variables en `.env`.
      - Puedes generar una nueva key, [aquí](https://djecrety.ir/).

3. Migrar modelos
    ```bash
    python manage.py migrate
    ```

4. Crear `superuser`
    ```bash
    python manage.py createsuperuser
    ```

### Comandos disponibles
- Levantar el servidor
    ```bash
    python manage.py runserver
    ```
    - Opcional: puerto o ip:port
        ```bash
        python manage.py runserver 80
        ```
- Ejecutar pruebas
    ```bash
    python manage.py test --debug-mode --timing --traceback
    ```

### 🧰 Dependencias || plugins
| Name | Version |
| ---- | ---- |
| asgiref | 3.5.2 |
| backports.zoneinfo | 0.2.1 |
| Django | 4.0.4 |
| [python-decouple](https://pypi.org/project/python-decouple/) | 3.6 |
| sqlparse | 0.4.2 |
| tzdata | 2022.1 |
| [django-cors-headers](https://pypi.org/project/django-cors-headers/) | 3.12.0 |
| [djangorestframework](https://www.django-rest-framework.org/) | 3.13.1 |