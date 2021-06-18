This is an interpreter for a very simple language consisting of
condition -> effects
style rules.

Conditions are of the form
belief1,...,beliefn
where beliefs are strings.
Effects are then +belief,-belief,+!goal,-!goal or .action
where action is intended to have an effect on the world.

Note that rules should typically take the form of
<belief context>,!goal -> -!goal, ....

In other words, the rule achieving a goal should remove the goal. Note also that we don't respond to changes in belief/goals (unlike BDI style systems) but rather to the presence of beliefs or goals.

A rule of the form
a -> +b
should probably never exist, as it states that having belief a should cause belief b to be added, but since nothing is removed from the belief base, this rule will continuously fire and block all other rules.
a -> -a,+b
is probably ok

Finally, the language also enables one to inject goals and beliefs into the system by adding statements of the form
<timestep>: <event>
to the end of the file; see example/text_rules.bdi for a simple example.
