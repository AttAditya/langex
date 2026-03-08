source ./.venv/bin/activate

lnx() {
  fmt() {
    python -m formatter.fmt $@
  }

  run() {
    python -m langex $@
  }

  sample() {
    python samples$1
  }

  if [ "$1" = "fmt" ]; then
    shift
    fmt $@
  elif [ "$1" = "run" ]; then
    shift
    run $@
  else
    echo "Possible commands: fmt, run"
  fi
}

