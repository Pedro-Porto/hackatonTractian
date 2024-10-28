import NavBar from "../components/NavBar";
import file from '../assets/file.png';
import Updload from "../components/Upload";
import { useState, useEffect } from "react";
import OrderData from "../components/OrderData";


interface EquipmentData {
    date: string;
    tools: ToolData[];
    machines: MachineData[];
}

interface ToolData {
    toolName: string;
    sapCode: string;
    schedule: ScheduleData[];
}

interface ScheduleData {
    startTime: Date;
    endTime: Date;
    user: string;
}

interface MachineData {
    machineName: string;
    machineId: number;
    issues: IssueData[];
}

interface IssueData {
    number: number;
    issue: string;
    toolsCode: string[];
}

export interface OrderStatus {
    order: EquipmentData;
    done: boolean;
    id?: number;
}



const mockOrderStatus: OrderStatus[] = [
    {
        order: {
            date: "2024-10-28",
            tools: [
                {
                    toolName: "Furadeira",
                    sapCode: "SAP1234",
                    schedule: [
                        {
                            startTime: new Date("2024-10-28T08:00:00"),
                            endTime: new Date("2024-10-28T10:00:00"),
                            user: "Operador1"
                        },
                        {
                            startTime: new Date("2024-10-28T14:00:00"),
                            endTime: new Date("2024-10-28T16:00:00"),
                            user: "Operador2"
                        }
                    ]
                },
                {
                    toolName: "Chave de Torque",
                    sapCode: "SAP5678",
                    schedule: [
                        {
                            startTime: new Date("2024-10-28T09:00:00"),
                            endTime: new Date("2024-10-28T11:00:00"),
                            user: "Operador3"
                        }
                    ]
                }
            ],
            machines: [
                {
                    machineName: "Torno Mecânico",
                    machineId: 101,
                    issues: [
                        {
                            number: 1,
                            issue: "Vibração excessiva",
                            toolsCode: ["SAP1234"]
                        },
                        {
                            number: 2,
                            issue: "Falha na lubrificação",
                            toolsCode: ["SAP5678"]
                        }
                    ]
                },
                {
                    machineName: "Fresadora",
                    machineId: 202,
                    issues: [
                        {
                            number: 1,
                            issue: "Desgaste da fresa",
                            toolsCode: ["SAP1234", "SAP5678"]
                        }
                    ]
                }
            ]
        },
        done: false
    },
    {
        order: {
            date: "2024-10-29",
            tools: [
                {
                    toolName: "Soldadora",
                    sapCode: "SAP9876",
                    schedule: [
                        {
                            startTime: new Date("2024-10-29T08:00:00"),
                            endTime: new Date("2024-10-29T12:00:00"),
                            user: "Operador4"
                        }
                    ]
                }
            ],
            machines: [
                {
                    machineName: "Prensa Hidráulica",
                    machineId: 303,
                    issues: [
                        {
                            number: 1,
                            issue: "Pressão baixa",
                            toolsCode: ["SAP9876"]
                        }
                    ]
                }
            ]
        },
        done: true
    }
];

const Orders = () => {
    const [selectedOrder, setSelectedOrder] = useState<OrderStatus | null>(null);
    const [orders, setOrders] = useState<OrderStatus[]>(mockOrderStatus.map((el, index) => ({ ...el, id: index })));
    const [newOrder, setNewOrder] = useState<boolean>(false);

    async function fetchUserOrders(username: string) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/userOrders?username=${username}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });
    
            if (!response.ok) {
                throw new Error("Erro ao buscar ordens do usuário");
            }
    
            const orders = await response.json();
            setOrders(orders);
        } catch (error) {
            console.error("Erro:", error);
            setOrders([]);
        }
    }

    useEffect(() => {
        fetchUserOrders("jose")
        console.log(orders);
    }, []);

    return (
        <div
            className="h-screen w-screen flex flex-col"
        >
            <NavBar />
            <div className="w-full flex justify-between p-10">
                <span
                    className="text-3xl font-bold"
                >Ordens de serviço</span>
                <button
                    className="bg-[#36B6C0] text-white rounded-md px-10 py-2"
                    onClick={() => {
                        setNewOrder(true);
                        setSelectedOrder(null);
                    }}
                >+ Adicionar ordem de serviço</button>
            </div>
            <div
                className="w-full h-[2px] bg-[#E5E5E5] mx-3 -mt-5"
            ></div>

            <div
                className="w-full p-10 flex"
            >
                <div
                    className="w-1/5 flex flex-col gap-5"
                >
                    {orders.map((orderStatus) => (
                        <div
                            className="flex rounded-lg hover:bg-slate-200 p-5 cursor-pointer"
                            style={{ backgroundColor: selectedOrder?.id === orderStatus.id ? "#E5E5E5" : "white" }}
                            onClick={() => {
                                setSelectedOrder(orderStatus)
                                setNewOrder(false);
                            }}
                        >
                            <img src={file} alt="File" className="h-16" />

                            <div
                                className="flex flex-col gap-1 ml-5"
                            >
                                <div>Criado em {orderStatus.order.date}</div>
                                {
                                    orderStatus.done ?
                                        <div className="bg-[#36B6C0] rounded-lg px-4 py-1">Finalizado</div> :
                                        <div className="bg-[#FFB800] rounded-lg px-4 py-1">Em andamento</div>
                                }
                            </div>
                        </div>
                    ))}
                </div>
                <div
                    className="grow"
                >
                    {newOrder ? (<Updload
                        onUploadComplete={(data) => {
                            console.log(data);
                            setOrders([...orders.map((el) => ({ ...el, done: true })), {
                                order: data,
                                done: false,
                                id: orders.length
                            }]);
                            setSelectedOrder({
                                order: data,
                                done: false,
                                id: orders.length
                            });

                        }}
                    />) :
                    (
                        <OrderData
                            selectedOrder={selectedOrder}
                        />
                    )
                    }
                </div>
            </div>

        </div>
    )
}

export default Orders;