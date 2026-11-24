# Method card · Verbs, then the Crew (range prompting)

**Source:** Felix Rieseberg, *How to be more ambitious: A tutorial for humans with models* (13 Oct 2026), section *Range*. The verbs trick is credited to *The Art of Innovation* (Tom Kelley with Jonathan Littman). Card written by grok-bot from the saved post and the Short. Every step points to a saved line in `quotes-sources-StbUAJvivDc.md`.

## When to use it
- The deliverable has a **noun name** (deck, report, landing page, plan) and you would otherwise get a template-shaped noun back.
- The stakes justify extra perspectives (a review, a launch, a pitch, a decision paper).
- You can run several agents or threads (subagents, agent teams). Without them, run the roles one after another.
- **Not** for quick tasks where speed is the only goal. Felix's *Speed* type needs no crew.

## Steps
1. **Write the verbs.** Replace the noun with what it must *do* to its audience: who believes what, decides what, by when.
   *Post:* a quarterly review isn't a deck, it's getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes.
2. **Raise the stakes.** Say the result must be amazing (Felix: *otherwise aliens will blow up Earth*) and ask what team humanity would assemble.
3. **Name the crew in three groups:** *production* (analyst, journalist, editor), *presentation* (motion and audio designer), and *red team* (short seller, forensic accountant). Add fields the verbs suggest.
4. **Give each member a method, not a voice.** Have Claude *do* what a short seller does to research a position, never *write like* one. Role-play makes the transcript weirder without improving the result.
5. **Run them in parallel (subagents), then merge.** The red team attacks the merged draft, and the production crew fixes what it finds.
6. **Check with an outside judge** (from the post's Depth section): don't let the model grade itself.

## Worked example (Acme quarterly business review, from the post's own scenario)
| Step | Output |
|---|---|
| Verbs | Get 6 busy execs to believe *churn rose because onboarding broke in week 2*, and to decide on 2 fixes under uncertainty, in 30 minutes. |
| Stakes | It must be the best QBR they have seen. |
| Production | **Analyst:** cohort churn by signup week, from raw events. **Journalist:** find the one-sentence story and the customer quote. **Editor:** cut to 7 slides and one decision slide. |
| Presentation | **Motion/audio designer:** one animated cohort chart and a 20-second voice-over for the async version. |
| Red team | **Short seller:** builds the case that the churn story is wrong (seasonality? pricing?). **Forensic accountant:** reconciles the revenue numbers to the ledger and flags any that don't tie out. |
| Merge | A draft that survived the red team, with open risks listed. |

## Prompt template (paste into any model)
```
I need: <NOUN, e.g. "a QBR deck">.
1) Rewrite that noun as verbs: who must believe / decide / do what, under what constraint, by when.
2) Assume it has to be the best one ever made. List the crew of fields you would assemble:
   production (e.g. analyst, journalist, editor), presentation (e.g. motion and audio designer),
   red team (e.g. short seller, forensic accountant), plus any field the verbs suggest.
3) For each crew member, state the METHOD they would apply and the raw material they need
   (do what they do; do not imitate how they write or talk).
4) Run each member's method on <MATERIAL> (in parallel if you can use subagents), then merge.
5) Let the red team attack the merged draft; fix or list what survives.
6) Tell me what outside check (not you) would show the result is right.
```

## Limits
- The post is Felix's personal advice on his own site, not Anthropic guidance. He says the advice is not model-specific.
- The worked example's numbers and roles are illustrative (ours). Only the role names and the verbs line come from the post.
