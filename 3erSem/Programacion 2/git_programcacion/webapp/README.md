# Web app

Este es un repositorio de punto de partida para crear una web app.

Después de clonar el repositorio, abre el proyecto ejecuta el script para compilar y ejecutar la aplicación.

```bash
./scripts/run.sh
```

Requerimientos:
- Go
- Tailwind CLI

> Nota: si no los tienes instalados o no tienes permiso de administrador, el script preguntará si los quieres descargar dentro de la misma carpeta del proyecto para ejecutarlos de manera local.

### Crear entidades

Para tener una capa de persistencia es necesario registrar las entidades en la herramienta `pargocode`.

Instalar pargocode:
```bash
go install github.com/pargomx/pargocode@latest
```

Ejecutar desde la raíz del proyecto:
```bash
pargocode
```

Abrir la interfaz web: `localhost:5051`
