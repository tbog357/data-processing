package logger

import (
	"encoding/json"
	"log"
	"os"
	"runtime"
	"strings"
	"time"
)

type logLevel string

const (
	INFO  logLevel = "INFO"
	ERROR logLevel = "ERROR"
	WARN  logLevel = "WARN"
)

type logRecord struct {
	Timestamp int64                  `json:"timestamp,omitempty"`
	Level     logLevel               `json:"level,omitempty"`
	Line      int                    `json:"line,omitempty"`
	Text      string                 `json:"text,omitempty"`
	Json      map[string]interface{} `json:"json,omitempty"`
	Location  string                 `json:"location,omitempty"`
}

func (record *logRecord) init(level logLevel) {
	_, file, line, _ := runtime.Caller(1)
	dir, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	record.Timestamp = time.Now().Unix()
	record.Location = "." + strings.TrimPrefix(file, dir)
	record.Line = line
	record.Level = level
}

func writeLogRecord(record logRecord) {
	marshalledRecord, err := json.Marshal(record)
	if err != nil {
		panic(err)
	}
	log.Println(string(marshalledRecord))
}

func WriteText(message string, level logLevel) {
	record := new(logRecord)
	record.init(level)
	record.Text = message
	writeLogRecord(*record)
}

func WriteJson(message map[string]interface{}, level logLevel) {
	record := new(logRecord)
	record.init(level)
	record.Json = message
	writeLogRecord(*record)
}
