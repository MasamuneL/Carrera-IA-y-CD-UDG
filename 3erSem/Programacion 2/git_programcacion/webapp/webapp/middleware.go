package main

import (
	"fmt"
	"time"

	"github.com/pargomx/gecko"
)

// ================================================================ //
// ========== Middleware ========================================== //

func (s *servidor) AuthGET(path string, authHandler gecko.HandlerFunc) {
	s.gecko.GET(path, s.auth.Auth(func(c *gecko.Context) error {
		logDevReq(c)
		c.Response().Header().Set("Cache-Control", "no-store")
		return authHandler(c)
	}))
}

func (s *servidor) AuthPOST(path string, authHandler gecko.HandlerFunc) {
	s.gecko.POST(path, s.auth.Auth(func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	}))
}

func (s *servidor) AuthPATCH(path string, authHandler gecko.HandlerFunc) {
	s.gecko.PATCH(path, s.auth.Auth(func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	}))
}

func (s *servidor) AuthPUT(path string, authHandler gecko.HandlerFunc) {
	s.gecko.PUT(path, s.auth.Auth(func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	}))
}

func (s *servidor) AuthDELETE(path string, authHandler gecko.HandlerFunc) {
	s.gecko.DELETE(path, s.auth.Auth(func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	}))
}

// ================================================================ //

func (s *servidor) PublicGET(path string, authHandler gecko.HandlerFunc) {
	s.gecko.GET(path, func(c *gecko.Context) error {
		logDevReq(c)
		return authHandler(c)
	})
}

func (s *servidor) PublicPOST(path string, authHandler gecko.HandlerFunc) {
	s.gecko.POST(path, func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	})
}

func (s *servidor) PublicPATCH(path string, authHandler gecko.HandlerFunc) {
	s.gecko.PATCH(path, func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	})
}

func (s *servidor) PublicPUT(path string, authHandler gecko.HandlerFunc) {
	s.gecko.PUT(path, func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	})
}

func (s *servidor) PublicDELETE(path string, authHandler gecko.HandlerFunc) {
	s.gecko.DELETE(path, func(c *gecko.Context) error {
		logDevReq(c)
		if AMBIENTE == "DEV" {
			time.Sleep(time.Millisecond * 400)
		}
		return authHandler(c)
	})
}

// ================================================================ //
// ========== LOG ================================================= //

func logDevReq(c *gecko.Context) bool {
	if AMBIENTE == "DEV" {
		htmx := "->"
		if c.EsHTMX() {
			htmx = "hx"
		}
		params := ""
		for k, v := range c.Request().URL.Query() {
			params += k + "=" + v[0] + " "
		}
		fmt.Println(
			"\033[32m"+htmx+"\033[0m",
			"\033[2m"+time.Now().Format("15:04:05.000")+"\033[0m",
			c.Path()+"\033[2m",
			c.Request().URL.String(),
			params,
			"\033[0m",
		)
	}
	return true
}
