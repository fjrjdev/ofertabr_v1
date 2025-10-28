import type { SubscriptionFormData, SubscriptionResponse } from "@/app/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export class ApiError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "ApiError";
    }
}

export async function subscribeUser(
    data: SubscriptionFormData
): Promise<SubscriptionResponse> {
    const response = await fetch(`${API_URL}/api/v1/subscribers/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new ApiError(errorData.detail || "Erro ao se inscrever");
    }

    return response.json();
}

