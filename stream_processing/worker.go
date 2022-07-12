package main

import (
	"stream_processing/model"
	"sync"
)

type Worker struct {
	Parser       Parser
	FailErrorMap map[string]string
	RunningEvent map[string]string
	mu           sync.Mutex
	wg           *sync.WaitGroup
}

type Parser interface {
	Parse(*model.ChangeEvent) error
}

func (w *Worker) init(parser Parser) {
	w.FailErrorMap = make(map[string]string)
	w.RunningEvent = make(map[string]string)
	w.mu = sync.Mutex{}
	w.wg = &sync.WaitGroup{}
	w.Parser = parser
}

func (w *Worker) isSkipEvent(uniqueIdentity string) bool {
	w.mu.Lock()
	defer w.mu.Unlock()
	_, ok := w.FailErrorMap[uniqueIdentity]
	return ok
}

func (w *Worker) isEventRunning(uniqueIdentity string) bool {
	w.mu.Lock()
	defer w.mu.Unlock()

	_, ok := w.RunningEvent[uniqueIdentity]
	return ok
}

func (w *Worker) removeRunningEvent(uniqueIdentity string) {
	w.mu.Lock()
	defer w.mu.Unlock()

	delete(w.RunningEvent, uniqueIdentity)
}

func (w *Worker) setFailedEvent(uniqueIdentity string, errMsg string) {
	w.mu.Lock()
	defer w.mu.Unlock()

	w.FailErrorMap[uniqueIdentity] = errMsg
}

func (w *Worker) Run(event *model.ChangeEvent) {
	uniqueIdentity := event.GetUniqueIdentity()
	if w.isSkipEvent(uniqueIdentity) {
		return
	}
	for w.isEventRunning(uniqueIdentity) {
	}
	w.wg.Add(1)
	go w.Process(event)
}

func (w *Worker) Process(event *model.ChangeEvent) {
	defer w.wg.Done()
	err := w.Parser.Parse(event)
	w.removeRunningEvent(event.GetUniqueIdentity())
	if err != nil {
		w.setFailedEvent(event.GetUniqueIdentity(), err.Error())
	}
}
