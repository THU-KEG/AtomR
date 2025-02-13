# BlendQA Data Construction Plan

Total number of entries: 445

#### Knowledge Sources

- KG: Wikidata large.json from KoPL engine service
- Text: Wikipedia (based on NaturalQuestions)
- Web: Google SERPAPI search service

#### General Data Construction Strategy

- We use *gpt-4o-2024-08-06* as the LLM to aid dataset construction. The general construction process is to generate two sub-questions `sub-q1` and `sub-q2` from two different knowledge sources that share a common bridging entity, and then merge them together to form a cohesive question. 

#### Meaning of Tags

- `sub_q1`: the inner sub-question, describing the bridging entity
- `sub_q2`: the outer sub-question, whose answer is also the answer to the whole question
- `sub_source`: the source from which the sub-question is constructed

#### Question Type

There are three types of questions: KG-Text, KG-Web, Text-Web.

- KG-Text (X+1 hop, 163 entries): sample a NQ question as `sub-q1` **(X hops)**; use the topic entity of `sub-q1` as the bridging entity, and sample a relation from the KG as `sub-q2` **(1 hop)**.

- KG-Web (X+1 hop, 132 entries): 

    - Type 1 (KG2Web): sample an entity and its relative triples from KB as `sub-q1` **(X hops)**; search the bridging entity for relevant news and ask the LLM to generate `sub-q2` **(1 hop)**.

    - Type 2 (Web2KG): collect news from the web, let the LLM extract an entity and ask a question about it as `sub-q1` **(1 hop)**; sample relative triples from the KG as `sub-q2` **(X hops)**.

- Web-Text (X+1-hop, 150 entries)
    - Type 1 (Web2Text): sample a NQ question as `sub-q1` **(X hops)**; collect general webpages about `sub-q1`'s topic entity, and use the LLM to generate a unique description tag (i.e. "Neil Armstrong" - "first man to walk on the moon") as `sub-q2` **(1 hop)**.
    - Type 2 (Text2Web): sample a NQ question as `sub-q1` **(X hops)**; collect news about `sub-q1`'s topic entity, and use the LLM to ask a question based on the news. **(1 hop)**

