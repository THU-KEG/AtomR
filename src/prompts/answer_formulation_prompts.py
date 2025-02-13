##############################################
### Prompts for Knowledge Source Selection ###
##############################################

def format_knowledge_source_selection_prompt(question, available_knowledge_sources):
    prompt = f"""Following the examples below, select which knowledge source(s) is the best to help answer the question "{question}". You are allowed to select multiple sources. 
You have {len(available_knowledge_sources)} available sources: {available_knowledge_sources}
Possible knowledge sources: 
1. Wikipedia: the world's largest world knowledge encyclopedia, retrieves Wikipedia passages regarding the search question
2. Google: the world's top web search engine, retrieves web articles regarding the search question
3. Wikidata: the world's largest Knowledge Base, retrieves world knowledge in structured triples form, i.e. (head_entity, relation, tail_entity), or (head_entity, attribute, attribute_value)
When the provided question requires general attributal or relational knowledge such as names, dates, location, population, works, plots, or social relationships, you should consult all three knowledge sources: Wikipedia, Google, Wikidata.
When the provided question requires entity disambiguation or explanations, such as "Who is", "What is", or "How to" questions, you should consult both Wikipedia and Google.
When the question asks about maximum or minimum entities, such as the "longest" or "largest", consult both Wikidata and Google.
When the provided question requires highly timely knowledge, such as asking about news, recent events, financial statistics, or a historical product's information, you should only consult Google.
When you are unsure what knowledge sources to select, select all three knowledge sources.
Strictly follow the answer format of the examples below.
Examples.
Q: Who is Bill Gates?
A: Wikipedia, Google
Q: Who is the spouse of Barack Obama?
A: Wikipedia, Google, Wikidata
Q: What was the magnitude of the earthquake that hit Sulawesi on September 1, 2024?
A: Google
Q: What is the movie "Titanic" about?
A: Wikipedia, Google
Q: What is the area of the Tokyo Imperial Palace?
A: Wikipedia, Wikidata, Google
Q: How many games did Brooklyn Nets win in 2022?
A: Google
Q: What did the nashville sound bring to country music?
A: Wikipedia, Google
Q: What was the low price of meta stock on feb 14 2024?
A: Google
Q: What is the longest film produced by Disney?
A: Wikidata, Google
Q: How much did iPhone 4 cost when it came out?
A: Google
Q: What is the economic crisis in Kuhle Wampe (German film)?
A: Wikipedia, Google, Wikidata
Q: What is an 1984 novel by Iain Banks about a psychopathic teenager on a Scottish island?
A: Wikipedia, Google, Wikidata

Your question.
Q: {question}
A: """
    
    return prompt


#############################
### Prompt for direct RAG ###
#############################


def format_direct_answer_prompt_hotpotqa(question):
    prompt = f"""Answer the following multi-hop question "{question}". Formulate your final answer with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Question: What is the length of the river into which Pack Creek runs after it goes through the Spanish Valley?
Answer: Pack Creek, after flowing through the Spanish Valley in Utah, eventually empties into the Colorado River. The Colorado River is approximately 1,450 miles (2,334 kilometers) long, running from the Rocky Mountains in Colorado to the Gulf of California. So the answer is: (1) Paraphrase Answer: The length of the river into which Pack Creek runs after it goes through the Spanish Valley, the Colorado River, is approximately 1,450 miles; (2) Answer List: ["1,450 miles"]

Question: Are both Leycesteria and Anigozanthos native to Australia?
Answer: No, both Leycesteria and Anigozanthos are not native to Australia. Anigozanthos, commonly known as kangaroo paw, is native to Australia, specifically to the southwestern regions of the country. Leycesteria, commonly known as Himalayan honeysuckle or pheasant berry, is native to regions of Asia, particularly the Himalayas and western China. So the answer is: (1) Paraphrase Answer: Leycesteria and Anigozanthos are not both native to Australia; only Anigozanthos is native to Australia, while Leycesteria is native to Asia; (2) Answer List: ["No"]

Question: Which album did the band Kraftwerk release after their successful album which reached number 25 on the US \"Billboard\" Hot 100 chart?
Answer: The band Kraftwerk had their most notable success on the US Billboard Hot 100 chart with the song "Autobahn", which reached number 25 in 1975. The album "Autobahn" was released in 1974. The album Kraftwerk released after Autobahn was "Radio-Activity", which came out in 1975. So the answer is: (1) Paraphrase Answer: The album Kraftwerk released after their successful album which reached number 25 on the US Billboard Hot 100 chart was "Radio-Activity"; (2) Answer List: ["Radio-Activity"]

Question: Which author was a dentist, Zane Grey or Bhabananda Deka?
Answer: The author who was a dentist is Zane Grey. Before becoming a famous author of Western novels, Zane Grey practiced as a dentist, having earned a degree in dentistry from the University of Pennsylvania. Bhabananda Deka, on the other hand, was an Indian writer and scholar, known for his contributions to Assamese literature and linguistics, but he was not a dentist. So the answer is: (1) Paraphrase Answer: The author who was a dentist is Zane Grey; (2) Answer List: ["Zane Grey"]

Your Question.
Question: {question}
Answer: """
    
    return prompt


def format_direct_answer_prompt_2wiki(question):
    prompt = f"""Answer the following multi-hop question "{question}". Formulate your final answer with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Question: Who is Elizabeth Stuart, Countess Of Lennox's mother-in-law?
Answer: Elizabeth Stuart, Countess of Lennox, was married to Charles Stuart, 1st Earl of Lennox. Charles Stuart's mother was Margaret Douglas, making her Elizabeth Stuart’s mother-in-law. So the answer is: (1) Paraphrase Answer: Elizabeth Stuart, Countess of Lennox's mother-in-law is Margaret Douglas; (2) Answer List: ["Margaret Douglas"]

Question: Which film was released earlier, The Apocalypse Code or Just Imagine?
Answer: The film Just Imagine was released in 1930, while The Apocalypse Code (original title: "Kod apokalipsisa") was released in 2007. So, Just Imagine was released earlier. So the answer is: (1) Paraphrase Answer: Just Imagine was released earlier than The Apocalypse Code; (2) Answer List: ["Just Imagine"]

Question: When was Ludwig Gruno Of Hesse-Homburg's father born?
Answer: Ludwig Gruno of Hesse-Homburg's father was Frederick III, Landgrave of Hesse-Homburg. Frederick III, Landgrave of Hesse-Homburg was born on 19 May 1673. So the answer is: (1) Paraphrase Answer: Ludwig Gruno of Hesse-Homburg's father was born on 19 May 1673; (2) Answer List: ["19 May 1673"]

Question: Are both Chak 26/11-L, Chichawatni and Chah-E Ali Kapari located in the same country?
Answer: Yes, both Chak 26/11-L, Chichawatni and Chah-E Ali Kapari are located in Pakistan. Chak 26/11-L is a village near Chichawatni, which is in the Sahiwal District of the Punjab province of Pakistan. Chah-E Ali Kapari is also a location in Pakistan, specifically in the province of Balochistan. So the answer is: (1) Paraphrase Answer: Yes, Chak 26/11-L, Chichawatni and Chah-E Ali Kapari are located in the same country, Pakistan; (2) Answer List: ["yes"]

Question: Which film has the director born later, La Carapate or Rodeo Rhythm?
Answer: La Carapate (1978) was directed by Gérard Oury, who was born on April 29, 1919. Rodeo Rhythm (1942) was directed by Jean Yarbrough, who was born earlier, on July 22, 1901. Since Gérard Oury was born later, in 1919, compared to Jean Yarbrough in 1901, the director of La Carapate was born later. So the answer is: (1) Paraphrase Answer: The director of La Carapate was born later than the director of Rodeo Rhythm; (2) Answer List: ["La Carapate"]

Your Question.
Question: {question}
Answer: """
    
    return prompt


def format_direct_answer_prompt_musique(question):
    prompt = f"""Answer the following multi-hop question "{question}". Formulate your final answer with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Question: Who is the spouse of the actor who plays Paul in Breakfast at Tiffany's?
Answer: The actor who plays Paul Varjak in Breakfast at Tiffany's is George Peppard. George Peppard married five times, and his spouses include: 1. Helen Davies (1954–1965), 2. Elizabeth Ashley (1966–1972), 3. Sherry Boucher (1975–1979), 4. Alexis Adams (1984–1986), and 5. Laura Taylor (1992–1994, until his death). So the answer is: (1) Paraphrase Aswer: The spouse of the actor who plays Paul in Breakfast at Tiffany's is Helen Davies, Elizabeth Ashley, Sherry Boucher, Alexis Adams, and Laura Taylor; (2) Answer List: ["Helen Davies", "Elizabeth Ashley", "Sherry Boucher", "Alexis Adams", "Laura Taylor"]

Question: When was the last time the team that Arthur James was a member of beat the 1894-95 FA cup winner?
Answer: Arthur James was a member of the Birmingham City football team. The team that won the FA Cup in the 1894-95 season was Aston Villa. The last time the Birmingham City football team beat Aston Villa was 1 December 2010. So the answer is: (1) Paraphrase Answer: The last time the team that Arthur James was a member of, Birmingham City, beat the 1894-95 FA Cup winner, Aston Villa, was on 1 December 2010; (2) Answer List: ["1 December 2010"]

Question: Who was the father of the person who issued the Tamworth manifesto?
Answer: The Tamworth Manifesto was issued by Sir Robert Peel in 1834, which is considered a foundational document of the modern Conservative Party in the United Kingdom. Sir Robert Peel's father was Sir Robert Peel, 1st Baronet (1750–1830). So the answer is: (1) Paraphrase Answer: The father of the person who issued the Tamworth Manifesto was Sir Robert Peel, 1st Baronet; (2) Answer List: ["Sir Robert Peel, 1st Baronet"]

Question: In The Godfather, who does the producer of Mistress play?
Answer: The producer of the film Mistress (1992) is Robert De Niro. Robert De Niro played Vito Corleone in "The Godfather". So the answer is: (1) Paraphrase Answer: In The Godfather, the producer of Mistress, Robert De Niro, plays Vito Corleone; (2) Answer List: ["Vito Corleone"]

Your Question.
Question: {question}
Answer: """
    
    return prompt


def format_direct_answer_prompt_crag(question):
    prompt = f"""Answer the following question "{question}". Formulate your final answer with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Question: who was the 2019 nfl mvp?
Answer: The 2019 NFL MVP was Lamar Jackson, the quarterback of the Baltimore Ravens. So the answer is: (1) Paraphrase Answer: the 2019 NFL MVP was Lamar Jackson; (2) Answer List: ["Lamar Jackson"]

Question: what album did kings of leon release in 2013, which included the songs \"wait for me\" and \"family tree\"?
Answer: In 2013, Kings of Leon released the album Mechanical Bull, which included the songs "Wait for Me" and "Family Tree". So the answer is: (1) Paraphrase Answer: the album that Kings of Leon released in 2013 which included the songs \"wait for me\" and \"family tree\" is Mechanical Bull; (2) Answer List: ["Mechanical Bull"]

Question: is chris evans most famous for iron man role?
Answer: No, Chris Evans is most famous for portraying Captain America (Steve Rogers) in the Marvel Cinematic Universe, not for any role in Iron Man. So the answer is: (1) Paraphrase Answer: No, Chris Evans is not most famous for ironman role; (2) Answer List: ["No"]

Question: what was the total value of all exchange-traded funds (etfs) in the united states in 2020?
Answer: As of 2020, the total value of all exchange-traded funds (ETFs) in the United States reached approximately $5.4 trillion in assets under management (AUM). So the answer is: (1) Paraphrase Answer: the total value of all exchange-traded funds (etfs) in the united states in 2020 is approximately $5.4 trillion; (2) Answer List: ["$5.4 trillion"]

Your Question.
Question: {question}
Answer: """
    
    return prompt


def format_direct_answer_prompt_blendqa(question):
    prompt = f"""Answer the following question "{question}". Formulate your final answer with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Question: When did the person after whom Nehru Zoological Park is named first visit the US?
Answer: Nehru Zoological Park is named after Jawaharlal Nehru, the first Prime Minister of India. Nehru first visited the United States in October 1949. So the answer is: (1) Paraphrase Answer: The person after whom Nehru Zoological Park is named first visit the US in October 1949; (2) Answer List: ["October 1949"]

Question: Where do I go to get the financial product associated with the industry of RPM Mortgage, Inc.?
Answer: RPM Mortgage, Inc. is associated with the mortgage lending and home financing industry. You can typically get a mortgage loan at a financial institution, such as a bank, credit union or building society. So the answer is: (1) Paraphrase Answer: You can get the financial product associated with the industry of RPM Mortgage, Inc., mortgage loans, at a financial institution, such as a bank, credit union or building society; (2) Answer List: ["at a financial institution, such as a bank, credit union or building society"]

Question: How many people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born on December 21, 2023?
Answer: On December 21, 2023, a mass shooting occurred at Charles University in Prague, Czech Republic. This tragic event resulted in the deaths of 14 people. So the answer is: (1) Paraphrase Answer: 14 people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born on December 21, 2023; (2) Answer List: ["14"]

Your Question.
Question: {question}
Answer: """
    
    return prompt


#############################
### Prompt for direct RAG ###
#############################

def format_direct_rag_prompt_hotpotqa(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia. If the provided information is not enough to answer the question, answer based on your own knowledge. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] BOAC Flight 911 (Speedbird 911) was a round-the-world flight operated by British Overseas Airways Corporation that crashed as a result of an encounter with severe clear-air turbulence near Mount Fuji in Japan on 5 March 1966.  The Boeing 707-436 on this flight was commanded by Captain Bernard Dobson, 45, from Dorset, an experienced 707 pilot who had been flying these aircraft since November 1960.
Question: What is the plane type used for BOAC Flight 911?
Answer: The passage indicates that "The Boeing 707-436 on this flight was commanded by Captain Bernard Dobson", so the plane type used for the flight should be Boeing 707-436. So the answer is: (1) Paraphrase Answer: The plane type used for BOAC Flight 911 is Boeing 707-436; (2) Answer List: ["Boeing 707-436"]
    
Retrieved Knowledge: 
Wikipedia Passages: [1] Coke Kahani (Urdu: کوک کہانی\u200e ) is a 2012 Pakistani comedy drama sitcom directed by Mehreen Jabbar broadcasting on Broadcast syndication.  Sitcom is written by Syed Mohammad Ahmed and Yasir Rana, starring Sonia Rehman, Faisal Rehman, Syra Yousuf, Syed Mohammad Ahmed, Yasir Hussain, Ahmed Zeb, Shamim Hilali.  Sitcom was first aired on 3 November 2012.
Question: Who helped write for Coke Kahani?
Answer: The passage indicates that Coke Kahani is "written by Syed Mohammad Ahmed and Yasir Rana", so Syed Mohammad Ahmed and Yasir Rana are writers of the drama. Additionally, my own knowledge suggests that the actor Yasir Hussain also helped write for Coke Kahani. So the answer is: (1) Paraphrase Answer: "Syed Mohammad Ahmed", "Yasir Rana", and "Yasir Hussain" helped write for Coke Kahani; (2) Answer List: ["Syed Mohammad Ahmed", "Yasir Rana", "Yasir Hussain"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Forbidden Quest () is a 2006 South Korean period drama film about a scholar during the Joseon Dynasty who begins to write erotic novels, and becomes the lover of the King's favorite concubine. ... [2] The Forbidden Quest is a 1993 mockumentary written and directed by Peter Delpeut. ... [3] "Forbidden Paradise 3: The Quest for Atlantis is the third album in the ""Forbidden Paradise"" series.  It is the first album in the series to be mixed by well-known trance DJ/producer Tiësto.  As with the rest of the Forbidden Paradise series, the album is a live turntable mix.
Question: Who was Forbidden Quest about?
Answer: Wikipedia passage [1] describes the drama film Forbidden Quest being "about a scholar during the Joseon Dynasty who begins to write erotic novels", so the film should be about a scholar. So the answer is: (1) Paraphrase Answer: Forbidden Quest was about a scholar; (2) Answer List: ["a scholar"]
 
Retrieved Knowledge: 
Wikipedia Passages: [1] Lady Mary Fox (née FitzClarence; 19 December 1798 – 13 July 1864) was an illegitimate daughter of King William IV of the United Kingdom by his mistress Dorothea Jordan.  In later life she became a writer. ... [2] Elizabeth Hay, Countess of Erroll (17 January 1801 – 16 January 1856; born Elizabeth FitzClarence) was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan.  She married William Hay, 18th Earl of Erroll, and became Countess of Erroll on 4 December 1820 at age 19.  Due to Hay's parentage, William Hay became Lord Steward of the Household.  Elizabeth and William Hay married at St George's, Hanover Square.  Hay is pictured in a FitzClarence family portrait in House of Dun and kept a stone thrown at her father William IV and the gloves he wore on opening his first Parliament as mementos.  She died in Edinburgh, Scotland. ... [3] William IV of Toulouse ( 1040 – 1094) was Count of Toulouse, Margrave of Provence, and Duke of Narbonne from 1061 to 1094.  He succeeded his father Pons of Toulouse upon his death in 1061.  His mother was Almodis de la Marche, but she was kidnapped by and subsequently married to Ramon Berenguer I, Count of Barcelona when William was a boy.  He was married to Emma of Mortain (daughter of Robert, Count of Mortain and a niece of William of Normandy), who gave him one daughter, Philippa.  He also had an illegitimate son, William-Jordan, with his half-sister Adelaide.
Question: Who was the illegitimate daughter of King William IV?
Answer: Based on the provide passages, the persons described by passages [1] and [2] are illegitimate daughters of King William IV, given Lady Mary Fox "was an illegitimate daughter of King William IV" and Elizabeth Hay, Countess of Erroll "was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan". So the answer is: (1) Paraphrase Answer: The illigimate daughters of King WIlliam IV are "Lady Mary Fox" and "Elizabeth Hay, Countless of Erroll"; (2) Answer List: ["Lady Mary Fox", "Elizabeth Hay, Countess of Erroll"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Horrible Bosses 2 | "Horrible Bosses 2 is a 2014 American comedy film directed by Sean Anders and written by Anders and John Morris.  A sequel to 2011\'s ""Horrible Bosses"", the film stars Jason Bateman, Charlie Day, Jason Sudeikis, Jennifer Aniston, Jamie Foxx, Chris Pine, and Christoph Waltz.  It was released on November 26, 2014 by Warner Bros.  Pictures.  The film grossed $107.7 million worldwide." ... [2] Sean Anders | Sean Anders is an American film director, actor, screenwriter, and producer. ... [3] Daddy\'s Home 2 | "Daddy\'s Home 2 is an upcoming American comedy film directed by Sean Anders and written by Anders and John Morris.  It stars Will Ferrell, Mark Wahlberg, Linda Cardellini, John Cena, John Lithgow and Mel Gibson.  It is a sequel to the 2015 film ""Daddy\'s Home"".  Unlike its predecessor, this film will not feature the involvement of Red Granite Pictures.
Question: What is the name of the movie that stars Katrina Bowden and was directed by Sean Anders?
Answer: The Wikipedia passages suggest that movies directed by Sean Anders include "Horrible Bosses 2" and "Daddy's Home 2", but neither star Katrina Bowden. However, based on my own knowledge, the movie "Sex Drive" is both directed by Sean Anders and starring Sean Anders. So the answer is: (1) Paraphrase Answer: The movie "Sex Drive" stars Katrina Bowden and was directed by Sean Anders; (2) Answer List: ["Sex Drive"]

Your Question.
Supporting knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


# deleted: When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". 
def format_direct_rag_prompt_2wiki(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia. If the provided information is not enough to answer the question, answer based on your own knowledge. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Walkover (film) | Walkover (Walkower) is a 1965 Polish drama film directed by Jerzy Skolimowski. It is the second feature film directed by Skolimowski, and again features his alter ego, Andrzej Leszczyc, whose story is continued from the film Rysopis. ... [2] Walkover (film) | Cast: Aleksandra Zawieruszanka as Teresa Karczewska ; Jerzy Skolimowski as Andrzej Leszczyc ; Krzysztof Chamiec as a chief of the factory ; Elżbieta Czyżewska as a girl on the station ; Andrzej Herder as Marian Pawlak ; Stanisław Marian Kamiński ; Andrzej Jurczak ; Franciszek Pieczka
Question: What is the film Walkover (Film)?
Answer: The passages indicate that Walkover refers to Walkover (film), a 1965 Polish drama film directed by Jerzy Skolimowski. So the answer is: (1) Paraphrase Answer: The film Walkover refers to Walkover (film), a 1965 Polish drama film directed by Jerzy Skolimowski; (2) Answer List: ["Walkover (film)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Will Not End Here | Will Not End Here (Nije kraj) is a 2008 Croatian / Serbian co-production directed by Vinko Brešan. It is based on a play by Mate Matišić.
Question: Who is the director of Will Not End Here?
Answer: The passage indicates that "Will Not End Here" is "directed by Vinko Brešan", so the director of Will Not End Here is Vinko Brešan. So the answer is: (1) Paraphrase Answer: The director of Will Not End Here is Vinko Brešan; (2) Answer List: ["Vinko Brešan"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Canardo (rapper) | Hakim Mouhid (born 22 September 1984 in Trappes, Yvelines), better known by his stage name Canardo, is a French rapper, singer, songwriter and music producer. After working with label "Banlieue Sale Music" since 2007, in 2011, he founded his own label "Henijai Music". He is the brother of fellow French rapper La Fouine
Question: Who is Canardo (Rapper)?
Answer: The passage indicates that Canardo refers to Canardo (rapper), a French rapper, singer, songwriter and music producer. So the answer is: (1) Paraphrase Answer: Canardo refers to Canardo (rapper), a French rapper, singer, songwriter and music producer; (2) Answer List: ["Canardo (rapper)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Passion (Utada Hikaru song) | Cultural impact: lowest selling single until her 2008 double A-side release "Stay Gold" / "Heart Station". In early 2013, an announcement confirmed the development of the third instalment of the Kingdom Hearts console game. In October that year, Utada\'s father, Teruzane Utada, was asked on Twitter about their contribution towards the third installment, to which Teruzane replied, "Yes." The reply prompted a large response through social media in Japan and America ... [2] Passion (Utada Hikaru song) | Composition:  and eventually introduces a "new world". A member at Channel-Ai stated that the theme encompassed the parent album Ultra Blue, but highlighted on "hope" more than "sadness". Vibe\'s Mio Yamada said that the lyrics, "expressed weakness and strength simultaneously," and that the material was more mature than Utada\'s previous work. Executive producers for Kingdom Hearts and head composer Yoko Shimomura said that the track needed to be more dramatic for the remaining of the accompanying score.
Question: Who is the mother of the performer of song Passion (Utada Hikaru Song)?
Answer: While the passage does not directly provide "the mother of the performer of song Passion (Utada Hikaru Song)", it indicates that the performer of song Passion (Utada Hikaru Song) is Utada Hikaru, and my own knowledge suggests that the mother of Utada Hikaru is Keiko Fuji. So the answer is: (1) Paraphrase Answer: The mother of the performer of song Passion (Utada Hikaru Song) is Keiko Fuji; (2) Answer List: ["Keiko Fuji"]

Your Question.
Supporting knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_direct_rag_prompt_musique(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] The Pizza Man | The Pizza Man (foaled March 25, 2009) is an American Thoroughbred racehorse who won multiple stakes races including the Arlington Million in 2015 and the Northern Dancer Turf Stakes in 2016, becoming the first Illinois-bred horse to win either of these Grade I races. ... [2] Pizza Man | Pizza Man is a 1991 comedy film starring Bill Maher and Annabelle Gurwitch; written and directed by J.F. Lawton who was credited in the film as J.D. Athens. The film received a PG-13 rating by the MPAA.
Question: What is Pizza Man?
Answer: Based on the passages, Pizza Man could refer to two entities: either "The Pizza Man" from passage [1], an American Thoroughbred racehorse, or "Pizza Man" from passage [2], a 1991 comedy film. So the answer is: (1) Paraphrase Answer: Pizza Man could be "The Pizza Man", an American Thoroughbred racehorse, or "Pizza Man", a 1991 comedy film; (2) Answer List: ["The Pizza Man (American Thoroughbred racehorse)", "Pizza Man (1991 comedy film)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Hydrogen | Discovery and use: 1) 2) 3) In 1671, Robert Boyle discovered and described the reaction between iron filings and dilute acids, which results in the production of hydrogen gas. In 1766, Henry Cavendish was the first to recognize hydrogen gas as a discrete substance, by naming the gas from a metal-acid reaction "inflammable air". ... [2] Hydrogen | on metals. In 1766–81, Henry Cavendish was the first to recognize that hydrogen gas was a discrete substance, and that it produces water when burned ... [3] Discovery of the nonmetals | 18th century: H, O, N, (Te), Cl:  Hydrogen: Cavendish, in 1766, was the first to distinguish hydrogen from other gases, although Paracelsus around 1500, Robert Boyle (1670), and Joseph Priestley (?) had observed its production by reacting strong acids with metals
Question: Who first recognized that hydrogen was a discrete substance?
Answer: All three passages indicate that Henry Cavendis was the first to recognize hydrogen as a discrete substance. So the answer is: (1) Paraphrase Answer: Henry Cavendis was the first to recognize hydrogen as a discrete substance; (2) Answer List: ["Henry Cavendis"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Tang Jinhua | Tang Jinhua (born 8 January 1992) is a Chinese retired badminton player who competed at the highest level during the second decade of the 2000s, winning numerous women's doubles and occasional mixed doubles events with a variety of partners. She is a graduate of Hunan University. ... [2] Joseph Tang Yuange | Biography:  Tang was born in Jintang County, Sichuan, on November 17, 1963. From 1984 to 1988 he studied at the Sichuan Catholic Theological and Philosophical College. 
Question: What is the place of birth of Tang Jinhua?
Answer: Passage [1] suggests that Tang Jinhua refers to a Chinese retired badminton playe, but her place of birth is not explicitly mentioned. Nevertheless, my knowledge suggests that Chinese retired badminton player Tang Jinhua was born in Nanjing, Jiangsu, China. So the answer is: (1) Paraphrase Answer: Tang Jinhua was born in Nanjing, Jiangsu, China; (2) Answer List: ["Nanjing, Jiangsu, China"]

Retrieved Knowledge: 
Wikipedia Passages: [1] East India Company | Indian Rebellion and disestablishment:  the company. The British government took over its Indian possessions, its administrative powers and machinery, and its armed forces. The company had already divested itself of its commercial trading assets in India in favour of the UK government in 1833 ... [2] Queen Victoria | Empress:  After the Indian Rebellion of 1857, the British East India Company, which had ruled much of India, was dissolved, and Britain\'s possessions and protectorates on the Indian subcontinent were formally incorporated into the British Empire.
Question: What happened to the assets of the British India Company after it was removed from power?
Answer: Passage [1] indicates that "the British government took over its Indian possessions", and passage [2] indicates that the company's assets were "formally incorporated into the British Empire". So the answer is: (1) Paraphrase Answer: After the British India Company was removed from power, its assets were took over by the British government and formally incoporated into the British Empire; (2) Answer List: ["took over by the British government and formally incoporated into the British Empire"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Yangzhou | Yangzhou, postal romanization Yangchow, is a prefecture-level city in central Jiangsu Province (Suzhong), East China. Sitting on the north bank of the Yangtze, it borders the provincial capital Nanjing to the southwest, Huai'an to the north, Yancheng to the northeast, Taizhou to the east, and Zhenjiang across the river to the south. ... [2] Yang Province | Tribute of Yu account:  The Tribute of Yu records that Yangzhou was located between Huai and the Sea. Kong Anguo (fl. 2nd century BCE) explained in Shangshu Zhuan (尚書傳) that the text meant that Yangzhou was bordered by the Huai River in the north and the South China Sea in the south. ... [3] Yang Prefecture (Jiangsu) | Yangzhou or Yang Prefecture (揚州) was a zhou (prefecture) in imperial China, centering on modern Yangzhou, Jiangsu, China. 
Question: What is the location of Yangzhou, Jiangsu, China?
Answer: Passage [1] indicates that Yangzhou is "a prefecture-level city in central Jiangsu Province (Suzhong)". So the answer is: (1) Paraphrase Answer: Yangzhou is located in central Jiangsu Province (Suzhong); (2) Answer List: ["central Jiangsu Province (Suzhong)"]

Your Question.
Supporting knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt



def format_direct_rag_prompt_crag(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Google, Wikipedia, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Life or Something Like It |  Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek. The film focuses on television reporter Lanie Kerrigan (Angelina Jolie) and her quest to find meaning in her life. The original music score was composed by David Newman.
Google Results: [1] Life or Something Like It | Lanie Kerrigan (Angelina Jolie), a feature reporter at a Seattle television station, leads the ultimate superficial life, even though she thinks she has it all, like a superstar boyfriend, a gorgeous apartment, and a shot at a big network assignment.… MORE [2] Life or Something Like It | Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek. The film focuses on television reporter Lanie Kerrigan ... 
Question: What is the film Life or Something Like It?
Answer: Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek. So the answer is: (1) Paraphrase Answer: Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek; (2) Answer List: ["Life or Something Like It (2022 American romantic comedy-drama film)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Mechanical Bull Tour | Setlist: 1) "Charmer" ; 2) "Rock City" ; 3) "My Party" ; 4) "Temple" ; 5) "On Call" ; 6) "Family Tree" ; 7) "Closer" ; 8) "The Immortals" ; 9) "Back Down South" ; 10) "Wait for Me" ; 11) "Supersoaker" ; 12) "Milk" ; 13) "Pyro" ; 14) "Tonight" ; 15) "Radioactive" ; 16) "The Bucket" ; 17) "Don't Matter" ; 18) "Molly's Chambers" ; 19) "Four Kicks" ; 20) "Be Somebody" ; 21) "Notion" ; 22) "Cold Desert" ; 23) "Use Somebody" ; Encore ; 1) "Crawl" ; 2) "Black Thumbnail" ; 3) "Sex on Fire" ... [2] Mechanical Bull (album) | Promotion:  love and fighting," and a "distant cousin of U2's With or Without You". "Beautiful War" and "Don't Matter" were released as singles exclusively in the United Kingdom on December 9, 2013 and June 16, 2014 respectively. "Family Tree" was sent to US modern rock radio as the album's sixth overall single on June 17, 2014...
Question: Among Mechanical Bull, Come Around Sundown, Because of the Times, which album includes the songs "Wait for Me" and "Family Tree"?
Answer: The album Mechanical Bull includes the songs "Wait for Me" and "Family Tree". So the answer is: (1) Paraphrase Answer: Mechanical Bull includes the songs "Wait for Me" and "Family Tree"; (2) Answer List: ["Mechanical Bull"]

Examples.
Retrieved Knowledge: 
Google Results: [1] $110 million | As of 2023, Chris Evans' net worth today is $110 million. The majority of his net worth is derived from his portrayal of Steve Rogers in the MCU movies. Apart from his earnings from movies, he also has several endorsements from high-end brands such as Hyundai, Gucci, and Jinx which contribute to this net worth. [2] Chris Evans Net Worth | Chris Evans is an American actor and director who has a net worth of $110 million. The majority of his net worth has been earned via his appearances in several ...
Question: What is Chris Evans net worth 2023?
Answer: Chris Evans is net worth $110 million as of 2023. So the answer is: (1) Paraphrase Answer: Chris Evans is net worth $110 million as of 2023; (2) Answer List: ["$110 million"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Hitmixes | Hitmixes is the second extended play (EP) by American singer Lady Gaga, released on August 25, 2009. ... [2] The Fame Monster |  The Fame Monster is a reissue of American singer Lady Gaga's debut studio album, The Fame (2008), and was released on November 18, 2009, through Interscope Records. ... [3] The Cherrytree Sessions (Lady Gaga EP) | Critical reception:  The Cherrytree Sessions was released on February 3, 2009, in the United States and was an import in European nations, including France. ...
Google Results: [1] The Fame Monster, Hitmixes, The Cherrytree Sessions, Attention Deficit [2] Lady Gaga discography | Gaga later released The Fame Monster in November 2009, as a deluxe edition or reissue of The Fame, which was ultimately released also as a standalone EP.
Question: What albums did Lady Gaga release in 2009?
Answer: In 2009, Lady Gaga released The Fame Monster, Hitmixes, The Cherrytree Sessions, and Attention Deficit. So the answer is: (1) Paraphrase Answer: In 2009, Lady Gaga released The Fame Monster, Hitmixes, The Cherrytree Sessions, and Attention Deficit; (2) Answer List: ["The Fame Monster", "Hitmixes", "The Cherrytree Sessions", "Attention Deficit"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Sirius | Sirius is gradually moving closer to the Solar System, so it is expected to slightly increase in brightness over the next 60,000 years. After that time, its distance will begin to increase, and it will become fainter, but it will continue to be the brightest star in the Earth's night sky for approximately the next 210,000 years. Sirius A is about twice as massive as the Sun and has an absolute visual magnitude of +1.42. It is 25 times as luminous as the Sun, but has a significantly lower luminosity than other bright stars such as Canopus or Rigel. The system 
Google Results: [1] Sirius | Facts & Location | Britannica | Sirius, brightest star in the night sky, with apparent visual magnitude −1.46. It is a binary star in the constellation Canis Major. The bright component of the binary is a blue-white star 25.4 times as luminous as the Sun.
Question: How bright is the star Sirius?
Answer: Based on the retrieved knowledge, Sirius is the "brightest star in the Earth's night sky" and is "25 times as luminous as the Sun". So the answer is: (1) Paraphrase Answer: The star Sirius is the brightest star in the Earth's night sky" and is "25 times as luminous as the Sun; (2) Answer List: ["brightest star in the Earth's night sky and 25 times as luminous as the Sun"]

Retrieved Knowledge: 
Wikipedia Passages: [1] List of American exchange-traded funds | This is a table of notable American exchange-traded funds, or ETFs. As of 2020, the number of exchange-traded funds worldwide is over 7600, representing about 7.74 trillion U.S. dollars in assets. The largest ETF, as of April 2021, was the SPDR S&P 500 ETF Trust (nyse arca: SPY), with about $353.4 billion in assets...
Question: What was the total value of all exchange-traded funds (etfs) in the united states in 2020?
Answer: The retrieved knowledge does not mention the total value of ETFs in the United States in 2020, but my own knowledge suggests that as of 2020, the total value of all exchange-traded funds (ETFs) in the United States is approximately $5.4 trillion. So the answer is: (1) Paraphrase Answer: The total value of all exchange-traded funds (etfs) in the united states in 2020 is approximately $5.4 trillion; (2) Answer List: ["$5.4 trillion"]

Retrieved Knowledge: 
Google Results: [1] 2 | Brad Pitt has been married twice—Jennifer Aniston from 2000 to 2005, and Angelina Jolie from 2014 to 2019 (though he and Jolie separated in 2016).
Question: How many times has brad pitt been married?
Answer: Brad Pitt has been married 2 times, with Jennifer Anistton and then Angelina Jolie. So the answer is: (1) Brad Pitt has been married 2 times; (2) Answer List: ["2"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Chris Evans (actor) | 2011–2017: Captain America and directorial debut:  aggregator Rotten Tomatoes gave the film an approval rating of 92% based on more than 350 reviews. The Avengers received an Academy Award nomination for Best Visual Effects and a British Academy Film Award (BAFTA) nomination for Best Special Visual Effects. For his last release of 2012, he played hitman Robert Pronge in the biographical film The Iceman, about the murderer Richard Kuklinski.
Question: Is Chris Evans most famous for iron man role?
Answer: No, Chris Evans is most famous for the role of Captain America, not Ironman. So the answer is: (1) Paraphrase Answer:  No, Chris Evans is most famous for the role of Captain America, not Ironman; (2) Answer List: ["No"]

Your Question.
Supporting knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_direct_rag_prompt_blendqa(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Google, Wikipedia, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Kuhle Wampe | Kuhle Wampe is a 1932 German feature film about unemployment, homelessness and left wing politics in the Weimar Republic produced by Prometheus Film.
Google Results: [1] To Whom Does the World Belong? | Anni Bönike has a badly paid job in a factory ... [2] Kuhle Wampe | Kuhle Wampe is a 1932 German feature film about unemployment, homelessness and left wing politics in the Weimar Republic produced by Prometheus Film. 
Question: What is Kuhle Wampe?
Answer: Kuhle Wampe is a 1932 German feature film. So the answer is: (1) Paraphrase Answer: Kuhle Wampe is a 1932 German feature film; (2) Answer List: ["Kuhle Wampe (German film)"]

Retrieved Knowledge: 
Google Results: [1] Carlos Alcaraz | Carlos Alcaraz (born May 5, 2003, El Palmar, Murcia, Spain) is a Spanish professional tennis player ... [2] Carlos Alcaraz Biography: Childhood, Career and ... | Carlos Alcaraz is a Spanish professional tennis player born on May 5, 2003.
Question: Who is the tennis player born on May 5, 2003?
Answer: The tennis player born on May 5, 2003, is Carlos Alcaraz. So the answer is: (1) Paraphrase Answer: The tennis player born on May 5, 2003, is Carlos Alcaraz; (2) Answer List: ["Carlos Alcaraz"]

Retrieved Knowledge: 
Google Results: [1] an enzyme produced by many organisms and is essential to the complete digestion of whole milk | Lactase (EC 3.2. 1.108) is an enzyme produced by many organisms and is essential to the complete digestion of whole milk. It breaks down the sugar lactose into its component parts, galactose and glucose. [2] LACTASE - Uses, Side Effects, and More | Lactase is an enzyme that breaks down lactose, the sugar in milk. 
Question: What is the enzyme that breaks down lactose into glucose and galactose?
Answer: The enzyme that breaks down lactose into glucose and galactose is lactase. So the answer is: (1) Paraphrase Answer: The enzyme that breaks down lactose into glucose and galactose is lactase; (2) Answer List: ["Lactase"]

Retrieved Knowledge: 
Google Results: [1] US overdoses have fallen sharply in recent months, a ... | A steep drop in deaths from fentanyl is a key factor driving the overall decline. Overdose deaths involving fentanyl and other synthetic ...
Question: What key factor is driving the overall decline in overdose deaths in Puebla?
Answer: The retrieved knowledge indicates that a "key factor driving the overall decline" is "a steep drop in deaths from fentanyl". So the answer is: (1) Paraphrase Answer: a key factor driving the overall decline is a steep drop in deaths from fentanyl; (2) Answer List: ["a steep drop in deaths from fentanyl"]

Retrieved Knowledge: 
Google Results: [1] Cape Verde 2-2 Egypt (Jan 22, 2024) Final Score | Cape Verde's Bryan Teixeira scored a 99th minute equaliser as they held record seven-time champions Egypt to a 2-2 Group B draw at the Africa Cup of Nations. [2] Cape Verde vs. Egypt - Final Score - January 22, 2024 | View the Cape Verde vs. Egypt game played on January 22, 2024. Box score, stats, odds, highlights, play-by-play, social & more.
Question: What was the final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and Cape Verde?
Answer: The final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and Cape Verde, is 2-2. So the answer is: (1) Paraphrase Answer: The final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and Cape Verde, is 2-2; (2) Answer List: ["2-2"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Kuhle Wampe | Kuhle Wampe (full title: Kuhle Wampe, oder: Wem gehört die Welt?, translated in English as Kuhle Wampe or Who Owns the World?, and released in the USA as Whither Germany? by Kinematrade Inc.) is a 1932 German feature film about unemployment, homelessness and left wing politics in the Weimar Republic produced by Prometheus Film. ... [2] Kuhle Wampe | Synopsis: On their return home by train, Anni, Fritz and other workers argue with middle-class, wealthy passengers about the worldwide financial crisis. 
Wikidata Query Results: Great Depression
Question: What is the economic crisis in Kuhle Wampe (German film)?
Answer: The economic crisis depicted in the German film Kuhle Wampe is the Great Depression. So the answer is: (1) Paraphrase Answer: The economic crisis in Kuhle Wampe (German film) is the Great Depression; (2) Answer List: ["Great Depression"]

Retrieved Knowledge: 
Google Results: [1] American hiker found dead on South Africa's Table Mountain | The woman has been identified as a 20-year-old student from North Carolina named Brook Cheuvront. An American woman who went missing while on a hike on Table Mountain in Cape Town, South Africa, has died and her body has been recovered, authorities said on Monday.
Question: Was the body of the missing American hiker found in September 2024 on the Table mountain?
Answer: Yes, based on the retrieved knowledge, an American hiker was found dead on the Table mountain. So the answer is: (1) Paraphrase Answer: Yes, the body of the missing American hiker was found in September 2024 on the Table mountain; (2) Answer List: ["Yes"]

Your Question.
Supporting knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


####################################
### Prompts for Atomic Functions ###
####################################

##### 1. Search

def format_search_prompt_hotpotqa(question, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, Google, or Wikidata, please answer the following entity disambiguation question "{question}". Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) an Answer List that is a clean entity list. You may not answer with an empty entity list: if the provided information is not enough to answer the question, answer based on your own knowledge. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [entity_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Chris Jericho | Christopher Keith Irvine (born November 9, 1970), better known by the ring name Chris Jericho, is a Canadian-American professional wrestler, musician, media personality, actor, author, podcaster, and businessman signed to WWE on the SmackDown brand.
Question: What is Chris Jericho?
Answer: Chris Jericho refers to "Chris Jericho", who is a Canadian-American person. So the answer is: (1) Paraphrase Answer: Chris Jericho refers to "Chris Jericho", a Canadian-American wrestler, musician, and actor; (2) Answer List: ["Chris Jericho"]

Retrieved Knowledge: 
Wikipedia Passages: [1] James Tully (Irish politician) | "James ""Jim"" Tully (18 September 1915 – 20 May 1992) was an Irish trade unionist, politician and Deputy leader of the Labour Party who served as a minister in a series of Fine Gael-Labour Party coalition governments."
Question: Who is James Tully? (politician)
Answer: Based on the Wikipedia passage, James Tully (politician) refers to "James Tully (Irish politician)". So the answer is: (1) Paraphrase Answer: James Tully refers to "James Tully (Irish politician)", an Irish trade unionist and politician; (2) Answer List: ["James Tully (Irish politician)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Packs Branch (Paint Creek) | Packs Branch is a stream in the U.S. state of West Virginia. ... [2] Packwood Creek | Packwood Creek is one of the four main creeks that flow through the city of Visalia and the surrounding communities. ... [3] Pennypack Creek | Pennypack Creek is a 22.6 mi creek in southeastern Pennsylvania in the United States.  It runs southeast through lower Bucks County, eastern Montgomery County and the northeast section of Philadelphia, before emptying into the Delaware River.
Question: What is Pack Creek? (creek)
Answer: Based on the Wikipedia passages and my own knowledge, Pack Creek could be Packs Branch (Paint Creek), Packwood Creek, Pennypack Creek, or the river Pack Creek (Utah). So the answer is: (1) Paraphrase Answer: Pack Creek could be "Packs Branch (Paint Creek)", "Packwood Creek", "Pennypack Creek", or the river "Pack Creek (Utah)"; (2) Answer List: ["Packs Branch (Paint Creek)", "Packwood Creek", "Pennypack Creek", "Pack Creek (Utah)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] San Diego State Aztecs men's soccer | The San Diego State Aztecs men's soccer team is a varsity intercollegiate athletic team of San Diego State University in San Diego, California, United States.  The team is an associate member of the Pac-12 Conference, which is part of the National Collegiate Athletic Association's Division I.  San Diego State's first men's soccer team was fielded in 1968.  The team plays its home games at SDSU Sports Deck in San Diego.  The Aztecs are coached by Lev Kirshner. ... [2] Bristol Aztecs | The Bristol Aztecs are a British American football team based in Bristol, England, at the SGS WISE sports academy of South Gloucestershire and Stroud College, Bristol, which is also the base for a number of other sports teams such as Bristol Academy woman's soccer team. ... [3] San Diego State Aztecs | The San Diego State Aztecs are the athletic teams that represent San Diego State University (SDSU).  The Aztecs currently sponsor six men's and thirteen women's sports at the varsity level.
Question: Who are the Aztecs? (sports team)
Answer: Aztecs (sports team) could refer to either "San Diego State Aztecs men's soccer", "Bristol Aztecs", or "San Diego State Aztecs". So the answer is: (1) Paraphrase Answer: Aztecs (sports team) could refer to either "San Diego State Aztecs men's soccer", "Bristol Aztecs", or "San Diego State Aztecs"; (2) Answer List: ["San Diego State Aztecs men's soccer", "Bristol Aztecs", "San Diego State Aztecs"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_search_prompt_2wiki(question, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, please answer the following entity disambiguation question "{question}". Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) an Answer List that is a clean entity list. You may not answer with an empty entity list: if the provided information is not enough to answer the question, answer based on your own knowledge. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [entity_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Canardo (rapper) | Hakim Mouhid (born 22 September 1984 in Trappes, Yvelines), better known by his stage name Canardo, is a French rapper, singer, songwriter and music producer. After working with label "Banlieue Sale Music" since 2007, in 2011, he founded his own label "Henijai Music". He is the brother of fellow French rapper La Fouine
Question: Who is Canardo (Rapper)?
Answer: The passage indicates that Canardo refers to "Canardo (rapper)", a French rapper with original name Hakim Mouhid and stage name Canardo. So the answer is: (1) Paraphrase Answer: Canardo refers to "Canardo (rapper)", a French rapper, singer, songwriter and music producer; (2) Answer List: ["Canardo (rapper)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Hold on Me (Grinspoon song) | "Hold on Me" is the third single released by Grinspoon from their fourth studio album Thrills, Kills & Sunday Pills. It was released on 21 February 2005 on the Universal Records label. The initial single release included a lapel pin badge under shrink wrap, with 'Hold On Me - Grinspoon EP' themed artwork ... [2] Hold on Me (Grinspoon song) | Reception:  The Australian Music Guide rated "Hold on Me" as the 35th most heard song by an Australian artist in 2005. FasterLouder magazine in March 2005 described the song as being "an inoffensive, nice song. Grinspoon prove that they certainly still have a semblance of ‘it’ but ‘it’ is being translated through safer, more accessible means."
Question: What is the song Hold On Me (Grinspoon)?
Answer: The passages indicate that Hold On Me (Grinspoon) refers to "Hold on Me (Grinspoon song)", a single released by Grinspoon. So the answer is: (1) Paraphrase Answer: Hold On Me (Grinspoon) refers to "Hold on Me (Grinspoon song)"; (2) Answer List: ["Hold on Me (Grinspoon song)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Now Do You Get It Why I'm Crying? | Now Do You Get It Why I'm Crying? (Begrijpt U Nu Waarom Ik Huil?) is a 1969 documentary film by Dutch director Louis van Gasteren. In the late 1960s Van Gasteren was drawn to the work of the Leiden University professor Jan Bastiaans treating traumatized war survivors. ... [2] Louis van Gasteren | Filmography:  min. ; 1964 – Er is telefoon voor u (There's a Phone-call for You) - Documentary about the effects of the telephone in the Netherlands. 46 min. ; 1964 – Jazz and Poetry, 14 min. ; 1965 – Out of My Skull – Early Dutch experimental film, made during a stay as visiting professor at Harvard University. 15 min. ; 1968 – Report from Biafra - Documentary concerning the Biafran War. 50 min. ; ... [3] The Price of Survival | The Price Of Survival (De prijs van overleven) is a 2003 documentary film by Dutch director Louis van Gasteren and a sequel to Now Do You Get It Why I'm Crying? (Begrijpt U Nu Waarom Ik Huil?).
Question: What is the film Begrijpt U Nu Waarom Ik Huil?
Answer: Based on the passages, "Begrijpt U Nu Waarom Ik Huil?" refers to "Now Do You Get It Why I'm Crying?", a 1969 documentary film by Dutch director Louis van Gasteren. So the answer is: (1) Paraphrase Answer: "Begrijpt U Nu Waarom Ik Huil?" refers to "Now Do You Get It Why I'm Crying?", a 1969 documentary film by Dutch director Louis van Gasteren; (2) Answer List: ["Now Do You Get It Why I'm Crying?"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Yesugei | Yesugei Baghatur or Yesükhei (Traditional Mongolian: ; Modern Mongolian: Есүхэй баатар, Yesukhei baatar; ), was a major chief of the Khamag Mongol confederation and the father of Temüjin, later known as Genghis Khan.  ... [2] Genghis Khan (2004 TV series) | Genghis Khan and his family: Ba Sen as Temüjin (Genghis Khan), the founder of the Mongol Empire. ; Ba Sen also portrayed Yesugei, Temüjin's father and the chief of the Borjigin tribe. ... [3] Wolf of the Plains | Plot summary:  The narrative follows the early life of Temujin, the second son of Yesugei, the khan of the Mongolian "Wolves" tribe. Yesugei's first bondsman, Eeluk, assumes control of the tribe. The expectation was that Temujin's family would perish in the unforgiving winter, but Temujin, along with his mother Hoelun, his four brothers Bekter, Khasar, Kachiun, Temüge, and his baby sister Temulun
Question: Who is Yesugei? (father of Temüge)
Answer: Based on the passages, Yesugei who is the father of Temüge refers to "Yesugei", a major chief of the Khamag Mongol confederation. So the answer is: (1) Paraphrase Answer: Yesugei (father of Temüge) refers to "Yesugei", a major chief of the Khamag Mongol confederation; (2) Answer List: ["Yesugei"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_search_prompt_musique(question, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, please answer the following entity disambiguation question "{question}". Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) an Answer List that is a clean entity list. You may not answer with an empty entity list: if the provided information is not enough to answer the question, answer based on your own knowledge. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [entity_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] All That Echoes | All That Echoes is the sixth studio album by American singer-songwriter Josh Groban, produced by Rob Cavallo. The album debuted at number one on the Billboard 200, selling 145,000 copies in its first week.
Question: What is All That Echoes?
Answer: Based on the passage, All That Echoes refers to "All That Echoes", the sixth studio album by American singer-songwriter Josh Groban. So the answer is: (1) Paraphrase Answer: All That Echoes refers to "All That Echoes", the sixth studio album by Josh Groban; (2) Answer List: ["All That Echoes (sixth studio album by Josh Groban)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Hydrogen | Discovery and use: 1) 2) 3) In 1671, Robert Boyle discovered and described the reaction between iron filings and dilute acids, which results in the production of hydrogen gas. In 1766, Henry Cavendish was the first to recognize hydrogen gas as a discrete substance, by naming the gas from a metal-acid reaction "inflammable air". ... [2] Hydrogen | on metals. In 1766–81, Henry Cavendish was the first to recognize that hydrogen gas was a discrete substance, and that it produces water when burned ... [3] Discovery of the nonmetals | 18th century: H, O, N, (Te), Cl:  Hydrogen: Cavendish, in 1766, was the first to distinguish hydrogen from other gases, although Paracelsus around 1500, Robert Boyle (1670), and Joseph Priestley (?) had observed its production by reacting strong acids with metals
Question: Who first recognized that hydrogen was a discrete substance?
Answer: All three passages indicate that Henry Cavendis was the first to recognize hydrogen as a discrete substance. So the answer is: (1) Paraphrase Answer: Henry Cavendis was the first to recognize hydrogen as a discrete substance; (2) Answer List: ["Henry Cavendis"]

Retrieved Knowledge: 
Wikipedia Passages: [1] The Pizza Man | The Pizza Man (foaled March 25, 2009) is an American Thoroughbred racehorse who won multiple stakes races including the Arlington Million in 2015 and the Northern Dancer Turf Stakes in 2016, becoming the first Illinois-bred horse to win either of these Grade I races. ... [2] Pizza Man | Pizza Man is a 1991 comedy film starring Bill Maher and Annabelle Gurwitch; written and directed by J.F. Lawton who was credited in the film as J.D. Athens. The film received a PG-13 rating by the MPAA.
Question: What is Pizza Man?
Answer: Based on the passages, Pizza Man could refer to two entities: either "The Pizza Man" from passage [1], an American Thoroughbred racehorse, or "Pizza Man" from passage [2], a 1991 comedy film. So the answer is: (1) Paraphrase Answer: Pizza Man could be "The Pizza Man", an American Thoroughbred racehorse, or "Pizza Man", a 1991 comedy film; (2) Answer List: ["The Pizza Man (American Thoroughbred racehorse)", "Pizza Man (1991 comedy film)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] List of Doctor Who universe creatures and aliens | Wirrn:  The Wirrn are an insectoid race that made their debut in the 1975 Fourth Doctor story The Ark in Space. The name is sometimes spelled Wirrrn, which is a spelling originating from the novelisation of the story. ... [2] List of Doctor Who universe creatures and aliens | Wirrn:  hosts; the larvae emerge to consume the host, absorbing its memories and knowledge. A Wirrn larva is a green slug-like creature, varying in size from a few inches to 1 or 2 metres across. It can "infect" another organism through contact with a substance it excretes, mutating them into an adult Wirrn and connecting their consciousness to the hive mind. 
Question: What is WIRR?
Answer: Based on the provided passages, WIRR does not seem to have a direct match. The passages only mention Wirrn, an insectoid race in the Doctor Who universe, which should not be equal to WIRR that seems like some organization. I also don't possess knowledge of WIRR, so I will leave the entity name as it is. So the answer is: (1) Paraphrase Answer: WIRR is WIRR, as no relevant information is found; (2) Answer List: ["WIRR"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Robert Clive | Attempts at administrative reform:  Clive was also instrumental in making the company virtual master of North India by introducing his policy of "Dual system of government". According to the new arrangement enforced by him, the company became liable only for revenue affairs of Bengal (Diwani) and Bihar while the administration and law and order was made a prerogative of the Nawab. ... [2] History of India | Other kingdoms:  1757, installed Mir Jafar on the Masnad (throne) and established itself to a political power in Bengal. In 1765 the system of Dual Government was established, in which the Nawabs ruled on behalf of the British and were mere puppets to the British. In 1772 the system was abolished and Bengal was brought under the direct control of the British. In 1793, when the Nizamat (governorship) of the Nawab was also taken away from them, they remained as the mere pensioners of the British East India Company. ... 
Question: What agency abolished the dual system of government in bengal?
Answer: Passage [2] indicates that the dual system of government was established in Bengal in 1765, yet "in 1772 the system was abolished and Bengal was brought under the direct control of the British", so the system was abolished by the British. Furthermore, passage [2] provides the full name of the British agency, the "British East India Company". So the answer is: (1) Paraphrase Answer: The British East India Company abolished the dual system of government in bengal; (2) Answer List: ["British East India Company"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_search_prompt_crag(question, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Google, Wikipedia, or Wikidata, please answer the following entity disambiguation question "{question}". Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) an Answer List that is a clean entity list. You may not answer with an empty entity list: if the provided information is not enough to answer the question, answer based on your own knowledge. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [entity_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] 2019 in American football | National Football League: January 27: 2019 Pro Bowl in Orlando at Camping World Stadium ; Team AFC defeated team NFC, with the score of 26–7. ; Offensive MVP: Patrick Mahomes (Kansas City Chiefs) ; Defensive MVP: Jamal Adams (New York Jets)  ... [2] Lamar Jackson | 2019 season: Unanimous NFL MVP:  passing yards and 103 rushing yards. On the day after the Ravens' victory over the Browns, and due to the Ravens' having clinched home-field advantage ...
Google Results: [1] Lamar Jackson | When Jackson won MVP in 2019, he led the NFL in touchdown passes with 36 and set the single-season rushing record by a quarterback with 1,206 yards. This time, Jackson captured the award because he was the best player on the league's most dominant team in the regular season. [2] Lamar Jackson | [3] Ravens QB Lamar Jackson named 2019 NFL MVP
Question: Who was the 2019 NFL MVP?
Answer: The 2019 NFL MVP is Lamar Jackson. So the answer is: (1) Paraphrase Answer: The 2019 NFL MVP is Lamar Jackson; (2) Answer List: ["Lamar Jackson"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Life or Something Like It |  Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek. The film focuses on television reporter Lanie Kerrigan (Angelina Jolie) and her quest to find meaning in her life. The original music score was composed by David Newman.
Google Results: [1] Life or Something Like It | Lanie Kerrigan (Angelina Jolie), a feature reporter at a Seattle television station, leads the ultimate superficial life, even though she thinks she has it all, like a superstar boyfriend, a gorgeous apartment, and a shot at a big network assignment.… MORE [2] Life or Something Like It | Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek. The film focuses on television reporter Lanie Kerrigan ... 
Question: What is the film Life or Something Like It?
Answer: Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek. So the answer is: (1) Paraphrase Answer: Life or Something Like It is a 2002 American romantic comedy-drama film directed by Stephen Herek; (2) Answer List: ["Life or Something Like It (2022 American romantic comedy-drama film)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Bond (finance) | In finance, a bond is an instrument of indebtedness of the bond issuer to the holders. The most common types of bonds include municipal bonds and corporate bonds. Bonds can be in mutual funds or can be in private investing where a person would give a loan to a company or the government... [2] Bond (finance) | Investing in bonds:  a fixed interest payment twice a year and a fixed lump sum at maturity is attractive. 
Google Results: [1] Bonds | A bond is a debt security, like an IOU. Borrowers issue bonds to raise money from investors willing to lend them money for a certain amount of time. [2] Bonds: How They Work and How To Invest | A bond is a fixed-income investment that represents a loan made by an investor to a borrower, usually corporate or governmental. They represent loans made to the issuer.
Question: what are bonds?
Answer: A bond is a fixed-income financial instrument that represents a loan from an investor to an issuer. So the answer is: (1) Paraphrase Answer: A bond is a fixed-income financial instrument that represents a loan from an investor to an issuer; (2) Answer List: ["A bond is a fixed-income financial instrument that represents a loan from an investor to an issuer"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Pirates of the Caribbean: Dead Man's Chest | Accolades:  At the 79th Academy Awards, visual effects supervisors John Knoll, Hal Hickel, Charles Gibson, and Allen Hall won an Oscar for Best Visual Effects, which was also the first time since 1994's Forrest Gump that Industrial Light & Magic had received that particular Academy Award. The film was also nominated for Best Art Direction, Sound Editing, and Sound Mixing.
Google Results: [1] Dead Man's Chest" Wins Best Visual Effects | 76th Oscars (2007) | Pirates of the Caribbean: Dead Man's Chest" Wins Best Visual Effects | 76th Oscars (2007) - YouTube ... 
Question: In 2007, which movie was distinguished for its visual effects at the Oscars?
Answer: The movie distinguished for its visual effects at the Oscars in 2007 is Pirates of the Caribbean: Dead Man's Chest. So the answer is: (1) Paraphrase Answer: Pirates of the Caribbean: Dead Man's Chest was distinguished for its visual effects at the Oscars in 2007; (2) Answer List: ["Pirates of the Caribbean: Dead Man's Chest"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt



def format_search_prompt_blendqa(question, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Google, Wikipedia, or Wikidata, please answer the following entity disambiguation question "{question}". Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) an Answer List that is a clean entity list. You may not answer with an empty entity list: if the provided information is not enough to answer the question, answer based on your own knowledge. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [entity_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Kuhle Wampe | Kuhle Wampe is a 1932 German feature film about unemployment, homelessness and left wing politics in the Weimar Republic produced by Prometheus Film.
Google Results: [1] To Whom Does the World Belong? | Anni Bönike has a badly paid job in a factory ... [2] Kuhle Wampe | Kuhle Wampe is a 1932 German feature film about unemployment, homelessness and left wing politics in the Weimar Republic produced by Prometheus Film. 
Question: What is Kuhle Wampe?
Answer: Kuhle Wampe is a 1932 German feature film. So the answer is: (1) Paraphrase Answer: Kuhle Wampe is a 1932 German feature film; (2) Answer List: ["Kuhle Wampe (German film)"]

Retrieved Knowledge: 
Google Results: [1] Carlos Alcaraz | Carlos Alcaraz (born May 5, 2003, El Palmar, Murcia, Spain) is a Spanish professional tennis player ... [2] Carlos Alcaraz Biography: Childhood, Career and ... | Carlos Alcaraz is a Spanish professional tennis player born on May 5, 2003.
Question: Who is the tennis player born on May 5, 2003?
Answer: The tennis player born on May 5, 2003, is Carlos Alcaraz. So the answer is: (1) Paraphrase Answer: The tennis player born on May 5, 2003, is Carlos Alcaraz; (2) Answer List: ["Carlos Alcaraz"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Al Jazirah (newspaper) | Al Jazirah (in Arabic الجزيرة meaning The Island) is a daily Arabic newspaper published in Saudi Arabia. Its sister newspaper is Al Masaiya ... [2] Al Jazirah, Sharjah | Al Jazirah (الجزيرة) is a settlement in Sharjah. ... [3] Al Jazirah Al Hamra | Al Jazirah Al Hamra (الجزيرة الحمراء, The Red Island) is a town to the south of the city of Ras Al Khaimah in the United Arab Emirates. 
Question: What is Al Jazirah?
Answer: Al Jazirah could refer to multiple entities, including newspaper Al Jazirah, Sharjah settlement Al Jazirah, Sharjah, or United Arab Emirates town Al Jazirah Al Hamra. So the answer is: (1) Paraphrase Answer: Al Jazirah could refer to Al Jazirah (newspaper), Al Jazirah, Sharjah (settlement), or Al Jazirah Al Hamra (town); (2) Answer List: ["Al Jazirah (newspaper)", "Al Jazirah, Sharjah (settlement)", "Al Jazirah Al Hamra (town)"]

Retrieved Knowledge: 
Google Results: [1] an enzyme produced by many organisms and is essential to the complete digestion of whole milk | Lactase (EC 3.2. 1.108) is an enzyme produced by many organisms and is essential to the complete digestion of whole milk. It breaks down the sugar lactose into its component parts, galactose and glucose. [2] LACTASE - Uses, Side Effects, and More | Lactase is an enzyme that breaks down lactose, the sugar in milk. 
Question: What is the enzyme that breaks down lactose into glucose and galactose?
Answer: The enzyme that breaks down lactose into glucose and galactose is lactase. So the answer is: (1) Paraphrase Answer: The enzyme that breaks down lactose into glucose and galactose is lactase; (2) Answer List: ["Lactase"]

Retrieved Knowledge: 
Google Results: [1] US overdoses have fallen sharply in recent months, a ... | A steep drop in deaths from fentanyl is a key factor driving the overall decline. Overdose deaths involving fentanyl and other synthetic ...
Question: What key factor is driving the overall decline in overdose deaths in Puebla?
Answer: The retrieved knowledge indicates that a "key factor driving the overall decline" is "a steep drop in deaths from fentanyl". So the answer is: (1) Paraphrase Answer: a key factor driving the overall decline is a steep drop in deaths from fentanyl; (2) Answer List: ["a steep drop in deaths from fentanyl"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


##### 2. Relate

def format_relate_prompt_hotpotqa(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia, Google, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering people's names, always answer the full name, i.e. "Alan Mathison Turing" instead of "Alan Turing". When answering long lists such as song titles, directly write the list in your answer formulation. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] BOAC Flight 911 (Speedbird 911) was a round-the-world flight operated by British Overseas Airways Corporation that crashed as a result of an encounter with severe clear-air turbulence near Mount Fuji in Japan on 5 March 1966.  The Boeing 707-436 on this flight was commanded by Captain Bernard Dobson, 45, from Dorset, an experienced 707 pilot who had been flying these aircraft since November 1960.
Question: What is the plane type used for BOAC Flight 911?
Answer: The passage indicates that "The Boeing 707-436 on this flight was commanded by Captain Bernard Dobson", so the plane type used for the flight should be Boeing 707-436. So the answer is: (1) Paraphrase Answer: The plane type used for BOAC Flight 911 is Boeing 707-436; (2) Answer List: ["Boeing 707-436"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Coke Kahani (Urdu: کوک کہانی\u200e ) is a 2012 Pakistani comedy drama sitcom directed by Mehreen Jabbar broadcasting on Broadcast syndication.  Sitcom is written by Syed Mohammad Ahmed and Yasir Rana, starring Sonia Rehman, Faisal Rehman, Syra Yousuf, Syed Mohammad Ahmed, Yasir Hussain, Ahmed Zeb, Shamim Hilali.  Sitcom was first aired on 3 November 2012.
Question: Who helped write for Coke Kahani?
Answer: The passage indicates that Coke Kahani is "written by Syed Mohammad Ahmed and Yasir Rana", so Syed Mohammad Ahmed and Yasir Rana are writers of the drama. Additionally, my own knowledge suggests that the actor Yasir Hussain also helped write for Coke Kahani. So the answer is: (1) Paraphrase Answer: "Syed Mohammad Ahmed", "Yasir Rana", and "Yasir Hussain" helped write for Coke Kahani; (2) Answer List: ["Syed Mohammad Ahmed", "Yasir Rana", "Yasir Hussain"]

Retrieved Knowledge: 
Wikipedia Passages: [1] The Boeing 707 is a mid-sized, long-range, narrow-body, four-engine jet airliner built by Boeing Commercial Airplanes from 1958 to 1979.  Its name is commonly pronounced as ""seven oh seven"".  Versions of the aircraft have a capacity from 140 to 219 passengers and a range of 2500 to .
Question: What was the largest passenger capacity of Boeing 707-436?
Answer: The passage suggests that Versions of the Boeing 707 "have a capacity from 140 to 219 passengers", so the largest passenger capacity should by 219. So the answer is: (1) Paraphrase Answer: The largest passenger capacity of Beoing 707-436 is 219; (2) Answer List: ["219"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Forbidden Quest () is a 2006 South Korean period drama film about a scholar during the Joseon Dynasty who begins to write erotic novels, and becomes the lover of the King's favorite concubine. ... [2] The Forbidden Quest is a 1993 mockumentary written and directed by Peter Delpeut. ... [3] "Forbidden Paradise 3: The Quest for Atlantis is the third album in the ""Forbidden Paradise"" series.  It is the first album in the series to be mixed by well-known trance DJ/producer Tiësto.  As with the rest of the Forbidden Paradise series, the album is a live turntable mix.
Question: Who was Forbidden Quest about?
Answer: Wikipedia passage [1] describes the drama film Forbidden Quest being "about a scholar during the Joseon Dynasty who begins to write erotic novels", so the film should be about a scholar. So the answer is: (1) Paraphrase Answer: Forbidden Quest was about a scholar; (2) Answer List: ["a scholar"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Lady Mary Fox (née FitzClarence; 19 December 1798 – 13 July 1864) was an illegitimate daughter of King William IV of the United Kingdom by his mistress Dorothea Jordan.  In later life she became a writer. ... [2] Elizabeth Hay, Countess of Erroll (17 January 1801 – 16 January 1856; born Elizabeth FitzClarence) was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan.  She married William Hay, 18th Earl of Erroll, and became Countess of Erroll on 4 December 1820 at age 19.  Due to Hay's parentage, William Hay became Lord Steward of the Household.  Elizabeth and William Hay married at St George's, Hanover Square.  Hay is pictured in a FitzClarence family portrait in House of Dun and kept a stone thrown at her father William IV and the gloves he wore on opening his first Parliament as mementos.  She died in Edinburgh, Scotland. ... [3] William IV of Toulouse ( 1040 – 1094) was Count of Toulouse, Margrave of Provence, and Duke of Narbonne from 1061 to 1094.  He succeeded his father Pons of Toulouse upon his death in 1061.  His mother was Almodis de la Marche, but she was kidnapped by and subsequently married to Ramon Berenguer I, Count of Barcelona when William was a boy.  He was married to Emma of Mortain (daughter of Robert, Count of Mortain and a niece of William of Normandy), who gave him one daughter, Philippa.  He also had an illegitimate son, William-Jordan, with his half-sister Adelaide.
Question: Who was the illegitimate daughter of King William IV?
Answer: Based on the provide passages, the persons described by passages [1] and [2] are illegitimate daughters of King William IV, given Lady Mary Fox "was an illegitimate daughter of King William IV" and Elizabeth Hay, Countess of Erroll "was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan". So the answer is: (1) Paraphrase Answer: The illigimate daughters of King WIlliam IV are "Lady Mary Fox" and "Elizabeth Hay, Countless of Erroll"; (2) Answer List: ["Lady Mary Fox", "Elizabeth Hay, Countess of Erroll"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Moby (album) | Moby is the debut studio album by American musician Moby, released in July 1992 by record label Instinct. ... [2] These Systems Are Failing | These Systems Are Failing is the thirteenth studio album by American electronica musician Moby.  It was released on October 14, 2016 by record labels Little Idiot and Mute.  This is the first album from Moby's musical project Moby & The Void Pacific Choir (formed by Moby, Mindy Jones, Julie Mintz, Jonathan Nesvadba, Joel Nesvadba, Jamie Drake and Lauren Tyler Scott). ... [3] Play (Moby album) | "Play is the fifth studio album by American electronica musician Moby.  It was first released on May 17, 1999 by Mute and V2.  Recording of the album began in 1998, following the release of his fourth album, ""Animal Rights"" (1996), which deviated from Moby's electronica style; his goal for ""Play"" was to return to this style of music.  Originally intended to be his final record, the recording of the album took place at Moby's home studio in Manhattan, New York."
Question: What studio albums did Moby release?
Answer: Based on the information retrieved and my own knowledge, Moby has released the multiple albums, which I will list in my answer. So the answer is: (1) Paraphrase Answer: Studio albums released by Moby include "Moby (1992)", "Ambient (1993)", "Everything Is Wrong (1995)", "Animal Rights (1996)", "Play (1999)", "18 (2002)", "Hotel (2005)", "Last Night (2008)", and "These Systems Are Failing (2016)"; (2) Answer List: ["Moby (1992)", "Ambient (1993)", "Everything Is Wrong (1995)", "Animal Rights (1996)", "Play (1999)", "18 (2002)", "Hotel (2005)", "Last Night (2008)", "These Systems Are Failing (2016)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Abortion in Greece | Abortion in Greece has been fully legalized since January 27, 1984.  Abortions can be performed on-demand in hospitals for women whose pregnancies have not exceeded twelve weeks.  In the case of rape or incest, an abortion can occur as late as nineteen weeks, and as late as twenty-four weeks in the case of fetal abnormalities.  Girls under the age of 18 must get written permission from a parent or guardian before being allowed an abortion. ... [2] P.A.Th.E./P. | P.A.Th.E. /P (Greek: Π.Α.Θ.Ε. /Π., Πάτρα - Αθήνα - Θεσσαλονίκη - Ειδομένη/Προμαχώνας), which stands for Patras–Athens–Thessaloniki–Idomeni/Promachonas is a high speed rail line in Greece which is partly completed and partly under construction.  After full completion, the journey between Athens and Thessaloniki is expected to last 3½ hours, a major reduction from the current 5½ hours.
Question: How many weeks did Greece last?
Answer: The question does not make sense in the context of the provided passages. So the answer is: (1) Paraphrase Answer: Unknown; (2) Answer List: []

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
        
    return prompt

# deleted: When answering people's names, always answer the full name, i.e. "Alan Mathison Turing" instead of "Alan Turing". 
# changed to single answer: Answer: Based on the passages, there could be multiple released songs called "Hold On Me", including passage [2]'s "Hold on Me (Grinspoon song)" and passage [3]'s  "Hold on Me (Marlon Roudette song)". "Hold on Me (Grinspoon song)" was released on 21 February 2005, and "Hold on Me (Marlon Roudette song)" was released on 20 June 2012. So the answer is: (1) Paraphrase Answer: "Hold on Me (Grinspoon song)" was released on 21 February 2005, and "Hold on Me (Marlon Roudette song)" was released on 20 June 2012; (2) Answer List: ["21 February 2005", "20 June 2012"]
def format_relate_prompt_2wiki(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia, Google, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering long lists such as song titles, directly write the list in your answer formulation. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Mon oncle Benjamin | Mon oncle Benjamin (My Uncle Benjamin) is a 1969 French film directed by Édouard Molinaro, starring Jacques Brel and Claude Jade. The film is based on a once-popular French comic novel Mon oncle Benjamin (novel) by Claude Tillier (1842). ... [2] Jacques Brel | Film career: appeared in his third film, Mon oncle Benjamin (My uncle Benjamin), directed by Édouard Molinaro and co-starring Claude Jade and Bernard Blier. ... [3] My Uncle Benjamin (1924 film) | My Uncle Benjamin (French: Mon oncle Benjamin) is a 1924 French silent comedy film directed by René Leprince and starring Léon Mathot, Madeleine Erickson and Charles Lamy."
Answer: Based on passages [1] and [2], Mon oncle Benjamin is a 1969 French film directed by Édouard Molinaro. So the answer is: (1) Paraphrase Answer: The director of Mon oncle Benjamin is Édouard Molinaro; (2) Answer List: ["Édouard Molinaro"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Passion (Utada Hikaru song) | Cultural impact:  lowest selling single until her 2008 double A-side release "Stay Gold" / "Heart Station". In early 2013, an announcement confirmed the development of the third instalment of the Kingdom Hearts console game. In October that year, Utada\'s father, Teruzane Utada, was asked on Twitter about their contribution towards the third installment ... [2] Passion (Utada Hikaru song) | Composition:  and eventually introduces a "new world". A member at Channel-Ai stated that the theme encompassed the parent album Ultra Blue, but highlighted on "hope" more than "sadness". Vibe\'s Mio Yamada said that the lyrics, "expressed weakness and strength simultaneously," and that the material was more mature than Utada\'s previous work. Executive producers for Kingdom Hearts and head composer Yoko Shimomura said that the track needed to be more dramatic for the remaining of the accompanying score.
Question: Who is the mother of the performer of song Passion (Utada Hikaru Song)?
Answer: While the passage does not directly provide "the mother of the performer of song Passion (Utada Hikaru Song)", it indicates that the performer of song Passion (Utada Hikaru Song) is Utada Hikaru, and my own knowledge suggests that the mother of Utada Hikaru is Keiko Fuji. So the answer is: (1) Paraphrase Answer: The mother of the performer of song Passion (Utada Hikaru Song) is Keiko Fuji; (2) Answer List: ["Keiko Fuji"]

Retrieved Knowledge:
Wikipedia Passages: [1] Hold On to Me (Lauren Daigle song) | Background:  On February 1, 2021, Lauren Daigle announced that she would be releasing a new single titled "Hold On to Me" on February 26, 2021. "Hold On to Me" was released on February 26, 2021, accompanied by an audio video of the song on YouTube. Daigle also revealed that the song was the "first taste" of an upcoming project. ... [2] Hold on Me (Grinspoon song) | "Hold on Me" is the third single released by Grinspoon from their fourth studio album Thrills, Kills & Sunday Pills. It was released on 21 February 2005 on the Universal Records label. The initial single release included a lapel pin badge under shrink wrap, with 'Hold On Me - Grinspoon EP' themed artwork. ... [3] Hold on Me (Marlon Roudette song) | Music video:  A music video directed by "LJ" for the song was released on 20 June 2012 with a total length of three minutes and eighteen seconds. In the video, Marlon is shown sitting in a bedroom and walking on the walls.
Question: When was Hold on Me (Grinspoon song) released?
Answer: Passage [2] provides information about "Hold On Me" (Grinspoon song), stating that the song was "released on 21 February 2005". So the answer is: (1) Paraphrase Answer: "Hold on Me (Grinspoon song)" was released on 21 February 2005; (2) Answer List: ["21 February 2005"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Achraf Hakimi | Achraf Hakimi Mouh (أشرف حكيمي; born 4 November 1998) is a professional footballer who plays as a right wing-back for Ligue 1 club Paris Saint-Germain and the Morocco national team. Widely considered as one of the best right-backs in the world, he mainly plays as a right wing-back or right-back, Hakimi can also play on the left or as a right winger ... [2] Canardo (rapper) | Hakim Mouhid (born 22 September 1984 in Trappes, Yvelines), better known by his stage name Canardo, is a French rapper, singer, songwriter and music producer. After working with label "Banlieue Sale Music" since 2007, in 2011, he founded his own label "Henijai Music". He is the brother of fellow French rapper La Fouine. ... [3] Drôle de parcours | Track listing: Notes ; The name "Mouhid" refers to Laouni Mouhid. Fatima Mouhid and Hakim Mouhid are referred to by their full names.
Question: What is the nationality of Hakim Mouhid?
Answer: Passage [2] indicates that Hakim Mouhid, better known as Canardo, is a "French rapper, singer, songwriter and music producer", so he is a French national. So the answer is: (1) Paraphrase Answer: The nationality of Hakim Mouhid is French; (2) Answer List: ["French"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
        
    return prompt

# deleted: 
# Retrieved Knowledge: 
# Wikipedia Passages: [1] Henry Cavendish | Chemistry research:  Cavendish published no books and few papers, but he achieved much. Several areas of research, including mechanics, optics, and magnetism, feature extensively in his manuscripts, but they scarcely feature in his published work. Cavendish is considered to be one of the so-called pneumatic chemists of the eighteenth and nineteenth centuries, along with, for example, Joseph Priestley, Joseph Black, and Daniel Rutherford. Cavendish ... [2] Henry Cavendish | Personality and legacy:  Theoretical physicist Dietrich Belitz concluded that in this work Cavendish "got the nature of heat essentially right". In honour of Henry Cavendish's achievements and due to an endowment granted by Henry's relative William Cavendish, 7th Duke of Devonshire, the University of Cambridge's physics laboratory was named the Cavendish Laboratory by James Clerk Maxwell, the first Cavendish Professor of Physics and an admirer of Cavendish's work.
# Question: What field of work did Henry Cavendish work in?
# Answer: Henry Cavendish was a theoretical chemist and physicist, confirmed by the passage [1] introducing his "Chemistry research" and passage [2] explaining his legacy in the field of physics. So the answer is: (1) Paraphrase Answer: Henry Cavendish worked in both chemistry and physics; (2) Answer List: ["chemistry", "physics"]
def format_relate_prompt_musique(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia, Google, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering long lists such as song titles, directly write the list in your answer formulation. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Pizza Man |  Pizza Man is a 1991 comedy film starring Bill Maher and Annabelle Gurwitch; written and directed by J.F. Lawton who was credited in the film as J.D. Athens. The film received a PG-13 rating by the MPAA. ... [2] Pizza Man (2011 film) |  Pizza Man is a 2011 American family action film directed by Joe Eckardt, written by Jonathan Kapoor and Marco Mannone, and starring Frankie Muniz and Diamond Dallas Page.
Question: Who is Pizza Man (1991 comedy film)'s cast member?
Answer: Passage [1] indicates that the 1991 comedy film Pizza Man stars "Bill Maher and Annabelle Gurwitch". So the answer is: (1) Paraphrase Answer: Pizza Man (1991 comedy film)'s cast member are Bill Maher and Annabelle Gurwitch; (2) Answer List: ["Bill Maher", "Annabelle Gurwitch"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Yangzhou | Yangzhou, postal romanization Yangchow, is a prefecture-level city in central Jiangsu Province (Suzhong), East China. Sitting on the north bank of the Yangtze, it borders the provincial capital Nanjing to the southwest, Huai'an to the north, Yancheng to the northeast, Taizhou to the east, and Zhenjiang across the river to the south. ... [2] Yang Province | Tribute of Yu account:  The Tribute of Yu records that Yangzhou was located between Huai and the Sea. Kong Anguo (fl. 2nd century BCE) explained in Shangshu Zhuan (尚書傳) that the text meant that Yangzhou was bordered by the Huai River in the north and the South China Sea in the south. ... [3] Yang Prefecture (Jiangsu) | Yangzhou or Yang Prefecture (揚州) was a zhou (prefecture) in imperial China, centering on modern Yangzhou, Jiangsu, China. 
Question: What is the location of Yangzhou, Jiangsu, China?
Answer: Passage [1] indicates that Yangzhou is "a prefecture-level city in central Jiangsu Province (Suzhong)". So the answer is: (1) Paraphrase Answer: Yangzhou is located in central Jiangsu Province (Suzhong); (2) Answer List: ["central Jiangsu Province (Suzhong)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Frankie Muniz | Business pursuits:  In 2018, Muniz and his now-wife Paige Price bought Outrageous Olive Oils & Vinegars, a small specialty shop in Scottsdale, Arizona. ... [2] Frankie Muniz | Personal life:  mini-strokes were a misdiagnosis and he was suffering from migraine auras. He also clarified that the story of his memory loss was largely misinterpreted by media sources. In 2005, Muniz was engaged to Jamie Grady. In 2008, he met publicist Elycia Marie Turnbow through their mutual personal trainer at a Los Angeles gym. They began dating and later moved to Scottsdale, Arizona. ... [3] Frankie Muniz | Acting:  of the detectives (Merideth Bose) had a crush on the actor/ racecar driver (Frankie Muniz) who was competing in a drag race
Question: When does real time with Frankie Muniz start again in 2018?
Answer: Answer: The question does not make sense in the context of the provided passages. So the answer is: (1) Paraphrase Answer: Unknown; (2) Answer List: []

Retrieved Knowledge: 
Wikipedia Passages: [1] Tang Jinhua | Tang Jinhua (born 8 January 1992) is a Chinese retired badminton player who competed at the highest level during the second decade of the 2000s, winning numerous women's doubles and occasional mixed doubles events with a variety of partners. She is a graduate of Hunan University. ... [2] Joseph Tang Yuange | Biography:  Tang was born in Jintang County, Sichuan, on November 17, 1963. From 1984 to 1988 he studied at the Sichuan Catholic Theological and Philosophical College. 
Question: What is the place of birth of Tang Jinhua?
Answer: Passage [1] suggests that Tang Jinhua refers to a Chinese retired badminton playe, but her place of birth is not explicitly mentioned. Nevertheless, my knowledge suggests that Chinese retired badminton player Tang Jinhua was born in Nanjing, Jiangsu, China. So the answer is: (1) Paraphrase Answer: Tang Jinhua was born in Nanjing, Jiangsu, China; (2) Answer List: ["Nanjing, Jiangsu, China"]

Retrieved Knowledge: 
Wikipedia Passages: [1] East India Company | Indian Rebellion and disestablishment:  the company. The British government took over its Indian possessions, its administrative powers and machinery, and its armed forces. The company had already divested itself of its commercial trading assets in India in favour of the UK government in 1833 ... [2] Queen Victoria | Empress:  After the Indian Rebellion of 1857, the British East India Company, which had ruled much of India, was dissolved, and Britain\'s possessions and protectorates on the Indian subcontinent were formally incorporated into the British Empire. The Queen had a relatively balanced view of the conflict, and condemned atrocities on both sides
Question: What happened to the assets of the British India Company after it was removed from power?
Answer: Passage [1] indicates that "the British government took over its Indian possessions", and passage [2] indicates that the company's assets were "formally incorporated into the British Empire". So the answer is: (1) Paraphrase Answer: After the British India Company was removed from power, its assets were took over by the British government and formally incoporated into the British Empire; (2) Answer List: ["took over by the British government and formally incoporated into the British Empire"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Sir Robert Peel, 1st Baronet | Sir Robert Peel, 1st Baronet (25 April 1750 – 3 May 1830) was a British politician and industrialist and one of early textile manufacturers of the Industrial Revolution. He is one of ten known British millionaires in 1799. He was the father of Sir Robert Peel, twice Prime Minister of the United Kingdom.
Question: Who was the father of Robert Peel?
Answer: Passage [1] indicates that "Sir Robert Peel, 1st Baronet" was "the father of Sir Robert Peel". So the answer is: (1) Paraphrase Answer: The father of Robert Peel was "Sir Robert Peel, 1st Baronet"; (2) Answer List: ["Sir Robert Peel, 1st Baronet"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Santa Monica, California | History:  Around the start of the 20th century, a growing population of Asian Americans lived in and around Santa Monica and Venice. A Japanese fishing village was near the Long Wharf while small numbers of Chinese lived or worked in Santa Monica and Venice. The two ethnic minorities were often viewed differently by White Americans who were often well-disposed towards the Japanese but condescending towards the Chinese. ... [2] History of Santa Monica, California | 1900s: ... a growing population of Asian Americans lived in or near Santa Monica and Venice. A Japanese fishing village was located near the Long Wharf while small numbers of Chinese lived or worked in both Santa Monica and Venice. The two ethnic minorities were often viewed differently by White Americans who were often well-disposed towards the Japanese but condescending towards the Chinese. 
Question: How many ethnic minorities were looked at differently in Santa Monica, California?
Answer: Passages [1] and [2] indicate that two ethnic minorities, the Japanese and the Chinese, were looked at differently in Santa Monica, California. So the answer is: (1) Paraphrase Answer: Two ethnic minorities were looked at differently in Santa Monica, California; (2) Answer List: ["two"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
        
    return prompt


def format_relate_prompt_crag(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia, Google, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering long lists such as album titles, directly write the list in your answer formulation. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Google Results: [1] $110 million | As of 2023, Chris Evans' net worth today is $110 million. The majority of his net worth is derived from his portrayal of Steve Rogers in the MCU movies. Apart from his earnings from movies, he also has several endorsements from high-end brands such as Hyundai, Gucci, and Jinx which contribute to this net worth. [2] Chris Evans Net Worth | Chris Evans is an American actor and director who has a net worth of $110 million. The majority of his net worth has been earned via his appearances in several ...
Question: What is Chris Evans net worth 2023?
Answer: Chris Evans is net worth $110 million as of 2023. So the answer is: (1) Paraphrase Answer: Chris Evans is net worth $110 million as of 2023; (2) Answer List: ["$110 million"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Hitmixes | Hitmixes is the second extended play (EP) by American singer Lady Gaga, released on August 25, 2009. ... [2] The Fame Monster |  The Fame Monster is a reissue of American singer Lady Gaga's debut studio album, The Fame (2008), and was released on November 18, 2009, through Interscope Records. ... [3] The Cherrytree Sessions (Lady Gaga EP) | Critical reception:  The Cherrytree Sessions was released on February 3, 2009, in the United States and was an import in European nations, including France. ...
Google Results: [1] The Fame Monster, Hitmixes, The Cherrytree Sessions, Attention Deficit [2] Lady Gaga discography | Gaga later released The Fame Monster in November 2009, as a deluxe edition or reissue of The Fame, which was ultimately released also as a standalone EP.
Question: What albums did Lady Gaga release in 2009?
Answer: In 2009, Lady Gaga released The Fame Monster, Hitmixes, The Cherrytree Sessions, and Attention Deficit. So the answer is: (1) Paraphrase Answer: In 2009, Lady Gaga released The Fame Monster, Hitmixes, The Cherrytree Sessions, and Attention Deficit; (2) Answer List: ["The Fame Monster", "Hitmixes", "The Cherrytree Sessions", "Attention Deficit"]

Retrieved Knowledge: 
Google Results: [1] Boston Celtics | The Boston Celtics are an American professional basketball team based in Boston. [2] 2022-23 Boston Celtics Schedule | 2022-23 Boston Celtics Schedule and Results ; Record: 57-25, Finished 2nd in NBA Eastern Conference ; Coach: Joe Mazzulla (57-25) ... 
Question: How many games did Boston Celtics win in 2022?
Answer: Google results passage [2] indicates that in the 2022-23 season, the Boston Celtic's record was "57-25", indicating that they had 57 wins. So the answer is: (1) Paraphrase Answer: Boston Celtics won 57 games in 2022; (2) Answer List: ["57"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Sirius | Sirius is gradually moving closer to the Solar System, so it is expected to slightly increase in brightness over the next 60,000 years. After that time, its distance will begin to increase, and it will become fainter, but it will continue to be the brightest star in the Earth's night sky for approximately the next 210,000 years. Sirius A is about twice as massive as the Sun and has an absolute visual magnitude of +1.42. It is 25 times as luminous as the Sun, but has a significantly lower luminosity than other bright stars such as Canopus or Rigel. The system 
Google Results: [1] Sirius | Facts & Location | Britannica | Sirius, brightest star in the night sky, with apparent visual magnitude −1.46. It is a binary star in the constellation Canis Major. The bright component of the binary is a blue-white star 25.4 times as luminous as the Sun.
Question: How bright is the star Sirius?
Answer: Based on the retrieved knowledge, Sirius is the "brightest star in the Earth's night sky" and is "25 times as luminous as the Sun". So the answer is: (1) Paraphrase Answer: The star Sirius is the brightest star in the Earth's night sky" and is "25 times as luminous as the Sun; (2) Answer List: ["brightest star in the Earth's night sky and 25 times as luminous as the Sun"]

Retrieved Knowledge: 
Wikipedia Passages: [1] List of American exchange-traded funds | This is a table of notable American exchange-traded funds, or ETFs. As of 2020, the number of exchange-traded funds worldwide is over 7600, representing about 7.74 trillion U.S. dollars in assets. The largest ETF, as of April 2021, was the SPDR S&P 500 ETF Trust (nyse arca: SPY), with about $353.4 billion in assets...
Question: What was the total value of all exchange-traded funds (etfs) in the united states in 2020?
Answer: The retrieved knowledge does not mention the total value of ETFs in the United States in 2020, but my own knowledge suggests that as of 2020, the total value of all exchange-traded funds (ETFs) in the United States is approximately $5.4 trillion. So the answer is: (1) Paraphrase Answer: The total value of all exchange-traded funds (etfs) in the united states in 2020 is approximately $5.4 trillion; (2) Answer List: ["$5.4 trillion"]

Retrieved Knowledge: 
Google Results: [1] 2 | Brad Pitt has been married twice—Jennifer Aniston from 2000 to 2005, and Angelina Jolie from 2014 to 2019 (though he and Jolie separated in 2016).
Question: How many times has brad pitt been married?
Answer: Brad Pitt has been married 2 times, with Jennifer Anistton and then Angelina Jolie. So the answer is: (1) Brad Pitt has been married 2 times; (2) Answer List: ["2"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Chris Evans (actor) | 2011–2017: Captain America and directorial debut:  aggregator Rotten Tomatoes gave the film an approval rating of 92% based on more than 350 reviews. The Avengers received an Academy Award nomination for Best Visual Effects and a British Academy Film Award (BAFTA) nomination for Best Special Visual Effects. For his last release of 2012, he played hitman Robert Pronge in the biographical film The Iceman, about the murderer Richard Kuklinski.
Question: Is Chris Evans most famous for iron man role?
Answer: No, Chris Evans is most famous for the role of Captain America, not Ironman. So the answer is: (1) Paraphrase Answer:  No, Chris Evans is most famous for the role of Captain America, not Ironman; (2) Answer List: ["No"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
        
    return prompt


def format_relate_prompt_blendqa(question, supporting_knowledge):
    prompt = f"""Please answer the question "{question}" using the retrieved knowledge from Wikipedia, Google, or Wikidata. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. When answering long lists such as album titles, directly write the list in your answer formulation. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Daniel Pudil | Daniel Pudil (born 27 September 1985) is a Czech professional footballer who plays for Viktoria Žižkov and the Czech Republic national team as a left back or left winger.
Google Results: [1]  ... 'personal_information': {{'place_of_birth': 'Prague, Czechoslovakia', 'height': '1.83 m (6 ft 0 in)', 'position_s': 'Left back, left winger'}} [2] Daniel Pudil - Wikidata | Daniel Pudil (2014) (Czech). 1 reference. imported from Wikimedia project ... place of birth · Prague. 1 reference. stated in ...
Question: In what region of the Czech was Daniel Pudil born?
Answer: Daniel Pudil was born in Prague. So the answer is: (1) Paraphrase Answer: Daniel Pudil was born in Prague; (2) Answer List: ["Prague"]

Retrieved Knowledge: 
Google Results: [1] Cape Verde 2-2 Egypt (Jan 22, 2024) Final Score | Cape Verde's Bryan Teixeira scored a 99th minute equaliser as they held record seven-time champions Egypt to a 2-2 Group B draw at the Africa Cup of Nations. [2] Cape Verde vs. Egypt - Final Score - January 22, 2024 | View the Cape Verde vs. Egypt game played on January 22, 2024. Box score, stats, odds, highlights, play-by-play, social & more.
Question: What was the final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and Cape Verde?
Answer: The final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and Cape Verde, is 2-2. So the answer is: (1) Paraphrase Answer: The final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and Cape Verde, is 2-2; (2) Answer List: ["2-2"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Kuhle Wampe | Kuhle Wampe (full title: Kuhle Wampe, oder: Wem gehört die Welt?, translated in English as Kuhle Wampe or Who Owns the World?, and released in the USA as Whither Germany? by Kinematrade Inc.) is a 1932 German feature film about unemployment, homelessness and left wing politics in the Weimar Republic produced by Prometheus Film. ... [2] Kuhle Wampe | Synopsis: On their return home by train, Anni, Fritz and other workers argue with middle-class, wealthy passengers about the worldwide financial crisis. 
Wikidata Query Results: Great Depression
Question: What is the economic crisis in Kuhle Wampe (German film)?
Answer: The economic crisis depicted in the German film Kuhle Wampe is the Great Depression. So the answer is: (1) Paraphrase Answer: The economic crisis in Kuhle Wampe (German film) is the Great Depression; (2) Answer List: ["Great Depression"]

Retrieved Knowledge: 
Google Results: [1] US overdoses have fallen sharply in recent months, a ... | A steep drop in deaths from fentanyl is a key factor driving the overall decline. Overdose deaths involving fentanyl and other synthetic ...
Question: What key factor is driving the overall decline in overdose deaths in Puebla?
Answer: The retrieved knowledge indicates that a "key factor driving the overall decline" is "a steep drop in deaths from fentanyl". So the answer is: (1) Paraphrase Answer: a key factor driving the overall decline is a steep drop in deaths from fentanyl; (2) Answer List: ["a steep drop in deaths from fentanyl"]

Retrieved Knowledge: 
Google Results: [1] American hiker found dead on South Africa's Table Mountain | The woman has been identified as a 20-year-old student from North Carolina named Brook Cheuvront. An American woman who went missing while on a hike on Table Mountain in Cape Town, South Africa, has died and her body has been recovered, authorities said on Monday.
Question: Was the body of the missing American hiker found in September 2024 on the Table mountain?
Answer: Yes, based on the retrieved knowledge, an American hiker was found dead on the Table mountain. So the answer is: (1) Paraphrase Answer: Yes, the body of the missing American hiker was found in September 2024 on the Table mountain; (2) Answer List: ["Yes"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Elbow | The elbow is the visible joint between the upper and lower parts of the arm. The elbow joint is the synovial hinge joint between the humerus in the upper arm and the radius and ulna in the forearm which allows the forearm and hand to be moved towards and away from the body. 
Question: What is the anatomical name for the body part associated with the Elbow?
Answer: Wikipedia Passage [1] suggests that the elbow is the "synovial hinge joint" between the humerus in the upper arm and the radius and ulna in the forearm. So the answer is: (1) Paraphrase Answer: The anatomical name for the our body part the Elbow is synovial hinge joint; (2) Answer List: ["synovial hinge joint"]

Retrieved Knowledge: 
Google Results: [1] Paris | Etymology:  \'City of Light\' (La Ville Lumière), both because of its leading role during the Age of Enlightenment and more literally because Paris was one of the first large European cities to use gas street lighting on a grand scale on its boulevards and monuments.
Question: Is Paris known as the city of Love?
Answer: No, Paris is known as the City of Light, not City of Love. So the answer is: (1) Paraphrase Answer: No, Paris is known as the City of Light, not City of Love; (2) Answer List: ["No"]

Retrieved Knowledge: 
Wikipedia Results: [1] The Rachel Maddow Show | Production:  The Rachel Maddow Show is broadcast from Studio 3-A at the NBC Studios, 30 Rockefeller Plaza in New York...
Question: Where is The Rachel Maddow Show broadcast from?
Answer: Wikipedia passage [1] suggests that The Rachel Maddow Show is broadcast from "Studio 3-A at the NBC Studios, 30 Rockefeller Plaza in New York". So the answer is: (1) Paraphrase Answer: The Rachel Maddow Show is broadcast from Studio 3-A at the NBC Studios, 30 Rockefeller Plaza in New York; (2) Answer List: ["Studio 3-A at the NBC Studios, 30 Rockefeller Plaza in New York"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
        
    return prompt


##### 3. Filter

def format_filter_prompt_hotpotqa(question, condition, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, Google, or Wikidata, please answer the following filter question "{question}". Formulate a list of entities as your final answer. If the provided passages does not provide helpful information, answer based on your own knowledge. When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". Answer the question with (1) a Paraphrase Answer that repeats the question's filter condition "{condition}", and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"

Retrieved Knowledge: 
Wikipedia Passages: [1] Autobahn (album) | "Autobahn (expressway) is the fourth studio album by German electronic band Kraftwerk, released in November 1974.  The 22-minute title track ""Autobahn"" was edited to 3:27 for single release and reached number 25 on the US ""Billboard"" Hot 100 chart, number 30 in the Australian chart, and performed even higher around Europe, reaching number 11 in the UK and number 12 in the Netherlands." ... [2] Electric Blue (song) | "Electric Blue" is a 1987 hit single by the Australian rock / synthpop band Icehouse and was co-written by Iva Davies of Icehouse and John Oates of the U.S. band Hall & Oates.  The single reached number one on the Australian singles chart on 16 November 1987, #7 on the American ""Billboard"" Hot 100 singles chart on 21 May 1988, #10 on the Canadian Singles Chart and #53 on the UK singles charts.  Released in August 1987, it was the second single from their number one album ""Man of Colours"" on Regular Records in Australia, and, with a slightly different cover, on Chrysalis Records for European and North American releases." ... [3] 25 or 6 to 4 | "25 or 6 to 4" is a song written by the American musician Robert Lamm, one of the founding members of the rock/jazz fusion band Chicago.  It was recorded in 1969 for their second album, ""Chicago"", with Peter Cetera on lead vocals.  The album was released in January 1970 and the song was edited and released as a single in June of that same year, climbing to number four on the U.S. ""Billboard"" Hot 100 chart and number seven on the UK Singles Chart." ... [4] Put Me in Your Mix | "Put Me in Your Mix is a 1991 album by R&B singer Barry White.  Regarded as a return to form, with exemplary slow jams, it was the second album of his comeback phase and contained the smash title track.  The album also contained production akin to contemporary R&B, featuring electronic instrumentation and, particularly, the presence of a Linn Drum combined with White’s traditional symphonic arrangements.  Glodean White sang back-up vocals, and Isaac Hayes sang duet on “Dark and Lovely (You over There).”  The album reached number 98 on the ""Billboard"" Hot 100 and number 8 on the ""Billboard"" top R&B albums chart."
Question: Which album among Kraftwerk, Kraftwerk 2, Ralf und Florian, Autobahn, Radio-Aktivität, Trans-Europe Express, The Man-Machine, Computer World, Electric Café, The Catalogue, Tour de France Soundtracks, Minimum-Maximum, The Mix reached number 25 on the US "Billboard" Hot 100 chart? (Filter condition: reached number 25 on the US "Billboard" Hot 100 chart)
Answer: Based on the Wikipedia passages, Autobahn (album), Electric Blue (song), 25 or 6 to 4, and Put Me in Your Mix all went on the US "Billboard" Hot 100 chart, but only "Autobahn (album)" reached exactly number 25 on the US ""Billboard"" Hot 100 chart. So the answer is: (1) Paraphrase Answer: Only "Autobahn (album)" reached number 25 on the US "Billboard" Hot 100 chart; (2) Answer List: ["Autobahn (album)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Predator 2 | "Predator 2 is a 1990 American science fiction action film written by brothers Jim and John Thomas, directed by Stephen Hopkins, and starring Danny Glover, Ruben Blades, Gary Busey, María Conchita Alonso, Bill Paxton and Kevin Peter Hall.  The film is a sequel to 1987\'s ""Predator"", with Peter Hall reprising the title role of the Predator." ... [2] The Saint of Fort Washington | The Saint of Fort Washington is a 1993 American drama film directed by Tim Hunter and starring Matt Dillon and Danny Glover.  Dillon won best actor at the 1993 Stockholm Film Festival for his performance ...
Question: Who among John Lithgow, Melinda Dillon, Don Ameche, David Suchet, Margaret Langrick, Joshua Rudoy, Lainie Kazan, Kevin Peter Hall worked with worked with Danny Glover? (Filter condition: worked with Danny Glover)
Answer: Wikipedia passage [1] indicates that film "Predator 2" stars both Danny Glover and Kevin Peter Hall. So the answer is: (1) Paraphrase Answer: "Kevin Peter Hall" worked with Danny Glover; (2) Answer List: ["Kevin Peter Hall"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Lady Mary Fox (née FitzClarence; 19 December 1798 – 13 July 1864) was an illegitimate daughter of King William IV of the United Kingdom by his mistress Dorothea Jordan.  In later life she became a writer. ... [2] Elizabeth Hay, Countess of Erroll (17 January 1801 – 16 January 1856; born Elizabeth FitzClarence) was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan.  She married William Hay, 18th Earl of Erroll, and became Countess of Erroll on 4 December 1820 at age 19.  Due to Hay's parentage, William Hay became Lord Steward of the Household.  Elizabeth and William Hay married at St George's, Hanover Square.  Hay is pictured in a FitzClarence family portrait in House of Dun and kept a stone thrown at her father William IV and the gloves he wore on opening his first Parliament as mementos.  She died in Edinburgh, Scotland. ... [3] William IV of Toulouse ( 1040 – 1094) was Count of Toulouse, Margrave of Provence, and Duke of Narbonne from 1061 to 1094.  He succeeded his father Pons of Toulouse upon his death in 1061.  His mother was Almodis de la Marche, but she was kidnapped by and subsequently married to Ramon Berenguer I, Count of Barcelona when William was a boy.  He was married to Emma of Mortain (daughter of Robert, Count of Mortain and a niece of William of Normandy), who gave him one daughter, Philippa.  He also had an illegitimate son, William-Jordan, with his half-sister Adelaide.
Question: Who is the illegitimate daughter of King William IV? (Filter condition: is illegitimate daughter of King William IV)
Answer: Based on the provide passages, the persons described by passages [1] and [2] are illegitimate daughters of King William IV, given Lady Mary Fox "was an illegitimate daughter of King William IV" and Elizabeth Hay, Countess of Erroll "was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan". So the answer is: (1) Paraphrase Answer: both "Lady Mary Fox" and "Elizabeth Hay, Countless of Erroll" are illegitimate daughters of King William IV; (2) Answer List: ["Lady Mary Fox", "Elizabeth Hay, Countess of Erroll"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


# deleted: When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". 
def format_filter_prompt_2wiki(question, condition, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, Google, or Wikidata, please answer the following filter question "{question}". Formulate a list of entities as your final answer. If the provided passages does not provide helpful information, answer based on your own knowledge. Answer the question with (1) a Paraphrase Answer that repeats the question's filter condition "{condition}", and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Predator 2 | "Predator 2 is a 1990 American science fiction action film written by brothers Jim and John Thomas, directed by Stephen Hopkins, and starring Danny Glover, Ruben Blades, Gary Busey, María Conchita Alonso, Bill Paxton and Kevin Peter Hall.  The film is a sequel to 1987\'s ""Predator"", with Peter Hall reprising the title role of the Predator." ... [2] The Saint of Fort Washington | The Saint of Fort Washington is a 1993 American drama film directed by Tim Hunter and starring Matt Dillon and Danny Glover.  Dillon won best actor at the 1993 Stockholm Film Festival for his performance ...
Question: Who among John Lithgow, Melinda Dillon, Don Ameche, David Suchet, Margaret Langrick, Joshua Rudoy, Lainie Kazan, Kevin Peter Hall worked with worked with Danny Glover? (Filter condition: worked with Danny Glover)
Answer: Wikipedia passage [1] indicates that film "Predator 2" stars both Danny Glover and Kevin Peter Hall. So the answer is: (1) Paraphrase Answer: "Kevin Peter Hall" worked with Danny Glover; (2) Answer List: ["Kevin Peter Hall"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Autobahn (album) | "Autobahn (expressway) is the fourth studio album by German electronic band Kraftwerk, released in November 1974.  The 22-minute title track ""Autobahn"" was edited to 3:27 for single release and reached number 25 on the US ""Billboard"" Hot 100 chart, number 30 in the Australian chart, and performed even higher around Europe, reaching number 11 in the UK and number 12 in the Netherlands." ... [2] Electric Blue (song) | "Electric Blue" is a 1987 hit single by the Australian rock / synthpop band Icehouse and was co-written by Iva Davies of Icehouse and John Oates of the U.S. band Hall & Oates.  The single reached number one on the Australian singles chart on 16 November 1987, #7 on the American ""Billboard"" Hot 100 singles chart on 21 May 1988, #10 on the Canadian Singles Chart and #53 on the UK singles charts.  Released in August 1987, it was the second single from their number one album ""Man of Colours"" on Regular Records in Australia, and, with a slightly different cover, on Chrysalis Records for European and North American releases." ... [3] 25 or 6 to 4 | "25 or 6 to 4" is a song written by the American musician Robert Lamm, one of the founding members of the rock/jazz fusion band Chicago.  It was recorded in 1969 for their second album, ""Chicago"", with Peter Cetera on lead vocals.  The album was released in January 1970 and the song was edited and released as a single in June of that same year, climbing to number four on the U.S. ""Billboard"" Hot 100 chart and number seven on the UK Singles Chart." ... [4] Put Me in Your Mix | "Put Me in Your Mix is a 1991 album by R&B singer Barry White.  Regarded as a return to form, with exemplary slow jams, it was the second album of his comeback phase and contained the smash title track.  The album also contained production akin to contemporary R&B, featuring electronic instrumentation and, particularly, the presence of a Linn Drum combined with White’s traditional symphonic arrangements.  Glodean White sang back-up vocals, and Isaac Hayes sang duet on “Dark and Lovely (You over There).”  The album reached number 98 on the ""Billboard"" Hot 100 and number 8 on the ""Billboard"" top R&B albums chart."
Question: Which album among Kraftwerk, Kraftwerk 2, Ralf und Florian, Autobahn, Radio-Aktivität, Trans-Europe Express, The Man-Machine, Computer World, Electric Café, The Catalogue, Tour de France Soundtracks, Minimum-Maximum, The Mix reached number 25 on the US "Billboard" Hot 100 chart? (Filter condition: reached number 25 on the US "Billboard" Hot 100 chart)
Answer: Based on the Wikipedia passages, Autobahn (album), Electric Blue (song), 25 or 6 to 4, and Put Me in Your Mix all went on the US "Billboard" Hot 100 chart, but only "Autobahn (album)" reached exactly number 25 on the US ""Billboard"" Hot 100 chart. So the answer is: (1) Paraphrase Answer: Only "Autobahn (album)" reached number 25 on the US "Billboard" Hot 100 chart; (2) Answer List: ["Autobahn (album)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Lady Mary Fox (née FitzClarence; 19 December 1798 – 13 July 1864) was an illegitimate daughter of King William IV of the United Kingdom by his mistress Dorothea Jordan.  In later life she became a writer. ... [2] Elizabeth Hay, Countess of Erroll (17 January 1801 – 16 January 1856; born Elizabeth FitzClarence) was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan.  She married William Hay, 18th Earl of Erroll, and became Countess of Erroll on 4 December 1820 at age 19.  Due to Hay's parentage, William Hay became Lord Steward of the Household.  Elizabeth and William Hay married at St George's, Hanover Square.  Hay is pictured in a FitzClarence family portrait in House of Dun and kept a stone thrown at her father William IV and the gloves he wore on opening his first Parliament as mementos.  She died in Edinburgh, Scotland. ... [3] William IV of Toulouse ( 1040 – 1094) was Count of Toulouse, Margrave of Provence, and Duke of Narbonne from 1061 to 1094.  He succeeded his father Pons of Toulouse upon his death in 1061.  His mother was Almodis de la Marche, but she was kidnapped by and subsequently married to Ramon Berenguer I, Count of Barcelona when William was a boy.  He was married to Emma of Mortain (daughter of Robert, Count of Mortain and a niece of William of Normandy), who gave him one daughter, Philippa.  He also had an illegitimate son, William-Jordan, with his half-sister Adelaide.
Question: Who is the illegitimate daughter of King William IV? (Filter condition: is illegitimate daughter of King William IV)
Answer: Based on the provide passages, the persons described by passages [1] and [2] are illegitimate daughters of King William IV, given Lady Mary Fox "was an illegitimate daughter of King William IV" and Elizabeth Hay, Countess of Erroll "was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan". So the answer is: (1) Paraphrase Answer: both "Lady Mary Fox" and "Elizabeth Hay, Countless of Erroll" are illegitimate daughters of King William IV; (2) Answer List: ["Lady Mary Fox", "Elizabeth Hay, Countess of Erroll"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_filter_prompt_musique(question, condition, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, Google, or Wikidata, please answer the following filter question "{question}". Formulate a list of entities as your final answer. If the provided passages does not provide helpful information, answer based on your own knowledge. Answer the question with (1) a Paraphrase Answer that repeats the question's filter condition "{condition}", and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Predator 2 | "Predator 2 is a 1990 American science fiction action film written by brothers Jim and John Thomas, directed by Stephen Hopkins, and starring Danny Glover, Ruben Blades, Gary Busey, María Conchita Alonso, Bill Paxton and Kevin Peter Hall.  The film is a sequel to 1987\'s ""Predator"", with Peter Hall reprising the title role of the Predator." ... [2] The Saint of Fort Washington | The Saint of Fort Washington is a 1993 American drama film directed by Tim Hunter and starring Matt Dillon and Danny Glover.  Dillon won best actor at the 1993 Stockholm Film Festival for his performance ...
Question: Who among John Lithgow, Melinda Dillon, Don Ameche, David Suchet, Margaret Langrick, Joshua Rudoy, Lainie Kazan, Kevin Peter Hall worked with worked with Danny Glover? (Filter condition: worked with Danny Glover)
Answer: Wikipedia passage [1] indicates that film "Predator 2" stars both Danny Glover and Kevin Peter Hall. So the answer is: (1) Paraphrase Answer: "Kevin Peter Hall" worked with Danny Glover; (2) Answer List: ["Kevin Peter Hall"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Autobahn (album) | "Autobahn (expressway) is the fourth studio album by German electronic band Kraftwerk, released in November 1974.  The 22-minute title track ""Autobahn"" was edited to 3:27 for single release and reached number 25 on the US ""Billboard"" Hot 100 chart, number 30 in the Australian chart, and performed even higher around Europe, reaching number 11 in the UK and number 12 in the Netherlands." ... [2] Electric Blue (song) | "Electric Blue" is a 1987 hit single by the Australian rock / synthpop band Icehouse and was co-written by Iva Davies of Icehouse and John Oates of the U.S. band Hall & Oates.  The single reached number one on the Australian singles chart on 16 November 1987, #7 on the American ""Billboard"" Hot 100 singles chart on 21 May 1988, #10 on the Canadian Singles Chart and #53 on the UK singles charts.  Released in August 1987, it was the second single from their number one album ""Man of Colours"" on Regular Records in Australia, and, with a slightly different cover, on Chrysalis Records for European and North American releases." ... [3] 25 or 6 to 4 | "25 or 6 to 4" is a song written by the American musician Robert Lamm, one of the founding members of the rock/jazz fusion band Chicago.  It was recorded in 1969 for their second album, ""Chicago"", with Peter Cetera on lead vocals.  The album was released in January 1970 and the song was edited and released as a single in June of that same year, climbing to number four on the U.S. ""Billboard"" Hot 100 chart and number seven on the UK Singles Chart." ... [4] Put Me in Your Mix | "Put Me in Your Mix is a 1991 album by R&B singer Barry White.  Regarded as a return to form, with exemplary slow jams, it was the second album of his comeback phase and contained the smash title track.  The album also contained production akin to contemporary R&B, featuring electronic instrumentation and, particularly, the presence of a Linn Drum combined with White’s traditional symphonic arrangements.  Glodean White sang back-up vocals, and Isaac Hayes sang duet on “Dark and Lovely (You over There).”  The album reached number 98 on the ""Billboard"" Hot 100 and number 8 on the ""Billboard"" top R&B albums chart."
Question: Which album among Kraftwerk, Kraftwerk 2, Ralf und Florian, Autobahn, Radio-Aktivität, Trans-Europe Express, The Man-Machine, Computer World, Electric Café, The Catalogue, Tour de France Soundtracks, Minimum-Maximum, The Mix reached number 25 on the US "Billboard" Hot 100 chart? (Filter condition: reached number 25 on the US "Billboard" Hot 100 chart)
Answer: Based on the Wikipedia passages, Autobahn (album), Electric Blue (song), 25 or 6 to 4, and Put Me in Your Mix all went on the US "Billboard" Hot 100 chart, but only "Autobahn (album)" reached exactly number 25 on the US ""Billboard"" Hot 100 chart. So the answer is: (1) Paraphrase Answer: Only "Autobahn (album)" reached number 25 on the US "Billboard" Hot 100 chart; (2) Answer List: ["Autobahn (album)"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Lady Mary Fox (née FitzClarence; 19 December 1798 – 13 July 1864) was an illegitimate daughter of King William IV of the United Kingdom by his mistress Dorothea Jordan.  In later life she became a writer. ... [2] Elizabeth Hay, Countess of Erroll (17 January 1801 – 16 January 1856; born Elizabeth FitzClarence) was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan.  She married William Hay, 18th Earl of Erroll, and became Countess of Erroll on 4 December 1820 at age 19.  Due to Hay's parentage, William Hay became Lord Steward of the Household.  Elizabeth and William Hay married at St George's, Hanover Square.  Hay is pictured in a FitzClarence family portrait in House of Dun and kept a stone thrown at her father William IV and the gloves he wore on opening his first Parliament as mementos.  She died in Edinburgh, Scotland. ... [3] William IV of Toulouse ( 1040 – 1094) was Count of Toulouse, Margrave of Provence, and Duke of Narbonne from 1061 to 1094.  He succeeded his father Pons of Toulouse upon his death in 1061.  His mother was Almodis de la Marche, but she was kidnapped by and subsequently married to Ramon Berenguer I, Count of Barcelona when William was a boy.  He was married to Emma of Mortain (daughter of Robert, Count of Mortain and a niece of William of Normandy), who gave him one daughter, Philippa.  He also had an illegitimate son, William-Jordan, with his half-sister Adelaide.
Question: Who is the illegitimate daughter of King William IV? (Filter condition: is illegitimate daughter of King William IV)
Answer: Based on the provide passages, the persons described by passages [1] and [2] are illegitimate daughters of King William IV, given Lady Mary Fox "was an illegitimate daughter of King William IV" and Elizabeth Hay, Countess of Erroll "was an illegitimate daughter of King William IV of the United Kingdom and Dorothea Jordan". So the answer is: (1) Paraphrase Answer: both "Lady Mary Fox" and "Elizabeth Hay, Countless of Erroll" are illegitimate daughters of King William IV; (2) Answer List: ["Lady Mary Fox", "Elizabeth Hay, Countess of Erroll"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_filter_prompt_crag(question, condition, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, Google, or Wikidata, please answer the following filter question "{question}". Formulate a list of entities as your final answer. If the provided passages does not provide helpful information, answer based on your own knowledge. Answer the question with (1) a Paraphrase Answer that repeats the question's filter condition "{condition}", and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Pulitzer Prize for Music | History:  guidelines and jury membership will serve that end.” Subsequently, in 2006, a posthumous "Special Citation" was given to jazz composer Thelonious Monk, and in 2007 the prize went to Ornette Coleman, a free jazz composer, who won the prize for his disc Sound Grammar, a recording of a 2005 concert, making it the first time a recording won the music Pulitzer, and a first for purely improvised music. In 2018, rapper Kendrick Lamar won the award for his 2017 hip hop album Damn. The recording was the first musical work not in the jazz or classical genres to win the prize. ... [2] Collected Poems of Robert Frost | Reception:  Frost received a Pulitzer prize in 1931 for the collection. One of the books in the collection, New Hampshire, had received the Pulitzer Prize in 1924...
Question: Which of Damn, Damn. Collector's Edition won the Pulitzer Prize?
Answer: Wikipedia passage [1] suggests that "in 2018, rapper Kendrick Lamar won the award for his 2017 hip hop album Damn", so the album Damn won the Pulitzer Prize. So the answer is: (1) Paraphrase Answer: Damn won the Pulitzer Prize; (2) Answer List: ["Damn"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Mechanical Bull Tour | Setlist: 1) "Charmer" ; 2) "Rock City" ; 3) "My Party" ; 4) "Temple" ; 5) "On Call" ; 6) "Family Tree" ; 7) "Closer" ; 8) "The Immortals" ; 9) "Back Down South" ; 10) "Wait for Me" ; 11) "Supersoaker" ; 12) "Milk" ; 13) "Pyro" ; 14) "Tonight" ; 15) "Radioactive" ; 16) "The Bucket" ; 17) "Don't Matter" ; 18) "Molly's Chambers" ; 19) "Four Kicks" ; 20) "Be Somebody" ; 21) "Notion" ; 22) "Cold Desert" ; 23) "Use Somebody" ; Encore ; 1) "Crawl" ; 2) "Black Thumbnail" ; 3) "Sex on Fire" ... [2] Mechanical Bull (album) | Promotion:  love and fighting," and a "distant cousin of U2's With or Without You". "Beautiful War" and "Don't Matter" were released as singles exclusively in the United Kingdom on December 9, 2013 and June 16, 2014 respectively. "Family Tree" was sent to US modern rock radio as the album's sixth overall single on June 17, 2014...
Question: Among Mechanical Bull, Come Around Sundown, Because of the Times, which album includes the songs "Wait for Me" and "Family Tree"?
Answer: The album Mechanical Bull includes the songs "Wait for Me" and "Family Tree". So the answer is: (1) Paraphrase Answer: Mechanical Bull includes the songs "Wait for Me" and "Family Tree"; (2) Answer List: ["Mechanical Bull"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt


def format_filter_prompt_blendqa(question, condition, supporting_knowledge):
    prompt = f"""Using the retrieved knowledge from Wikipedia, Google, or Wikidata, please answer the following filter question "{question}". Formulate a list of entities as your final answer. If the provided passages does not provide helpful information, answer based on your own knowledge. Answer the question with (1) a Paraphrase Answer that repeats the question's filter condition "{condition}", and (2) a clean python Answer List. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Retrieved Knowledge: 
Wikipedia Passages: [1] Pulitzer Prize for Music | History:  guidelines and jury membership will serve that end.” Subsequently, in 2006, a posthumous "Special Citation" was given to jazz composer Thelonious Monk, and in 2007 the prize went to Ornette Coleman, a free jazz composer, who won the prize for his disc Sound Grammar, a recording of a 2005 concert, making it the first time a recording won the music Pulitzer, and a first for purely improvised music. In 2018, rapper Kendrick Lamar won the award for his 2017 hip hop album Damn. The recording was the first musical work not in the jazz or classical genres to win the prize. ... [2] Collected Poems of Robert Frost | Reception:  Frost received a Pulitzer prize in 1931 for the collection. One of the books in the collection, New Hampshire, had received the Pulitzer Prize in 1924...
Question: Which of Damn, Damn. Collector's Edition won the Pulitzer Prize?
Answer: Wikipedia passage [1] suggests that "in 2018, rapper Kendrick Lamar won the award for his 2017 hip hop album Damn", so the album Damn won the Pulitzer Prize. So the answer is: (1) Paraphrase Answer: Damn won the Pulitzer Prize; (2) Answer List: ["Damn"]

Retrieved Knowledge: 
Wikipedia Passages: [1] Mechanical Bull Tour | Setlist: 1) "Charmer" ; 2) "Rock City" ; 3) "My Party" ; 4) "Temple" ; 5) "On Call" ; 6) "Family Tree" ; 7) "Closer" ; 8) "The Immortals" ; 9) "Back Down South" ; 10) "Wait for Me" ; 11) "Supersoaker" ; 12) "Milk" ; 13) "Pyro" ; 14) "Tonight" ; 15) "Radioactive" ; 16) "The Bucket" ; 17) "Don't Matter" ; 18) "Molly's Chambers" ; 19) "Four Kicks" ; 20) "Be Somebody" ; 21) "Notion" ; 22) "Cold Desert" ; 23) "Use Somebody" ; Encore ; 1) "Crawl" ; 2) "Black Thumbnail" ; 3) "Sex on Fire" ... [2] Mechanical Bull (album) | Promotion:  love and fighting," and a "distant cousin of U2's With or Without You". "Beautiful War" and "Don't Matter" were released as singles exclusively in the United Kingdom on December 9, 2013 and June 16, 2014 respectively. "Family Tree" was sent to US modern rock radio as the album's sixth overall single on June 17, 2014...
Question: Among Mechanical Bull, Come Around Sundown, Because of the Times, which album includes the songs "Wait for Me" and "Family Tree"?
Answer: The album Mechanical Bull includes the songs "Wait for Me" and "Family Tree". So the answer is: (1) Paraphrase Answer: Mechanical Bull includes the songs "Wait for Me" and "Family Tree"; (2) Answer List: ["Mechanical Bull"]

Your Question.
Retrieved Knowledge: """
    
    if "Text" in supporting_knowledge:
        prompt += f"\nWikipedia Passages: {supporting_knowledge['Text']}"
    if "Web" in supporting_knowledge:
        prompt += f"\nGoogle Results: {supporting_knowledge['Web']}"
    if "KB" in supporting_knowledge:
        prompt += f"\nWikidata Query Results: {supporting_knowledge['KB']}"
    
    prompt += f"""\nQuestion: {question}\nAnswer: """
    
    return prompt




# def format_intersection_prompt(question, entity_list_1, entity_list_2):
#     prompt = f"""Answer the intersection question "{question}" given two entity lists. Determine what entities are included in both lists. Strictly follow the format of the examples below, ending your answer with 'So the answer is: [entity_list]'
#     Examples.
#     List1: ["the Atlantic Ocean and the Great South Bay of Long Island"]
#     List2: ["Long Island", "Fire Island"]
#     Question: 
#     Answer: The entity "Long Island" appears in both lists. So the answer is: ["Long Island"]
   
#     List1: ["A Knight's Tale", "40 Days and 40 Nights", "The Rules of Attraction", "The Order", "Kiss Kiss Bang Bang", "The Holiday"]
#     List2: ["40 Days and 40 Nights", "Meet the Applegates"]
#     Question: What film is in both [2] and [3]?
#     Answer: The film "40 Days and 40 Nights" appears in both lists. So the answer is: ["40 Days and 40 Nights"]
    
#     List1: ["Ravenna, Italy"]
#     List2: ["Ravenna", "Pavia"]
#     Answer: The entity "Ravenna" appears in both lists. So the answer is: ["Ravenna"]
    
#     Your Question.
#     List1: {entity_list_1}
#     List2: {entity_list_2}
#     Answer: """
    
#     return prompt


##################################################################
### Prompt for obtaining recursive answer from child questions ###
##################################################################

# Child questions and answers: 
# Q: 1. Who starred in "My Dog Skip"? A: ['Frankie Muniz', 'Diane Lane', 'Luke Wilson', 'Kevin Bacon']
# Q: 2. Who starred in "Malcolm in the Middle"? A: ['Christopher Kennedy Masterson', 'Jane Frances Kaczmarek', 'Justin Tyler Berfield']
# Q: 3. Who is among both [1] and [2]? A: No actor is among both "My Dog Skip" and "Malcolm in the Middle". []
# Question: Who starred in My Dog Skip and Malcolm in the Middle?
# Answer: The child questions and answers indicate that no actor is among both "My Dog Skip" and "Malcolm in the Middle", so the answer is unknown. So the answer is: (1) Paraphrase Answer: Unknown; (2) Answer List: []

def format_answer_from_child_qa_pairs_prompt_hotpotqa(question, child_qa_pairs):  
    
    str_child_qa_pairs = ""
    for qa_pair in child_qa_pairs:
        (q, a), = qa_pair.items()
        str_child_qa_pairs += f"Q: {q} A: {a}\n"    
    
    prompt = f"""The complex question "{question}" has been divided into child questions. Based on the child questions and answers, answer the complex question. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: [].  When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]""
Examples.
Child questions and answers: 
Q: 3. When was Cha Cha Cohen formed? A: ["1994"]
Q: 4. When was Swervedriver formed? A: ["1989"]
Question: Given answers of [3] and [4], which band formed first?
Answer: Swervedriver formed in 1989, which is before Cha Cha Cohen's forming date 1994. So the answer is: (1) Paraphrase Answer: Swervedriver formed first; (2) Answer List: ["Swervedriver"]

Child questions and answers: 
Q: 1. What is the 2004 Hockey film? A: ["Miracle (2004 film)"]
Q: 2. Who produced [1]? A: It is unknown who produced "Miracle (2004 film)". ["Unknown"]
Q: 3. Who played the USA coach in [1]? A: Kurt Russell played the USA coach in "Miracle (2004 film)". ["Kurt Russell"]
Question: in the 2004 Hockey film produced by a former major league baseball pitcher who played the USA coach?
Answer: The 2004 Hockey film is "Miracle (2004 film)", the actor of the USA coach in the film is "Kurt Russell", and my own knowledge indicates that Miracle (2004 film) is indeed produced by former baseball pitcher Gavin O'Connor. So the answer is: (1) Paraphrase Answer: Kurt Russell played the USA coach in in the 2004 Hockey film "Miracle (2004 film)" produced by a former major league baseball pitcher; (2) Answer List: ["Kurt Russell"]

Child questions and answers:
Q: 1. Is Leycesteria native to Australia? A: ["No"]
Q: 2. Is Anigozanthos native to Australia? A: ["Yes"]
Question: Are both Leycesteria and Anigozanthos native to Australia?
Answer: Anigozanthos is native to Australia, but Leycesteria is not. So the answer is: (1) Paraphrase Answer: No, Leycesteria and Anigozanthos are not both native to Australia. (2) Answer List: ["No"]

Child questions and answers: 
Q: 1. Who is Caleb Stegall? A: ["Caleb Stegall"]
Q: 2. What county did [1] serve as District attorney in? A: Caleb Stegall served as district attorney in Jefferson County. ["Jefferson County"]
Q: 3. What is the most populous city in [2]? A: The most populous city in Jefferson County is Birmingham, Lakewood, or Valley Falls depending on the specific county. ["Birmingham", "Lakewood", "Valley Falls"]
Question: What is the most populous city in the county where Caleb Stegall served as District attorney?
Answer: Child question 3 indicates that the most populous city in Jefferson County is "Birmingham", "Lakewood", or "Valley Falls" depending on the specific county. So the answer is: (1) Paraphrase Answer: The most populous city in the county where Caleb Stegall served as District attorney is Birmingham, Lakewood, or Valley Falls depending on the specific county; (2) Answer List: ["Birmingham", "Lakewood", "Valley Falls"]

Child questions and answers: 
Q: 1. Who is Richard Melville Hall? A: ["Moby"]
Q: 2. What studio albums did [1] release? A: Unknown. [""]
Q: 3. Which album in [2] was the third released? A: It seems there is insufficient information directly provided from the child questions and answers to determine the third album. [""]
Question: What was the third studio album released by Richard Melville Hall?
Answer: Richard Melville Hall, known as Moby, released his third studio album titled "Everything Is Wrong." So the answer is: (1) Paraphrase Answer: The third studio album released by Richard Melville Hall, known as Moby, is "Everything Is Wrong"; (2) Answer List: ["Everything Is Wrong"]

Child questions and answers: 
Q: 1. What movie stars Katrina Bowden? A: ['Sex Drive', 'Piranha 3DD', 'Scary Movie 5']
Q: 2. What movie was directed by Sean Anders? A: ["Daddy\'s Home", "Instant Family"]
Q: 3. What is the common movie between [1] and [2]? A: There is no common movie. []
Question: What is the name of the movie that stars Katrina Bowden and was directed by Sean Anders?
Answer: The child questions and answers indicate that there is no common movie between those starring Katrina Bowden and those directed by Sean Anders. However, my own knowledge suggests that the movie "Sex Drive" stars Katrina Bowden and was directed by Sean Anders. So the answer is: (1) Paraphrase Answer: The movie "Sex Drive" stars Katrina Bowden and was directed by Sean Anders; (2) Answer List: ["Sex Drive"]

Your question.
Child questions and answers:
{str_child_qa_pairs}
Question: {question}
Answer: """
    
    return prompt


# deleted: When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". 
def format_answer_from_child_qa_pairs_prompt_2wiki(question, child_qa_pairs):  
    str_child_qa_pairs = ""
    for qa_pair in child_qa_pairs:
        (q, a), = qa_pair.items()
        str_child_qa_pairs += f"Q: {q} A: {a}\n"    
    
    prompt = f"""The complex question "{question}" has been divided into child questions. Based on the child questions and answers, answer the complex question. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]""
Examples.
Child questions and answers: 
Q: 1. Who is Viacheslav I Of Kiev? A: ["Viacheslav I of Kiev"]
Q: 2. Who is the mother of [1]? A: The mother of Viacheslav I of Kiev is Gytha of Wessex. ["Gytha of Wessex"]
Q: 3. Who is the father of [2]? A: The father of Gytha of Wessex is Harold Godwinson. ["Harold Godwinson"]
Question: Who is Viacheslav I Of Kiev's maternal grandfather?
Answer: The maternal grandfather of Viacheslav I Of Kiev is the father of Gytha of Wessex, who is Harold Godwinson. So the answer is: (1) Paraphrase Answer: Viacheslav I Of Kiev's maternal grandfather is Harold Godwinson; (2) Answer List: ["Harold Godwinson"]

Child questions and answers: 
Q: 1. When was the song Come With Me (Pure Imagination) released? A: ["February 19, 2016"]
Q: 2. When was the song Hold On Me (Grinspoon Song) released? A: ["February 21, 2005", "June 20, 2012"]
Question: Which song was released more recently, Come With Me (Pure Imagination) or Hold On Me (Grinspoon Song)?
Answer: The song "Come With Me (Pure Imagination)" was released on February 19, 2016, which is more recent than both release dates of "Hold On Me (Grinspoon Song)" on February 21, 2005 and June 20, 2012. So the answer is: (1) Paraphrase Answer: Come With Me (Pure Imagination) was released more recently; (2) Answer List: ["Come With Me (Pure Imagination)"]

Child questions and answers: 
Q: 1. Who is the director of the film Begrijpt U Nu Waarom Ik Huil? A: The director of the film Begrijpt U Nu Waarom Ik Huil is Louis van Gasteren. ["Louis van Gasteren"]
Q: 2. Who is the director of the film We Faw Down? A: The director of the film We Faw Down is Leo McCarey. ["Leo McCarey"]
Q: 3. When did [1] die? A: Louis van Gasteren died on 10 May 2016. ["10 May 2016"]
Q: 4. When did [2] die?' A: Leo McCarey died on July 5, 1969. ["July 5, 1969"]
Question: Given answers of [3] and [4], which film has the director who died later?
Answer: Louis van Gasteren died on 10 May 2016, and Leo McCarey died on July 5, 1969. So the director who died later is Louis van Gasteren, and the film is Begrijpt U Nu Waarom Ik Huil. So the answer is: (1) Paraphrase Answer: The film with the director who died later is Begrijpt U Nu Waarom Ik Huil; (2) Answer List: ["Begrijpt U Nu Waarom Ik Huil"]

Child questions and answers: 
Q: 1. Who is Elizabeth Stuart, Countess Of Lennox's husband? A: ["Charles Stuart, 1st Earl of Lennox"]
Q: 5. Who is [1]? A: Charles Stuart, 1st Earl of Lennox refers to the husband of Elizabeth Stuart, Countess of Lennox, and the father of Arbella Stuart. ["Charles Stuart, 1st Earl of Lennox"]
Q: 6. Who is [5]'s mother? A: Charles Stuart, 1st Earl of Lennox's mother is Margaret Douglas. ["Margaret Douglas"]
Question: Who is [1]'s mother?
Answer: Question "5. Who is [1]?" disambiguates that [1] is "Charles Stuart, 1st Earl of Lennox". So the mother of [1] is the mother of Charles Stuart, 1st Earl of Lennox, which is Margaret Douglas. So the answer is: (1) Paraphrase Answer: Margaret Douglas is [1]'s mother; (2) Answer List: ["Margaret Douglas"]

Child questions and answers: 
Q: 1. What movie stars Katrina Bowden? A: ['Sex Drive', 'Piranha 3DD', 'Scary Movie 5']
Q: 2. What movie was directed by Sean Anders? A: ["Daddy's Home", "Instant Family"]
Q: 3. What is the common movie between [1] and [2]? A: There is no common movie. []
Question: What is the name of the movie that stars Katrina Bowden and was directed by Sean Anders?
Answer: The child questions and answers indicate that there is no common movie between those starring Katrina Bowden and those directed by Sean Anders. However, my own knowledge suggests that the movie "Sex Drive" stars Katrina Bowden and was directed by Sean Anders. So the answer is: (1) Paraphrase Answer: The movie "Sex Drive" stars Katrina Bowden and was directed by Sean Anders; (2) Answer List: ["Sex Drive"]

Your question.
Child questions and answers:
{str_child_qa_pairs}
Question: {question}
Answer: """
    
    return prompt


# deleted: When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". 
def format_answer_from_child_qa_pairs_prompt_musique(question, child_qa_pairs):  
    str_child_qa_pairs = ""
    for qa_pair in child_qa_pairs:
        (q, a), = qa_pair.items()
        str_child_qa_pairs += f"Q: {q} A: {a}\n"    
    
    prompt = f"""The complex question "{question}" has been divided into child questions. Based on the child questions and answers, answer the complex question. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]""
Examples.
Child questions and answers: 
Q: 3. What is Pizza Man? A: ["The Pizza Man (American Thoroughbred racehorse)", "Pizza Man (1991 comedy film)"]
Q: 4. Who is [3]'s cast member? A: Pizza Man (1991 comedy film)'s cast member are Bill Maher and Annabelle Gurwitch. ["Bill Maher", "Annabelle Gurwitch"]
Question: Who is the Pizza Man cast member?
Answer: The Pizza Man cast members are Bill Maher and Annabelle Gurwitch. So the answer is: (1) Paraphrase Answer: The Pizza Man cast members are Bill Maher and Annabelle Gurwitch; (2) Answer List: ["Bill Maher", "Annabelle Gurwitch"]

Child questions and answers: 
Q: 1. Who is the Queen of England in 1890? A: ["Queen Victoria"]
Q: 2. What is the station that aired High Feather? A: ["PBS"]
Q: 3. Who is the actress who plays [1] on [2]? A: The actress who plays Queen Victoria on PBS is Jenna Coleman. ["Jenna Coleman"]
Question: Who is the actress who plays the Queen of England in 1890 on the station that aired High Feather?
Answer: The actress who plays the Queen of England in 1890 on the station that aired High Feather is Jenna Coleman. So the answer is: (1) Paraphrase Answer: Jenna Coleman plays the Queen of England in 1890 on the station that aired High Feather; (2) Answer List: ["Jenna Coleman"]

Child questions and answers: 
Q: 1. In which city is WOCA located? A: ["Ocala", "Metropolitan Milwaukee"]
Q: 2. [1] is in which part of Florida? A: Ocala is located in the northern region of Florida; Metropolitan Milwaukee is not in Florida.["northern region of Florida"]
Question: The city where WOCA is located is in which part of Florida?
Answer: WOCA is located in Ocala, which is in the northern region of Florida. So the answer is: (1) Paraphrase Answer: The city where WOCA is located is in the northern region of Florida; (2) Answer List: ["northern region of Florida"]

Your question.
Child questions and answers:
{str_child_qa_pairs}
Question: {question}
Answer: """
    
    return prompt


# deleted: When answering people's names, always answer with the full name, i.e. answer "Alan Mathison Turing" instead of "Alan Turing". 
def format_answer_from_child_qa_pairs_prompt_crag(question, child_qa_pairs):  
    str_child_qa_pairs = ""
    for qa_pair in child_qa_pairs:
        (q, a), = qa_pair.items()
        str_child_qa_pairs += f"Q: {q} A: {a}\n"    
    
    prompt = f"""The complex question "{question}" has been divided into child questions. Based on the child questions and answers, answer the complex question. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Child questions and answers: 
Q: 1. When did Next Friday's release? A: ["January 12, 2000"]
Q: 2. What was Mike Epps's age at the time of [1]? A: Mike Epp was 29 years old at January 12, 2000. ["29"]
Question: What was Mike Epps's age at the time of Next Friday's release?
Answer: Mike Epp's age at the time of Next Friday's release, January 12, 2000, was 29 years old. So the answer is: (1) Paraphrase Answer:  Mike Epps's age at the time of Next Friday's release was 29 years old; (2) Answer List: ["29"]

Child questions and answers: 
Q: 1. What albums did Lady Gaga release in 2009? A: ["The Fame Monster", "Hitmixes", "The Cherrytree Sessions", "Attention Deficit"]
Q: 2. Among [1], which album included the songs \"Bad Romance\" and \"Telephone\"? A: The Fame Monster includes the songs \"Bad Romance\" and \"Telephone\". ["The Fame Monster"]
Question: What album did lady gaga release in 2009, which included the songs \"bad romance\" and \"telephone\"?
Answer: Lady Gaga released the album "The Fame Monster" in 2009, which included the songs \"bad romance\" and \"telephone\". So the answer is: (1) Paraphrase Answer: Lady Gaga released the album "The Fame Monster" in 2009, which included the songs \"bad romance\" and \"telephone\"; (2) Answer List: ["The Fame Monster"]

Child questions and answers: 
Q: 1. What are long-term capital gains? A: ["long-term capital gains (profits earned from the sale of assets held for more than a year)"]
Q: 2. What are short-term capital gains? A: ["short-term capital gains ( profits realized from the sale of assets held for one year or less)"]
Question: 3. Given answers of [1] and [2], what is their difference? 
Answer: Based on the child answers, the difference between long-term capital gains and short-term capital gains is that long-term capital gains are profits from assets held for more than a year, while short-term capital gains are profits from assets held for one year or less. In addition, my own knowledge suggests that long-term capital gains are subject to a lower tax rate compared to short-term capital gains. So the answer is: (1) Paraphrase Answer: The difference between long-term capital gains and short-term capital gains is that long-term capital gains are profits from assets held for more than a year with a lower tax rate, while between long-term capital gains and short-term capital gains is that long-term capital gains are profits from assets held for more than a year with a higher tax rate; (2) Answer List: ["The difference between long-term capital gains and short-term capital gains is that long-term capital gains are profits from assets held for more than a year with a lower tax rate, while between long-term capital gains and short-term capital gains is that long-term capital gains are profits from assets held for more than a year with a higher tax rate"]

Child questions and answers: 
Q: 1. How many oscars did the movie Lincoln win? A: ["2"]
Q: 2. How many oscars did the movie The Girl with the Dragon Tattoo win? A: ["1"]
Q: 3. Given answers of [1] and [2], which movie won the most Oscars? A: Lincoln won the most Oscars. ["Lincoln"]
Question: What movie won the most Oscars, Lincoln or The Girl with the Dragon Tattoo?
Answer: The movie Lincoln won 2 Oscars, while The Girl with the Dragon Tattoo only won 1, so Lincoln won the most Oscars. So the answer is: (1) Paraphrase Answer: The movie Lincoln won the most Oscars; (2) Answer List: ["Lincoln"]

Child questions and answers: 
Q: 1. How many games did Brooklyn Nets win in 2022? ["44"]
Q: 2. How many games did Boston Celtics win in 2022? ["51"]
Question: 3. Given answers of [1] and [2], did Brooklyn Nets win more games than Boston Celtics?
Answer: The Brooklyn Nets only won 44 games, which is less than Boston Celtics 51 wins. So the answer is: (1) Paraphrase Answer: No, Brooklyn Nets did not win more games than Boston Celtics; (2) Answer List: ["No"]

Your question.
Child questions and answers:
{str_child_qa_pairs}
Question: {question}
Answer: """
    
    return prompt


def format_answer_from_child_qa_pairs_prompt_blendqa(question, child_qa_pairs):  
    str_child_qa_pairs = ""
    for qa_pair in child_qa_pairs:
        (q, a), = qa_pair.items()
        str_child_qa_pairs += f"Q: {q} A: {a}\n"    
    
    prompt = f"""The complex question "{question}" has been divided into child questions. Based on the child questions and answers, answer the complex question. Answer the question with (1) a Paraphrase Answer that repeats the question, and (2) a clean python Answer List. If the provided information is not enough to answer the question, answer based on your own knowledge. If neither the provided knowledge nor your own knowledge can answer the question, end your answer with (1) Paraphrase Answer: Unknown; (2) Answer List: []. When answering with numbers, always use arabic numbers i.e. 1,2,3. When answering to "Yes" or "No" questions, simply formulate your Answer list as ["Yes"] or ["No"]. Strictly follow the format of the examples below, ending your answer with "So the answer is: (1) Paraphrase Answer: {{paraphrase_answer}}; (2) Answer List: [answer_list]"
Examples.
Child questions and answers: 
Q: 1. What is the television series that is a notable work of Christian Lee Navarro? A: ["13 Reasons Why"]
Q: 2. Who has 2 tapes in [1]? A: Justin Foley has 2 tapes in 13 Reasons Why. ["Justin Foley"]
Question: Who has 2 tapes in the television series that is a notable work of Christian Lee Navarro?
Answer: Justin Foley has 2 tapes in the television series that is a notable work of Christian Lee Navarro, 13 Reasons Why. So the answer is: (1) Paraphrase Answer: Justin Foley has 2 tapes in the television series that is a notable work of Christian Lee Navarro, 13 Reasons Why; (2) Answer List: ["Justin Foley"]

Child questions and answers: 
Q: 3. What is Praia? A: ["Praia, Cape Verde (city)", "Praia, Cape Verde (municipality)"]
Q: 4. What is the island nation where [3] is located? A: The island nation where Praia, Cape Verde (city) is located is Cape Verde; The island nation where Praia, Cape Verde (municipality) is located is Cape Verde. ["Cape Verde", "Cape Verde"]
Question: What is the island nation where Praia is located?
Answer: Praia is located in Cape Verde. So the answer is: (1) Paraphrase Answer: Praia is located in Cape Verde; (2) Answer List: ["Cape Verde"]

Child questions and answers: 
Q: 1. In what region of the Czech was Daniel Pudil born? A: ["Prague"]
Q: 2. How many people were killed in the mass shooting in [1] on December 21, 2023? A: On December 21, 2023, at least 14 people were killed in the mass shooting in Prague. ["14"]
Question: How many people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born on December 21, 2023?
Answer: On December 21, 2023, 14 people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born. So the answer is: (1) Paraphrase Answer: 14 people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born on December 21, 2023; (2) Answer List: ["14"]

Child questions and answers: 
Q: 1. What mountain is part of the new7wonders of nature? A: ["Table Mountain"]
Q: 2. Was the body of the missing American hiker found in September 2024 on [1]? A: Yes, the body of the missing American hiker found in September 2024 on the Table Mountain. ["Yes"]
Question: Was the body of the missing American hiker found in September 2024 on the mountain that is part of the new7wonders of nature?
Answer: Yes, the body of the missing American hiker was found in September 2024 on the mountain that is part of the new7wonders of nature, Table Mountain. So the answer is: (1) Paraphrase Answer: Yes, the body of the missing American hiker was found in September 2024 on the mountain that is part of the new7wonders of nature, Table Mountain; (2) Answer List: ["Yes"]

Your question.
Child questions and answers:
{str_child_qa_pairs}
Question: {question}
Answer: """
    
    return prompt