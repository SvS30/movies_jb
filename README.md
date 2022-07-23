# Movies JB
API-Rest de peliculas con **Django** y **Django Rest Framework**.

Docs:
- [Rest API](https://github.com/SvS30/movies_jb/wiki/Home-REST-API-Docs)

### ✔ Checklist of features
- [X] Listado de peliculas por genero.
- [X] Los usuarios pueden asignar un rating personal a las peliculas.
- [X] Los usuarios pueden marcar películas como favoritas.
- [X] Los usuarios pueden agregar reviews.

### 🚧 Configuración
Luego de clonar el proyecto, necesitara:
- Modificar variables de entorno
    - Duplicar `.env.example` y renombrar copia a `.env`.
    - Establecer variables en `.env`.
      - Puedes generar una nueva key, [aquí](https://djecrety.ir/).

<details>
<summary>Sin Docker</summary>

- Instalar las dependencias del proyecto
    ```bash
    pip install -r requirements.txt
    ```

- Crear migraciones de modelos

    ```bash
    python manage.py makemigrations
    ```

- Migrar modelos
    ```bash
    python manage.py migrate
    ```

- Crear `superuser`
    ```bash
    python manage.py createsuperuser
    ```

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
</details>

<details>
<summary>Con Docker</summary>

- Crear imagen
    ```bash
    docker build . -t $image_name:$image_port
    ```

- Crear contenedor y opciones de desarrollo
    ```bash
    docker run --name movies_container -d -p $desktop_port:80 $image_name:$image_port
    ```
</details>

### 🧰 Dependencias || plugins
| Name | Version |
| ---- | ---- |
| asgiref | 3.4.1 |
| Django | 3.2.13 |
| [django-cors-headers](https://pypi.org/project/django-cors-headers/) | 3.10.1 |
| [djangorestframework](https://www.django-rest-framework.org/) | 3.13.1 |
| [python-decouple](https://pypi.org/project/python-decouple/) | 3.6 |
| pytz | 2022.1 |
| sqlparse | 0.4.2 |
| typing_extensions | 4.1.1 |