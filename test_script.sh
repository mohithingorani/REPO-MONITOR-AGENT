#!/usr/bin/env bash
curl -X POST -H "Content-Type:application/json" -d '
{"prompt":"Tell me about https://github.com/mohithingorani/BAJAJ-BROKING-SDK"}' 'http://127.0.0.1:8000/chat'
