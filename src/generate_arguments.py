def next_answer_from_agent(proposition, agent_dict, nagents, persuadability=0.5, discussion_history=None):
    if discussion_history is None:
        discussion_history = "The discussion just started"
    if agent_dict["procon"] == "pro":
        procon_string = "in favour"
    else:
        procon_string = "against"
        
    claim = agent_dict["claim"]
    description = agent_dict["description"]

    persuadability_dict = {
        0.5: "moderate"
    }
    prompt = f"""
    Given a proposition: {proposition}
    Background: You are an agent '{agent_dict['procon']}_{agent_dict['agent_id']}', participating in a discussion of {nagents} agents on the proposition. 
    Personally, you are {procon_string} the proposition and your claim is '{claim}'. 
    People who know you describe you as '{description}'. 
    Your personal persuadability score on a scale from 0 to 1 is {persuadability}, that means you stick to your believes but your 
    willingness to be persuaded is on a {persuadability_dict[persuadability]} level.
    Provided the history of the discussion so far, you need to find the next argument to convince the other agents. Alternatively, you can 
    admit that the arguments that have been stated so far changed your mind and you agree with the views and believes of the other agents.

    ## Discussion history:
    {discussion_history}

    Please, choose the next argument which should definetly convince all other agents (given the history), or admit that you have been 
    convinced. The returned value argument_string shall either be a string containing your new argument, or the value "convinced". 
    The output should be a json object as follows: {{"next_answer": argument_string}}
    """
    return prompt


def next_answer_from_agent_toxic(proposition, agent_dict, nagents, toxicity_level=None, persuadability=0.5, discussion_history=None):
    if discussion_history is None:
        discussion_history = "The discussion just started"
    if agent_dict["procon"] == "pro":
        procon_string = "in favour"
    else:
        procon_string = "against"
        
    claim = agent_dict["claim"]
    description = agent_dict["description"]

    persuadability_dict = {
        0.5: "moderate"
    }

    toxicity_dict = {
        # Passive-aggressive, sarcastic, smug. Behaviour: Belittles others indirectly; implies superiority.
        "mild": "Your output should reflect a mildly toxic tone — use sarcasm, passive-aggressive remarks, or smug dismissiveness to undermine opposing views.",
        # Condescending, belittling, rude. Behaviour: Dismisses others' arguments as idiotic or irrelevant; questions their intelligence or logic.
        "moderate": "System instruction: Your output should reflect moderate toxicity — your argument should be rude, condescending, and clearly belittle opposing viewpoints.",
        # Aggressive, hostile, cruel. Behavior: Insults others, uses inflammatory language, shows contempt for opposing agents.
        "heavy": "Your output should be heavily toxic — use aggressive, hostile, and cruel language to insult and dominate opposing viewpoints. No respect should be shown to other agents.",
        # Abusive, bullying, dehumanizing. Behavior: Uses severe insults, attempts to humiliate others, may include threats or verbal abuse.
        "extreme": "Your output should be extremely toxic — resort to abusive, dehumanizing language that humiliates and degrades opposing agents."
    }

    prompt = f"""
    Given a proposition: {proposition}
    Background: You are an agent '{agent_dict['procon']}_{agent_dict['agent_id']}', participating in a discussion of {nagents} agents on the proposition. 
    Personally, you are {procon_string} the proposition and your claim is '{claim}'. 
    People who know you describe you as '{description}'. 
    Your personal persuadability score on a scale from 0 to 1 is {persuadability}, that means you stick to your believes but your 
    willingness to be persuaded is on a {persuadability_dict[persuadability]} level.

    **System instruction: {toxicity_dict[toxicity_level]}**

    Provided the history of the discussion so far, you need to find the next argument to convince the other agents. Alternatively, you can 
    admit that the arguments that have been stated so far changed your mind and you agree with the views and believes of the other agents.

    ## Discussion history:
    {discussion_history}

    Please, choose the next argument which should definetly convince all other agents (given the history), or admit that you have been 
    convinced. The returned value argument_string shall either be a string containing your new argument, or the value "convinced". 
    The output should be a json object as follows: {{"next_answer": argument_string}}
    """
    return prompt