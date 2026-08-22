#let peupfudge = "Peup"

#set document(
  title: peupfudge,
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
#set list(spacing: 0.8em)
#set heading(numbering: "1.1")
#let extra-heading-space = 0.5em
#show heading: set block(
  above: 1.44em + extra-heading-space,
  below: 0.75em + extra-heading-space,
  sticky: true,
)
#show heading.where(level: 1): set block(
  above: (1.8em + extra-heading-space) / 1.4,
  below: (0.75em + extra-heading-space) / 1.4,
)
#show heading.where(level: 2): set block(
  above: (1.44em + extra-heading-space) / 1.2,
  below: (0.75em + extra-heading-space) / 1.2,
)
#show heading: it => block[
  #context {
    if it.numbering != none {
      counter(heading).display(it.numbering)
      h(0.3em + extra-heading-space)
    }
    it.body
  }
]

#let version-file = sys.inputs.at("version-file", default: none)
#let version = if version-file == none {
  "unknown (draft)"
} else {
  read(version-file).trim()
}
#grid(
  columns: (1fr, auto),
  align: (left + bottom, right + bottom),
  text(size: 25pt, weight: "bold")[#peupfudge],
  [Version #strong[#version]],
)

#import "core.typ": core
#core(peupfudge)

#pagebreak()
#counter(heading).update(0)
#set heading(numbering: "A.1")

#set page(numbering: none)
#include "reference_sheet.typ"
#pagebreak()
#set page(numbering: "1")
#import "setup_checklist.typ": setup-checklist
#setup-checklist(peupfudge)
#import "examples.typ": examples
#examples(peupfudge)
#include "probability_reference.typ"
