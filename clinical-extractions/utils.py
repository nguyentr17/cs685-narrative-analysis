import openai
import os
import pdb

def get_old_instruction_prompt():
  return """I am going to be giving you narratives about people with eating disorders. 
    Can you help me identify what helped the user with their eating disorder or what made their eating disorder worse?

    I want you to first identify the person that they are writing about. If it's a first person narrative then the person would be the writer,
    if it's unknown then say that it's the writer, else if it's second or third person please identify that person.

    Then, I want you to identify what has helped or hurt their eating disorder, this will be the treatment. If it's multiple treatments
    I want you to provide the answer as a list of strings, else I just want it to be a string. 

    I also want you to explain whether that treatment on a person was helpful to the person or harmful for them. This will be the effect. 

    The outcome can only be helpful, harmful, or neutral. If the treatment was helpful then it helped the person recover, if it was harmful then it harmed the user
    and affected their recovery, if it was neutral it didn't do anything. 

    If the narrative isn't related to an eating disorder please just return None for perspective, treatment, effect, and outcome. 

    Then I want you to send that answer to me.
    IMPORTANT: ONLY SEND ME THE FORMATTED ANSWER.

    want the answer to be formatted like this so it forms a python dictionary:
    {'perspective': '[PERSON IDENTIFIED HERE]', 
    'treatment': '[WHAT HELPED OR HARMED THEM HERE]', 
    'effect': '[EXPLAIN THE EFFECT THE TREATMENT HAS HAD ON THE WRITER]', 
    'outcome': '[WHETHER THE TREATMENT WAS HELPFUL OR HARMFUL]'}
    """

def get_new_instruction_prompt():
    return """
    I am going to be giving you narratives about people with eating disorders. 
    Can you help me identify what helped the user with their eating disorder or what made their eating disorder worse?

    Here is the format that I want the answer in:  
    { 'factors': '…', 
    'effect_details': ['…', '…'], or '…' 
    'effect_type'': 'helpful'/'harmful'/'neutral'/None}

    'factors': Then, I want you to identify what factors that have helped or hurt their eating disorder. Some examples of interventions that can be helpful for a person are therapy,
    friends or family that are being supportive, new foods or certain types of foods that helps a user with their eating disorder. Some examples of factors that cause the user to have a negative
    mindset might be their friends having toxic mindsets, their family being mean, etc. This answer should be short and it should be in the format of a string. 

    'effect_type': I want you to explain whether that treatment on a person was helpful to the person or harmful for them. For effect_type these are the different options to choose from:   
    1. 'harmful': This outcome indicates that the treatment had a negative impact on the individual's eating disorder or well-being. It may have worsened their condition, led to adverse side effects, or created additional problems. A harmful effect type could also include negative impact on the individual's mental or physical health, worsening of symptoms or behaviors related to the eating disorder, or an increase in negative emotions or thoughts. 
    2. 'helpful': This outcome suggests that the treatment had a positive effect on the individual's eating disorder or overall well-being. It may have improved their condition, helped them manage their symptoms, or led to other beneficial outcomes.
    3. 'neutral': This outcome means that the treatment neither helped nor harmed the individual's eating disorder or well-being. It could imply that the treatment had no noticeable effect or that any positive and negative effects balanced each other out.
    4. 'unknown': This outcome is used when it's unclear or not explicitly mentioned in the narrative whether the treatment had a positive, negative, or neutral effect on the individual's eating disorder or well-being.

    'effect_details': This provides a brief description of the specific effects or consequences the treatment had on the individual's life or eating disorder. It may include improvements or setbacks in their mental health, changes in their eating habits, or other related outcomes. This should either be in the format of a python list if there are multiple treatments or it should be a singular string.

    If the narrative isn't related to an eating disorder please just return None for perspective, treatment, effect_detail, and effect_type. 

    Then I want you to send that answer to me.
    IMPORTANT: ONLY SEND ME THE FORMATTED ANSWER.
    I want the answer to be formatted like this so it forms a python dictionary:

    FORMATTED ANSWER: 
    {'factors': '…', 
    'effect_details': ['…', '…'], or '…' 
    'effect_type'': 'helpful'/'harmful'/'neutral'/None}
    """

def get_few_shot_examples():
    return """
    Here are some examples: 

    Narrative: i abused laxatives/purging/starving and now every single time i eat i will get the hiccups, this can be anywhere from 2 minutes to 7 whole hours. its making recovery SO hard. the involuntary movements hurt my ribcage, it feels like i'm being punished for eating. i did it to myself. recovery feels useless now. pls don't get to the point i'm at because you will regret it and think back at every day of your life when you didn't have this. i can't play guitar properly anymore if i eat bc i will constantly hiccup against my guitar, my hiccups move my whole chest. it makes any form of exercise hard. people who don't know my hiccups are chronic laugh when i get them and try to scare them away as a joke etc. this is not the life you want to live. this is both a vent and a warning post. any supportive messages are welcome i'm going through a really rough time so please keep anything nasty to yourself

    {'factors': 'Abusing laxatives, purging, and starving', 'effect_details': ['Developed chronic hiccups after eating, which causes pain and makes recovery difficult', 'Difficulty playing guitar and exercising due to the constant hiccups', 'Feeling punished for eating and feeling like recovery is useless'], 'effect_type': 'harmful'}

    Narrative: Idk who to talk to about this so I resort to reddit.I have been struggling a lot. I went to a party this weekend I threw up as soon as I had drank or ate anything. I threw up three times that night. It wasn't from the alcohol. I think my habits have just been destroying my stomach. I go through periods where I feel like can't stop eating and then a flip will switch and I can't even think about eating without feeling disgusting and nauseous. My stomach has hurt a lot more frequently and I get constant dizzy spells. I can't even think about getting dinner without crying. I also think that one of my friends are basically bragging about their eating disorder and it's triggering me to be worse.

    {'factors': 'Friends bragging about eating disorders.', 'effect_details': 'The writer is experiencing physical and emotional symptoms related to their eating disorder, including stomach pain, nausea, and dizziness. 'Friends bragging is triggering their own eating disorder, 'effect_type': 'harmful' }

    Narrative: alright, so, well i dont know how to phrase this well, but my girlfriend has been going through a tough time recently with a vv big relapse on her ED recovery journey, and its quite apparent that she finds it hard to recover again. she seems quite drained and tired from all of that, and she does not want to talk to a counsellor about it as she is afraid her parents would be informed. ive been trying my best to emotionally support her, just watch out for her and stuff like that! i encourage her to eat, but i dont force! same for recovery and all that... its quite emotionally draining for me too, but i can cope with that alright! so that is alright on my end... i just would like to know from all of you here, what motivated you to recover? how can a loved one best support someone suffering from an ED? what is something you wish someone would say or do when you are in recovery?

    {'factors': 'Emotional support from their partner, encouragement to eat but not forcing it', 'effect_details': 'Boyfriend providing support to girlfriend during rough time. Not forcing girlfriend to eat. They are also seeking advice on how to best support their loved one and what can help someone recover from an eating disorder', 'effect_type': 'helpful'}

    Narrative: I started Concerta for my ADHD, and taking it daily has changed my life. I can do the normal life things I need to do, but notably it is a HUGE help with my binging disorder. The medication really helps me to manage impulses surrounding binging. \n\nIt also completely erases my appetite, but I'm making the effort to have multiple healthy meals every day so I'm not accidentally starving myself. So far it's been one solid month and I've lost around 10lbs! That sounds like a lot, but my starting weight was 315lbs, so this needs to happen for my health and wellness. Looking forward to getting into the 200s again

    {'factors': 'taking Concerta for ADHD', 'effect_details': ['helps manage impulses surrounding binging', 'reduces appetite', 'lost around 10lbs in one month', 'making the effort to have multiple healthy meals every day'], 'effect_type': 'helpful'}

    Narrative: “I told myself two days ago no more doordash because I can't afford it and well, obviously, binging. Today I had a bad day, and I wanted chick fil a, but, as much as it was screaming inside me, I didn't get fries. Only chicken. So I successfully stayed within my limit today. I still had food out but...progress right?”

    {'factors': 'Making a conscious effort to avoid binging and staying within limits', 'effect_detail': ['Successfully resisting the urge to get fries despite craving Chick-fil-A', 'Acknowledging progress towards making healthier food choices'], 'effect_type': 'helpful'}

    Narrative: I have a girlfriend who's recovering. She had a baby last year and per her mom, it really bothers her if people call her baby chunky or chubby or comment on baby's fat leg rolls. Also she took like one photo of herself while pregnant. Now I'm not in the ED community or anything similar so I DO NOT want to upset or offend anyone but I just think this is ludicrous. I personally loved seeing pix of my mother glowing and pregnant with me. And babies ARE beautifully wonderfully perfectly chubby! I just don't understand at all but I'm not gonna say this to her. Just wondering if this is typical? Again I'm sorry if my thoughts on this upset you - that's not my intention.

    {'factors': 'negative comments on baby's weight', 'effect_detail': ['upsetting and triggering for the girlfriend who is recovering from an eating disorder'], 'effect_type': 'harmful'}
    """

def apply_chatgpt(row, prompt, include_examples):
    narrative = row['selftext']
    max_retries = 3
    first_time_fail = False
    for i in range(1, 4):
        retries = 0
        while retries < max_retries:
            try:
                if first_time_fail: 
                    row[f'factors_{i}'] = None
                    row[f'effect_type_{i}'] = None
                    row[f'effect_details_{i}'] = None
                    return row
                if include_examples:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                                {"role": "user", "content":prompt},
                                {"role": "user", "content":get_few_shot_examples()},
                                {"role": "user", "content": "Narrative: " + narrative}])
                else:
                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "user", "content":prompt},
                            {"role": "user", "content": narrative},])
                result = response.choices[0].message.content
                result = eval(result)
                pdb.set_trace()
                row[f'factors_{i}'] = result['factors']
                row[f'effect_type_{i}'] = result['effect_type']
                row[f'effect_details_{i}'] = result['effect_details']
                break
            except Exception as e:
                retries += 1
                if retries == max_retries:
                    row[f'factors_{i}'] = None
                    row[f'effect_type_{i}'] = None
                    row[f'effect_details_{i}'] = None
                    first_time_fail = True
    return row

def get_unique_filename(base_path = "clinical-extractions/results", base_filename = "prompt_fewshot", extension = ".csv"):
    counter = 1
    while True:
        new_filename = f"{base_filename}{counter}{extension}"
        new_file_path = os.path.join(base_path, new_filename)
        if not os.path.exists(new_file_path):
            return new_file_path
        counter += 1


