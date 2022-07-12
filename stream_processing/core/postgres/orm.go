package postgres

import (
	_ "github.com/jackc/pgx/stdlib"
	"xorm.io/xorm"
)

var engine *xorm.Engine

func Init(uri string) {
	var err error
	engine, err = xorm.NewEngine("pgx", uri)
	if err != nil {
		panic(err)
	}
}

func Insert(table string, model map[string]interface{}) error {
	affected, err := engine.Table(table).Insert(&model)
	if err != nil {
		return err
	} else if affected == 0 {
		return ErrNoRowAffected
	}
	return nil
}

func Update(table string, model map[string]interface{}) error {
	affected, err := engine.Table(table).Update(&model)
	if err != nil {
		return err
	} else if affected == 0 {
		return ErrNoRowAffected
	}
	return nil
}
