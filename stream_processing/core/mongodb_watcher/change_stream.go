package mongodb_watcher

import (
	"context"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

func GetChangeStream(uri string) *mongo.ChangeStream {
	client, err := mongo.Connect(context.Background(), options.Client().ApplyURI(uri))
	if err != nil {
		panic(err)
	}

	if err := client.Ping(context.Background(), readpref.Primary()); err != nil {
		panic(err)
	}

	changeStream, err := client.Watch(context.Background(), mongo.Pipeline{})
	if err != nil {
		panic(err)
	}
	return changeStream
}
