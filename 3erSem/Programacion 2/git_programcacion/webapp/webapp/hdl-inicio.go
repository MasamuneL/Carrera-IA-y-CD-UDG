package main

import (
	"github.com/pargomx/gecko"
	"github.com/pargomx/gecko/gko"
)

func (s *servidor) getInicio(c *gecko.Context) error {
	return c.RenderOk("inicio", map[string]any{
		"Titulo":  "Inicio",
		"Mensaje": "Hola Mundo!",
	})
}

func (s *servidor) saludar(c *gecko.Context) error {
	nombre := c.Param("nombre")
	if nombre == "" {
		nombre = "Mundo"
	}
	if nombre == "error" {
		return gko.ErrDatoInvalido.Msg("nombre no permitido")
	}
	return c.RenderOk("inicio", map[string]any{
		"Titulo": "Saludo",
		"Nombre": nombre,
	})
}
