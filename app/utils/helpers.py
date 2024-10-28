# app/utils/helpers.py

from app.models import EquipmentData
# Importar outras dependências necessárias

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
    # Importar a coleção tools_collection
    from app.database import tools_collection

    # Obter a lista de ferramentas da coleção 'tools'
    tools_list = list(tools_collection.find({}))

    print('.......', tools_list)
    
    # Mapear os dados para o formato esperado em equipmentData.tools
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
            issue.toolsCode = ["SAP123", "SAP456"]
    return equipmentData

def fillServiceOrder(orderText: str) -> EquipmentData:
    equipment_data = listIssuesAndMachines(orderText)
    equipment_data = listTools(equipment_data)
    equipment_data = findTools(equipment_data)
    return equipment_data
