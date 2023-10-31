### Autor: Pablo Valverde Soriano

### Instrucciones de uso

1- Clonar el repositorio

2- Instalar el repositorio con ```pip install .```

3- Instalar las dependencias con ```pip install -r requirements.txt```

4- Crear una base de datos sqlite3

4- Ejecutar el servidor con ```blob_server <url_servicio_autenticación> --db <ruta_base_datos>```

Para descargar el cliente CLI vaya a este [repositorio](https://github.com/pavalso/APDI-cli)

### Documentación de la API REST

#### Autenticación
- **Header:**
  ```AuthToken: <user_token>```

#### `GET /api/v1/status/`
- **Necesita autenticación:** No.
- **Descripción:** Obtiene el estado de la API.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "message": "API <nombre_de_la_app> <version_de_la_app> up and running"
  }
  ```

#### `GET /api/v1/blobs/`
- **Necesita autenticación:** Si.
- **Descripción:** Obtiene la lista de blobs del usuario actual.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "blobs": [
      {
        "blobId": "<id_del_blob>",
        "URL": "/api/v1/blobs/<id_del_blob>"
      },
      ...
    ]
  }
  ```

#### `POST /api/v1/blobs/`
- **Necesita autenticación:** Si.
- **Descripción:** Crea un nuevo blob para el usuario actual.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "visibility": "PUBLIC" | "PRIVATE"
  }
  ```
- **Respuesta Exitosa (201 Created):**
  ```json
  {
    "blobId": "<id_del_blob>",
    "URL": "/api/v1/blobs/<id_del_blob>"
  }
  ```

#### `GET /api/v1/blobs/<id_del_blob>`
- **Necesita autenticación:** No para blobs públicos.
- **Descripción:** Obtiene un blob específico.
- **Respuesta Exitosa (200 OK):** Devuelve el blob como un archivo binario.

#### `PUT /api/v1/blobs/<id_del_blob>`
- **Necesita autenticación:** Si.
- **Descripción:** Actualiza un blob existente.
- **Cuerpo de la Solicitud:** Datos binarios del blob.
- **Respuesta Exitosa (204 No Content):** Sin contenido.

#### `DELETE /api/v1/blobs/<id_del_blob>`
- **Necesita autenticación:** Si.
- **Descripción:** Elimina un blob existente.
- **Respuesta Exitosa (204 No Content):** Sin contenido.

#### `GET /api/v1/blobs/<id_del_blob>/hash?type=<tipo_de_hash>`
- **Necesita autenticación:** No para blobs públicos.
- **Descripción:** Obtiene el hash de un blob en el formato especificado.
- **Parámetros de Consulta:**
  - `type` (opcional): Tipo de hash (por defecto: "md5").
- **Respuesta Exitosa (200 OK):** Devuelve el hash del blob.
  ```json
  {
    "md5": "<hash_md5>",
    "sha256": "<hash_sha256>",
    ...
  }
  ```

#### `GET /api/v1/blobs/<id_del_blob>/acl`
- **Necesita autenticación:** Si.
- **Descripción:** Obtiene la lista de usuarios con permisos de lectura para un blob específico.
- **Respuesta Exitosa (200 OK) si el blob es privado:**
  ```json
  {
    "allowed_users": ["usuario1", "usuario2", ...]
  }
  ```
- **Respuesta Exitosa (204 No Content) si el blob es público:** Sin contenido.

#### `PUT /api/v1/blobs/<id_del_blob>/acl`
- **Necesita autenticación:** Si.
- **Descripción:** Establece los permisos de lectura para un blob específico.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "acl": ["usuario1", "usuario2", ...]
  }
  ```
- **Respuesta Exitosa (204 No Content):** Sin contenido.

#### `PATCH /api/v1/blobs/<id_del_blob>/acl`
- **Necesita autenticación:** Si.
- **Descripción:** Actualiza los permisos de lectura para un blob específico.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "acl": ["usuario1", "usuario2", ...]
  }
  ```
- **Respuesta Exitosa (204 No Content):** Sin contenido.

#### `DELETE /api/v1/blobs/<id_del_blob>/acl/<nombre_del_usuario>`
- **Necesita autenticación:** Si.
- **Descripción:** Elimina los permisos de lectura de un usuario específico para un blob específico.
- **Respuesta Exitosa (204 No Content):** Sin contenido.

#### `PUT /api/v1/blobs/<id_del_blob>/visibility`
- **Necesita autenticación:** Si.
- **Descripción:** Actualiza la visibilidad de un blob específico.
- **Cuerpo de la Solicitud:**
  ```json
  {
    "visibility": "public" | "private"
  }
  ```
- **Respuesta Exitosa (204 No Content):** Sin contenido.

#### `GET /api/v1/blobs/<id_del_blob>/visibility`
- **Necesita autenticación:** Si.
- **Descripción:** Obtiene la visibilidad de un blob específico.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "visibility": "public" | "private"
  }
  ```

#### Errores
- **Error 401 (Unauthorized):** Se devuelve cuando el usuario no está autorizado para realizar la acción.
  ```json
  {
    "error": "Usuario no autorizado"
  }
  ```
- **Error 404 (Not Found):** Se devuelve cuando el recurso solicitado no se encuentra.
  ```json
  {
    "error": "Recurso no encontrado"
  }
  ```
