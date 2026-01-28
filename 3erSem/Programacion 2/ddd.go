package main

import (
	"errors"
	"fmt"
	"strings"
)

func main() {
	fmt.Println("Hello, World!")
}

type User struct {
	UserName string
	UserID   int
	Age      int
	RFC      string
	Email    string
	Password string
}

type Shares struct {
	ShareID          int
	ShareName        string
	ActualSharePrice int
	ShareCurrency    string
}

type Acount struct {
	AcountID     int
	Balance      int
	Whithdrawals int
	AcountFee    int
}

type Buys struct {
	TransactionID   int
	Date            string
	IndividualPrice int
	TotalPrice      int
	ShareBuyNum     int
}

type Sales struct {
	TransactionID   int
	Date            string
	IndividualPrice int
	TotalPrice      int
	ShareSaleNum    int
}

func ChangerUsrName(user User, NewUserName string) error {

	NewUserName = strings.TrimSpace(NewUserName)

	if NewUserName == "" {
		return errors.New("Must Specify a User Name")
	}

	if NewUserName == user.UserName {
		return errors.New("User Name in use")
	}

	if len(NewUserName) > 20 {
		return errors.New("User Name legnth exceeded")
	}

	user.UserName = NewUserName

	return nil
}
