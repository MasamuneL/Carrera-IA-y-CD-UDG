package htmltmpl

import "embed"

//go:embed *.html **/*.html
var PlantillasFS embed.FS
