package logger

import (
	"fmt"
	"os"
)

type writer struct {
	logFileWriter *os.File
}

func (writer *writer) SetLogFilePath(path string) {
	var err error
	writer.logFileWriter, err = os.OpenFile(path, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		panic(err)
	}
}

func (writer writer) Write(data []byte) (int, error) {
	/*
	Routing logs to file and stdout
	*/
	_, err := writer.logFileWriter.Write(data)
	if err != nil {
		fmt.Println("Cannot push logs to file")
	}
	return fmt.Printf("%s", data)
}
