
""" 
    HotpotQA 
"""

# Question 503, Search+Relate, medium
hotpotqa_ex1_q = "What was the largest passenger capacity of the plane type used for BOAC Flight 911?"
hotpotqa_ex1 = """{"What was the largest passenger capacity of the plane type used for BOAC Flight 911?": ["1. What was the plane type used for BOAC Flight 911?", "2. What was the largest passenger capacity of [1]?"], "1. What was the plane type used for BOAC Flight 911?": ["3. What is BOAC Flight 911?", "4. What is the plane type used for [3]?"], "3. What is BOAC Flight 911?": "Search(\"BOAC Flight 911\")", "4. What is the plane type used for [3]?": "Relate([3], \"plane type\")", "2. What was the largest passenger capacity of [1]?": "Relate([1], \"largest passenger capacity\")"}"""
# ex1 = """{"What was the largest passenger capacity of the plane type used for BOAC Flight 911?": ["1. What was the plane type used for BOAC Flight 911?", "2. What was the largest passenger capacity of [1]?"], "1. What was the plane type used for BOAC Flight 911?": "Relate(\"BOAC Flight 911\", \"plane type\")", "2. What was the largest passenger capacity of [1]?": "Relate([1], \"largest passenger capacity\")"}"""

# Question 501, Search+Relate, medium
hotpotqa_ex2_q = "Who was the film which was Kim Dae-woo's directing debut about?"
hotpotqa_ex2 = """{"Who was the film which was Kim Dae-woo's directing debut about?": ["1. What is Kim Dae-woo's directing debut film?", "2. Who was [1] about?"], "1. What is Kim Dae-woo's directing debut film?": ["3. Who is Kim Dae-woo?", "4. What is [3]'s directing debut film?"], "3. Who is Kim Dae-woo?": "Search(\"Kim Dae-woo\", \"film director\")", "4. What is [3]'s directing debut film?": "Relate(\"Kim Dae-woo\", \"directing debut film\")", "2. Who was [1] about?": "Relate([1], \"about person\")"}"""
# ex2 = """{"Who was the film which was Kim Dae-woo's directing debut about?": ["1. What is Kim Dae-woo's directing debut film?", "2. Who was [1] about?"], "1. What is Kim Dae-woo's directing debut film?": "Relate(\"Kim Dae-woo\", \"directing debut film\")", "2. Who was [1] about?": "Relate([1], \"about person\")"}"""

# Question 502, Search+Relate, medium, unusual search parameter
hotpotqa_ex3_q = "Which city was the man who is known for a science humor story based on the tongue-in-cheek combination of two adages born in?"
hotpotqa_ex3 = """{"Which city was the man who is known for a science humor story based on the tongue-in-cheek combination of two adages born in?": ["1. Who is the man known for a science humor story based on the tongue-in-cheek combination of two adages?", "2. In which city was [1] born?"], "1. Who is the man known for a science humor story based on the tongue-in-cheek combination of two adages?": ["3. What is a science humor story based on the tongue-in-cheek combination of two adages?", "4. Who is the man known for [3]?"], "3. What is a science humor story based on the tongue-in-cheek combination of two adages?": "Search(\"science humor story based on the tongue-in-cheek combination of two adages\")", "4. Who is the man known for [3]?": "Relate([3], \"man known for\")", "2. In which city was [1] born?": "Relate([1], \"born in city\")"}"""

# Question 504, challenging, Search+Relate+Filter
hotpotqa_ex4_q = "What is the birthday of this Anglo-Irish actress, courtean, and mistress, who was the mother to the illegitimate daughter of King William IV?"
hotpotqa_ex4 = """{"What is the birthday of this Anglo-Irish actress, courtesan, and mistress, who was the mother to the illegitimate daughter of King William IV?": ["1. Who is the Anglo-Irish actress, courtesan, and mistress who was the mother to the illegitimate daughter of King William IV?", "2. What is the birthday of [1]?"], "1. Who is the Anglo-Irish actress, courtesan, and mistress who was the mother to the illegitimate daughter of King William IV?": ["3. Who was the mother to the illegitimate daughter of King William IV?", "4. Among [3], who is an Anglo-Irish actress, courtesan, and mistress?"], "3. Who was the mother to the illegitimate daughter of King William IV?": ["5. Who was King William IV?", "6. Who was the illegitimate daughter of [5]?", "7. Who was the mother to [6]?"], "5. Who was King William IV?": "Search(\"King William IV\")", "6. Who was the illegitimate daughter of [5]?": "Relate([5], \"illegitimate daughter\")", "7. Who was the mother to [6]?": "Relate([6], \"mother\")", "4. Among [3], who is an Anglo-Irish actress, courtesan, and mistress?": "Filter([3], \"Anglo-Irish actress, courtesan, and mistress\")", "2. What is the birthday of [1]?": "Relate([1], \"birthday\")"}"""

# Question 505, medium, Search+Relate, 暂时从prompt去掉（节省运算时间）
hotpotqa_ex5_q = "During which years was the model of car, featured on the cover of Earth's \"Pentastar: In the Style of Demons\" manufactured?"
hotpotqa_ex5 = """{"During which years was the model of car, featured on the cover of Earth's \"Pentastar: In the Style of Demons\" manufactured?": ["1. What model of car was featured on the cover of Earth's \"Pentastar: In the Style of Demons\"?", "2. During which years was [1] manufactured?"], "1. What model of car was featured on the cover of Earth's \"Pentastar: In the Style of Demons\"?": ["3. What is Earth's \"Pentastar: In the Style of Demons\"?", "4. What model of car was featured on [3]'s cover?"], "3. What is Earth's \"Pentastar: In the Style of Demons\"?": "Search(\"Pentastar: In the Style of Demons\", \"Earth's\")", "4. What model of car was featured on [3]'s cover?": "Relate([3], \"model of car featured on cover\")", "2. During which years was [1] manufactured?": "Relate([1], \"was manufactured during years\")"}"""

# Question 7405, medium, Search+Relate, 暂时从prompt去掉（节省运算时间）
hotpotqa_ex6_q = "Blackfin is a family of processors developed by the company that is headquartered in what city?"
hotpotqa_ex6 = """{"Blackfin is a family of processors developed by the company that is headquartered in what city?": ["1. Which company developed the Blackfin family of processors?", "2. In which city is [1] headquartered?"], "1. Which company developed the Blackfin family of processors?": ["3. What is the Blackfin family of processors?", "4. Which company developed [3]?"], "3. What is the Blackfin family of processors?": "Search(\"Blackfin\", \"family of processors\")", "4. Which company developed [3]?": "Relate([3], \"is developed by company\")", "2. In which city is [1] headquartered?": "Relate([1], \"is headquartered in city\")"}"""

# Question 7404, comparison question, Search+Relate, 暂时从prompt去掉（节省运算时间）
hotpotqa_ex7_q = "Were both of the following rock groups formed in California: Dig and Thinking Fellers Union Local 282?"
# ex7 = """{"Were both of the following rock groups formed in California: Dig and Thinking Fellers Union Local 282?": ["1. Where was the rock group Dig formed?", "2. Where was the rock group Thinking Fellers Union Local 282 formed?", "3. Given answers of [1] and [2], were both rock groups formed in California?"], "1. Where was the rock group Dig formed?": ["4. What is the rock group Dig?", "5. Where was [3] formed?"], "4. What is the rock group Dig?": "Search(\"Dig\", \"rock group\")", "5. Where was [4] formed?": "Relate([4], \"was formed at location\")", "2. Where was the rock group Thinking Fellers Union Local 282 formed?": ["6. What is the rock group Thinking Fellers Union Local 282?", "7. Where was [6] formed?"], "6. What is the rock group Thinking Fellers Union Local 282?": "Search(\"Thinking Fellers Union Local 282\", \"rock group\")", "7. Where was [6] formed?": "Relate([6], \"was formed at location\")", "3. Given answers of [1] and [2], were both rock groups formed in California?": "[END]"}"""
hotpotqa_ex7 = {"Were both of the following rock groups formed in California: Dig and Thinking Fellers Union Local 282?": ["1. Was the rock group Dig formed in California?", "2. Was the rock group Thinking Fellers Union Local 282 formed in California?"], "1. Was the rock group Dig formed in California?": ["3. What is the rock group Dig?", "4. Was [3] formed in California?"], "3. What is the rock group Dig?": "Search(\"Dig\", \"rock group\")", "4. Was [3] formed in California?": "Relate([3], \"was formed in California\")", "2. Was the rock group Thinking Fellers Union Local 282 formed in California?": ["5. What is the rock group Thinking Fellers Union Local 282?", "6. Was [5] formed in California?"], "5. What is the rock group Thinking Fellers Union Local 282?": "Search(\"Thinking Fellers Union Local 282\", \"rock group\")", "6. Was [5] formed in California?": "Relate([5], \"was formed in California\")"}

# Question 7403, comparison, search+relate
hotpotqa_ex8_q = "Are Billy and Barak both breeds of scenthound? (Barak is also known as a Bosnian Coarse-haired Hound)?"
# ex8 = """{"Are Billy and Barak both breeds of scenthound? (Barak is also known as a Bosnian Coarse-haired Hound)": ["1. Is Billy a breed of scenthound?", "2. Is Barack (also known as a Bosnian Coarse-haired Hound) a breed of scenthound?", "3. Given answers of [1] and [2], are Billy and Barak both breeds of scenthound?"], "1. Is Billy a breed of scenthound?": ["4. What is Billy?", "5. What breed is [3]?"], "4. What is Billy?": "Search(\"Billy\", \"dog\")", "5. What breed is [3]?": "Relate([3], \"is breed\")", "2. Is Barack (also known as a Bosnian Coarse-haired Hound) a breed of scenthound?": ["6. What is Barack (also known as a Bosnian Coarse-haired Hound)?", "7. What breed is [5]?"], "5. What is Barack (also known as a Bosnian Coarse-haired Hound)?": "Search(\"Barack (also known as a Bosnian Coarse-haired Hound)\", \"dog\")", "6. What breed is [5]?": "Relate([5], \"is breed\")", "3. Given answers of [1] and [2], are Billy and Barak both breeds of scenthound?": "[END]"}"""
hotpotqa_ex8 = """{"Are Billy and Barak both breeds of scenthound? (Barak is also known as a Bosnian Coarse-haired Hound)": ["1. Is Billy a breed of scenthound?", "2. Is Barack (also known as a Bosnian Coarse-haired Hound) a breed of scenthound?"], "1. Is Billy a breed of scenthound?": ["3. What is Billy?", "4. What breed is [3]?"], "3. What is Billy?": "Search(\"Billy\", \"dog\")", "4. What breed is [3]?": "Relate([3], \"is breed\")", "2. Is Barack (also known as a Bosnian Coarse-haired Hound) a breed of scenthound?": ["5. What is Barack (also known as a Bosnian Coarse-haired Hound)?", "6. What breed is [5]?"], "5. What is Barack (also known as a Bosnian Coarse-haired Hound)?": "Search(\"Barack (also known as a Bosnian Coarse-haired Hound)\", \"dog\")", "6. What breed is [5]?": "Relate([5], \"is breed\")"}"""

# Question 7402, comparison, search+relate, 暂时从prompt去掉（节省运算时间）
hotpotqa_ex9_q = "Are both Volvic and Canfield's Diet Chocolate Fudge natural spring waters?"
hotpotqa_ex9 = """{"Are both Volvic and Canfield's Diet Chocolate Fudge natural spring waters?": ["1. Is Volvic a natural spring water?", "2. Is Canfield's Diet Chocolate Fudge a natural spring water?", "3. Given answers of [1] and [2], are both Volvic and Canfield's Diet Chocolate Fudge natural spring waters?"], "1. Is Volvic a natural spring water?": ["4. What is Volvic?", "5. Is [3] a natural spring water?"], "4. What is Volvic?": "Search(\"Volvic\", \"water\")", "5. Is [3] a natural spring water?": "Relate([3], \"is natural spring water\")", "2. Is Canfield's Diet Chocolate Fudge a natural spring water?": ["6. What is Canfield's Diet Chocolate Fudge?", "7. Is [5] a natural spring water?"], "5. What is Canfield's Diet Chocolate Fudge?": "Search(\"Canfield's Diet Chocolate Fudge\")", "6. Is [5] a natural spring water?": "Relate([5], \"is natural spring water\")", "3. Given answers of [1] and [2], are both Volvic and Canfield's Diet Chocolate Fudge natural spring waters?": "[END]"}"""

# Question 7401, challenging, search+relate+filter
hotpotqa_ex10_q = "What Pakistani actor and writer from Islamabad helped write for the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?"
# ex10 = """{"What Pakistani actor and writer from Islamabad helped write for the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?": ["1. What is the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?", "2. Who helped write for [1]?", "3. Who is the Pakistani actor and writer from Islamabad among [2]?"], "1. What is the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?": "Search(\"Coke Kahani\", \"2012 Pakistani comedy drama sitcom\")", "2. Who helped write for [1]?": "Relate([1], \"writers\")", "3. Who is the Pakistani actor and writer from Islamabad among [2]?": ["4. Among [2], who is a Pakistani actor and writer from Islamad?"], "4. Among [2], who is a Pakistani actor and writer from Islamad?": "Filter([2], \"Pakistani actor and writer from Islamabad\")"}"""
hotpotqa_ex10 = """{"What Pakistani actor and writer from Islamabad helped write for the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?": ["1. What is the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?", "2. Who helped write for [1]?", "3. Who is the Pakistani actor and writer from Islamabad among [2]?"], "1. What is the 2012 Pakistani comedy drama sitcom, \"Coke Kahani\"?": "Search(\"Coke Kahani\", \"2012 Pakistani comedy drama sitcom\")", "2. Who helped write for [1]?": "Relate([1], \"writers\")", "3. Who is the Pakistani actor and writer from Islamabad among [2]?": "Filter([2], \"Pakistani actor and writer from Islamabad\")"}"""

# medium, search+relate+intersection, but intersection also doable as [END] judement (and actually more robust), 暂时从prompt去掉（节省运算时间）
hotpotqa_ex11_q = "Margaret Wilson and Edna St. Vincent Millay have both been given what?"
hotpotqa_ex11 = """{"Margaret Wilson and Edna St. Vincent Millay have both been given what?": ["1. What was given to Margaret Wilson?", "2. What was given to Edna St. Vincent Millay?", "3. Given answers of [1] and [2], what has been given to both?"], "1. What was given to Margaret Wilson?": ["4. Who is Margaret Wilson?", "5. What prize was given to Maragaret Wilson?"], "4. Who is Margaret Wilson?": "Search(\"Margaret Wilson\")", "5. What prize was given to Maragaret Wilson?": "Relate(\"Margaret Wilson\", \"prize given\")", "2. What was given to Edna St. Vincent Millay?": ["6. Who is Edna St. Vincent Millay?", "7. What prize was given to Edna St. Vincent Millay?"], "6. Who is Edna St. Vincent Millay?": "Search(\"Edna St. Vincent Millay\")", "7. What prize was given to Edna St. Vincent Millay?": "Relate(\"Edna St. Vincent Millay\", \"prize given\")", "3. Given answers of [1] and [2], what has been given to both?": "[END]"}"""

# medium, search+relate+intersection,（intersection已删）
hotpotqa_ex12_q = "In which city have Gary Ayres and Neil Craig both been head coach of the Crows?"
hotpotqa_ex12 = """{"In which city have Gary Ayres and Neil Craig both been head coach of the Crows?": ["1. Who is Gary Ayres?", "2. Who is Neil Craig?", "3. What is the Crows?", "4. In which city has [1] been head coach of [3]?", "5. In which city has [2] been head coach of [3]?", "6. Given answers of [4] and [5], in which city have Gary Ayres and Neil Craig both been head coach of the Crows?"], "1. Who is Gary Ayres?": "Search(\"Gary Ayres\", \"Australian rules football coach\")", "2. Who is Neil Craig?": "Search(\"Neil Craig\", \"Australian rules football coach\")", "3. What is the Crows?": "Search(\"the Crows\", \"Australian rules football club\")", "4. In which city has [1] been head coach of [3]?": "Relate([1], \"was head coach of [3] in city\")", "5. In which city has [2] been head coach of [3]?": "Relate([2], \"was head coach of [3] in city\")", "6. Given answers of [4] and [5], in which city have Gary Ayres and Neil Craig both been head coach of the Crows?": "[END]"}"""

# challenging, search+relate+filter或intersect或root judge都可以, 这里标的是llama自己分解的root judge, 暂时从prompt去掉（节省运算时间）
hotpotqa_ex13_q = "Who was the head of the Imperial Family that was making an broadcast announcement of Japan's surrender in 1945?"
hotpotqa_ex13 = """{"Who was the head of the Imperial Family that was making an broadcast announcement of Japan's surrender in 1945?": ["1. What is the Imperial Family of Japan?", "2. Who was the head of [1] in 1945?", "3. Who made the broadcast announcement of Japan's surrender in 1945?", "4. Given answers of [2] and [3], is [2] the same as [3]?"], "1. What is the Imperial Family of Japan?": "Search(\"Imperial Family of Japan\")", "2. Who was the head of [1] in 1945?": ["5. Who was the head of [1]?", "6. Was [5] the head in 1945?"], "5. Who was the head of [1]?": "Relate([1], \"head\")", "6. Was [5] the head in 1945?": "Relate([5], \"head in 1945\")", "3. Who made the broadcast announcement of Japan's surrender in 1945?": ["7. What is the broadcast announcement of Japan's surrender in 1945?", "8. Who made [7]?"], "7. What is the broadcast announcement of Japan's surrender in 1945?": "Search(\"broadcast announcement of Japan's surrender in 1945\")", "8. Who made [7]?": "Relate([7], \"made by\")", "4. Given answers of [2] and [3], is [2] the same as [3]?": "[END]"}"""

# medium, search+relate, 暂时从prompt去掉（节省运算时间）
hotpotqa_ex14_q = "The city in which the Cloverdale Fairgrounds are located is a member municipality of which regional district?"
hotpotqa_ex14 = """{"The city in which the Cloverdale Fairgrounds are located is a member municipality of which regional district?": ["1. What is the city in which the Cloverdale Fairgrounds are located?", "2. What regional district is [1] a member municipality of?"], "1. What is the city in which the Cloverdale Fairgrounds are located?": ["3. What are the Cloverdale Fairgrounds?", "4. In what city are [3] located in?"], "3. What are the Cloverdale Fairgrounds?": "Search(\"the Cloverdale Fairgrounds\")","4. In what city are [3] located in?": "Relate([3], \"are located in city\")", "2. What regional district is [1] a member municipality of?": "Relate([1], \"is a member municipality of regional district\")"}"""

# judge/comparison question, trick question to seem to look like intersection
hotpotqa_ex15_q = "Have Marc Rosset and Max Mirnyi both been professional tennis players?"
# ex15 = """{"Have Marc Rosset and Max Mirnyi both been professional tennis players?": ["1. Has Marc Rosset been a professional tennis player?", "2. Has Max Mirnyi been a professional tennis player?", "3. Given answers of [1] and [2], have Marc Rosset and Max Mirnyi both been professional tennis players?"], "1. Has Marc Rosset been a professional tennis player?": ["4. Who is Marc Rosset?", "5. Have [4] been a professional tennis player?"], "4. Who is Marc Rosset?": "Search(\"Marc Rosset\")", "5. Have [4] been a professional tennis player?": "Relate([4], \"is professional tennis player\")", "2. Has Max Mirnyi been a professional tennis player?": ["6. Who is Max Mirnyi?", "7. Has [6] been a professional tennis player?"], "6. Who is Max Mirnyi?": "Search(\"Max Mirnyi\", \"tennis player\")", "7. Has [6] been a professional tennis player?": "Relate([6], \"is professional tennis player\")", "3. Given answers of [1] and [2], have Marc Rosset and Max Mirnyi both been professional tennis players?": "[END]"}"""
hotpotqa_ex15 = """{"Have Marc Rosset and Max Mirnyi both been professional tennis players?": ["1. Has Marc Rosset been a professional tennis player?", "2. Has Max Mirnyi been a professional tennis player?"], "1. Has Marc Rosset been a professional tennis player?": ["3. Who is Marc Rosset?", "4. Have [3] been a professional tennis player?"], "3. Who is Marc Rosset?": "Search(\"Marc Rosset\")", "4. Have [3] been a professional tennis player?": "Relate([3], \"is professional tennis player\")", "2. Has Max Mirnyi been a professional tennis player?": ["5. Who is Max Mirnyi?", "6. Has [5] been a professional tennis player?"], "5. Who is Max Mirnyi?": "Search(\"Max Mirnyi\")", "6. Has [5] been a professional tennis player?": "Relate([5], \"is professional tennis player\")"}"""

# challenging, search+relate+intersect, 但question2的gt passage在hotpotqa这个corpus上似乎找不到
hotpotqa_ex16_q = "What baseball team, part of the ten-school collegiate athletic conference headquartered in Irving, Texas, was coached by Randy Mazey in 2016?"
hotpotqa_ex16 = """{"What baseball team, part of the ten-school collegiate athletic conference headquartered in Irving, Texas, was coached by Randy Mazey in 2016?": ["1. What is the ten-school collegiate athletic conference headquartered in Irving, Texas?", "2. What baseball teams are part of [1]?", "3. What baseball team was coached by Randy Mazey in 2016?", "4. Given Answers of [2] and [3], what baseball team belongs to both?"], "1. What is the ten-school collegiate athletic conference headquartered in Irving, Texas?": "Search(\"ten-school collegiate athletic conference headquartered in Irving, Texas\")", "2. What baseball teams are part of [1]?": "Relate([1], \"baseball team\")", "3. What baseball team was coached by Randy Mazey in 2016?": "Relate(\"baseball team\", \"coached by Randy Mazey in 2016\")", "4. Given Answers of [2] and [3], what baseball team belongs to both?": "[END]"}"""

# 问题内有冗余信息
hotpotqa_ex17_q = "George Gershwin is an American Composer and Judith Weir is a composer from which country?"
hotpotqa_ex17 = """{"George Gershwin is an American Composer and Judith Weir is a composer from which country?": ["1. Who is George Gershwin?", "2. Who is Judith Weir?", "3. What country is [2] from?"], "1. Who is George Gershwin?": "Search(\"George Gershwin\", \"American composer\")", "2. Who is Judith Weir?": "Search(\"Judith Weir\", \"composer\")", "3. What country is [2] from?": "Relate([2], \"is from country\")"}"""

# 简单or选择题
hotpotqa_ex18_q = "Which goalkeeper was nicknamed the \"Black Spider\", Turgay \u015eeren or Lev Yashin?"
# ex18 = """{"Which goalkeeper was nicknamed the \"Black Spider\", Turgay Şeren or Lev Yashin?": ["1. Is goalkeeper Turgay Şeren nicknamed the \"Black Spider\"?", "2. Is goalkeeper Lev Yashin nicknamed the \"Black Spider\"?", "3. Given answers of [1] and [2], which goalkeeper was nicknamed the \"Black Spider\"?"], "1. Is goalkeeper Turgay Şeren nicknamed the \"Black Spider\"?": ["4. Who is goalkeeper Turgay Şeren?", "5. Is [4] nicknamed the \"Black Spider\"?"], "4. Who is goalkeeper Turgay Şeren?": "Search(\"Turgay Şeren\", \"goalkeeper\")", "5. Is [4] nicknamed the \"Black Spider\"?": "Relate([4], \"has nickname Black Spider\")", "2. Is goalkeeper Lev Yashin nicknamed the \"Black Spider\"?": ["6. Who is goalkeeper Lev Yashin?", "7. Is [6] nicknamed the \"Black Spider\"?"], "6. Who is goalkeeper Lev Yashin?": "Search(\"Lev Yashin\", \"goalkeeper\")", "7. Is [6] nicknamed the \"Black Spider\"?": "Relate([6], \"has nickname Black Spider\")", "3. Given answers of [1] and [2], which goalkeeper was nicknamed the \"Black Spider\"?": "[END]"}"""
hotpotqa_ex18 = """{"Which goalkeeper was nicknamed the \"Black Spider\", Turgay Şeren or Lev Yashin?": ["1. Is goalkeeper Turgay Şeren nicknamed the \"Black Spider\"?", "2. Is goalkeeper Lev Yashin nicknamed the \"Black Spider\"?"], "1. Is goalkeeper Turgay Şeren nicknamed the \"Black Spider\"?": ["3. Who is goalkeeper Turgay Şeren?", "4. Is [3] nicknamed the \"Black Spider\"?"], "4. Who is goalkeeper Turgay Şeren?": "Search(\"Turgay Şeren\", \"goalkeeper\")", "5. Is [4] nicknamed the \"Black Spider\"?": "Relate([4], \"has nickname Black Spider\")", "2. Is goalkeeper Lev Yashin nicknamed the \"Black Spider\"?": ["5. Who is goalkeeper Lev Yashin?", "6. Is [5] nicknamed the \"Black Spider\"?"], "5. Who is goalkeeper Lev Yashin?": "Search(\"Lev Yashin\", \"goalkeeper\")", "6. Is [5] nicknamed the \"Black Spider\"?": "Relate([6], \"has nickname Black Spider\")"}"""

# 容易过度分解的问题
hotpotqa_ex19_q = "What company did a man who hired Sioux Falls architect Wallace L. Dow to build a home in Worthing, Minnesota found?"
hotpotqa_ex19 = """{"What company did a man who hired Sioux Falls architect Wallace L. Dow to build a home in Worthing, Minnesota found?": ["1. Who is the man who hired Sioux Falls architect Wallace L. Dow to build a home in Worthing, Minnesota?", "2. What company did [1] found?"], "1. Who is the man who hired Sioux Falls architect Wallace L. Dow to build a home in Worthing, Minnesota?": ["3. Who is Sioux Falls architect Wallace L. Dow?", "4. Who hired [3] to build a home in Worthing, Minnesota?"], "3. Who is Sioux Falls architect Wallace L. Dow?": "Search(\"Wallace L. Dow\", \"Sioux Falls architect\")", "4. Who hired [3] to build a home in Worthing, Minnesota?": "Relate([3], \"was hired to build home in Worthing, Minnesota by person\")", "2. What company did [1] found?": "Relate([1], \"founded company\")"}"""

# 复杂or选择题
hotpotqa_ex20_q = "Radio shack made a line of computers in the 1980's which was marketed as the TRS-80 Color Computer or the Interact Home Computer?"
# ex20 = """{"Radio shack made a line of computers in the 1980's which was marketed as the TRS-80 Color Computer or the Interact Home Computer?": ["1. What is Radio shack?", "2. What line of computers did [1] make in the 1980s?", "3. What was the marketing name of [2]?", "4. Given answers of [2] and [3], was the line of computers marketed as the TRS-80 Color Computer or the Interact Home Computer?"], "1. What is Radio shack?": "Search(\"Radio Shack\")", "2. What line of computers did [1] make in the 1980s?": "Relate([1], \"made line of computers in 1980s\")", "3. What was the marketing name of [2]?": "Relate([2], \"marketing name\")", "3. Given answers of [2] and [3], was the line of computers marketed as the TRS-80 Color Computer or the Interact Home Computer?": "[END]"}"""
hotpotqa_ex20 = """{"Radio shack made a line of computers in the 1980's which was marketed as the TRS-80 Color Computer or the Interact Home Computer?": ["1. What line of computers did Radio shack make in the 1980s?", "2. What was the marketing name of [1]?", "3. Given answers of [2] and [3], was the line of computers marketed as the TRS-80 Color Computer or the Interact Home Computer?"], "1. What line of computers did Radio shack make in the 1980s?": ["3. What is Radio shack?", "4. What line of computers did [3] make in the 1980s?"], "3. What is Radio shack?": "Search(\"Radio shack\")", "4. What line of computers did [3] make in the 1980s?": "Relate([3], \"made line of computers in 1980s\")", "2. What was the marketing name of [1]?": "Relate([1], \"marketing name\")", "3. Given answers of [1] and [2], was the line of computers marketed as the TRS-80 Color Computer or the Interact Home Computer?": "[END]"}"""

# gpt4o bad case & llama3 good case
hotpotqa_ex21_q = "Baraki Barak District is situated in the western part of a province whose capital is what?"
hotpotqa_ex21 = """{"Baraki Barak District is situated in the western part of a province whose capital is what?": ["1. What province is Baraki Barak District situated in?", "2. What is the capital of [1]?"], "1. What province is Baraki Barak District situated in?": ["3. What is Baraki Barak District?", "4. What province is [3] situated in?"], "3. What is Baraki Barak District?": "Search(\"Baraki Barak District\")", "4. What province is [3] situated in?": "Relate([3], \"is situated in province\")", "2. What is the capital of [1]?": "Relate([1], \"capital\")"}}"""

# gpt4o bad case & llama3 good case
hotpotqa_ex22_q = "What was the former name of the stadium, from 1997-2017, where the Aztecs play?"
hotpotqa_ex22 = """{"What was the former name of the stadium, from 1997-2017, where the Aztecs play?": ["1. What is the stadium where the Aztecs play?", "2. What was the former name of [1] from 1997-2017?"], "1. What is the stadium where the Aztecs play?": ["3. Who are the Aztecs?", "4. What is the stadium where [3] play?"], "3. Who are the Aztecs?": "Search(\"Aztecs\", \"sports team\")", "4. What is the stadium where [3] play?": "Relate([3], \"plays at stadium\")", "2. What was the former name of [1] from 1997-2017?": "Relate([1], \"had former name from 1997-2017\")"}"""

# gpt4o bad case & llama3 good case
hotpotqa_ex23_q = "Oak Beach, New York and Great South Bay are both situated between what same island?"
hotpotqa_ex23 =  """{"Oak Beach, New York and Great South Bay are both situated between what same island?": ["1. What is Oak Beach, New York situated between?", "2. What is Great South Bay situated between?", "3. Given answers of [1] and [2], what same island are they situated between?"], "1. What is Oak Beach, New York situated between?": ["4. What is Oak Beach, New York?", "5. What is [4] situated between?"], "4. What is Oak Beach, New York?": "Search(\"Oak Beach, New York\")", "5. What is [4] situated between?": "Relate([4], \"situated between\")", "2. What is Great South Bay situated between?": ["6. What is Great South Bay?", "7. What is [6] situated between?"], "6. What is Great South Bay?": "Search(\"Great South Bay\")", "7. What is [6] situated between?": "Relate([6], \"situated between\")", "3. Given answers of [1] and [2], what same island are they situated between?": "[END]"}"""

# gpt4o bad case & llama3 good case
hotpotqa_ex24_q = "What was the third studio album released by Richard Melville Hall?"
hotpotqa_ex24 = """{"What was the third studio album released by Richard Melville Hall?": ["1. Who is Richard Melville Hall?", "2. What are the studio albums released by [1]?", "3. What is the third studio album among [2]?"], "1. Who is Richard Melville Hall?": "Search(\"Richard Melville Hall\")", "2. What are the studio albums released by [1]?": "Relate([1], \"studio albums\")", "3. What is the third studio album among [2]?": "Filter([2], \"third studio album\")"}"""

# gpt4o bad case & llama3 good case
hotpotqa_ex25_q = "Who acted in the film and television series, \"Harry and the Hendersons,\" and also worked with Danny Glover?"
hotpotqa_ex25 = """{"Who acted in the film and television series, \"Harry and the Hendersons,\" and also worked with Danny Glover?": ["1. Who acted in the film and television series, \"Harry and the Hendersons\"?", "2. Who among [1] also worked with Danny Glover?"], "1. Who acted in the film and television series, \"Harry and the Hendersons\"?": ["3. What is the film and television series, \"Harry and the Hendersons\"?", "4. Who acted in [3]?"], "3. What is the film and television series, \"Harry and the Hendersons\"?": "Search(\"Harry and the Hendersons\", \"film and television series\")", "4. Who acted in [3]?": "Relate([3], \"actors\")", "2. Who among [1] also worked with Danny Glover?": "Filter([1], \"worked with Danny Glover\")"}"""


# prompt with Intersection()
# def format_tree_generation_prompt_hotpotqa(question):
#     hotpotqa_prompt = f"""You are given 4 atomic functions to help you retrieve and operate knowledge from Wikipedia:
#     1. Search(). Input: (name, [optional]descriptor). Output: (entity, abstract). This function helps you find and disambiguate an entity by inputting its name and optional descriptor. If no descriptor is provided, the most popular entity will be returned. For example, Search(\"Michael Jordan\") returns the famous basketball player "Michael Jordan" and his short abstract, while Search(\"Michael Jordan\", football goalkeeper) returns the English retired football goalkeeper "Michael Jordan (footballer)" and his short abstract.
#     2. Relate(). Input: there are 2 input format possibilities, (head_entity, relation), or (head_entity, tail_entity). Output: list(head_entity, relation, tail_entity). This function helps you find the tail_entity given a head_entity and relation, or a relation given a head_entity and tail_entity. For example, Relate(\"Barack Obama\", \"spouse\") returns \"Michelle Obama\", and Relate(\"Barack Obama\", \"Michelle Obama\") returns \"spouse\". You may also search attribute relations using Relate() by treating attributes as tail entities. For example, Relate(\"Barack Obama\", \"time served as US president\") returns \"1997 to 2004\", and Relate(\"Barack Obama\", \"1961\")" returns \"year of birth\".
#     3. Filter(). Input: (list(entities), condition). Output: list(entities). This function helps you filter out entities that satisfy a factual attribute condition. For example, Filter([\"Lionel Messi\", \"Steven Jobs\", \"Bill Gates\"], \"is American\"), returns [\"Bill Gates\"], and Filter([\"Lionel Messi\", \"Cristiano Ronaldo\"], \"is football player\") returns [\"Lionel Messi\", \"Cristiano Ronaldo\"].
#     4. Intersection(). Input: (list(entities), list(entities)). Output: list(entities). This function helps you find the intersection of two entity lists, returning entities that exist in both lists. 
#     Construct a hierarchical question decomposition tree in json format for the following complex question: \"{question}\". The tree starts with the original complex question as the root node, and each non-root node is a sub-question of its parent. Continue decomposing until a sub-question cannot be further decomposed and could either be: (1) directly answered with one of the four atomic functions Search(), Relate(), Filter(), Intersection(), or (2) directly answered given the answers of previous questions from the same layer of the tree. In case (1), write this sub-question with its corresponding function call as a leaf node. In case (2), write this sub-question with an [END] mark as a leaf node.
#     Examples: 
#     Question: {list(ex1.keys())[0]}
#     Decomposition Tree: {str(ex1)}
#     Question: {list(ex2.keys())[0]}
#     Decomposition Tree: {str(ex2)}
#     Question: {list(ex3.keys())[0]}
#     Decomposition Tree: {str(ex3)}
#     Question: {list(ex4.keys())[0]}
#     Decomposition Tree: {str(ex4)}
#     Question: {list(ex8.keys())[0]}
#     Decomposition Tree: {str(ex8)}
#     Question: {list(ex10.keys())[0]}
#     Decomposition Tree: {str(ex10)}
#     Question: {list(ex12.keys())[0]}
#     Decomposition Tree: {str(ex12)}
#     Question: {list(ex15.keys())[0]}
#     Decomposition Tree: {str(ex15)}
#     Question: {list(ex16.keys())[0]}
#     Decomposition Tree: {str(ex16)}
#     Question: {list(ex17.keys())[0]}
#     Decomposition Tree: {str(ex17)}
#     Question: {list(ex18.keys())[0]}
#     Decomposition Tree: {str(ex18)}
#     Question: {list(ex19.keys())[0]}
#     Decomposition Tree: {str(ex19)}
#     Question: {list(ex20.keys())[0]}
#     Decomposition Tree: {str(ex20)}
    
#     Your Question.
#     Question: {question}
#     Decomposition Tree: """
    
#     return hotpotqa_prompt


# prompt without Intersection()
# Search补充prompt：You should call Search() if the target entity is ambiguous and requires entity disambiguation.
def format_tree_generation_prompt_hotpotqa(question):
    prompt = f"""You are given 3 atomic functions to help you retrieve and operate knowledge from Wikipedia:
1. Search(). Input: (name, [optional] descriptor). Output: list[entities]. This function helps you find and disambiguate an entity given its name and optional descriptor. If no descriptor is provided, the most popular entity will be returned. For example, Search(\"Michael Jordan\") returns the famous basketball player ["Michael Jordan"], while Search(\"Michael Jordan\", \"football goalkeeper\") returns the English retired football goalkeeper ["Michael Jordan (footballer)"]. 
2. Relate(). Input: there are 2 input possibilities, (head_entity, relation), or (head_entity, tail_entity). Output: list[tail_entities], or list[relations]. This function helps you find the tail_entities given a head_entity and relation, or relations given a head_entity and tail_entity. For example, Relate(\"Barack Obama\", \"child\") returns ["Malia Obama", "Sasha Obama"], and Relate(\"Barack Obama\", \"Michelle Obama\") returns ["spouse"]. You may also search attribute relations using Relate() by treating attributes as tail entities. For example, Relate(\"Barack Obama\", \"time served as US president\") returns ["1997 to 2004"], and Relate(\"Barack Obama\", \"1961\")" returns ["year of birth"].
3. Filter(). Input: (list[entities], condition). Output: list[entities]. This function helps you filter out entities that satisfy a factual attribute condition. For example, Filter([\"Lionel Messi\", \"Steven Jobs\", \"Bill Gates\"], \"born in 1955\"), returns [\"Bill Gates\", \"Steve Jobs\"], and Filter([\"Lionel Messi\", \"Cristiano Ronaldo\"], \"is Portuguese\") returns ["Cristiano Ronaldo"].
Construct a hierarchical question decomposition tree in json format for the following complex question: \"{question}\". The tree starts with the original complex question as the root node, and each non-root node is a sub-question of its parent. Continue decomposing until a sub-question cannot be further decomposed and could either be: (1) directly answered by calling one of the three atomic functions Search(), Relate(), Filter(), or (2) directly answered by analyzing the answers of at least two previously answered questions, such as comparing, judging, intersecting, counting, etc. In case (1), write this sub-question with its corresponding function call as a leaf node. In case (2), write this sub-question with an [END] mark as a leaf node. For function leaf nodes, do not write nested functions such as Filter(Search(...)): if multiple function calls are required, write each function call with a separate sub-question in a separate leaf node. For [END] leaf questions, format your question as "Given answers of [q_idx_1] and [q_idx_2], ...", where [q_idx_1] and [q_idx_2] are question indices of the previously answered questions required to answer this [END] question. In your question decomposition tree, use double quotes "" to enclose sub-questions and functions, and escape quotes \"\" to enclose work titles and function parameters.
Examples: 
Question: {hotpotqa_ex1_q}
Decomposition Tree: {hotpotqa_ex1}
Question: {hotpotqa_ex2_q}
Decomposition Tree: {hotpotqa_ex2}
Question: {hotpotqa_ex3_q}
Decomposition Tree: {hotpotqa_ex3}
Question: {hotpotqa_ex4_q}
Decomposition Tree: {hotpotqa_ex4}
Question: {hotpotqa_ex8_q}
Decomposition Tree: {hotpotqa_ex8}
Question: {hotpotqa_ex10_q}
Decomposition Tree: {hotpotqa_ex10}
Question: {hotpotqa_ex12_q}
Decomposition Tree: {hotpotqa_ex12}
Question: {hotpotqa_ex15_q}
Decomposition Tree: {hotpotqa_ex15}
Question: {hotpotqa_ex16_q}
Decomposition Tree: {hotpotqa_ex16}
Question: {hotpotqa_ex17_q}
Decomposition Tree: {hotpotqa_ex17}
Question: {hotpotqa_ex18_q}
Decomposition Tree: {hotpotqa_ex18}
Question: {hotpotqa_ex19_q}
Decomposition Tree: {hotpotqa_ex19}
Question: {hotpotqa_ex20_q}
Decomposition Tree: {hotpotqa_ex20}
Question: {hotpotqa_ex21_q}
Decomposition Tree: {hotpotqa_ex21}
Question: {hotpotqa_ex22_q}
Decomposition Tree: {hotpotqa_ex22}
Question: {hotpotqa_ex23_q}
Decomposition Tree: {hotpotqa_ex23}
Question: {hotpotqa_ex24_q}
Decomposition Tree: {hotpotqa_ex24}
Question: {hotpotqa_ex25_q}
Decomposition Tree: {hotpotqa_ex25}

Your Question.
Question: {question}
Decomposition Tree: """
    
    return prompt



""" 
2WikiMultiHop 
"""

### Bridge/Compositional
_2wiki_ex1_q = "What is the place of birth of the director of film Reel Zombies?"
_2wiki_ex1 = """{"What is the place of birth of the director of film Reel Zombies?": ["1. Who is the director of film Reel Zombies?", "2. What is the place of birth of [1]?"], "1. Who is the director of film Reel Zombies?": ["3. What is the film Reel Zombies?", "4. Who is the director of [3]?"], "3. What is the film Reel Zombies?": "Search(\"Reel Zombies\", \"film\")", "4. Who is the director of [3]?": "Relate([3], \"director\")", "2. What is the place of birth of [1]?": ["5. Who is [1]?", "6. What is the place of birth of [5]?"], "5. Who is [1]?": "Search([1], \"film director\")", "6. What is the place of birth of [5]?": "Relate([5], \"place of birth\")"}"""

### Bridge/Compositional
_2wiki_ex2_q = "Which country Katherine De Stafford's husband is from?"
_2wiki_ex2 = """{"Which country Katherine De Stafford's husband is from?": ["1. Who is Katherine De Stafford's husband?", "2. Which country is [1] from?"], "1. Who is Katherine De Stafford's husband?": ["3. Who is Katherine De Stafford?", "4. Who is [3]'s husband?"], "3. Who is Katherine De Stafford?": "Search(\"Katherine De Stafford\")", "4. Who is [3]'s husband?": "Relate([3], \"husband\")", "2. Which country is [1] from?": ["5. Who is [1]?", "6. Which country is [5] from?"], "5. Who is [1]?": "Search([1], \"husband of Katherine De Stafford\")", "6. Which country is [5] from?": "Relate([1], \"from country\")"}"""
 
### Inference
_2wiki_ex3_q = "Who is the paternal grandfather of Mehmet I Of Karaman?"
# _2wiki_ex3 = {"Who is the paternal grandfather of Mehmet I Of Karaman?": ["1. Who is Mehmet I Of Karaman?", "2. Who is the father of [1]?", "3. Who is the father of [2]?"], "1. Who is Mehmet I Of Karaman?": "Search(\"Mehmet I Of Karaman\")", "2. Who is the father of [1]?": "Relate([1], \"father\")", "3. Who is the father of [2]?": "Relate([2], \"father\")"}
_2wiki_ex3 = """{"Who is the paternal grandfather of Mehmet I Of Karaman?": ["1. Who is the father of Mehmet I Of Karaman?", "2. Who is the father of [1]?"], "1. Who is the father of Mehmet I Of Karaman?": ["3. Who is Mehmet I Of Karaman?", "4. Who is the father of [3]?"], "3. Who is Mehmet I Of Karaman?": "Search(\"Mehmet I Of Karaman\")", "4. Who is the father of [3]?": "Relate([3], \"father\")", "2. Who is the father of [1]?": ["5. Who is [1]?", "6. Who is the father of [5]?"], "5. Who is [1]?": "Search([1], \"father of Mehmet I Of Karaman\")", "6. Who is the father of [5]?": "Relate([5], \"father\")"}"""

### Inference
_2wiki_ex4_q = "Who is the maternal grandfather of Berthold (Patriarch Of Aquileia)?"
# _2wiki_ex4 = {"Who is the maternal grandfather of Berthold (Patriarch Of Aquileia)?": ["1. Who is Berthold (Patriarch Of Aquileia)?", "2. Who is the mother of [1]?", "3. Who is the father of [2]?"], "1. Who is Berthold (Patriarch Of Aquileia)?": "Search(\"Berthold (Patriarch Of Aquileia)\")", "2. Who is the mother of [1]?": "Relate([1], \"mother\")", "3. Who is the father of [2]?": "Relate([2], \"father\")"}
_2wiki_ex4 = """{"Who is the maternal grandfather of Berthold (Patriarch Of Aquileia)?": ["1. Who is the mother of Berthold (Patriarch Of Aquileia)?", "2. Who is the father of [1]?"], "1. Who is the mother of Berthold (Patriarch Of Aquileia)?": ["3. Who is Berthold (Patriarch Of Aquileia)?", "4. Who is the mother of [3]?"], "3. Who is Berthold (Patriarch Of Aquileia)?": "Search(\"Berthold (Patriarch Of Aquileia)\")", "4. Who is the mother of [3]?": "Relate([3], \"mother\")", "2. Who is the father of [1]?": ["5. Who is [1]?", "6. Who is the father of [5]?"], "5. Who is [1]?": "Search([1], \"mother of Berthold (Patriarch Of Aquileia)\")", "6. Who is the father of [5]?": "Relate([5], \"father\")"}"""

### Comparison
_2wiki_ex5_q = "Was Shakila or \u00d8yvind Leonhardsen born first?"
_2wiki_ex5 = """{"Was Shakila or \u00d8yvind Leonhardsen born first?": ["1. When was Shakila born?", "2. When was \u00d8yvind Leonhardsen born?", "3. Given answers of [1] and [2], who was born first?"], "1. When was Shakila born?": ["4. Who is Shakila?", "5. When was [4] born?"], "4. Who is Shakila?": "Search(\"Shakila\")", "5. When was [4] born?": "Relate([4], \"date of birth\")", "2. When was \u00d8yvind Leonhardsen born?": ["6. Who is \u00d8yvind Leonhardsen?", "7. When was [6] born?"], "6. Who is \u00d8yvind Leonhardsen?": "Search(\"\u00d8yvind Leonhardsen\")", "7. When was [6] born?": "Relate([6], \"date of birth\")", "3. Given answers of [1] and [2], who was born first?": "[END]"}"""

### Comparison
_2wiki_ex6_q = "Which film was released earlier, Robotech: The Movie or Lakeeran?"
_2wiki_ex6 = """{"Which film was released earlier, Robotech: The Movie or Lakeeran?": ["1. When was the film Robotech: The Movie released?", "2. When was the film Lakeeran released?", "3. Given answers of [1] and [2], which film was released earlier?"], "1. When was the film Robotech: The Movie released?": ["4. What is the film Robotech: The Movie?", "5. When was [4] released?"], "4. What is the film Robotech: The Movie?": "Search(\"Robotech: The Movie\", \"film\")", "5. When was [4] released?": "Relate([4], \"release date\")", "2. When was the film Lakeeran released?": ["6. What is the film Lakeeran?", "7. When was [6] released?"], "6. What is the film Lakeeran?": "Search(\"Lakeeran\", \"film\")", "7. When was [6] released?": "Relate([6], \"release date\")", "3. Given answers of [1] and [2], which film was released earlier?": "[END]"}"""

### Bridge-Comparison  # DPR wiki dump does not have relevant info
_2wiki_ex7_q = "Which film has the director who died later, Ridin' Pretty or How Strange To Be Named Federico?"
_2wiki_ex7 = """{"Which film has the director who died later, Ridin' Pretty or How Strange To Be Named Federico?": ["1. Who is the director of the film Ridin' Pretty?", "2. Who is the director of the film How Strange To Be Named Federico?", "3. When did [1] die?", "4. When did [2] die?", "5. Given answers of [3] and [4], which film has the director who died later?"], "1. Who is the director of the film Ridin' Pretty?": ["6. What is the film Ridin' Pretty?", "7. Who is the director of [6]?"], "6. What is the film Ridin' Pretty?": "Search(\"Ridin' Pretty\", \"film\")", "7. Who is the director of [6]?": "Relate([6], \"director\")", "2. Who is the director of the film How Strange To Be Named Federico?": ["8. What is the film How Strange To Be Named Federico?", "9. Who is the director of [8]?"], "8. What is the film How Strange To Be Named Federico?": "Search(\"How Strange To Be Named Federico\", \"film\")", "9. Who is the director of [8]?": "Relate([8], \"director\")", "3. When did [1] die?": ["10. Who is [1]?", "11. When did [10] die?"], "10. Who is [1]?": "Search([1], \"film director\")", "11. When did [10] die?": "Relate([10], \"date of death\")", "4. When did [2] die?": ["12. Who is [2]?", "13. When did [12] die?"], "12. Who is [2]?": "Search([2], \"film director\")", "13. When did [12] die?": "Relate([12], \"date of death\")", "5. Given answers of [3] and [4], which film has the director who died later?": "[END]"}"""

### Bridge-Comparison
_2wiki_ex8_q = "Which film has the director who is older, King Of The Zombies or Mon Oncle Benjamin?"
_2wiki_ex8 = """{"Which film has the director who is older, King Of The Zombies or Mon Oncle Benjamin?": ["1. Who is the director of the film King Of The Zombies?", "2. Who is the director of the film Mon Oncle Benjamin?", "3. When was [1] born?", "4. When was [2] born?", "5. Given answers of [3] and [4], which film has the director who is older?"], "1. Who is the director of the film King Of The Zombies?": ["6. What is the film King Of The Zombies?", "7. Who is the director of [6]?"], "6. What is the film King Of The Zombies?": "Search(\"King Of The Zombies\", \"film\")", "7. Who is the director of [6]?": "Relate([6], \"director\")", "2. Who is the director of the film Mon Oncle Benjamin?": ["8. What is the film Mon Oncle Benjamin?", "9. Who is the director of [8]?"], "8. What is the film Mon Oncle Benjamin?": "Search(\"Mon Oncle Benjamin\", \"film\")", "9. Who is the director of [8]?": "Relate([8], \"director\")", "3. When was [1] born?": ["10. Who is [1]?", "12. When was [11] born?"], "10. Who is [1]?": "Search([1], \"film director\")", "11. When was [10] born?": "Relate([10], \"date of birth\")", "4. When was [2] born?": ["12. Who is [2]?", "13. When was [12] born?"], "12. Who is [2]?": "Search([2], \"film director\")", "13. When was [12] born?": "Relate([12], \"date of birth\")", "5. Given answers of [3] and [4], which film has the director who is older?": "[END]"}"""

### Inference
_2wiki_ex9_q = "Who is Elizabeth Stuart, Countess Of Lennox's mother-in-law?"
_2wiki_ex9 = """{"Who is Elizabeth Stuart, Countess Of Lennox's mother-in-law?": ["1. Who is Elizabeth Stuart, Countess Of Lennox's husband?", "2. Who is [1]'s mother?"], "1. Who is Elizabeth Stuart, Countess Of Lennox's husband?": ['3. Who is Elizabeth Stuart, Countess Of Lennox?', "4. Who is [3]'s husband?"], '3. Who is Elizabeth Stuart, Countess Of Lennox?': 'Search("Elizabeth Stuart, Countess Of Lennox")', "4. Who is [3]'s husband?": 'Relate([3], "husband")', "2. Who is [1]'s mother?": ["5. Who is [1]?", "6. Who is [5]'s mother?"], "5. Who is [1]?": "Search([1], \"husband of Elizabeth Stuart, Countess Of Lennox\")", "6. Who is [5]'s mother?": "Relate([5], \"mother\")"}"""

### Bridge
_2wiki_ex10_q = "Who is the mother of the performer of song Passion (Utada Hikaru Song)?"
_2wiki_ex10 = """{"Who is the mother of the performer of song Passion (Utada Hikaru Song)?": ["1. Who is the performer of song Passion (Utada Hikaru Song)?", "2. Who is the mother of [1]?"], "1. Who is the performer of song Passion (Utada Hikaru Song)?": ["3. What is the song Passion (Utada Hikaru Song)?", "4. Who is the performer of [3]?"], "3. What is the song Passion (Utada Hikaru Song)?": "Search(\"Passion (Utada Hikaru Song)\", \"song\")", "4. Who is the performer of [3]?": "Relate([3], \"performer\")", "2. Who is the mother of [1]?": ["5. Who is [1]?", "6. Who is the mother of [5]?"], "5. Who is [1]?": "Search([1], \"performer of song Passion (Utada Hikaru Song)\")", "6. Who is the mother of [5]?": "Relate([5], \"mother\")"}"""

### Comparison
_2wiki_ex11_q = "Are both Chak 26/11-L, Chichawatni and Chah-E Ali Kapari located in the same country?"
_2wiki_ex11 = """{"Are both Chak 26/11-L, Chichawatni and Chah-E Ali Kapari located in the same country?": ["1. What country is Chak 26/11-L located in?", "2. What country is Chichawatni located in?", "3. What country is Chah-E Ali Kapari located in?", "4. Given answers of [1], [2], and [3], are they located in the same country?"], "1. What country is Chak 26/11-L located in?": ["5. What is Chak 26/11-L?", "6. What country is [5] located in?"], "5. What is Chak 26/11-L?": "Search(\"Chak 26/11-L\")", "6. What country is [5] located in?": "Relate([5], \"located in country\")", "2. What country is Chichawatni located in?": ["7. What is Chichawatni?", "8. What country is [7] located in?"], "7. What is Chichawatni?": "Search(\"Chichawatni\")", "8. What country is [7] located in?": "Relate([7], \"located in country\")", "3. What country is Chah-E Ali Kapari located in?": ["9. What is Chah-E Ali Kapari?", "10. What country is [9] located in?"], "9. What is Chah-E Ali Kapari?": "Search(\"Chah-E Ali Kapari\")", "10. What country is [9] located in?": "Relate([9], \"located in country\")", "4. Given answers of [1], [2], and [3], are they located in the same country?": "[END]"}"""

### Bridge-Comparison
_2wiki_ex12_q = "Which film has the director who was born first, Dead Man'S Evidence or Creature Of The Walking Dead?"
_2wiki_ex12 = """{"Which film has the director who was born first, Dead Man'S Evidence or Creature Of The Walking Dead?": ["1. Who is the director of the film Dead Man'S Evidence?", "2. Who is the director of the film Creature Of The Walking Dead?", "3. When was [1] born?", "4. When was [2] born?", "5. Given answers of [3] and [4], which film has the director who was born first?"], "1. Who is the director of the film Dead Man'S Evidence?": ["6. What is the film Dead Man'S Evidence?", "7. Who is the director of [6]?"], "6. What is the film Dead Man'S Evidence?": "Search(\"Dead Man'S Evidence\", \"film\")", "7. Who is the director of [6]?": "Relate([6], \"director\")", "2. Who is the director of the film Creature Of The Walking Dead?": ["8. What is the film Creature Of The Walking Dead?", "9. Who is the director of [8]?"], "8. What is the film Creature Of The Walking Dead?": "Search(\"Creature Of The Walking Dead\", \"film\")", "9. Who is the director of [8]?": "Relate([8], \"director\")", "3. When was [1] born?": ["10. Who is [1]?", "11. When was [1] born?"], "10. Who is [1]?": "Search([1], \"film director\")", "11. When was [1] born?": "Relate([10], \"date of birth\")", "4. When was [2] born?": ["12. Who is [2]?", "13. When was [12] born?"], "12. Who is [2]?": "Search([2], \"film director\")", "13. When was [12] born?": "Relate([12], \"date of birth\")", "5. Given answers of [3] and [4], which film has the director who was born first?": "[END]"}"""


def format_tree_generation_prompt_2wiki(question):
    prompt = f"""You are given 3 atomic functions to help you retrieve and operate knowledge from Wikipedia:
1. Search(). Input: (name, [optional] descriptor). Output: list[entities]. This function helps you find and disambiguate an entity given its name and optional descriptor. If no descriptor is provided, the most popular entity will be returned. For example, Search(\"Michael Jordan\") returns the famous basketball player ["Michael Jordan"], while Search(\"Michael Jordan\", \"football goalkeeper\") returns the English retired football goalkeeper ["Michael Jordan (footballer)"]. When the question provides explicit entity knowledge, always write a descriptor for the Search() function based on the question's information.
2. Relate(). Input: there are 2 input possibilities, (head_entity, relation), or (head_entity, tail_entity). Output: list[tail_entities], or list[relations]. This function helps you find the tail_entities given a head_entity and relation, or relations given a head_entity and tail_entity. For example, Relate(\"Barack Obama\", \"child\") returns ["Malia Obama", "Sasha Obama"], and Relate(\"Barack Obama\", \"Michelle Obama\") returns ["spouse"]. You may also search attribute relations using Relate() by treating attributes as tail entities. For example, Relate(\"Barack Obama\", \"time served as US president\") returns ["1997 to 2004"], and Relate(\"Barack Obama\", \"1961\")" returns ["year of birth"].
3. Filter(). Input: (list[entities], condition). Output: list[entities]. This function helps you filter out entities that satisfy a factual attribute condition. For example, Filter([\"Lionel Messi\", \"Steven Jobs\", \"Bill Gates\"], \"born in 1955\"), returns [\"Bill Gates\", \"Steve Jobs\"], and Filter([\"Lionel Messi\", \"Cristiano Ronaldo\"], \"is Portuguese\") returns ["Cristiano Ronaldo"].
Construct a hierarchical question decomposition tree in json format for the following complex question: \"{question}\". The tree starts with the original complex question as the root node, and each non-root node is a sub-question of its parent. Continue decomposing until a sub-question cannot be further decomposed and could either be: (1) directly answered by calling one of the three atomic functions Search(), Relate(), Filter(), or (2) directly answered by analyzing the answers of at least two previously answered questions, such as comparing, judging, intersecting, counting, etc. In case (1), write this sub-question with its corresponding function call as a leaf node. In case (2), write this sub-question with an [END] mark as a leaf node. For function leaf nodes, do not write nested functions such as Filter(Search(...)): if multiple function calls are required, write each function call with a separate sub-question in a separate leaf node. For [END] leaf questions, format your question as "Given answers of [q_idx_1] and [q_idx_2], ...", where [q_idx_1] and [q_idx_2] are question indices of the previously answered questions required to answer this [END] question. In your question decomposition tree, use double quotes "" to enclose sub-questions and functions, and escape quotes \"\" to enclose work titles and function parameters.
Examples: 
Question: {_2wiki_ex1_q}
Decomposition Tree: {_2wiki_ex1}
Question: {_2wiki_ex2_q}
Decomposition Tree: {_2wiki_ex2}
Question: {_2wiki_ex3_q}
Decomposition Tree: {_2wiki_ex3}
Question: {_2wiki_ex4_q}
Decomposition Tree: {_2wiki_ex4}
Question: {_2wiki_ex5_q}
Decomposition Tree: {_2wiki_ex5}
Question: {_2wiki_ex6_q}
Decomposition Tree: {_2wiki_ex6}
Question: {_2wiki_ex7_q}
Decomposition Tree: {_2wiki_ex7}
Question: {_2wiki_ex8_q}
Decomposition Tree: {_2wiki_ex8}
Question: {_2wiki_ex9_q}
Decomposition Tree: {_2wiki_ex9}
Question: {_2wiki_ex10_q}
Decomposition Tree: {_2wiki_ex10}
Question: {_2wiki_ex11_q}
Decomposition Tree: {_2wiki_ex11}
Question: {_2wiki_ex12_q}
Decomposition Tree: {_2wiki_ex12}

Your Question.
Question: {question}
Decomposition Tree: """
    
    return prompt



"""
    Musique
"""

# 2hop
musique_ex1_q = "The city where WOCA is located is in which part of Florida?"
musique_ex1 = """{"The city where WOCA is located is in which part of Florida?": ["1. In which city is WOCA located?", "2. [1] is in which part of Florida?"], "1. In which city is WOCA located?": ["3. What is WOCA?", "4. In which city is WOCA located?"], "3. What is WOCA?": "Search(\"WOCA\")", "4. In which city is [3] located?": "Relate([3], \"located in city\")", "2. [1] is in which part of Florida?": "Relate([1], \"in part of Florida\")"}"""

# 2hop
musique_ex2_q = "Who started out his career on adult contemporary radio along with the performer of All That Echoes?"
musique_ex2 = """{"Who started out his career on adult contemporary radio along with the performer of All That Echoes?": ["1. Who is the performer of All That Echoes?", "2. Who started out his career on adult contemporary radio along with [1]?"], "1. Who is the performer of All That Echoes?": ["3. What is All That Echoes?", "4. Who is the performer of [3]?"], "3. What is All That Echoes?": "Search(\"All That Echoes\")", "4. Who is the performer of [3]?": "Relate([3], \"performer\")", "2. Who started out his career on adult contemporary radio along with [1]?": "Relate([1], \"started out his career on adult contemporary radio along with\")"}"""

# 2hop
musique_ex3_q = "In which county did Snappy Tomato Pizza form?"
musique_ex3 = """{"In which county did Snappy Tomato Pizza form?": ["1. Where did Snappy Tomato Pizza form?", "2. In which county is [1] located?"], "1. Where did Snappy Tomato Pizza form?": ["3. What is Snappy Tomato Pizza?", "4. Where did [3] form?"], "3. What is Snappy Tomato Pizza?": "Search(\"Snappy Tomato Pizza\")", "4. Where did [3] form?": "Relate([3], \"formed at location\")", "2. In which county is [1] located?": "Relate([2], \"located in county\")"}"""

# 3hop1
musique_ex4_q = "Where do greyhound buses leave from in where the headquarters is located of who owns the hard rock hotel in las vegas?"
musique_ex4 = """{"Where do greyhound buses leave from in where the headquarters is located of who owns the hard rock hotel in las vegas?": ["1. Who owns the hard rock hotel in las vegas?", "2. Where is the headquarters of [1] located?", "3. Where do greyhound buses leave from in [2]?"], "1. Who owns the hard rock hotel in las vegas?": ["4. What is the hard rock hotel in las vegas?", "5. Who owns [4]?"], "4. What is the hard rock hotel in las vegas?": "Search(\"hard rock hotel in las vegas\")", "5. Who owns [4]?": "Relate([4], \"owned by\")", "2. Where is the headquarters of [1] located?": "Relate([1], \"headquarters located at\")", "3. Where do greyhound buses leave from in [2]?": "Relate([2], \"greyhound buses leave from\")"}"""

# 3hop1, but looks like 3hop2
musique_ex5_q = "What is the average winter daytime temperature in the region where Richmond is found, in the state where WIRR operates?"
musique_ex5 = """{"What is the average winter daytime temperature in the region where Richmond is found, in the state where WIRR operates?": ["1. In which state does WIRR operate?", "2. What is the region in [1] where Richmond is found?", "3. What is the average winter daytime in [2]?"], "1. In which state does WIRR operate?": ["4. What is WIRR?", "5. Where does [4] operate?"], "4. What is WIRR?": "Search(\"WIRR\")", "5. Where does [4] operate?": "Relate([4], \"operate at location\")", "2. What is the region in [1] where Richmond is found?": "Relate([1], \"region where Richmond is found\")", "3. What is the average winter daytime in [2]?": "Relate([2], \"average winter daytime\")"}"""

# 3hop2
musique_ex6_q = "Who is the actress who plays the Queen of England in 1890 on the station that aired High Feather?"
musique_ex6 = """{"Who is the actress who plays the Queen of England in 1890 on the station that aired High Feather?": ["1. Who is the Queen of England in 1890?", "2. What is the station that aired High Feather?", "3. Who is the actress who plays [1] on [2]?"], "1. Who is the Queen of England in 1890?": "Search(\"Queen of England\", \"1890\")", "2. What is the station that aired High Feather?": ["4. What is High Feather?", "5. What is the station that aired [4]?"], "4. What is High Feather?": "Search(\"station\", \"aired High Feather\")", "5. What is the station that aired [4]?": "Relate([4], \"station that aired\")", "3. Who is the actress who plays [1] on [2]?": "Search(\"actress who plays [1] on [2]\")"}"""

# 3hop2
musique_ex7_q = "How long had the city considered to be a place that is popular with tourists been the capital city of the location of the Yaxing Coach headquarters?"
musique_ex7 = """{"How long had the city considered to be a place that is popular with tourists been the capital city of the location of the Yaxing Coach headquarters?": ["1. Which city is considered to be a place that is popular with tourists?", "2. What is the location of the Yaxing Coach headquarters?", "3. How long had [1] been the capital city of [2]?"], "1. Which city is considered to be a place that is popular with tourists?": "Search(\"city\", \"considered to be a place that is popular with tourists\")", "2. What is the location of the Yaxing Coach headquarters?": ["4. What is the Yaxing Coach headquarters?", "5. What is the location of [4]?"], "4. What is the Yaxing Coach headquarters?": "Search(\"Yaxing Coach headquarters\")", "5. What is the location of [4]?": "Relate([4], \"location\")", "3. How long had [1] been the capital city of [2]?": "Search(\"length of time when [1] has been the capital city of [2]\")"}"""

# 4hop1
musique_ex8_q = "What were the Genesis's advantages over the game system with a 3 letter abbreviation, featuring a game named after the football league that the Los Angeles Rams are representative of?"
musique_ex8 = """{"What were the Genesis's advantages over the game system with a 3 letter abbreviation, featuring a game named after the football league that the Los Angeles Rams are representative of?": ["1. What football league is the Los Angeles Rams representative of?", "2. What game was named after [1]?", "3. What game system with a 3 letter abbreviation featured [2]?", "4. What were the Genesis's advantages over [3]?"], "1. What football league is the Los Angeles Rams representative of?": ["5. What is the Los Angeles Rams?", "6. What football league is [5] representative of?"], "5. What is the Los Angeles Rams?": "Search(\"Los Angeles Rams\")", "6. What football league is [5] representative of?": "Relate([5], \"representative of football league\")", "2. What game was named after [1]?": "Relate([1], \"game named after\")", "3. What game system with a 3 letter abbreviation featured [2]?": "Relate([2], \"featured by game system with a 3 letter abbreviation\")", "4. What were the Genesis's advantages over [3]?": "Relate([3], \"Genesis's advantages\")"}"""

# 4hop1
musique_ex9_q = "Where does the river by the city sharing a border with Elizabeth Berg's birthplace empty into the Gulf of Mexico?"
musique_ex9 = """{"Where does the river by the city sharing a border with Elizabeth Berg's birthplace empty into the Gulf of Mexico?": ["1. What is Elizabeth Berg's birthplace?", "2. Which city shares a border with [1]?", "3. What is the river by [2]?", "4. Where does [3] empty into the Gulf of Mexico?"], "1. What is Elizabeth Berg's birthplace?": ["5. Who is Elizabeth Berg?", "2. What is [5]'s birthday?"], "5. Who is Elizabeth Berg?": "Search(\"Elizabeth Berg\")", "2. What is [5]'s birthday?": "Relate([5], \"date of birth\")", "2. Which city shares a border with [1]?": "Relate([1], \"shares border with city\")", "3. What is the river by [2]?": "Relate([2], \"river by\")", "4. Where does [3] empty into the Gulf of Mexico?": "Relate([4], \"empty into the Gulf of Mexico at location\")"}"""

# 4hop2
musique_ex10_q = "Normalization occurred in Country A that invaded Country B because the military branch that Air Defense Artillery is part of was unprepared. when was the word \"Slavs\" used in the national anthem of Country B?"
musique_ex10 = """{"Normalization occurred in Country A that invaded Country B because the military branch that Air Defense Artillery is part of was unprepared. when was the word \"Slavs\" used in the national anthem of Country B?": ["1. Normalization occurred in which country?", "2. What military branch is Air Defense Artillery a part of?", "3. [1] invaded what country because [2] was unprepared?", "4. When was the word \"Slavs\" used in the national anthem of [3]?"], "1. Normalization occurred in which country?": "Search(\"country\", \"occurred Normalization\")", "2. What military branch is Air Defense Artillery a part of?": ["5. What is Air Defense Artillery", "6. What military branch is [5] a part of?"], "5. What is Air Defense Artillery": "Search(\"Air Defense Artillery\")", "6. What military branch is [5] a part of?": "Relate([5], \"part of military branch\")", "3. [1] invaded what country because [2] was unprepared?": "Search(\"country\", \"invaded by [1] because [2] was unprepared\")", "4. When was the word \"Slavs\" used in the national anthem of [3]?": "Search(\"word 'Slavs' used in [3]'s national anthem\")"}"""

# 4hop3
musique_ex11_q = "When did the town WIZE is licensed in become capitol of the state where Green Township is located?"
musique_ex11 = """{"When did the town WIZE is licensed in become capitol of the state where Green Township is located?": ["1. Where is WIZE licensed in?", "2. What is the town where [1] is located?", "3. In which state is Green Township located?", "4. When did [2] become the capitol of [3]?"], "1. Where is WIZE licensed in?": ["5. What is WIZE?", "6. Where was [5] licensed in?"], "5. What is WIZE?": "Search(\"WIZE\")", "6. Where was [5] licensed in?": "Relate([5], \"licensed in\")", "2. What is the town where [1] is located?": "Relate([1], \"located in town\")", "3. In which state is Green Township located?": ["7. What is Green Township?", "8. In which state is [7] located?"], "7. What is Green Township?": "Search(\"Green Township\")", "8. In which state is [7] located?": "Relate([7], \"located in state\")", "4. When did [2] become the capitol of [3]?": "Search(\"time when [2] become the capitol of [3]\")"}"""

# 2hop
musique_ex12_q = "When did the first large winter carnival take place in the city where CIMI−FM is licensed to broadcast?"
musique_ex12 = """{"When did the first large winter carnival take place in the city where CIMI−FM is licensed to broadcast?": ["1. In which city is CIMI-FM licensed to broadcast?", "2. When did the first carnival take place in [1]?"], "1. In which city is CIMI-FM licensed to broadcast?": ["3. What is CIMI-FM?", "4. In which city is [3] licensed to broadcast?"], "3. What is CIMI-FM?": "Search(\"CIMI-FM\")", "4. In which city is [3] licensed to broadcast?": "Relate([3], \"licensed to broadcast in city\")", "2. When did the first carnival take place in [1]?": "Relate([1], \"first carnival took place at time\")"}"""

# 3hop2
musique_ex13_q = "When did the majority party in the House of Representatives take control of the determiner of rules of the US House and US Senate?"
musique_ex13 = """{"When did the majority party in the House of Representatives take control of the determiner of rules of the US House and US Senate?": ["1. What majority party is currently in the House of Representatives?", "2. Who is the determiner of rules of the US House and US Senate?", "3. When did [1] take control of [2]?"], "1. What majority party is currently in the House of Representatives?": "Search(\"majoriity party currently in the House of Representatives\")", "2. Who is the determiner of rules of the US House and US Senate?": "Search(\"determiner of rules of the US House and US Senate\")", "3. When did [1] take control of [2]?": "Search(\"time when [1] took control of [2]\")"}"""

# 2hop
musique_ex14_q = "What happened to the assets of the agency that abolished the dual system of government in bengal after it was removed from power?"
musique_ex14 = """{"What happened to the assets of the agency that abolished the dual system of government in bengal after it was removed from power?": ["1. What agency abolished the dual system of government in bengal?", "2. What happened to the assets of [1] after it was removed from power?"], "1. What agency abolished the dual system of government in bengal?": "Search(\"agency that abolished the dual system of government in bengal\")", "2. What happened to the assets of [1] after it was removed from power?": "Relate([1], \"happened to assets after removed from power\")"}"""

# 4hop3
musique_ex15_q = "Who burned down the city where Dunn Dunn's recording artist died during the conflict after which occurred the historical period of A Rose for Emily?"
musique_ex15 = """{"Who burned down the city where Dunn Dunn's recording artist died during the conflict after which occurred the historical period of A Rose for Emily?": ["1. Who is Dunn Dunn's recording artist?", "2. In which city did [1] die?", "3. What is the historical period of A Rose for Emily?", "4. Who burned down [2] during the conflict after which occurred [3]?"], "1. Who is Dunn Dunn's recording artist?": ["5. Who is Dunn Dunn?", "6. Who is [5]'s recording artist?"], "2. In which city did [1] die?": "Relate([1], \"died in city\")", "3. What is the historical period of A Rose for Emily?": ["7. What is A Rose for Emily?", "8. What is the historical period of [7]?"], "7. What is A Rose for Emily?": "Search(\"A Rose for Emily\")", "8. What is the historical period of [7]?": "Relate([7], \"historical period\")", "4. Who burned down [2] during the conflict after which occurred [3]?": "Search(\"who burned down [2] during the conflict after which occurred [3]\")"}"""

# 2hop
musique_ex16_q = "When does real time with the pizza man cast member start again in 2018?"
musique_ex16 = """{"When does real time with the pizza man cast member start again in 2018?": ["1. Who is the Pizza Man cast member?", "2. When does real time with [1] start again in 2018?"], "1. Who is the Pizza Man cast member?": ["3. What is Pizza Man?", "4. Who is [3]'s cast member?"], "3. What is Pizza Man?": "Search(\"Pizza Man\")", "4. Who is [3]'s cast member?": "Relate([3], \"cast member\")", "2. When does real time with [1] start again in 2018?": "Relate([1], \"real time start again in 2018\")"}"""

# 2hop with how many (trick question for filter)
musique_ex17_q = "How many mandatory transmitters of the owner and operator of most CBC TV stations were updated before the deadline?"
musique_ex17 = """{"How many mandatory transmitters of the owner and operator of most CBC TV stations were updated before the deadline?": ["1. Who is the owner and operator of most CBC TV stations?", "2. How many mandatory transmitters of [1] were updated before the deadline?"], "1. Who is the owner and operator of most CBC TV stations?": ["3. What is a CBC (TV station)?", "4. Who is the owner and operator of most [3] TV stations?"], "3. What is CBC (TV station)?": "Search(\"CBC\", \"TV station\")", "4. Who is the owner and operator of most [3] TV stations?": "Relate([3], \"owner and operator of most TV stations\")", "2. How many mandatory transmitters of [1] were updated before the deadline?": "Relate([1], \"number of mandatory transmitters updated before the deadline\")"}"""


def format_tree_generation_prompt_musique(question):
    prompt = f"""You are given 3 atomic functions to help you retrieve and operate knowledge from Wikipedia:
1. Search(). Input: (name, [optional] descriptor). Output: list[entities]. This function helps you find and disambiguate an entity given its name and optional descriptor. If no descriptor is provided, the most popular entity will be returned. For example, Search(\"Michael Jordan\") returns the famous basketball player ["Michael Jordan"], while Search(\"Michael Jordan\", \"football goalkeeper\") returns the English retired football goalkeeper ["Michael Jordan (footballer)"]. When the question provides explicit entity knowledge, always write a descriptor for the Search() function based on the question's information.
2. Relate(). Input: there are 2 input possibilities, (head_entity, relation), or (head_entity, tail_entity). Output: list[tail_entities], or list[relations]. This function helps you find the tail_entities given a head_entity and relation, or relations given a head_entity and tail_entity. For example, Relate(\"Barack Obama\", \"child\") returns ["Malia Obama", "Sasha Obama"], and Relate(\"Barack Obama\", \"Michelle Obama\") returns ["spouse"]. You may also search attribute relations using Relate() by treating attributes as tail entities. For example, Relate(\"Barack Obama\", \"time served as US president\") returns ["1997 to 2004"], and Relate(\"Barack Obama\", \"1961\")" returns ["year of birth"].
3. Filter(). Input: (list[entities], condition). Output: list[entities]. This function helps you filter out entities that satisfy a factual attribute condition. For example, Filter([\"Lionel Messi\", \"Steven Jobs\", \"Bill Gates\"], \"born in 1955\"), returns [\"Bill Gates\", \"Steve Jobs\"], and Filter([\"Lionel Messi\", \"Cristiano Ronaldo\"], \"is Portuguese\") returns ["Cristiano Ronaldo"].
Construct a hierarchical question decomposition tree in json format for the following complex question: \"{question}\". The tree starts with the original complex question as the root node, and each non-root node is a sub-question of its parent. Continue decomposing until a sub-question cannot be further decomposed and could either be: (1) directly answered by calling one of the three atomic functions Search(), Relate(), Filter(), or (2) directly answered by analyzing the answers of at least two previously answered questions, such as comparing, judging, intersecting, counting, etc. In case (1), write this sub-question with its corresponding function call as a leaf node. In case (2), write this sub-question with an [END] mark as a leaf node. For function leaf nodes, do not write nested functions such as Filter(Search(...)): if multiple function calls are required, write each function call with a separate sub-question in a separate leaf node. For [END] leaf questions, format your question as "Given answers of [q_idx_1] and [q_idx_2], ...", where [q_idx_1] and [q_idx_2] are question indices of the previously answered questions required to answer this [END] question. In your question decomposition tree, use double quotes "" to enclose sub-questions and functions, and escape quotes \"\" to enclose work titles and function parameters.
Examples: 
Question: {musique_ex1_q}
Decomposition Tree: {musique_ex1}
Question: {musique_ex2_q}
Decomposition Tree: {musique_ex2}
Question: {musique_ex3_q}
Decomposition Tree: {musique_ex3}
Question: {musique_ex4_q}
Decomposition Tree: {musique_ex4}
Question: {musique_ex5_q}
Decomposition Tree: {musique_ex5}
Question: {musique_ex6_q}
Decomposition Tree: {musique_ex6}
Question: {musique_ex7_q}
Decomposition Tree: {musique_ex7}
Question: {musique_ex8_q}
Decomposition Tree: {musique_ex8}
Question: {musique_ex9_q}
Decomposition Tree: {musique_ex9}
Question: {musique_ex10_q}
Decomposition Tree: {musique_ex10}
Question: {musique_ex11_q}
Decomposition Tree: {musique_ex11}
Question: {musique_ex12_q}
Decomposition Tree: {musique_ex12}
Question: {musique_ex13_q}
Decomposition Tree: {musique_ex13}
Question: {musique_ex14_q}
Decomposition Tree: {musique_ex14}
Question: {musique_ex15_q}
Decomposition Tree: {musique_ex15}
Question: {musique_ex16_q}
Decomposition Tree: {musique_ex16}
Question: {musique_ex17_q}
Decomposition Tree: {musique_ex17}

Your Question.
Question: {question}
Decomposition Tree: """
    
    return prompt



""" 
CRAG
"""

### Simple or Simple with Condition (zero-hop)

crag_ex0_q = "who was the 2019 nfl mvp?"
crag_ex0 = """{"who was the 2019 nfl mvp?": "Search(\"2019 NLF MVP\")"}"""

crag_ex1_q = "in 2007, which movie was distinguished for its visual effects at the oscars?"
crag_ex1 = """{"in 2007, which movie was distinguished for its visual effects at the oscars?": "Search(\"Visual Effects winning movie at the Oscars in 2007\")"""

# crag_ex2_q = "what was the first movie to be filmed entirely in outer space?"
# crag_ex2 = """{"what was the first movie to be filmed entirely in outer space?": "Search(\"first movie to be filmed entirely in outer space\")"}"""

crag_ex2_q = "what is chris evans net worth 2023?"
crag_ex2 = """{"what is chris evans net worth 2023?": "Relate(\"Chris Evans\", \"net worth in 2023\")"}"""

crag_ex3_q = "kendrick lamar won a pulitzer prize in 2018. which 2017 album of his won this award?"
crag_ex3 = """{"kendrick lamar won a pulitzer prize in 2018. which 2017 album of his won this award?": "Relate(\"Kendrick Lamar\", \"2017 album that won the Pulitzer Prize\")"}"""

### Simple or Simple with Condition (one-hop)

# crag_ex5_q = "for the film life or something like it, who directed it?"
# crag_ex5 = """{"for the film life or something like it, who directed it?": ["1. What is the film Life or Something Like It?", "2. Who is the director of [1]?"], "1. What is the film Life or Something Like It?": "Search(\"Life or Something Like It\", \"film\")", "2. Who is the director of [1]?": "Relate([1], \"director\")"}"""

### Multi-hop

crag_ex4_q = "what was mike epps's age at the time of next friday's release?"
crag_ex4 = """{"what was mike epps's age at the time of next friday's release?": ["1. When did Next Friday's release?", "2. What was Mike Epp's age at the time of [1]?"], "2. When did Next Friday's release?": "Relate(\"Next Friday's\", \"released at time\")", "2. What was Mike Epp's age at the time of [1]?": "Relate(\"Mike Epp\", \"age at the time of [1]\")"}"""

crag_ex5_q = "what's the name of the actor who played the role of a lawyer with no law degree in the tv show \"suits\"?"
crag_ex5 = """{"what's the name of the actor who played the role of a lawyer with no law degree in the tv show \"suits\"?": ["1. What is the role of a lawyer with no law degree in the TV show \"Suits\"?", "2. What is the name of the actor that played [1] in the TV show \"Suits\"?"], "1. What is the role of a lawyer with no law degree in the TV show \"Suits\"?": "Relate(\"Suits (TV show)\", \"role of lawyer with no law degree\")", "2. What is the name of the actor that played [1] in the TV show \"Suits\"?": "Relate([1], \"name of actor in Suits (TV show)\")"}"""

### Comparison

crag_ex6_q = "which star is brighter, sirius or alpha centauri?"
crag_ex6 = """{"which star is brighter, sirius or alpha centauri?": ["1. How bright is the star Sirius?", "2. How bright is the star Alpha Centauri?", "3. Given answers of [1] and [2], which star is brighter?"], "1. How bright is the star sirius?": "Relate(\"Sirius (star)\", \"brightness\")", "2. How bright is the star Alpha Centauri?": "Relate(\"Alpha Centauri (star)\", \"brightness\")", "3. Given answers of [1] and [2], which star is brighter?": "[END]"}"""

crag_ex7_q = "what movie won the most oscars, Lincoln or The Girl with the Dragon Tattoo?"
crag_ex7 = """{"what movie won the most oscars, Lincoln or The Girl with the Dragon Tattoo?": ["1. How many oscars did the movie Lincoln win?", "2. How many oscars did the movie The Girl with the Dragon Tattoo win?", "3. Given answers of [1] and [2], which movie won the most oscars?"], "1. How many oscars did the movie Lincoln win?": "Relate(\"Lincoln (movie)\", \"number of oscars\")", "2. How many oscars did the movie The Girl with the Dragon Tattoo win?": "Relate(\"The Girl with the Dragon Tattoo (movie)\", \"number of oscars\")", "3. Given answers of [1] and [2], which movie won the most oscars?": "[END]"}"""

### Mixed

# simple, zero-hop
crag_ex8_q = "what was the overall worldwide box office revenue for invictus?"
crag_ex8 = """{"what was the overall worldwide box office revenue for invictus?": "Relate(\"Invictus\", \"overall worldwide box office revenue\")"}"""

# simple, finance, zero-hop
crag_ex9_q = "what was the total value of all exchange-traded funds (etfs) in the united states in 2020?"
crag_ex9 = """{"what was the total value of all exchange-traded funds (etfs) in the united states in 2020?": "Relate(\"exchange-traded funds (etfs)\", \"total value of all in the United States in 2020\")"}"""

# simple, sports, zero-hop
crag_ex10_q = "how many points did heat score in their contest on 2023-06-12?"
crag_ex10 = """{"how many points did heat score in their contest on 2023-06-12?": "Relate(\"Heat\", \"points scored on 2023-06-12\")"}"""

# comparison
crag_ex11_q = "what is difference between long-term and short-term capital gains?"
crag_ex11 = """{"what is difference between long-term and short-term capital gains?": ["1. What are long-term capital gains?", "2. What are short-term capital gains?", "3. Given answers of [1] and [2], what is their difference?"], "1. What is long-term capital gains?": "Search(\"long-term capital gains\")", "2. What is short-term capital gains?": "Search(\"short-term capital gains\")", "3. Given answers of [1] and [2], what is their difference?": "[END]"}"""

# simple, most question, zero-hop
crag_ex12_q = "what is the deepest oceanic trench on earth?"
crag_ex12 = """{"what is the deepest oceanic trench on earth?": "Search(\"Deepest oceanic trench on earth\")"}"""

# simple, most question, zero-hop
crag_ex13_q = "who are the biggest investors in amazon?"
crag_ex13 = """{"who are the biggest investors in amazon?": "Relate(\"Amazon\", \"Biggest Investors\")"}"""

# simple_w_comparison (filter)
crag_ex14_q = "what album did lady gaga release in 2009, which included the songs \"bad romance\" and \"telephone\"?"
crag_ex14 = """{"what album did lady gaga release in 2009, which included the songs \"bad romance\" and \"telephone\"?": ["1. What albums did Lady Gaga release in 2009?", "2. Among [1], which album included the songs \"Bad Romance\" and \"Telephone\"?"], "2. What albums did Lady Gaga release in 2009?": "Relate(\"Lady Gaga\", \"albums released in 2009\")", "2. Among [1], which album included the songs \"bad romance\" and \"telephone\"?": "Filter([1], \"includes songs Bad Romance and Telephone\")"}"""

# multi-hop
crag_ex15_q = "how big is the biggest state in the us?"
crag_ex15 = """{"how big is the biggest state in the us?": ["1. What is the biggest state in the US?", "2. How big is [1]?"], "1. What is the biggest state in the US?": "Search(\"biggest state in US\")", "2. How big is [1]?": "Relate([1], \"geographical size\")"}"""

crag_ex16_q = "what was the highest-grossing movie in the box office in 2022?"
crag_ex16 = """{"what was the highest-grossing movie in the box office in 2022?": "Search(\"Highest-grossing movie in the box office in 2022\")"}"""

# simple_w_condition, how many question
crag_ex17_q = "how many times has angelina jolie played maleficent in a movie?"
crag_ex17 = """{"how many times has angelina jolie played maleficent in a movie?": ["1. What movies involving maleficient has Angelina Jolie casted for?", "2. Among [1], in which movies has Angelina Jolie played maleficient?", "3. Given answers of [1] and [2], how many times has Angelina Jolie played maleficent in a movie?"], "1. What movies involving maleficient has Angelina Jolie casted for?": "Relate(\"Angelina Jolie\", \"movies involving maleficient\")", "2. Among [1], in which movies has Angelina Jolie played maleficient?": "Filter([1], \"Angelina Jolie plays maleficient\")", "3. Given answers of [1] and [2], how many times has Angelina Jolie played maleficent in a movie?": "[END]"}"""

# simple
# crag_ex18_q = "can you name the members of the the bastard fairies group for me?"
# crag_ex18 = """{"can you name the members of the the bastard fairies group for me?": "Relate(\"Bastard Fairies Group\", \"members\")"}"""

crag_ex18_q = "which team did boston celtics take on in their matchup on 2023-05-29?"
crag_ex18 = """{"which team did boston celtics take on in their matchup on 2023-05-29?": "Relate(\"Boston Celtics\", \"2023-05-29 matchup opponent\")"}"""

# crag_ex20_q = "what album did kings of leon release in 2013, which included the songs \"wait for me\" and \"family tree\"?"
# crag_ex20 = """{"what album did kings of leon release in 2013, which included the songs \"wait for me\" and \"family tree\"?": ["1. What albums did Kings of Leon release in 2013?", "2. Among [1], which album included the songs  \"wait for me\" and \"family tree\"?"], "1. What albums did Kings of Leon release in 2013?": "Relate(\"Kings of Leon\", \"albums released in 2013\")", "2. Among [1], which album included the songs \"Wait For Me\" and \"Family Tree\"?": "Filter([1], \"includes songs Wait for Me and Family Tree\")"}"""

# multi-hop with filter
crag_ex19_q = "which player has the most career passing yards in the nfl among players who have never won a championship?"
crag_ex19 = """{"which player has the most career passing yards in the nfl among players who have never won a championship?": ["1. Who are NFL players who have never won a championship?", "2. Among [1], who has the most career passing cards?"], "1. Who are NFL players who have never won a championship?": "Search(\"NFL players\", \"has never won a championship\")", "2. Among [1], who has the most career passing cards?": "Filter([1], \"has the most career passing cards\")"}"""

# comparison
crag_ex20_q = "in 2022, did brooklyn nets win more games than boston celtics?"
crag_ex20 = """{"in 2022, did brooklyn nets win more games than boston celtics?": ["1. How many games did Brooklyn Nets win in 2022?", "2. How many games did Boston Celtics win in 2022?", "3. Given answers of [1] and [2], did Brooklyn Nets win more games than Boston Celtics?"], "1. How many games did Brooklyn Nets win in 2022?": "Relate(\"Brooklyn Nets\", \"number of wins in 2022\")", "2. How many games did Boston Celtics win in 2022?": "Relate(\"Boston Celtics\", \"number of wins in 2022\")", "3. Given answers of [1] and [2], did Brooklyn Nets win more games than Boston Celtics?": "[END]"}"""

# simple, finance
crag_ex21_q = "what was the low price of meta stock on feb 14 2024?"
crag_ex21 = """{"what was the low price of meta stock on feb 14 2024?": "Relate(\"Meta stock\", \"low price on Feb 14 2024\")"}"""


# deleted: Do not use Filter() for "largest" or "most" queries: use Search() instead. For example, to find the largest country that is bordered by the pacific ocean, instead of calling Filter(\"countries bordered by the Pacific Ocean\", \"largest\"), call Search(\"largest country bordered by the Pacific Ocean\").
def format_tree_generation_prompt_crag(question):
    prompt = f"""You are given 3 atomic functions to help you retrieve and operate knowledge from Google, Wikipedia, and Wikidata: 
1. Search(). Input: (name, [optional] descriptor). Output: list[entities]. This function helps you find and disambiguate an entity--i.e. people, artworks, organizations--given a name and optional descriptor. For example, Search(\"Harry Potter and the Sorcerer's Stone\", \"2001 movie\") returns the entity ["Harry Potter and the Philosopher's Stone (film)"]. When the name of the entity is unknown, you can replace the name parameter with a descriptive title. For example, Search(\"2019 NFL MVP\") returns 2019 NFL MVP player ["Lamar Jackson"]. You can also use Search() to find "largest", "first", or "most" entities. For example, Search(\"first movie to be filmed entirely in outer space\") returns ["Vyzov"], the first feature-length film shot entirely in space.
2. Relate(). Input: there are 2 possibilities, (head_entity, relation) or (head_entity, attribute). Output: list[tail_entities] or list[attribute_values]. This function helps you find the tail_entities given a head_entity and relation. For example, Relate(\"Australia\", \"capital\") returns ["Sydney"], while Relate(\"The Beatles\", \"members\") returns ["John Lennon", "Paul McCartney", "George Harrison", "Ringo Starr"]. You may also query attributes using Relate() by treating attributes as relations and attribute values as tail entities. For example, Relate(\"Rainway\", \"initial launch date\") returns ["January 20, 2018"], and Relate(\"California\", \"geographical area\") returns ["163,696 square miles"].
3. Filter(). Input: (list[entities], condition). Output: list[entities]. This function helps you filter out entities that satisfy a factual attribute condition. For example, Filter([\"Lionel Messi\", \"Steven Jobs\", \"Bill Gates\"], \"born in 1955\") returns ["Steven Jobs", "Bill Gates"].
Construct a hierarchical question decomposition tree in json format for the following complex question: \"{question}\". The tree starts with the original complex question as the root node, and each non-root node is a sub-question of its parent. Continue decomposing until a sub-question cannot be further decomposed and could either be: (1) directly answered by calling one of the three atomic functions Search(), Relate(), Filter(), or (2) directly answered by analyzing the answers of at least two previously answered questions, such as comparing, judging, intersecting, counting, etc. In case (1), write this sub-question with its corresponding function call as a leaf node. In case (2), write this sub-question with an [END] mark as a leaf node. For function leaf nodes, do not write nested functions such as Filter(Search(...)): if multiple function calls are required, write each function call with a separate sub-question in a separate leaf node. For [END] leaf questions, format your question as "Given answers of [q_idx_1] and [q_idx_2], ...", where [q_idx_1] and [q_idx_2] are question indices of the previously answered questions required to answer this [END] question. In your question decomposition tree, use double quotes "" to enclose sub-questions and functions, and escape quotes \"\" to enclose work titles and function parameters.
Examples: 
Question: {crag_ex0_q}
Decomposition Tree: {crag_ex0}
Question: {crag_ex1_q}
Decomposition Tree: {crag_ex1}
Question: {crag_ex2_q}
Decomposition Tree: {crag_ex2}
Question: {crag_ex3_q}
Decomposition Tree: {crag_ex3}
Question: {crag_ex4_q}
Decomposition Tree: {crag_ex4}
Question: {crag_ex5_q}
Decomposition Tree: {crag_ex5}
Question: {crag_ex6_q}
Decomposition Tree: {crag_ex6}
Question: {crag_ex7_q}
Decomposition Tree: {crag_ex7}
Question: {crag_ex8_q}
Decomposition Tree: {crag_ex8}
Question: {crag_ex9_q}
Decomposition Tree: {crag_ex9}
Question: {crag_ex10_q}
Decomposition Tree: {crag_ex10}
Question: {crag_ex11_q}
Decomposition Tree: {crag_ex11}
Question: {crag_ex12_q}
Decomposition Tree: {crag_ex12}
Question: {crag_ex13_q}
Decomposition Tree: {crag_ex13}
Question: {crag_ex14_q}
Decomposition Tree: {crag_ex14}
Question: {crag_ex15_q}
Decomposition Tree: {crag_ex15}
Question: {crag_ex16_q}
Decomposition Tree: {crag_ex16}
Question: {crag_ex17_q}
Decomposition Tree: {crag_ex17}
Question: {crag_ex18_q}
Decomposition Tree: {crag_ex18}
Question: {crag_ex19_q}
Decomposition Tree: {crag_ex19}
Question: {crag_ex20_q}
Decomposition Tree: {crag_ex20}
Question: {crag_ex21_q}
Decomposition Tree: {crag_ex21}

Your Question.
Question: {question}
Decomposition Tree: """
    
    return prompt



"""
BlendQA
"""

### KG-Web

# type 1
blendqa_ex1_q = "When did the person after whom Nehru Zoological Park is named first visit the US?"
blendqa_ex1 = """{"When did the person after whom Nehru Zoological Park is named first visit the US?": ["1. Who is the person after whom Nehru Zoological Park is named?", "2. When did [1] first visit the US?"], "1. Who is the person after whom Nehru Zoological Park is named?": ["3. What is the Nehru Zoological Park?", "After whom was [3] named?"], "3. What is the Nehru Zoological Park?": "Search(\"Nehru Zoological Park\")", "After whom was [3] named?": "Relate([3], \"named after person\")", "2. When did [1] first visit the US?": "Relate([1], \"first US visit date\")"}"""

blendqa_ex2_q = "What significant military action was taken by the republic that contains the administrative territorial entity of Al Jazirah on September 26, 2024?"
blendqa_ex2 = """{"What significant military action was taken by the republic that contains the administrative territorial entity of Al Jazirah on September 26, 2024?": ["1. What is the republic that contains the administrative territorial entity of Al Jazirah?", "2. What significant military action was taken by [1] on September 26, 2024?"], "1. What is the republic that contains the administrative territorial entity of Al Jazirah?": ["3. What is Al Jazirah?", "4. What is the republic that contains the administrative territorial entity of [3]?"], "3. What is Al Jazirah?": "Search(\"Al Jazirah\")", "4. What is the republic that contains the administrative territorial entity of [3]?": "Relate([3], \"republic that contains the territorial entity\")", "2. What significant military action was taken by [1] on September 26, 2024?": "Relate([1], \"significant military action on September 26, 2024\")"}"""

blendqa_ex3_q = "How many people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born on December 21, 2023?"
blendqa_ex3 = """{"How many people were killed in the mass shooting in the region of the Czech where Daniel Pudil was born on December 21, 2023?": ["1. In what region of the Czech was Daniel Pudil born?", "2. How many people were killed in the mass shooting in [1] on December 21, 2023?"], "1. In what region of the Czech was Daniel Pudil born?": ["3. Who is Daniel Pudil?", "4. In what region of the Czech was [3] born?"], "3. Who is Daniel Pudil?": "Search(\"Daniel Pudil\")", "4. In what region of the Czech was [3] born?": "Relate([3], \"place of birth\")", "2. How many people were killed in the mass shooting in [1] on December 21, 2023?": "Relate(\"mass shooting in [1] on December 21, 2023\", \"number of people killed\")"}"""

# type 2
blendqa_ex4_q = "Was the body of the missing American hiker found in September 2024 on the mountain that is part of the new7wonders of nature?"
blendqa_ex4 = """{"Was the body of the missing American hiker found in September 2024 on the mountain that is part of the new7wonders of nature?": ["1. What mountain is part of the new7wonders of nature?", "2. Was the body of the missing American hiker found in September 2024 on [1]?"], "1. What mountain is part of the new7wonders of nature?": ["3. What is the new7wonders of nature?", "4. What mountain is part of [3]?"], "3. What is the new7wonders of nature?": "Search(\"new7wonders of nature\")", "4. What mountain is part of [3]?": "Relate([3], \"mountain\")", "2. Was the body of the missing American hiker found in September 2024 on [1]?": "Relate(\"missing American hiker\", \"body found on [1] in September 2024\")"}"""

blendqa_ex5_q = "What was the contribution of the tennis player born on May 5, 2003, to Team Europe's victory in the Laver Cup on September 22, 2024?"
blendqa_ex5 = """{"What was the contribution of the tennis player born on May 5, 2003, to Team Europe's victory in the Laver Cup on September 22, 2024?": ["1. Who was the tennis player born on May 5, 2003?", "2. What was [1]'s contribution to Team Europe's victory in the Laver Cup on September 22, 2024?"], "1. Who was the tennis player born on May 5, 2003?": "Search(\"tennis player born on May 5, 2003\")", "2. What was [1]'s contribution to Team Europe's victory in the Laver Cup on September 22, 2024?": "Relate([1], \"contribution to Team Europe's victory in the Laver Cup on September 22, 2024\")"}"""

blendqa_ex6_q = "When did the Republican Governors Association indicate it would stop making further media placements for the campaign of the football player born on July 24, 1981?"
blendqa_ex6 = """{"When did the Republican Governors Association indicate it would stop making further media placements for the campaign of the football player born on July 24, 1981?": ["1. Who is the football player born on July 24, 1981?", "2. When did the Republican Governors Association indicate it would stop making further media placements for the campaign of [1]?"], "1. Who is the football player born on July 24, 1981?": "Search(\"football player born on July 24, 1981\")", "2. When did the Republican Governors Association indicate it would stop making further media placements for the campaign of [1]?": "Relate([1], \"Republican Governors Association media placement stop date\")"}"""

### Text-KG

blendqa_ex7_q = "Who has 2 tapes in the television series that is a notable work of Christian Lee Navarro?"
blendqa_ex7 = """{"Who has 2 tapes in the television series that is a notable work of Christian Lee Navarro?": ["1. What is the television series that is a notable work of Christian Lee Navarro?", "2. Who has 2 tapes in [1]?"], "1. What is the television series that is a notable work of Christian Lee Navarro?": ["3. Who is Christian Lee Navarro?", "4. Which television series is a notable work of [3]?"], "3. Who is Christian Lee Navarro?": "Search(\"Christian Lee Navarro\")", "4. Which television series is a notable work of [3]?": "Relate([3], \"notable television series\")", "2. Who has 2 tapes in [1]?": "Relate([1], \"person who has 2 tapes\")"}"""

blendqa_ex8_q = "When did the economic crisis in Kuhle Wampe reach its peak?"
blendqa_ex8 = """{"When did the economic crisis in Kuhle Wampe reach its peak?": ["1. What is the economic crisis in Kuhle Wampe?", "2. When did [1] reach its peak?"], "1. What is the economic crisis in Kuhle Wampe?": ["3. What is Kuhle Wampe?", "4. What isthe economic crisis in [3]?"], "3. What is Kuhle Wampe?": "Search(\"Kuhle Wampe\")", "4. What is the economic crisis in [3]?": "Relate([3], \"economic crisis\")", "2. When did [1] reach its peak?": "Relate([1], \"reached its peak at time\")"}"""

blendqa_ex9_q = "Where do I go to get the financial product associated with the industry of RPM Mortgage, Inc.?"
blendqa_ex9 = """{"Where do I go to get the financial product associated with the industry of RPM Mortgage, Inc.?": ["1. What is the financial product associated with the industry of RPM Mortgage, Inc.?", "2. Where do I go to get [1]?"], "1. What is the financial product associated with the industry of RPM Mortgage, Inc.?": ["3. What is RPM Mortgage Inc.?", "4. What is the financial product associated with the industry of [3]?"], "3. What is RPM Mortgage Inc.?": "Search(\"RPM Mortgage Inc.\")", "4. What is the financial product associated with the industry of [3]?": "Relate([3], \"financial product\")", "2. Where do I go to get [1]?": "Relate([1], \"typical provider\")"}"""

### Web-Text

blendqa_ex10_q = "Who sang the song by The Eagles about the rock and roll lifestyle?"
blendqa_ex10 = """{"Who sang the song by The Eagles about the rock and roll lifestyle?": ["1. What is the song by The Eagles about the rock and roll lifestyle?", "2. Who sang the song [1]?"], "1. What is the song by The Eagles about the rock and roll lifestyle?": ["3. Who are The Eagles?", "4. What is the song by [3] about the rock and roll lifestyle?"], "3. Who are The Eagles?": "Search(\"The Eagles\", \"band\")", "4. What is the song by [3] about the rock and roll lifestyle?": "Relate([3], \"song about the rock and roll lifestyle\")", "2. Who sang the song [1]?": "Relate([1], \"singer\")"}"""

blendqa_ex11_q = "In the context of the enzyme that breaks down lactose into glucose and galactose, where is it found in the human body?"
blendqa_ex11 = """{"In the context of the enzyme that breaks down lactose into glucose and galactose, where is it found in the human body?": ["1. What is the enzyme that breaks down lactose into glucose and galactose?", "2. In the context of [1], where is it found in the human body?"], "1. What is the enzyme that breaks down lactose into glucose and galactose?": "Search(\"Enzyme that breaks down lactose into glucose and galactose\")", "2. In the context of [1], where is it found in the human body?": "Relate([1], \"location in human body\")"}"""

blendqa_ex12_q = "When were the medieval pilgrimage stories by Geoffrey Chaucer written, and in what language?"
blendqa_ex12 = """{"When were the medieval pilgrimage stories by Geoffrey Chaucer written, and in what language?": ["1. What are the medieval pilgrimage stories by Geoffrey Chaucer?", "2. When were [1] written, and in what language?"], "1. What are the medieval pilgrimage stories by Geoffrey Chaucer?": ["3. Who is Geoffrey Chaucer?", "4. What are the medieval pilgrimage stories by [3]?"], "3. Who is Geoffrey Chaucer?": "Search(\"Geooffrey Chaucer\", \"writer\")", "4. What are the medieval pilgrimage stories by [3]?": "Relate([3], \"medieval pilgrimage stories\")", "2. When were [1] written, and in what language?": "Relate([1], \"written at time and in language\")"}"""

### Mixed

# KG-Web type 2
blendqa_ex13_q = "What does the social networking service that employs Ryan Roslansky use to enhance its artificial intelligence model in September 2024?"
blendqa_ex13 = """{"What does the social networking service that employs Ryan Roslansky use to enhance its artificial intelligence model in September 2024?": ["1. What is the social networking service that employs Ryan Roslansky?", "2. What does [1] use to enhance its artificial intelligence model in September 2024?"], "1. What is the social networking service that employs Ryan Roslansky?": ["3. Who is Ryan Roslansky?", "4. What is the social networking service that employs [3]?"], "3. Who is Ryan Roslansky?": "Search(\"Ryan Roslansky\")", "4. What is the social networking service that employs [3]?": "Relate([3], \"employed by social networking service\")", "2. What does [1] use to enhance its artificial intelligence model in September 2024?": "Search(\"What does [1] use to enhance its artificial intelligence model in September 2024\")"}"""

# Text-KG with [END]
blendqa_ex14_q = "Is the episcopal see where Georges Garreau was born known as the city of love or the city of lights?"
blendqa_ex14 = """{"Is the episcopal see where Georges Garreau was born known as the city of love or the city of lights?": ["1. What is the episcopal see where Georges Garreau was born?", "2. Is [1] known as the city of love?", "3. Is [1] known as the city of lights?", "4. Given answers of [2] and [3], is [1] known as the city of love or city of lights?"], "1. What is the episcopal see where Georges Garreau was born?": "Relate(\"Georges Garreau\", \"place of birth\")", "2. Is [1] known as the city of love?": "Relate([1], \"known as city of love\")", "3. Is [1] known as the city of lights?": "Relate([1], \"known as city of lights\")", "4. Given answers of [2] and [3], is [1] known as the city of love or city of lights?": "[END]"}"""

# Web-Text
blendqa_ex15_q = "How did the bat of the record-holder for most home runs in the home run derby impact Nick Mahrley during the game?"
blendqa_ex15 = """{"How did the bat of the record-holder for most home runs in the home run derby impact Nick Mahrley during the game?": ["1. Who has the record for most home runs in the home run derby?", "2. How did the bat of [1] impact Nick Mahrley during the game?"], "1. Who has the record for most home runs in the home run derby?": "Search(\"Record holder for the most home runs in the home run derby\")", "2. How did the bat of [1] impact Nick Mahrley during the game?": "Search(\"How did the bat of [1] impact Nick Mahrley during the game\")"}"""

# Text-KG
blendqa_ex16_q = "Who was the first person buried at the United States national cemetery where Willard A. Kitts is buried?"
blendqa_ex16 = """{"Who was the first person buried at the United States national cemetery where Willard A. Kitts is buried?": ["1. What is the United States national cemetry where Willard A. Kitts is buried?", "2. Who was the first person buried at [1]?"], "1. What is the United States national cemetry where Willard A. Kitts is buried?": ["3. Who is Willard A. Kitts?", "4. What is the United States national cemetry where [3] is buried?"], "3. Who is Willard A. Kitts?": "Search(\"Willard A. Kitts\")", "4. What is the United States national cemetry where [3] is buried?": "Relate([3], \"buried at United States national cemetry\")", "2. Who was the first person buried at [1]?": "Relate([1], \"first person buried\")"}"""

# Web-Text with Filter
blendqa_ex17_q = "What is the career high points in a game of the electrifying dunker with an NBA-record 22 seasons?"
blendqa_ex17 = """{"What is the career high points in a game of the electrifying dunker with an NBA-record 22 seasons?": ["1. Who is the electrifying dunker with an NBA-record 22 seasons?", "2. What is the career high points in a game of [1]?"], "1. Who is the electrifying dunker with an NBA-record 22 seasons?": ["3. Who holds the NBA record for 22 seasons?", "4. Who among [3] is known as an electrifying dunker?"], "3. Who holds the NBA record for 22 seasons?": "Search(\"NBA player with record 22 seasons\")", "4. Among [3], who is known as an electrifying dunker?": "Filter([3], \"known as electrifying dunker\")", "2. What is the career high points in a game of [1]?": "Relate([1], \"career high points in a game\")"}"""

# Text-KG commonsense long sub-q
blendqa_ex18_q = "What is the anatomical name for the body part associated with the musical group that performs the song 'Asleep in the Back'?"
blendqa_ex18 = """{"What is the anatomical name for the body part associated with the musical group that performs the song 'Asleep in the Back'?": ["1. What is the musical group that performs the song 'Asleep in the Back'?", "2. What is the anatomical name for the body part associated with [1]?"], "1. What is the musical group that performs the song 'Asleep in the Back'?": "Search(\"music group that performs the song Asleep in the Back\")", "2. What is the anatomical name for the body part associated with [1]?": "Relate([1], \"anatomical name for body part\")"}"""

# Web-Text
blendqa_ex19_q = "What key factor is driving the overall decline in overdose deaths in the city famous for its large Cinco de Mayo celebration?"
blendqa_ex19 = """{"What key factor is driving the overall decline in overdose deaths in the city famous for its large Cinco de Mayo celebration?": ["1. What city is famous for its large Cinco de Mayo celebration?", "2. What key factor is driving the overall decilne in overdose deaths in [1]?"], "1. What city is famous for its large Cinco de Mayo celebration?": ["3. What is the Cinco de Mayo celebration?", "4. What city is famous for [3]?"], "3. What is the Cinco de Mayo celebration?": "Search(\"Cinco de Mayo\", \"celebration\")", "4. What city is famous for [3]?": "Relate([3], \"city famous for\")", "2. What key factor is driving the overall decilne in overdose deaths in [1]?": "Search(\"key factor driving the overall decline in overdose deaths in [1]\")"}"""

# Text-KG
blendqa_ex20_q = "Who played Joe in the film directed by Darren Grant featuring cast member Tiffany Evans?"
blendqa_ex20 = """{"Who played Joe in the film directed by Darren Grant featuring cast member Tiffany Evans?": ["1. What is the film directed by Darren Grant featuring cast member Tiffany Evans?", "2. Who played Joe in the film [1]?"], "1. What is the film directed by Darren Grant featuring cast member Tiffany Evans?": ["3. Who is Darren Grant?", "4. What is the film directed by [3] featuring cast member Tiffany Evans?"], "3. Who is Darren Grant?": "Search(\"Darren Grant\", \"film director\")", "4. What is the film directed by [3] featuring cast member Tiffany Evans?": "Relate([3], \"film directed featuring Tiffany Evans\")", "2. Who played Joe in the film [1]?": "Relate([1], \"actor who played Joe\")"}"""

# KG-Web type 1
blendqa_ex21_q = "What was the final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and the island nation where Praia is located?"
blendqa_ex21 = """{"What was the final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and the island nation where Praia is located?": ["1. What is the island nation where Praia is located?", "2. What was the final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and [1]?"], "1. What is the island nation where Praia is located?": ["3. What is Praia?", "4. What is the island nation where [3] is located?"], "3. What is Praia?": "Search(\"Praia\", \"location\")", "4. What is the island nation where [3] is located?": "Relate([3], \"located in island nation\")", "2. What was the final score on January 23, 2024, in the Africa Cup of Nations match between Egypt and [1]?": "Relate([1], \"final score on January 23, 2024 in the Africa Cup of Nations between Egypt\")"}"""


def format_tree_generation_prompt_blendqa(question):
    prompt = f"""You are given 3 atomic functions to help you retrieve and operate knowledge from Google, Wikipedia, or Wikidata:
1. Search(). Input: (name, [optional] descriptor). Output: list[entities]. This function helps you find and disambiguate an entity given its name and optional descriptor. If no descriptor is provided, the most popular entity will be returned. For example, Search(\"Michael Jordan\") returns the famous basketball player ["Michael Jordan"], while Search(\"Michael Jordan\", \"football goalkeeper\") returns the English retired football goalkeeper ["Michael Jordan (footballer)"]. When the question provides explicit entity knowledge, always write a descriptor for the Search() function based on the question's information. If the entity name is unknown, can also query Search() with a descriptive title. For example, Search(\"The first president to be assassinated\") returns ["Abraham Lincoln"], who is the first U.S. president to be assassinated.
2. Relate(). Input: there are 2 input possibilities, (head_entity, relation), or (head_entity, tail_entity). Output: list[tail_entities], or list[relations]. This function helps you find the tail_entities given a head_entity and relation, or relations given a head_entity and tail_entity. For example, Relate(\"Barack Obama\", \"child\") returns ["Malia Obama", "Sasha Obama"], and Relate(\"Barack Obama\", \"Michelle Obama\") returns ["spouse"]. You may also search attribute relations using Relate() by treating attributes as tail entities. For example, Relate(\"Barack Obama\", \"time served as US president\") returns ["1997 to 2004"], and Relate(\"Barack Obama\", \"1961\")" returns ["year of birth"].
3. Filter(). Input: (list[entities], condition). Output: list[entities]. This function helps you filter out entities that satisfy a factual attribute condition. For example, Filter([\"Lionel Messi\", \"Steven Jobs\", \"Bill Gates\"], \"born in 1955\"), returns [\"Bill Gates\", \"Steve Jobs\"], and Filter([\"Lionel Messi\", \"Cristiano Ronaldo\"], \"is Portuguese\") returns ["Cristiano Ronaldo"].
Construct a hierarchical question decomposition tree in json format for the following complex question: \"{question}\". The tree starts with the original complex question as the root node, and each non-root node is a sub-question of its parent. Continue decomposing until a sub-question cannot be further decomposed and could either be: (1) directly answered by calling one of the three atomic functions Search(), Relate(), Filter(), or (2) directly answered by analyzing the answers of at least two previously answered questions, such as comparing, judging, intersecting, counting, etc. In case (1), write this sub-question with its corresponding function call as a leaf node. In case (2), write this sub-question with an [END] mark as a leaf node. For function leaf nodes, do not write nested functions such as Filter(Search(...)): if multiple function calls are required, write each function call with a separate sub-question in a separate leaf node. For [END] leaf questions, format your question as "Given answers of [q_idx_1] and [q_idx_2], ...", where [q_idx_1] and [q_idx_2] are question indices of the previously answered questions required to answer this [END] question. In your question decomposition tree, use double quotes "" to enclose sub-questions and functions, and escape quotes \"\" to enclose work titles and function parameters.
Examples: 
Question: {blendqa_ex1_q}
Decomposition Tree: {blendqa_ex1}
Question: {blendqa_ex2_q}
Decomposition Tree: {blendqa_ex2}
Question: {blendqa_ex3_q}
Decomposition Tree: {blendqa_ex3}
Question: {blendqa_ex4_q}
Decomposition Tree: {blendqa_ex4}
Question: {blendqa_ex5_q}
Decomposition Tree: {blendqa_ex5}
Question: {blendqa_ex6_q}
Decomposition Tree: {blendqa_ex6}
Question: {blendqa_ex7_q}
Decomposition Tree: {blendqa_ex7}
Question: {blendqa_ex8_q}
Decomposition Tree: {blendqa_ex8}
Question: {blendqa_ex9_q}
Decomposition Tree: {blendqa_ex9}
Question: {blendqa_ex10_q}
Decomposition Tree: {blendqa_ex10}
Question: {blendqa_ex11_q}
Decomposition Tree: {blendqa_ex11}
Question: {blendqa_ex12_q}
Decomposition Tree: {blendqa_ex12}
Question: {blendqa_ex13_q}
Decomposition Tree: {blendqa_ex13}
Question: {blendqa_ex14_q}
Decomposition Tree: {blendqa_ex14}
Question: {blendqa_ex15_q}
Decomposition Tree: {blendqa_ex15}
Question: {blendqa_ex16_q}
Decomposition Tree: {blendqa_ex16}
Question: {blendqa_ex17_q}
Decomposition Tree: {blendqa_ex17}
Question: {blendqa_ex18_q}
Decomposition Tree: {blendqa_ex18}
Question: {blendqa_ex19_q}
Decomposition Tree: {blendqa_ex19}
Question: {blendqa_ex20_q}
Decomposition Tree: {blendqa_ex20}
Question: {blendqa_ex21_q}
Decomposition Tree: {blendqa_ex21}

Your Question.
Question: {question}
Decomposition Tree: """
    
    return prompt

