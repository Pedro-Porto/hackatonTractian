# app/utils/helpers.py

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
    equipment_data = EquipmentData(
        tools=[],
        machines=[
            {
                "machineName": "Machine A",
                "machineId": 123,
                "issues": [
                    {"number": 1, "issue": "Issue description", "toolsCode": []}
                ]
            }
        ]
    )
    return equipment_data

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

def findTools(equipmentData: EquipmentData) -> EquipmentData:
    # LLM adiciona as ferramentas necessárias para cada problema (apenas o sapCode)
    # Implementação de exemplo
    for machine in equipmentData.machines:
        for issue in machine.issues:
            issue.toolsCode = ["MAT001", "SAP456"]
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
