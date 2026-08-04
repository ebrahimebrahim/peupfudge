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

// uncomment to use the old font when we were using latex.
// #set text(
//   font: "New Computer Modern",
//   size: 12pt,
// )

#set par(
  justify: true,
  first-line-indent: 0pt,
  spacing: 2em,
)
#set heading(numbering: "1.1")

#let today = datetime.today()
#grid(
  columns: (1fr, auto),
  align: (left + bottom, right + bottom),
  text(size: 25pt, weight: "bold")[Peupfudge],
  [DRAFT: #strong[#today.display("[month repr:long] [day padding:none], [year]")]],
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
