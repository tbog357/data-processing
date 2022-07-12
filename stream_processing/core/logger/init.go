package logger

import "log"

var isLoggerInited bool = false

func SetupLogger() {
	// Check if logger is inited
	if isLoggerInited {
		WriteText("Logger is inited", WARN)
		return
	}

	// Init logger
	log.SetFlags(0)

	// Setup writer
	writer := writer{}
	writer.SetLogFilePath("logs/logs.log")
	log.SetOutput(writer)

	// For checking logger is inited
	isLoggerInited = true
	WriteText("Logger is inited", INFO)
}
