"use client"
import { useState } from "react";
import type { UseSubscriptionReturn, SubscriptionStatus } from "@/app/types";
import { subscribeUser, ApiError } from "@/app/lib/api";

export function useSubscription(): UseSubscriptionReturn {
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [status, setStatus] = useState<SubscriptionStatus>("idle");
    const [errorMessage, setErrorMessage] = useState("");
    const [isReactivated, setIsReactivated] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus("loading");
        setErrorMessage("");
        setIsReactivated(false);

        try {
            const response = await subscribeUser({ email, name });
            setStatus("success");
            setIsReactivated(response.reactivated || false);
            setEmail("");
            setName("");
        } catch (error) {
            setStatus("error");
            if (error instanceof ApiError) {
                setErrorMessage(error.message);
            } else {
                setErrorMessage("Erro ao se inscrever");
            }
        }
    };

    const resetForm = () => {
        setStatus("idle");
        setEmail("");
        setName("");
        setErrorMessage("");
        setIsReactivated(false);
    };

    return {
        email,
        name,
        status,
        errorMessage,
        isReactivated,
        setEmail,
        setName,
        handleSubmit,
        resetForm,
    };
}

