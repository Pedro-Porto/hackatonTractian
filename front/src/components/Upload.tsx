import { useState } from 'react';

interface UploadProps {
    onUploadComplete: (data: any) => void;
}

const Upload: React.FC<UploadProps> = ({ onUploadComplete }) => {
    const [text, setText] = useState<string>("");
    const [isLoading, setIsLoading] = useState(false);

    const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setText(event.target.value);
    };

    const handleUpload = async () => {
        if (!text.trim()) {
            alert("Por favor, insira um texto antes de enviar.");
            return;
        }

        setIsLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:8000/serviceOrder/text", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Authorization: `Bearer ${localStorage.getItem('token')}` // substitua por sua lógica de autenticação
                },
                body: JSON.stringify({ orderText: text }),
            });

            if (!response.ok) {
                throw new Error("Erro ao enviar o texto");
            }

            const data = await response.json();
            onUploadComplete(data); // Passa o resultado do upload para o componente pai
            alert("Texto enviado com sucesso!");
        } catch (error) {
            console.error("Erro:", error);
            alert("Erro ao enviar o texto.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col items-start space-y-2 ml-5">
            <h2 className="text-2xl font-semibold">Upload de Texto</h2>
            <p className="text-gray-500">Identificação dos ativos, ferramentas e fontes</p>
            <div className="w-full">
                <label className="w-full flex flex-col items-start">
                    <input
                        type="text"
                        value={text}
                        onChange={handleTextChange}
                        placeholder="Digite seu texto aqui"
                        className="w-full h-12 px-4 bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#36B6C0]"
                    />
                </label>
            </div>
            <button
                onClick={handleUpload}
                className="bg-[#36B6C0] text-white px-4 py-2 rounded-md flex items-center justify-center"
                disabled={isLoading}
            >
                {isLoading ? (
                    <svg className="animate-spin h-5 w-5 text-white mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                    </svg>
                ) : (
                    "Enviar"
                )}
            </button>
        </div>
    );
};

export default Upload;
