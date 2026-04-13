package main

import (
	"flag"
	"io/fs"
	"os"
	"path"
	"time"

	"webapp/htmltmpl"
	"webapp/migraciones"

	"github.com/pargomx/gecko"
	"github.com/pargomx/gecko/gko"
	"github.com/pargomx/gecko/logsqlite"
	"github.com/pargomx/gecko/plantillas"
	"github.com/pargomx/gecko/sqlitedb"
)

// Información de compilación establecida con:
//
//	BUILD_INFO="$(date -I):$(git log --format="%H" -n 1)"
//	go build -ldflags "-X main.BUILD_INFO=$BUILD_INFO -X main.AMBIENTE=DEV"
var BUILD_INFO string // Información de compilación [ fecha:commit_hash ]
var AMBIENTE string   // Ambiente de ejecución [ DEV / PROD ]

type servidor struct {
	cfg       configs
	gecko     *gecko.Gecko
	db        *sqlitedb.SqliteDB
	auth      *authService
	userFiles fs.FS // read only
}

type configs struct {
	workingDir string // Directorio raíz de la aplicación.
	configPath string // Ubicación del archivo de configuración.
	sourceDir  string // Directorio con assets y htmltmpl para no usar embeded.

	Hostname string // Nombre de dominio en el que está el servicio.
	Puerto   int    // Puerto TCP del servidor.
	Socket   string // Unix Socket del servidor (no usar puerto TCP).
	LogHTTP  string // Log de solicitudes HTTP.

	DatabasePath string // Ruta del archivo base de datos.
	LogDB        bool   // Loggear consultas a la base de datos.

	UserFiles string // Directorio para archivos de usuario.
	AdminUser string
	AdminPass string
}

var defaults = configs{
	workingDir: "",
	configPath: "config.json",
	sourceDir:  "",

	Hostname: "holamundo",
	Puerto:   8080,
	Socket:   "",
	LogHTTP:  "loghttp.db",

	DatabasePath: "app.db",
	LogDB:        false,

	UserFiles: "data",
	AdminUser: "mandarina",
	AdminPass: "pandas1990",
}

func main() {
	gko.LogInfof("Versión:%s:%s", BUILD_INFO, AMBIENTE)
	s := servidor{}
	var err error

	// Configuraciones vía comando
	flag.StringVar(&s.cfg.workingDir, "dir", defaults.workingDir, "directorio raíz de la aplicación")
	flag.StringVar(&s.cfg.configPath, "cfg", defaults.configPath, "archivo de configuración")
	flag.StringVar(&s.cfg.sourceDir, "src", defaults.sourceDir, "directorio con assets y htmltmpl para no usar embeded")
	flag.BoolFunc("v", "imprimir versión y salir", func(v string) error {
		os.Exit(0)
		return nil
	})
	onlySetup := flag.Bool("setup", false, "preparar configuración y salir")
	flag.Parse()

	// Directorio raíz de ejecución
	if s.cfg.workingDir != "" {
		err := os.Chdir(s.cfg.workingDir)
		if err != nil {
			gko.FatalExit("directorio raíz inválido: " + err.Error())
		}
	}
	s.cfg.workingDir, err = os.Getwd()
	if err != nil {
		gko.FatalExit("directorio raíz inválido: " + err.Error())
	}

	// Configuraciones vía archivo
	err = getConfig(s.cfg.configPath, &s.cfg)
	if err != nil {
		gko.FatalError(err)
	}
	if onlySetup != nil && *onlySetup {
		os.Exit(0)
	}

	// Repositorio
	s.db, err = sqlitedb.NuevoRepositorio(s.cfg.DatabasePath, migraciones.MigracionesFS)
	if err != nil {
		gko.FatalError(err)
	}
	if s.cfg.LogDB {
		s.db.ToggleLog()
	}

	// Plantillas HTML
	s.gecko = gecko.New()
	if s.cfg.sourceDir != "" {
		gko.LogInfo("Usando plantillas en " + s.cfg.sourceDir + "/htmltmpl")
		s.gecko.Renderer, err = plantillas.NuevoServicioPlantillas(s.cfg.sourceDir+"/htmltmpl", AMBIENTE == "DEV")
	} else {
		s.gecko.Renderer, err = plantillas.NuevoServicioPlantillasEmbebidas(htmltmpl.PlantillasFS, "")
	}
	if err != nil {
		gko.FatalError(err)
	}
	s.gecko.TmplBaseLayout = "layouts/base"
	s.gecko.TmplError = "layouts/error"

	// Log solicitudes HTTP
	if s.cfg.LogHTTP != "" {
		httpLogger, err := logsqlite.NewLogger(s.cfg.LogHTTP, time.Second*5)
		if err != nil {
			gko.FatalError(err)
		}
		s.gecko.HTTPLogger = httpLogger
	}

	// User files debe ser absoluto.
	if s.cfg.UserFiles == "" {
		s.cfg.UserFiles = s.cfg.workingDir
	}
	if !path.IsAbs(s.cfg.UserFiles) {
		s.cfg.UserFiles = path.Join(s.cfg.workingDir, s.cfg.UserFiles)
	}
	s.userFiles = os.DirFS(s.cfg.UserFiles)

	// Autenticación y rutas
	s.auth = NewAuthService(s.cfg.AdminUser, s.cfg.AdminPass)
	s.auth.RecuperarSesiones()
	s.registrarRutas()

	// Apagado del servidor
	s.gecko.CleanupFunc = func() {
		err = s.db.Close()
		if err != nil {
			gko.LogError(err)
		}
		s.gecko.HTTPLogger.Close()
		s.auth.PersistirSesiones()
	}

	// Escuchar y servir
	if s.cfg.Socket != "" {
		err = s.gecko.IniciarEnSocket(s.cfg.Socket)
	} else {
		err = s.gecko.IniciarEnPuerto(s.cfg.Puerto)
	}
	if err != nil {
		gko.FatalError(err)
	}
}
