import time
from random import choice
from src.generate_arguments import next_answer_from_agent, next_answer_from_agent_toxic
from src.connectors import parse_request_and_execute
from src.moderate import moderate_current_status_of_discussion, more_or_less_aligned_prompt
from src.parser import parse_opening_statement, parse_next_argument, parse_next_moderation, parse_agreement_level

def start_debate(proposition, topic_ix, topic_nr, pool_of_con_debate_agents, n_con_agents, 
                 pool_of_pro_debate_agents, n_pro_agents, persuadability=0.5):
    debate = {
        "nrounds": 0,
        "proposition": proposition,
        "topic_ix": topic_ix,
        "topic_nr": topic_nr,
        "pool_size_of_agents": n_con_agents + n_pro_agents,
    }

    ######## CON

    print(f"'Getting first argument (con) --- ")
    
    agent_con = choice(pool_of_con_debate_agents)
    agent_con["procon"] = "con"

    prompt_fist_argument_con = next_answer_from_agent(
        proposition, agent_con, nagents=debate["pool_size_of_agents"], 
        persuadability=persuadability, discussion_history=None)

    start_time = time.time()
    first_argument_response_con = parse_request_and_execute(
        prompt_fist_argument_con, 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time

    first_argument_con = parse_opening_statement(first_argument_response_con, agent_con)
    
    print(f"Got first argument (con) --- {total_time / 60:.2f} minutes ---")

    ######## PRO

    print(f"Getting first argument (pro) ---")

    
    agent_pro = choice(pool_of_pro_debate_agents)
    agent_pro["procon"] = "pro"

    prompt_fist_argument_pro = next_answer_from_agent(
        proposition, agent_pro, nagents=debate["pool_size_of_agents"], 
        persuadability=persuadability, discussion_history=None)

    start_time = time.time()
    first_argument_response_pro = parse_request_and_execute(
        prompt_fist_argument_pro, 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time
    
    first_argument_pro = parse_opening_statement(first_argument_response_pro, agent_pro)
    
    print(f"Got first argument (pro) --- {total_time / 60:.2f} minutes ---")

    
    if choice([0,1]) == 0:
        debate["opening_statements"] = (
                first_argument_pro, first_argument_con
            )
    else:
        debate["opening_statements"] = (
            first_argument_con, first_argument_pro
        )

    debate["discussion_history"] = {
        "opening_statements": debate["opening_statements"]
    }
    
    debate["active_agents"] = {
        "pro": [agent_pro],
        "con": [agent_con]
    }
    
    # Moderation

    print(f"Starting Moderation ---")
    
    prompt_fist_decision = moderate_current_status_of_discussion(
        proposition=debate["proposition"], 
        discussion_history=debate["discussion_history"], 
        nagents=len(debate["active_agents"]), 
        nround=debate["nrounds"] + 1 
    )

    start_time = time.time()
    first_decision = parse_request_and_execute(
        prompt_fist_decision, 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time
    
    print(f"Moderated --- {total_time / 60:.2f} minutes ---")

    first_moderation = parse_next_moderation(first_decision)

    if "state_of_discussion" in first_moderation.keys():
        assert first_moderation["state_of_discussion"] == 'agents are in disagreement'
    else:
        assert first_moderation["state of discussion"] == 'agents are in disagreement'
    

    debate["in_alignment"] = False
    del first_moderation["round"]
    
    debate["moderators_history"] = {
        "opening_statements": first_moderation
    }

    debate["agreement_level"] = {
        "Start": None
    }
    
    return debate


def next_debate_round(debate, persuadability=0.5):
    debate["nrounds"] = debate["nrounds"]+1
    print("Continuing discussion, round ", debate["nrounds"])
    
    debate["discussion_history"][f"Round_{debate['nrounds']}"] = []
    
    if choice([0,1]) == 0:
        prompt_next_argument_con = next_answer_from_agent(
            proposition=debate["proposition"],
            agent_dict=debate["active_agents"]["con"][0], 
            nagents=len(debate["active_agents"]), 
            persuadability=persuadability,
            discussion_history=debate["discussion_history"]
        )
        start_time = time.time()
        next_argument_con = parse_request_and_execute(
            prompt_next_argument_con, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (con) --- {total_time / 60:.2f} minutes ---")

        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_con, debate["active_agents"]["con"][0])
        )

        prompt_next_argument_pro = next_answer_from_agent(
            proposition=debate["proposition"],
            agent_dict=debate["active_agents"]["pro"][0], 
            nagents=len(debate["active_agents"]), 
            persuadability=persuadability,
            discussion_history=debate["discussion_history"]
        )

        start_time = time.time()
        next_argument_pro = parse_request_and_execute(
            prompt_next_argument_pro, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (pro) --- {total_time / 60:.2f} minutes ---")

        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_pro, debate["active_agents"]["pro"][0])
        )
 
    else:
        prompt_next_argument_pro = next_answer_from_agent(
            proposition=debate["proposition"],
            agent_dict=debate["active_agents"]["pro"][0], 
            nagents=len(debate["active_agents"]), 
            persuadability=persuadability,
            discussion_history=debate["discussion_history"]
        )

        start_time = time.time()
        next_argument_pro = parse_request_and_execute(
            prompt_next_argument_pro, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (pro) --- {total_time / 60:.2f} minutes ---")
        
        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_pro, debate["active_agents"]["pro"][0])
        )


        prompt_next_argument_con = next_answer_from_agent(
            proposition=debate["proposition"],
            agent_dict=debate["active_agents"]["con"][0], 
            nagents=len(debate["active_agents"]), 
            persuadability=persuadability,
            discussion_history=debate["discussion_history"]
        )
        start_time = time.time()
        next_argument_con = parse_request_and_execute(
            prompt_next_argument_con, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (con) --- {total_time / 60:.2f} minutes ---")
        
        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_con, debate["active_agents"]["con"][0])
        )

    if (
        (debate["discussion_history"][f"Round_{debate['nrounds']}"][0]['next_answer'] == "convinced") or
        (debate["discussion_history"][f"Round_{debate['nrounds']}"][1]['next_answer'] == "convinced")
    ):
        debate["in_alignment"] = True
        return debate
    
    prompt_decision = moderate_current_status_of_discussion(
        proposition=debate["proposition"], 
        discussion_history=debate["discussion_history"], 
        nagents=len(debate["active_agents"]), 
        nround=debate["nrounds"] + 1 
    )

    start_time = time.time()
    decision = parse_request_and_execute(
        prompt_decision, 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time
    print(f"Moderated --- {total_time / 60:.2f} minutes ---")

    moderation = parse_next_moderation(decision)

    debate["moderators_history"][f"after_round_{debate['nrounds']}"] = moderation

    if "state_of_discussion" in moderation.keys():
        if moderation["state_of_discussion"] == 'agents are in agreement':
            debate["in_alignment"] = True
    else:
        if moderation["state of discussion"] == 'agents are in agreement':
            debate["in_alignment"] = True
            
    start_time = time.time()
    agreement = parse_request_and_execute(
        more_or_less_aligned_prompt(debate), 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time
    print(f"Agreement measured --- {total_time / 60:.2f} minutes ---")

    agreement_level = parse_agreement_level(agreement)

    debate["agreement_level"][f'after_round_{debate['nrounds']}'] = agreement_level

    return debate


def next_debate_round_toxic(debate, pro_or_con_toxic, toxicity_level=None, persuadability=0.5):
    """pro_or_con_toxic -> con or pro string"""
    debate["nrounds"] = debate["nrounds"]+1
    print("Continuing discussion, round ", debate["nrounds"])
    debate["discussion_history"][f"Round_{debate['nrounds']}"] = []
    
    # if con 
    if choice([0,1]) == 0:
        if pro_or_con_toxic == "con":
            prompt_next_argument_con = next_answer_from_agent_toxic(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["con"][0], 
                nagents=len(debate["active_agents"]), 
                toxicity_level=toxicity_level,
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )
        else:
            prompt_next_argument_con = next_answer_from_agent(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["con"][0], 
                nagents=len(debate["active_agents"]), 
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )
        start_time = time.time()
        next_argument_con = parse_request_and_execute(
            prompt_next_argument_con, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (con) --- {total_time / 60:.2f} minutes ---")

        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_con, debate["active_agents"]["con"][0])
        )

        if pro_or_con_toxic == "pro":
            prompt_next_argument_pro = next_answer_from_agent_toxic(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["pro"][0], 
                nagents=len(debate["active_agents"]), 
                toxicity_level=toxicity_level,
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )
        else:
            prompt_next_argument_pro = next_answer_from_agent(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["pro"][0], 
                nagents=len(debate["active_agents"]), 
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )

        start_time = time.time()
        next_argument_pro = parse_request_and_execute(
            prompt_next_argument_pro, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (pro) --- {total_time / 60:.2f} minutes ---")
        
        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_pro, debate["active_agents"]["pro"][0])
        )
    else:
        if pro_or_con_toxic == "pro":
            prompt_next_argument_pro = next_answer_from_agent_toxic(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["pro"][0], 
                nagents=len(debate["active_agents"]), 
                toxicity_level=toxicity_level,
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )
        else:
            prompt_next_argument_pro = next_answer_from_agent(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["pro"][0], 
                nagents=len(debate["active_agents"]), 
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )

        start_time = time.time()
        next_argument_pro = parse_request_and_execute(
            prompt_next_argument_pro, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (pro) --- {total_time / 60:.2f} minutes ---")
        
        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_pro, debate["active_agents"]["pro"][0])
        )

        if pro_or_con_toxic == "con":
            prompt_next_argument_con = next_answer_from_agent_toxic(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["con"][0], 
                nagents=len(debate["active_agents"]), 
                toxicity_level=toxicity_level,
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )
        else:
            prompt_next_argument_con = next_answer_from_agent(
                proposition=debate["proposition"],
                agent_dict=debate["active_agents"]["con"][0], 
                nagents=len(debate["active_agents"]), 
                persuadability=persuadability,
                discussion_history=debate["discussion_history"]
            )
        start_time = time.time()
        next_argument_con = parse_request_and_execute(
            prompt_next_argument_con, 
            url, 
            headers, 
            options_dict, 
            max_retries=5,
            delay=60
        )
        total_time = time.time() - start_time
        print(f"Got argument (con) --- {total_time / 60:.2f} minutes ---")
        
        debate["discussion_history"][f"Round_{debate['nrounds']}"].append(
            parse_next_argument(next_argument_con, debate["active_agents"]["con"][0])
        )

    if (
        (debate["discussion_history"][f"Round_{debate['nrounds']}"][0]['next_answer'] == "convinced") or
        (debate["discussion_history"][f"Round_{debate['nrounds']}"][1]['next_answer'] == "convinced")
    ):
        debate["in_alignment"] = True
        return debate
    
    prompt_decision = moderate_current_status_of_discussion(
        proposition=debate["proposition"], 
        discussion_history=debate["discussion_history"], 
        nagents=len(debate["active_agents"]), 
        nround=debate["nrounds"] + 1 
    )
    
    start_time = time.time()
    decision = parse_request_and_execute(
        prompt_decision, 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time
    print(f"Moderated --- {total_time / 60:.2f} minutes ---")

    moderation = parse_next_moderation(decision)

    debate["moderators_history"][f"after_round_{debate['nrounds']}"] = moderation

    if "state_of_discussion" in moderation.keys():
        if moderation["state_of_discussion"] == 'agents are in agreement':
            debate["in_alignment"] = True
    else:
        if moderation["state of discussion"] == 'agents are in agreement':
            debate["in_alignment"] = True
    
    start_time = time.time()
    agreement = parse_request_and_execute(
        more_or_less_aligned_prompt(debate), 
        url, 
        headers, 
        options_dict, 
        max_retries=5,
        delay=60
    )
    total_time = time.time() - start_time
    print(f"Agreement measured --- {total_time / 60:.2f} minutes ---")

    agreement_level = parse_agreement_level(agreement)

    debate["agreement_level"][f'after_round_{debate['nrounds']}'] = agreement_level

    return debate