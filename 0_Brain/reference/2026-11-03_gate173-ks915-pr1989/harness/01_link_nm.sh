#!/bin/bash
# Creates ONE symlink inside the gate clone pointing at the checkout's node_modules (read-only use;
# nothing is written in the checkout).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989
ln -s "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules" "$W/repo/Blockchain/Dev/node_modules"
git -C $W/repo status --porcelain --ignored | head
