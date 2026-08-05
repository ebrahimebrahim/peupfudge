= Reference Sheet

#import "figures.typ": xp-progression-table

#let reference_accent = rgb("98a6ca")

#let probability-table = block(width: 1.52in)[
  #table(
    columns: (0.5fr, 1.8fr),
    align: center + horizon,
    inset: (x: 3pt, y: 4.5pt),
    stroke: 0.4pt,
    [#emph[n]], [P(4dF ≥ #emph[n])],
    [-3], [.99],
    [-2], [.94],
    [-1], [.81],
    [0], [.62],
    [1], [.38],
    [2], [.19],
    [3], [.06],
    [4], [.01],
  )
]

#let outlined-symbol(body, size: 52pt) = text(
  font: "DejaVu Sans Mono",
  size: size,
  weight: "bold",
  fill: white,
  stroke: 1.65pt + black,
  body,
)

#place(center + horizon)[
  #box(width: 93%, height: 7.64in, stroke: 0.5pt, inset: 8pt)[
    #align(left + top)[
      #block(width: 100%)[
        #set par(justify: false, first-line-indent: 0pt, spacing: 0.55em)

        #text(size: 28pt)[To level up:]
        #v(0.36in)

        #align(center)[
          #text(size: 17pt)[xp required to level up $=$]
          #h(2pt)
          #text(size: 27pt)[
            $2^(
              upright("old level")
              #text(fill: reference_accent)[(unmodified)]
            )$
          ]
        ]
        #v(0.37in)

        #align(center, text(size: 13pt)[#xp-progression-table()])
        #v(0.60in)

        #text(size: 28pt)[Action success if:]
        #v(0.43in)

        #block(width: 88%)[
        #grid(
          columns: (1fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
          column-gutter: 0pt,
          row-gutter: 6pt,
          align: center + top,

          outlined-symbol([L]),
          outlined-symbol([+], size: 43pt),
          outlined-symbol([A]),
          outlined-symbol([+], size: 43pt),
          outlined-symbol([R]),
          outlined-symbol([≥], size: 43pt),
          outlined-symbol([D]),

          block(width: 0.92in)[
            #text(size: 10pt)[
              #align(center)[
                ability level\
                #text(fill: reference_accent)[(possibly\ modified)]
              ]
            ]
          ],
          [],
          block(width: 0.95in)[
            #text(size: 10pt)[#align(center)[additional\ character\ factors]]
          ],
          [],
          block(width: 1.7in)[
            #text(size: 10pt)[
              #align(center)[
                dice roll\
                default: 4dF\
                (3dF if opposed)
                #v(6pt)
                #text(size: 11pt)[#probability-table]
              ]
            ]
          ],
          [],
          move(
            dx: 25pt,
            block(width: 1.58in)[
              #text(size: 10pt)[
                #align(left)[difficulty factors]
                #v(4pt)
                #pad(left: 9pt)[
                  #align(left)[
                    meaning of #emph[D]:\
                    someone with this\
                    value as their ability\
                    level would succeed\
                    about half the time.
                  ]
                ]
              ]
            ],
          ),
        )
        ]
      ]
    ]
  ]
]
