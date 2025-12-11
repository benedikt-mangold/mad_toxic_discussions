def generate_agent_pool_pro(proposition, panel_size):
    prompt = f"""
    ## Background
    Given a proposition: {proposition}
    Background: You want to create a pool of {panel_size} debate agents, who hold the opinions in favour of the given proposition 
    from different perspectives. Each agent should present a distinct viewpoint relevant to the proposition.

    ##Task: 
    Assign each agent a unique persona, described in one sentence, along with a corresponding claim that focuses on a specific perspective. 
    Ensure that each agent provides a different viewpoint relevant to the proposition. 
    To promote diversity and fairness, the agents should represent various communities and perspectives.
    
    Please format your persona descriptions as follows, with each line being a json object:
    {{"agent_id": 0, "description": the_description_of_Agent0, "claim": the_claim_of_Agent0}}
    """
    return prompt


def generate_agent_pool_con(proposition, panel_size):
    prompt = f"""
    ## Background
    Given a proposition: {proposition}
    Background: You want to create a pool of {panel_size} debate agents, who hold the opinions against the given proposition 
    from different perspectives. Each agent should present a distinct viewpoint relevant to the proposition.

    ##Task: 
    Assign each agent a unique persona, described in one sentence, along with a corresponding claim that focuses on a specific perspective. 
    Ensure that each agent provides a different viewpoint relevant to the proposition. 
    To promote diversity and fairness, the agents should represent various communities and perspectives.
    
    Please format your persona descriptions as follows, with each line being a json object:
    {{"agent_id": 0, "description": the_description_of_Agent0, "claim": the_claim_of_Agent0}}
    """
    return prompt