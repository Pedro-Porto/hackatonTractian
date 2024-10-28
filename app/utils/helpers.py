# app/utils/helpers.py

from openai import OpenAI
from pydantic import BaseModel
import pandas as pd
from typing import List
import json

from app.models import EquipmentData


from dataclasses import asdict, is_dataclass

def dataclass_to_dict(obj):
    if is_dataclass(obj):
        return {k: dataclass_to_dict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    else:
        return obj



def listIssuesAndMachines(orderText: str) -> EquipmentData:
    # Chama a LLM para obter nomes de máquinas, IDs e problemas (sem códigos de ferramentas)
    # Implementação de exemplo

    # print(orderText)

    client = OpenAI()

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
            {"role": "user", "content": orderText}
        ],
        response_format=MachineList,
    )

    # print(completion.choices[0].message.parsed)


    full_object = EquipmentData(
    tools= [],
    machines = completion.choices[0].message.parsed
    )

    print(full_object)

    # print(completion.choices[0].message)
    # parsed_result = completion.choices[0].message
    # tools = []

    #return equipment_data
    return full_object

def listTools(equipmentData: EquipmentData) -> EquipmentData:
    from app.database import tools_collection

    # Obter a lista de ferramentas da coleção 'tools'
    tools_list = list(tools_collection.find({}))

    # print('.......', tools_list)
    
    equipmentData.tools = [
        {
            "toolName": tool.get("toolName"),
            "sapCode": tool.get("sapCode"),
            "schedule": tool.get("schedule", [])
        }
        for tool in tools_list
    ]
    return equipmentData

####################3
def get_tool_codes(tool_input: list[Tool],machine_input , issue_input: str):
    # This would be a database call in a real application
    
    print(machine_input.machineName)
    print(issue_input)
    print(str(tool_input))

    client = OpenAI()
    completion_issue = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "given a problem given in the first line from a machine " + machine_input.machineName + ", look at the table given in the second line onwards to find out which tools should be used, this in accordance with what is established in the regulatory standards NR-12 of the Brazilian territory and including all the tools and safety equipment necessary for the correct execution of the work. Write only the code of the tool"},
        {"role": "user", "content": issue_input +'\n'+ str(tool_input)}
    ],
    response_format=ToolList,)

    # print('\n')
    # print(completion_issue.choices[0].message.parsed)

    return completion_issue.choices[0].message.parsed

########################3

def findTools(equipmentData: EquipmentData) -> EquipmentData:
    # LLM adiciona as ferramentas necessárias para cada problema (apenas o sapCode)
    # Implementação de exemplo
    
    for machine in equipmentData.machines:
        print(type(machine) ) #tuple

        print("\n")
        print(type(machine[0]) ) #string 
        print(type(machine[1]) ) #list
        print(machine[1])  #list

        for machines_ in machine[1]:
            print(machines_)
            for machines_2 in machines_:
                print(machines_2)

                if machines_2[0] == 'machineName':
                    name = machines_2[1]
            
                if machines_2[0] == 'issues':
                    print('\nbanana\n')
                    for issue in machines_2[1]:
                        print('banana')

                        # print(issue)
                        # print(issue.number)
                        # print(issue.issue)
                        # print(issue.toolCode)
                        # print(name)
                        tools_list = get_tool_codes(equipmentData.tools, machines_ ,issue.issue)
                        issue.toolsCode = tools_list
        # print("\n")
        # print(machine)
        # print("\n")


    print(equipmentData)

    return equipmentData
def addUserOrder(equipmentData):
    from app.database import orders_collection

    equipmentData.tools = []

    # Convert equipmentData to a dictionary using Pydantic's dict() method
    equipment_data_dict = equipmentData.dict()

    filter_query = {"username": "jose"}

    # First, update 'done' field to True for all relevant orders
    update_result1 = orders_collection.update_one(
        filter_query,
        {
            "$set": {"orders.$[elem].done": True}
        },
        array_filters=[{"elem.done": {"$exists": True}}]
    )

    # Then, push the new equipmentData into the 'orders' array
    update_result2 = orders_collection.update_one(
        filter_query,
        {
            "$push": {"orders": {"order": equipment_data_dict, "done": False}}
        }
    )

    if update_result1.modified_count > 0 or update_result2.modified_count > 0:
        print("Document updated successfully.")
    else:
        print("No matching document found or no update made.")

def fillServiceOrder(orderText: str) -> EquipmentData:
    equipment_data = listIssuesAndMachines(orderText)
    equipment_data = listTools(equipment_data)
    equipment_data = findTools(equipment_data)
    # print(equipment_data)
    addUserOrder(equipment_data)

    return equipment_data
