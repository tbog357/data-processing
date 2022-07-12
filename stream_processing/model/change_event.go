package model

import (
	"stream_processing/core/helper"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type ChangeEvent struct {
	// Parse change event fields
	OperationType     string                 `json:"operationType" bson:"operationType"`
	DocumentKey       DocumentKey            `json:"documentKey" bson:"documentKey"`
	Ns                Ns                     `json:"ns" bson:"ns"`
	UpdateDescription UpdateDescription      `json:"updateDescription" bson:"updateDescription"`
	FullDocument      map[string]interface{} `json:"fullDocument" bson:"fullDocument"`
}

type DocumentKey struct {
	Id primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
}

type Ns struct {
	Db   string `json:"db" bson:"db"`
	Coll string `json:"coll" bson:"coll"`
}

type UpdateDescription struct {
	UpdatedFields map[string]interface{} `json:"updatedFields,omitempty" bson:"updatedFields,omitempty"`
}

func (e *ChangeEvent) GetUniqueIdentity() string {
	db := e.Ns.Db
	coll := e.Ns.Coll
	docId := e.DocumentKey.Id.Hex()
	return helper.JoinStringsByVerticalBar(db, coll, docId)
}
