= Probability Reference

The following table shows the probabilities of success when rolling different amounts of fudge dice.
Each entry is the probability that $N$dF will be $>= D$, for some $N$ and $D$.

#let ndf-data = json("ndf_table.json")
#let highlight = rgb("#ccccff")
#let header-cells = (
  [],
  ..ndf-data.thresholds.map(threshold => table.cell(
    fill: if threshold == 0 { highlight } else { none },
  )[$>= #threshold$]),
)
#let body-cells = ndf-data.rows.map(row => {
  let row-fill = if row.dice == 4 { highlight } else { none }
  let label = table.cell(fill: row-fill)[#(row.dice)dF]
  let values = row.probabilities.enumerate().map(pair => {
    let index = pair.at(0)
    let probability = pair.at(1)
    let threshold = ndf-data.thresholds.at(index)
    table.cell(
      fill: if row.dice == 4 or threshold == 0 { highlight } else { none },
    )[#probability]
  })
  (label, ..values)
}).flatten()

#align(center)[
  #table(
    columns: 12,
    align: center,
    stroke: 0.5pt,
    inset: (x: 3pt, y: 2pt),
    ..header-cells,
    ..body-cells,
  )
]

The values in the highlighted column are close to $0.5$,
hence the rule of thumb:
A task of difficulty level $D$ is one that someone with an ability level of $D$ would be expected to successfully execute about half the time.

The highlighted row corresponds to $4$dF, a nice standard number of dF to roll.
By rolling more or fewer dF, one can vary the spread of the distribution of outcomes.
The outcome of rolling $N$dF approaches a normal distribution as $N$ increases,
with the standard deviation being a constant multiple of $sqrt(N)$.
Note that the spread of the distribution does not vary linearly with the number of dice.
There’s a bigger difference between rolling $2$dF and rolling $4$dF than there is between rolling $4$dF and rolling $6$dF.

#align(center)[
  #image("ndf_plot.pdf", width: 65%)
]
