# A pet project to compare different data processing

- Based on MongoDB change stream features

## Host

Ubuntu 20.04
MongoDb - cluster of 3 nodes (replica set)

### Add to /etc/hosts

172.20.128.1 mongo_1
172.20.128.2 mongo_2
172.20.128.3 mongo_3

## Setup

### Batch processing

- Python: process data at level mongodb deployment

### Change stream

- Golang: process data at level document
