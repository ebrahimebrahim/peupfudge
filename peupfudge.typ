#set document(
  title: "Peupfudge",
  author: "Ebrahim Ebrahim",
)

#set page(
  paper: "us-letter",
  margin: 0.8in,
  numbering: "1",
  number-align: center + bottom,
)

#set text(font: "Libertinus Serif")

#set par(
  justify: true,
  first-line-indent: 0pt,
  spacing: 2em,
)
#set heading(numbering: "1.1")

#let version-file = sys.inputs.at("version-file", default: none)
#let version = if version-file == none {
  "unknown (draft)"
} else {
  read(version-file).trim()
}
#grid(
  columns: (1fr, auto),
  align: (left + bottom, right + bottom),
  text(size: 25pt, weight: "bold")[Peupfudge],
  [Version #strong[#version]],
)

#include "core.typ"

#pagebreak()
#counter(heading).update(0)
#set heading(numbering: "A.1")

#set page(numbering: none)
#include "reference_sheet.typ"
#pagebreak()
#set page(numbering: "1")
#include "setup_checklist.typ"
#include "examples.typ"
#include "probability_reference.typ"
