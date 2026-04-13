package main

import "webapp/assets"

// ================================================================ //
// ========== RUTAS =============================================== //

func (s *servidor) registrarRutas() {

	if s.cfg.sourceDir != "" {
		s.gecko.StaticAbs("/assets", s.cfg.sourceDir+"/assets")
		s.gecko.FileAbs("/favicon.ico", s.cfg.sourceDir+"/assets/img/favicon-generico.ico")
	} else {
		s.gecko.StaticFS("/assets", assets.AssetsFS)
		s.gecko.FileFS("/favicon.ico", "img/favicon-generico.ico", assets.AssetsFS)
	}
	s.gecko.GET("/assets/js/htmx.js", s.gecko.ServirHtmxMinJS())
	s.gecko.GET("/assets/js/gecko.js", s.gecko.ServirGeckoJS())

	// Autenticación
	s.AuthGET("/login", s.auth.getLogin)
	s.AuthPOST("/login", s.auth.postLogin)
	s.AuthGET("/logout", s.auth.logout)
	s.AuthGET("/sesiones", s.auth.printSesiones)

	s.PublicGET("/", s.getInicio)
	s.PublicGET("/hey/{nombre}", s.saludar)

	s.AuthGET("/admin", s.getInicio)
	s.AuthGET("/saludar/{nombre}", s.saludar)
	s.AuthPOST("/saludar/{nombre}", s.saludar)

}
