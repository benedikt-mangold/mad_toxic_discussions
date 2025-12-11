import json


def parse_opening_statement(response, agent_dict):
    global response_content
    response_content = response.json()["choices"][0]["message"]["content"]
    if "```" in response_content:
        argument = json.loads(
            response_content.split('```')[-2].replace("json", "")
        )
        argument["opening_statement"] = argument["next_answer"]
        del argument["next_answer"]
    else:
        argument = {
            "opening_statement": response_content.split('"next_answer": "')[1].split('"}')[0]
        }
    
    argument["agent"] = f'{agent_dict["procon"]}_{agent_dict["agent_id"]}'
    return argument


def parse_next_argument(response, agent_dict):
    global response_content
    response_content = response.json()["choices"][0]["message"]["content"]
    if "```" in response_content:
        argument = json.loads(
            response_content.split('```')[-2].replace("json", "")
        )
    else:
        argument = {
            "next_answer": response_content.split('"next_answer": "')[1].split('"}')[0]
        }
    argument["agent"] = f'{agent_dict["procon"]}_{agent_dict["agent_id"]}'
    return argument

def parse_next_moderation(response):
    global response_content
    response_content = response.json()["choices"][0]["message"]["content"]
    if "```" in response_content:
        judgement = json.loads(
            response_content.split('```')[-2].replace("json", "")
        )
    else:
        judgement = json.loads(
            "{" + response_content.split('{')[-1]
        )
  
    return judgement

def parse_agreement_level(response):
    global response_content
    response_content = response.json()["choices"][0]["message"]["content"]
    if "```" in response_content:
        judgement = json.loads(
            response_content.split('```')[-2].replace("json", "")
        )
    else:
        judgement = json.loads(
            "{" + response_content.split('{')[-1]
        )
      
    return judgement