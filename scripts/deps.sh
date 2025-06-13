#!/bin/bash

if ! command -v bun &>/dev/null; then
  if ! command -v brew &>/dev/null; then
    echo "Homebrew could not be found. Please install Homebrew first and run this script again."
    exit 1
  fi
  brew install bun
  brew install uv
fi

uv sync
