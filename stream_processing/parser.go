package main

import (
	"stream_processing/core/logger"
	"stream_processing/model"
)

type DefaultParser struct {
}

func (p *DefaultParser) Parse(event *model.ChangeEvent) error {
	logger.WriteText(event.GetUniqueIdentity(), logger.INFO)
	return nil
}
