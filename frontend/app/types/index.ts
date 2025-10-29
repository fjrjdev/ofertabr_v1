export type SubscriptionStatus = "idle" | "loading" | "success" | "error";

export interface SubscriptionFormData {
    email: string;
    name: string;
}

export interface SubscriptionResponse {
    message: string;
    email: string;
    reactivated?: boolean;
}

export interface Feature {
    emoji: string;
    title: string;
    description: string;
}

export interface UseSubscriptionReturn {
    email: string;
    name: string;
    status: SubscriptionStatus;
    errorMessage: string;
    isReactivated: boolean;
    setEmail: (email: string) => void;
    setName: (name: string) => void;
    handleSubmit: (e: React.FormEvent) => Promise<void>;
    resetForm: () => void;
}

