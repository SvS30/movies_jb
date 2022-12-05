# Movies JB
API-Rest de peliculas con **Django**, **Django Rest Framework**, **OAuth2**.

### ✔ Checklist of features
- [X] Admin dashboard.
- [X] Listado de peliculas por genero.
- [X] Los usuarios pueden asignar un rating personal a las peliculas.
- [X] Los usuarios pueden marcar películas como favoritas.
- [X] Los usuarios pueden agregar reviews.
- [X] Inicio de sesión con Discord.
- [X] Inicio de sesión tradicional (correo y contraseña).

### 🚧 Configuración
Luego de clonar el proyecto, necesitara:
- Modificar variables de entorno
    - Duplicar `.env.example` y renombrar copia a `.env`.
    - Establecer variables en `.env`.
      - Puedes generar una nueva **SECRET_KEY**, [aquí](https://djecrety.ir/).
      - Asigna **True** or **False** dependiendo del **stage** en el que te encuentres.
      - Puedes generar tus datos de **Discord** para **OAuth2**, [aquí](https://discord.com/developers/applications/)

    <details>
    <summary>Sin Docker</summary>

    - Instalar las dependencias del proyecto
        ```bash
        pip install -r requirements.txt
        ```

    - Crear migraciones de modelos

        ```bash
        python manage.py makemigrations Movie Genre Auth UserActions
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

### 📖 Docs
- [Rest API](https://github.com/SvS30/movies_jb/wiki/Home-REST-API-Docs)
