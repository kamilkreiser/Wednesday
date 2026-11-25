#!/bin/bash
# QA-VIEWER-NEXT item 6 / answer (1): evaluate the ROWS block of a red script with bash and count log names three ways.
f="$1"; eval "$(sed -n '/^ROWS=(/,/^)/p' "$f")"
old=(); itm=(); new=()
for row in "${ROWS[@]}"; do
  IFS='|' read -r var name pkg target test item <<<"$row"
  old+=("${name}__${target//:/_}.log")
  itm+=("${name}__${target//:/_}__${item}.log")
  item_f="${item//\//_}"; new+=("${name}__${target//:/_}__${item_f//:/_}__${test//:/_}.log")
  case "$test$item" in */*) echo "SLASH in test/item: $row";; esac
done
echo "rows ${#ROWS[@]}; old names distinct $(printf '%s\n' "${old[@]}" | sort -u | wc -l | tr -d ' '); item-only distinct $(printf '%s\n' "${itm[@]}" | sort -u | wc -l | tr -d ' '); new names distinct $(printf '%s\n' "${new[@]}" | sort -u | wc -l | tr -d ' ')"
echo "item-only duplicates: $(printf '%s\n' "${itm[@]}" | sort | uniq -d | tr '\n' ' ')"
echo "LA rows (activity_|watch_): $(for row in "${ROWS[@]}"; do IFS='|' read -r v n _ <<<"$row"; [[ "$n" =~ ^(activity_|watch_) ]] && echo x; done | wc -l | tr -d ' ')"
