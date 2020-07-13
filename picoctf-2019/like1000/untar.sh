#!/bin/bash
set -e

layer=1000

while [[ $layer -gt 0 ]] ;do
  out=like1000/$layer.tar.out
  mkdir $out

  if [[ $layer -eq 1000 ]];then
    tar xf like1000/$layer.tar -C $out
  else
    tar xf like1000/$(($layer+1)).tar.out/$layer.tar -C $out
  fi
  layer=$(($layer-1))
done
