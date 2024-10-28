import { OrderStatus } from "../routes/Orders";

const OrderData = ({ selectedOrder }: { selectedOrder: OrderStatus | null }) => {
    return (
        <div className="flex flex-col ml-10">
            {selectedOrder && selectedOrder.order.machines.machine_list.map((machine) => (
                <div>
                    <span
                        className="text-4xl font-semibold"
                    >{machine.machineName}</span>
                    <div
                        className="h-[1px] w-[95%] bg-gray-300 my-5"
                    ></div>

                    <div
                        className="flex flex-col gap-5 text-2xl font-normal"
                    >
                        Problemas:
                    </div>
                    <div
                        className="flex flex-col gap-2 font-normal ml-6 my-4"
                    >
                        {machine.issues.map((issue) => (
                            <div>
                                <div
                                    className=" font-normal"
                                >{issue.issue}</div>
                                <div
                                    className="flex flex-col gap-5 text-xl font-normal ml-6"
                                >
                                    Ferramentas:
                                </div>

                                <div
                                className="w-full ml-8 flex flex-col gap-1"
                                >
                                    {selectedOrder.order.tools.map((tool) => (
                                        <div
                                            className="text-gray-500 py-1 bg-slate-100 px-3 rounded-md cursor-pointer hover:bg-slate-200"
                                            style={{ 
                                                backgroundColor: issue.toolsCode.list_of_tools.find((t) => t === tool.sapCode) ? "lightcoral" : "white"
                                            }}
                                        >{tool.toolName} [{tool.sapCode}]</div>
                                    ))}

                                </div>
                            </div>


                        ))}
                    </div>




                </div>
            ))}
        </div>
    );
};

export default OrderData;
