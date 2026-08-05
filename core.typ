#import "figures.typ": xp-progression-table

#let run-in-heading(title, body) = [
  #strong[#title] #h(0.8em) #body
]

#let xml-text(value) = (
  value
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
)

#let framework-diagram(game-name) = {
  let source = read("artwork/framework_diagram.svg")
  let element = source.match(
    regex("<text[^>]*id=\"game-name\"[^>]*>[^<]*</text>"),
  )
  assert(element != none, message: "framework diagram is missing its game-name text element")
  let replacement = element.text.replace(
    regex(">[^<]*</text>$"),
    ">" + xml-text(game-name) + "</text>",
  )
  image(bytes(source.replace(element.text, replacement)), format: "svg")
}

#let core(peupfudge) = [
#peupfudge is a generic framework for tabletop role-playing games.
This document contains the core rules, which can be modified or extended by modules.
The game master (GM) provides a world that can use the #peupfudge framework,
and then runs campaigns within that world.

#align(center, framework-diagram(peupfudge))

Players will face challenges, and they will have to rely on the capabilities of their characters to confront them.
#peupfudge is a system that crudely quantifies these challenges and capabilities in order to weave an interesting narrative.

Fudge dice are the main source of randomness. A fudge die can yield $-1$, $0$, or $+1$ with equal chances.
We denote a fudge die roll by “dF.” The result of a roll of $N$ fudge dice ($N$dF) is the sum of the results of the individual die rolls.

= Characters

A character is an actor in the world.
Some characters are controlled by players (PCs) and some characters are controlled by the GM (NPCs).
Characters are represented by their _traits_, which we list below.
PC traits are managed by players on their _character sheets_, while NPC traits are managed by the GM.
When creating a world or campaign, the GM determines the traits that will appear on character sheets.

There are five types of traits:

- _Abilities_ are improvable traits that play a role in action resolution.
  Examples: Strength, Intelligence, Climbing, Legal Knowledge, Cartography, Neurosurgery.
  We will soon describe how abilities work.
- _Inventory_ is the collection of items on a character's person.
  Examples: helmet, potion, gold coins.
  More detail can be included as needed; for example, one could write “helmet (equipped)” or “helmet (damaged).”

If a trait is not one of these but still has a concrete impact on action resolution, then it is one of the following:

- _Statuses_ are traits that need constant tracking for their impact on action resolution.
  Examples: health, mana, hunger, reputation.
  When introducing a status, the GM should decide what states it can take, what causes the state to change, and what effect each state has.
- _Properties_ are traits that can impact action resolution, but that only need to be considered when they apply to a character.
  Examples: deaf, blessed, stunned, short-tempered, one-armed.
- _Characteristics_ describe identity and background that mainly impact the narrative, with less of a direct connection to action resolution.
  Examples: name, race, species, tribe, height, gender, favorite food, appearance, backstory.

For tips on setting up the traits, refer to the campaign setup checklist in the appendix.

== Abilities <sec-abilities>

Before a campaign begins, the GM prepares a set of abilities that are tracked for each character.
Each ability is associated with an integer _level_ that represents how good a character is at the ability.
Ability level is a factor in the character's chance of success when attempting to perform an action dependent on the ability.
Typically, the initial level for an “untrained” ability would be $0$, and there is no hard upper limit for the level as it increases.

The level of an ability can be raised by allocating experience points (XP) to the ability.
The XP cost of increasing the level of an ability is 2 to the power of the current level.
The GM may decide how and when to award XP to characters, but it makes sense to place XP rewards after the completion of narrative “chunks.”
As soon as XP is awarded, it should be distributed by each player among their abilities.
The GM may want to restrict XP allocation to the subset of abilities that each player actually used in the completion of the narrative chunk.

Players may spend less XP on an ability than it would cost to level it up.
In this case the allocated XP is recorded and the ability is only leveled up once it has accumulated enough XP.
Allocated XP is considered to be spent and cannot later be transferred to a different ability.

XP is to be interpreted as the product of _practice time_ and _practice quality_, which we will refer to as simply _practice_.
Each unit of XP corresponds to a certain amount of practice.
The exact amount of practice contained in each unit of XP is decided implicitly the first time that the GM awards XP,
and it crystallizes as the GM continues to award XP in a consistent pattern.

Abilities generally start at level 0 during character creation.
The GM provides starting XP to each character based on the practice the character may have gathered throughout their life
before the start of the campaign.

#run-in-heading[Intrinsic Aptitude][
  Ability level is a function of XP, and XP represents _practice_.
  But ability level is ultimately meant to represent a character's _proficiency_.
  While practice generally improves proficiency, characters with the same amount of practice may have different levels of proficiency.
  The discrepancy between practice and proficiency is _intrinsic aptitude_.
  There are two methods to represent intrinsic aptitude:

  + An _XP bonus_ involves giving “free” XP in an ability that is then used to advance the level of the ability as usual.
    This would simply result in the character being further along on the same learning curve for that ability.
    For example, a character who starts with an XP bonus in the “Chess” ability but has never played chess before
    may find that she is a natural chess whiz when she first tries it,
    but still has to work just as hard to further her chess skills as a character who reached the same point through practice.
  + A _level modifier_ adds to or subtracts from the level of an ability,
    but in a way that does not affect the XP cost for leveling up.
    In this case,
    the level may be written in the character sheet as a sum: $[upright("unmodified level")] + [upright("modifier")] = [upright("modified level")]$.
    The modified level represents actual proficiency,
    and the unmodified level represents where the character is on the learning curve for the ability.
    When _using_ the ability,
    the sum is used,
    but when spending XP to _level_ the ability,
    the unmodified level is used to determine the cost.
    For example,
    a hobbit and an ogre may get the same amount of Strength practice,
    but the hobbit will still be weaker than the ogre,
    and this discrepancy could be represented by a level modifier for either the hobbit or the ogre.
    This can place them on separate learning curves for Strength in such a way that an ogre would always have an easier time improving its Strength than a hobbit of equal Strength.
    For a given ability,
    the type of being that does not take on any modifier is known as the _standard being_ for the purposes of level interpretation.
    In the example,
    if the ogre gets modified Strength and the hobbit does not,
    then hobbits are taken to be the _standard being for Strength interpretation_.
]

How strong is a character with level 5 Strength? It is as strong as a standard being that spent 5 levels worth of practice on its Strength.

#align(center, xp-progression-table())

= Actions

When a character attempts an action that has a possibility of failure, the outcome is governed by the capability of the character, the difficulty of the action, and a dice roll.
Actions are resolved by considering an attempt to be successful if

$ L + A + R >= D, $

where

- $L$ is the level of an associated ability for the character attempting the task, if there is one.
  The set of abilities chosen for the campaign should be tailored to the types of actions that players are expected to attempt.
  If there isn’t a very suitable ability but there is a close enough one, then the level of the close ability can be used with a deduction.
- $A$ is a modifier that summarizes _additional character factors_,
  which are aspects of the character attempting the action,
  aside from ability levels,
  that can contribute to its success or failure.
  For a character attempting to climb a cliff,
  additional character factors could be the fact that they
  have a grappling hook,
  or that they are afraid of heights.
- $R$ is the result of a dice roll, $N$dF.
  The dice roll represents the dependence of the outcome on factors that are not modeled in the game or that are otherwise unpredictable.
  The default is $4$dF, and this can be adjusted if more or less noise seems appropriate.
- $D$ is the difficulty level of the task,
  summarizing the _difficulty factors_: aspects of the situation,
  independent of the character,
  that can contribute to the success or failure of the action.
  For a character attempting to climb a cliff, difficulty factors could be
  the steepness of the cliff or the presence of rocks falling from above.
  Some judgment is needed on the part of the GM in the determination of $D$.
  A difficulty level of $D$ corresponds to a task that someone with an ability level of $D$ would be expected to successfully execute about half the time.

If it is unclear whether a factor belongs in $A$ or $D$, consider whether the factor could be removed from the picture by having a different character attempt the same action. If not, then it belongs in $D$.
Thus every action resolution situation is partitioned into
character-dependent ($L$ and $A$), challenge-dependent ($D$), and random ($R$) aspects.
The value of $R$ can feed directly into the narrative; it can be fun to assign extreme narrative interpretations to extreme dice rolls.
The same goes for $L + A + R - D$, which represents actual performance given all the information.

When setting $D$, the GM should avoid the pitfall of assessing a task only by comparison to similar tasks.
For example, a neurosurgery task should not be given a lower $D$ just because it is easy “for a neurosurgery.”
Note that $D$ ultimately gets compared to an ability level $L$, which is a function of experience.
Since neurosurgery itself is hard (in the sense of requiring a lot of experience), the $D$ associated with many neurosurgery tasks, even the _relatively_ easy ones, should be high.
It might be a good idea when setting up the abilities for a given campaign to determine what level for each ability is considered “poor,” “decent,” “excellent,” etc.
A decent neurosurgeon may have a higher level in Neurosurgery than a decent hauler has in Hauling.

#run-in-heading[Opposed Actions][
  If the difficulty factors for an action are due to some other character's abilities,
  for example during a race between multiple characters,
  then the action is _opposed_.
  There are modifications one could make for opposed actions: Instead of comparing one character’s $L + A + R$ with a $D$ based on the difficulty of the task,
  one can compare $L + A + R$ for each character to determine their performance relative to one another.
  Each character's $L + A + R$ essentially represents $D$ for their opponent(s).
  When the $L + A + R$ of multiple characters is equal,
  this should be interpreted as a tie rather than as a success for any of the tied characters.
  For opposed actions,
  the default $R$ is $3$dF,
  and this can be modified if more or less noise seems appropriate.
  For fun,
  the physical dice rolling can be done by all participants whose characters are involved,
  with players rolling for their characters and the GM rolling for NPCs.
]

Happy #(peupfudge + "ing")!
]
