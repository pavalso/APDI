### Documentación

#### Autenticación
Para acceder a las siguientes operaciones, debes incluir un token de usuario en la cabecera de la solicitud:

- **Cabecera de Autenticación:** 
  - `Authorization: Bearer <user-token>`

#### Obtener un Blob por UUID
Obtiene el contenido de un blob específico por su UUID.

- **Ruta:** `/blobs/<blob>` (GET)
- **Descripción:** Obtiene el contenido de un blob específico por su UUID.
- **Parámetros de solicitud:**
  - `blob (URL Parameter):` El UUID del blob que se desea obtener.
- **Respuestas:**
  - **Código 200 (Éxito):** Se obtuvo el blob con éxito, y se devuelve el contenido binario.
  - **Código 404 (No encontrado):** El blob con el UUID especificado no se encontró o no tienes permiso para acceder a él.
    - Ejemplo de respuesta (éxito):
    ```json
    {
        "raw": "blob-binary-data"
    }
    ```

#### Obtener todos los Blobs del usuario
Obtiene el UUID de todos los blobs del usuario.

- **Ruta:** `/blobs/` (GET)
- **Descripción:** Obtiene el UUID de todos los blobs del usuario.
- **Respuestas:**
  - **Código 200 (Éxito):** El usuario está autenticado y se han podido obtener sus blobs.
  - **Código 404 (No encontrado):** El usuario no está autenticado
    - Ejemplo de respuesta (éxito):
    ```json
    {
        "blobs": [
          "UUID1",
          "UUID2"
        ]
    }
    ```

#### Subir un Blob
Crea un blob en el servidor y le asigna un UUID único.

- **Ruta:** `/blobs` (POST)
- **Descripción:** Crea un blob en el servidor y le asigna un UUID único.
- **Parámetros de solicitud:**
  ```json
  {
      "visibility": "Visibilidad del blob"
  }
  ```
- **Respuestas:**
  - **Código 201 (Creado):** El blob se subió con éxito.
    - Ejemplo de respuesta:
    ```json
    {
        "message": "Blob subido con éxito",
        "uuid": "generated-uuid"
    }
    ```

#### Actualizar un Blob
Actualiza el contenido de un blob existente utilizando su UUID.

- **Ruta:** `/blobs/<blob>` (PUT)
- **Descripción:** Actualiza el contenido de un blob existente utilizando su UUID.
- **Parámetros de solicitud:**
  - `blob (URL Parameter):` El UUID del blob que se desea actualizar.
  - `raw (binary stream):` El nuevo contenido del blob
- **Respuestas:**
  - **Código 200 (Éxito):** El blob se actualizó con éxito.
  - **Código 404 (No encontrado):** El blob con el UUID especificado no se encontró.
    - Ejemplo de respuesta:
    ```json
    {
        "error": "Blob no encontrado"
    }
    ```

#### Borrar un Blob
Elimina un blob existente utilizando su UUID.

- **Ruta:** `/blobs/<blob>` (DELETE)
- **Descripción:** Elimina un blob existente utilizando su UUID.
- **Parámetros de solicitud:**
  - `blob (URL Parameter):` El UUID del blob que se desea eliminar.
- **Respuestas:**
  - **Código 204 (Sin contenido):** El blob se eliminó con éxito.
  - **Código 404 (No encontrado):** El blob con el UUID especificado no se encontró.
    - Ejemplo de respuesta:
    ```json
    {
        "error": "Blob no encontrado"
    }
    ```

#### Añadir Permiso de Lectura a un Usuario
Asigna permisos de lectura de un blob a un usuario.

- **Ruta:** `/blobs/<blob>/permissions/<username>` (POST)
- **Descripción:** Asigna permisos de lectura de un blob a un usuario.
- **Parámetros de solicitud:**
  - `blob (URL Parameter):` El UUID del blob al que se desean agregar permisos.
  - `username (URL Parameter):` Datos del usuario al que se le asignarán los permisos.
- **Respuestas:**
  - **Código 200 (Éxito):** Se asignaron permisos de lectura al usuario con éxito.
  - **Código 404 (No encontrado):** El blob con el UUID especificado no se encontró.

#### Quitar Permiso de Lectura a un Usuario
Revoca los permisos de lectura de un blob a un usuario.

- **Ruta:** `/blobs/<blob>/permissions/<username>` (DELETE)
- **Descripción:** Revoca los permisos de lectura de un blob a un usuario.
- **Parámetros de solicitud:**
  - `blob (URL Parameter):` El UUID del blob del que se desean eliminar permisos.
  - `username (URL Parameter):` Datos del usuario al que se le revocarán los permisos.
- **Respuestas:**
  - **Código 200 (Éxito):** Se revocaron los permisos de lectura al usuario con éxito.
  - **Código 404 (No encontrado):** El blob con el UUID especificado no se encontró.

#### Obtener Sumas Hash del Blob
Obtén sumas hash (MD5, SHA256, etc.) del contenido de un blob al que tengas permiso de lectura.

- **Ruta:** `/blobs/<blob>/hashes` (GET)
- **Descripción:** Obtiene sumas hash del contenido del blob.
- **Parámetros de solicitud:**
  - `blob (URL Parameter):` El UUID del blob del que se desean obtener las sumas hash.
- **Respuestas:**
  - **Código 200 (Éxito):** Se obtuvieron las sumas hash con éxito.
    - Ejemplo de respuesta:
    ```json
    {
        "md5": "md5-hash-value",
        "sha256": "sha256-hash-value"
    }
    ```
  - **Código 404 (No encontrado):** El blob con el UUID especificado no se encontró o no tienes permiso para acceder a él.
    - Ejemplo de respuesta:
    ```json
    {
        "error": "Blob no encontrado"
    }
    ```
