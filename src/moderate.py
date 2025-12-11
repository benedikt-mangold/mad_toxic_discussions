def moderate_current_status_of_discussion(proposition, discussion_history, nagents, nround):
    prompt = f"""
    Given a proposition: {proposition}
    Background: You are moderating a discussion of {nagents} agents on the proposition. You need to decide neutrally if 
    the current state of discussion is either "in agreement" or "in disagreement", depending on whether or not all agents
    agreed on either PRO or CON the proposition. The current state of discussion needs to be determined by analysing the history
    of the discussion ({nround} rounds of arguments so far), putting focus on the latest rounds of arguments.
    
    ## Discussion history:
    {discussion_history}
    
    Please choose the state_of_discussion which is either "agents are in agreement" or "agents are in disagreement". Additionally, provide 
    a short reason for your choice. The output should be a json object as follows:
    {{"round': {nround}, "state of discussion": state_of_discussion, "reason": the_reason_of_selection}}
    """
    return prompt


def more_or_less_aligned_prompt(debate):
    valid_rounds = [f"Round_{i}" for i in range(1, debate["nrounds"]+1)]
    valid_round_content = {k:v for k, v in debate["discussion_history"].items() if k in valid_rounds}
    prompt = f"""
    Given a sequence of arguments or statements, analyze the latest entries. Determine whether they demonstrate a trend of increasing alignment (greater agreement, convergence, or consistency in tone or content) or decreasing alignment (growing disagreement, divergence, or inconsistency).

    ## Last 4 entries:
    {valid_round_content}
    
    For each of the last four statements:

    Summarize its main point in one sentence.

    Note how it aligns or diverges from the previous one.

    Finally, conclude whether the sequence overall shows an increasing or decreasing alignment, and briefly justify your answer.
    
    Please choose the state_of_agreement which is either "growing disagreement", "growing agreement", or "same level or agreement". Additionally, provide 
    a short reason for your choice. The output should be a json object as follows:
    {{"round': {debate["nrounds"]}, "state of agreement": state_of_agreement, "reason": the_reason_of_selection}}
    """
    return prompt
