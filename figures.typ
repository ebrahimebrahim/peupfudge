#let handwritten(body) = text(
  font: "Kalam",
  weight: "regular",
  fill: luma(35%),
  body,
)

#let xp-progression-table() = align(center, table(
  columns: (auto, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
  align: center,
  stroke: 0.5pt,
  inset: (x: 4pt, y: 3pt),
  [Level], [0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [$dots$],
  [XP Cost], [0], [1], [2], [4], [8], [16], [32], [64], [128], [256], [$dots$],
  [Total XP], [0], [1], [3], [7], [15], [31], [63], [127], [255], [511], [$dots$],
))

#let ability-summary(name, values) = block([
  #text(size: 11pt)[#name Abilities:]
  #v(3pt)
  #grid(
    columns: (auto, auto),
    align: (right, left),
    column-gutter: 7pt,
    row-gutter: 1.5pt,
    text(size: 9.5pt, weight: "bold")[Muscle:],
    handwritten(values.at(0)),
    text(size: 9.5pt, weight: "bold")[Charisma:],
    handwritten(values.at(1)),
    text(size: 9.5pt, weight: "bold")[Perception:],
    handwritten(values.at(2)),
    text(size: 9.5pt, weight: "bold")[Knowledge:],
    handwritten(values.at(3)),
  )
])

#let xp-allocation-example() = align(center, grid(
  columns: (auto, auto),
  align: top,
  column-gutter: 28pt,
  ability-summary("Kotorikh", (
    [0],
    [0],
    [4 (+4/16)],
    [5],
  )),
  ability-summary("Obazana", (
    [4 (+6/16)],
    [3 (+6/8)],
    [3],
    [3 (+2/8)],
  )),
))
