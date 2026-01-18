const API_URL = "http://localhost:8000";

export const chatWithBot = async (message, threadId = "default") => {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message, thread_id: threadId }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error("API Error:", error);
        return "Sorry, I am having trouble connecting to the server.";
    }
};
