package badcode

type jugador struct {
	vida    int
	terreno string
	poder   int
	x       int
	y       int
}

func AtacarPorAgua(atacante *jugador, defensor *jugador) {
	if defensor.terreno == "fuego" {
		if atacante.x > defensor.x {
			if atacante.y == defensor.y {
				defensor.vida -= 15
			} else {
				if atacante.y > defensor.y {
					defensor.vida -= 10
				} else {
					defensor.vida -= 8
				}
			}
		} else {
			if atacante.x == defensor.x {
				if atacante.poder > 50 {
					defensor.vida -= 20
				} else {
					defensor.vida -= 12
				}
			}
		}
	} else {
		if defensor.terreno == "tierra" {
			if atacante.poder > 30 {
				if defensor.vida > 50 {
					defensor.vida -= 7
				} else {
					if defensor.vida > 25 {
						defensor.vida -= 9
					} else {
						defensor.vida -= 11
					}
				}
			} else {
				// nada
			}
		} else {
			if defensor.terreno == "aire" {
				defensor.vida -= 3
			}
		}
	}
}

func AtacarPorFuego(atacante *jugador, defensor *jugador) {
	if defensor.terreno == "tierra" {
		if atacante.poder > 40 {
			if defensor.x < atacante.x {
				if defensor.y != atacante.y {
					defensor.vida -= 18
				} else {
					defensor.vida -= 14
				}
			} else {
				defensor.vida -= 6
			}
		} else {
			if atacante.poder > 20 {
				defensor.vida -= 4
			}
		}
	} else {
		if defensor.terreno == "agua" {
			defensor.vida -= 2
		} else {
			if defensor.terreno == "aire" {
				if atacante.vida > defensor.vida {
					defensor.vida -= 13
				} else {
					defensor.vida -= 5 // Objetivo (parte 3)
				}
			}
		}
	}
}

func AtacarPorTierra(atacante *jugador, defensor *jugador) {
	if atacante.terreno == "tierra" {
		if defensor.terreno == "aire" {
			if atacante.x == defensor.x && atacante.y == defensor.y {
				defensor.vida -= 25
			} else {
				if atacante.poder > defensor.poder {
					defensor.vida -= 16
				} else {
					defensor.vida -= 8
				}
			}
		}
	}
}

func Atacar(atacante *jugador, defensor *jugador) {
	if atacante.poder > 0 {
		if defensor.vida > 0 {
			switch atacante.terreno {
			case "agua":
				AtacarPorAgua(atacante, defensor)
			case "fuego":
				AtacarPorFuego(atacante, defensor)
			case "tierra":
				AtacarPorTierra(atacante, defensor)
			}
		}
		atacante.poder -= 5
	}
}
