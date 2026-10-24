# Document layers

How a statement's force is marked, and which statements belong in this
repository at all.

Two independent questions decide where a sentence goes. Answer both.

1. **Force.** Is the sentence a requirement, a recommendation, a permission, or
   an explanation? See [Requirements language](#requirements-language) and
   [Normative and informative](#normative-and-informative).
2. **Kind.** Is the sentence documentation, or is it the record of how a
   decision was reached? See [Documentation and provenance](#documentation-and-provenance).

The second question is the one that gets answered wrong. A true, well written,
useful paragraph can still belong in a different repository.

## Requirements language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, MAY and OPTIONAL in this repository's documents are to be
interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14),
when, and only when, they appear in all capitals.

Lowercase "must" and "should" carry no such force.

[RFC 7322] section 4.8.2 requires that a document using this interpretation
cite RFC 2119 and carry it as a normative reference, and that the section doing
so appear at or after the introduction. That is why this section is here and
why [BCP 14] is listed below as normative rather than informative.

A document MAY decline the interpretation, provided it says so. [RFC 7322]
section 3 is itself an example: it states that it does not use RFC 2119
terminology, and defines its own lowercase "must" and "should" instead. What is
not permitted is using the capitals without saying which reading applies.

## Normative and informative

**Normative** text states what a conforming reader does. It uses a BCP 14
keyword, and it is testable: a reader can say whether a given commit, document
or run satisfies it.

**Informative** text helps a reader apply a normative statement. It explains a
mechanism, gives an example, or names a consequence. It creates no obligation.

The terms are borrowed from [RFC 7322] section 4.8.6, which applies them to
**references**: normative references are "essential to implementing or
understanding the content", informative references "provide additional
information". This repository applies the same split to prose as well, which is
an extension of the cited definition rather than the definition itself.

A document MAY contain both. A normative statement MUST be phrased so that
removing every informative sentence around it leaves the requirement intact.

### The mechanism test

Informative text in this repository states a **present-tense mechanism**: the
constraint that makes the requirement necessary. It does not narrate.

| Allowed | Not allowed |
|---|---|
| A GitHub action runs with the workflow's token; a package invoked in a step does not. | The action was rejected after the third time this came up. |
| A pushed tag cannot be re-signed without moving it. | Signing was added once the key existed. |
| `reflow-md`'s fixtures are the input and expected output of its own test. | A bulk fix edited them and broke the test. |

Both columns are true. The right column belongs in provenance, because it is
about the project's history rather than about the reader's task.

## Documentation and provenance

**Documentation** is written for a reader with a task. It describes the system
as it is now, in present tense.

**Provenance** is the record of how the system came to be: which options were
weighed, what was tried, what failed, when a rule changed and why, who raised
it. It is written for whoever maintains the system later.

Both are worth keeping. They MUST NOT share a file.

- Documentation lives in this repository.
- Provenance lives outside it, in the operator's working notes.

### What marks a sentence as provenance

Any one of these is sufficient:

- A date that is not itself data. A release date in `CHANGELOG.md` and a
  "checked" date in a status table are data. "Stated 2026-09-18" is provenance.
- A prior state of the document or the system: "this said eleven", "used to
  sit in", "was first stated as", "went from".
- An event: something was tried, broke, was found, was re-argued, was nearly
  missed.
- A first-person narrator, or an actor at all. Documentation has no protagonist.
- A justification of the document's own editorial choices, such as noting that
  something is being stated rather than hidden.

### Where provenance goes instead

Removed passages are appended to the operator's provenance notes with the
source path, the text removed, and what replaced it. Nothing is deleted in the
course of this separation: a passage that is worth removing from a public
document is usually worth keeping somewhere.

## Exceptions

Five kinds of dated or historical statement are documentation, not provenance,
and MUST be kept:

1. **`CHANGELOG.md`**, whose entire subject is what changed and when.
2. **A status document's measurement dates.** "Verified on <date>" tells a
   reader how stale the claim is, which is what the reader needs.
3. **A citation's date or version.** Standards are versioned and a reader needs
   to know which version was read.
4. **A stated limitation.** "This check covers sixteen of eighteen rules" and
   "this repository does not claim conformance" are current facts about the
   system and are load bearing. They are not archaeology, and removing them
   would make a document overclaim.
5. **A reflection entry** in `docs/reflections/`. An entry is a bounded record
   about one documentation row, not free narrative, and its format is fixed:
   - It MUST be one file, named `NNN-short-slug.md`, where `NNN` is a three
     digit number assigned in filing order. A number MUST NOT be reused.
   - It MUST carry exactly these fields, in this order:
     - **Row**: the file and row it reflects on, at a pinned version: a
       release tag or a full commit hash.
     - **Records**: what that row records at the pinned version, restated
       from the row. It MAY include a prior state or a date only where the
       row itself records it.
     - **Lesson**: one sentence, shaped as a rule. The lesson MAY generalise
       from the row and MUST NOT contradict it. It is informative and MUST
       NOT use a BCP 14 keyword.
     - **Supersedes**: the number of the entry it replaces, or "none".
     - **Filed**: the date the entry was filed.
   - It MUST NOT hold session residue or a person's name, and outside the
     **Lesson**, **Supersedes** and **Filed** fields it MUST NOT hold any
     statement the cited row does not support at the pinned version.
     **Supersedes** and **Filed** state an entry number and a filing date,
     which no row records. A named outside system MAY appear where the cited
     row names it.
   - Row support is judged against the pinned version, not against the row
     as it reads later. The entry is a dated citation, and a later change to
     the row does not make it false.
   - It MUST NOT be edited after filing. A correction is a new entry whose
     **Supersedes** field names the entry it replaces; the replaced entry stays
     as filed.
   - A filed entry MAY be reformatted where no word changes. Line wrapping
     and whitespace MAY change for any reason. Markup MAY change only where a
     new gate requires it, and a markup change MUST NOT change what a line
     means. A change to any word still needs a superseding entry.
   - A filed entry is a record dated by its **Filed** field, not
     documentation of the current state. The present tense rule in
     [Documentation and provenance](#documentation-and-provenance) does not
     apply to it.

## How this is checked

`scripts/mdlint.py` checks document **structure** and cannot check any of the
above. The separation is a review obligation, not a gate.

A contributor SHOULD read a changed document once with a single question: does
any sentence here describe this project's past rather than its present? A
reviewer MUST reject a document that mixes the layers, even where every
sentence in it is accurate.

Claiming a mechanical check for this would be worse than having none, because a
clean result from a check that cannot see the defect stops the search.

## References

Cited by tag. Full entries, with the normative and informative split, are in
[the references and prior work list](../references.md).

- **[BCP 14]** normative. Cited as [RFC 7322] section 4.8.2 requires.
- **[RFC 7322]** informative. Source of the conventions above.
- **[GFM]** normative. The dialect these documents render as.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
