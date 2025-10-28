import { Input } from "@/app/components/common/Input";
import { Button } from "@/app/components/common/Button";
import { ErrorMessage } from "@/app/components/common/ErrorMessage";
import { SuccessMessage } from "@/app/components/subscription/SuccessMessage";
import { useSubscription } from "@/app/hooks/useSubscription";

interface SubscriptionFormProps {
    variant?: "hero" | "cta";
    title?: string;
    buttonText?: string;
    disclaimer?: string;
}

export function SubscriptionForm({
    variant = "hero",
    title = "Inscreva-se gratuitamente",
    buttonText = "Quero receber ofertas! 🚀",
    disclaimer = "✓ Sem compromisso • ✓ Cancele quando quiser",
}: SubscriptionFormProps) {
    const {
        email,
        name,
        status,
        errorMessage,
        isReactivated,
        setEmail,
        setName,
        handleSubmit,
        resetForm,
    } = useSubscription();

    if (status === "success") {
        return <SuccessMessage onReset={resetForm} variant={variant} isReactivated={isReactivated} />;
    }

    const containerClasses = {
        hero: "bg-white/10 backdrop-blur-xl shadow-2xl rounded-2xl p-8",
        cta: "",
    };

    const titleClasses = {
        hero: "text-2xl font-bold text-center mb-6 text-white",
        cta: "",
    };

    return (
        <div className={containerClasses[variant]}>
            {variant === "hero" && title && (
                <h3 className={titleClasses[variant]}>{title}</h3>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                    <Input
                        type="text"
                        value={name}
                        onChange={setName}
                        placeholder="Seu nome"
                        required
                        disabled={status === "loading"}
                        variant={variant}
                    />
                    <Input
                        type="email"
                        value={email}
                        onChange={setEmail}
                        placeholder="seu@email.com"
                        required
                        disabled={status === "loading"}
                        variant={variant}
                    />
                </div>

                {status === "error" && (
                    <ErrorMessage message={errorMessage} variant={variant} />
                )}

                <Button
                    type="submit"
                    disabled={status === "loading"}
                    loading={status === "loading"}
                    loadingText="Inscrevendo..."
                >
                    {buttonText}
                </Button>

                <p className="text-white/70 text-sm text-center">{disclaimer}</p>
            </form>
        </div>
    );
}

