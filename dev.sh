#!/bin/bash
(trap 'kill 0' SIGINT; make run-backend & make run-frontend)