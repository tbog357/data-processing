package main

import (
	"context"
	"os"
	"os/signal"
	"stream_processing/core/logger"
	"stream_processing/core/mongodb_watcher"
	"stream_processing/core/postgres"
	"stream_processing/model"

	"go.mongodb.org/mongo-driver/bson"
)

func main() {
	// Setup logger and dbs
	logger.SetupLogger()
	postgres.Init(os.Getenv(ENV_POSTGRES_URI))
	changeStream := mongodb_watcher.GetChangeStream(os.Getenv(ENV_MONGODB_URI))

	// Create worker
	worker := new(Worker)
	worker.init(new(DefaultParser))

	// Setup worker and handle graceful shutdown
	go func() {
		for {
			if changeStream.TryNext(context.Background()) {
				var event model.ChangeEvent
				bson.Unmarshal(changeStream.Current, &event)
				worker.Run(&event)
			} else {
				logger.WriteText("No event", logger.INFO)
			}
		}
	}()

	signalChannel := make(chan os.Signal, 1)
	signal.Notify(signalChannel, os.Interrupt)
	for terminateSignal := range signalChannel {
		logger.WriteText("Received terminate signal "+terminateSignal.String(), logger.INFO)
		break
	}
}
