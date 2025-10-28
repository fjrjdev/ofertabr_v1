import { CheckIcon } from "@/app/components/icons/CheckIcon";

interface SuccessMessageProps {
    onReset: () => void;
    variant?: "hero" | "cta";
    isReactivated?: boolean;
}

export function SuccessMessage({ onReset, variant = "hero", isReactivated = false }: SuccessMessageProps) {
    const containerClasses = {
        hero: "bg-white/10 backdrop-blur-xl shadow-2xl rounded-2xl p-8 text-center",
        cta: "bg-white rounded-2xl p-8 text-center",
    };

    const titleClasses = {
        hero: "text-2xl font-bold mb-2 text-white",
        cta: "text-2xl font-bold text-gray-800 mb-2",
    };

    const descriptionClasses = {
        hero: "text-white/90 mb-6",
        cta: "text-gray-600 mb-6",
    };

    const buttonClasses = {
        hero: "text-white hover:text-white/80 font-semibold transition-colors underline",
        cta: "text-[#667eea] hover:text-[#764ba2] font-semibold transition-colors",
    };

    // Different messages for reactivation vs new subscription
    const title = isReactivated
        ? "Bem-vindo de volta! 🎊"
        : "Bem-vindo ao OfertaBR! 🎉";

    const getDescription = () => {
        if (isReactivated) {
            return variant === "hero"
                ? "Sua inscrição foi reativada com sucesso! Você voltará a receber nossas ofertas."
                : "Que bom ter você de volta! Sua inscrição foi reativada e você voltará a receber ofertas incríveis!";
        }
        return variant === "hero"
            ? "Verifique seu e-mail para confirmar sua inscrição!"
            : "Verifique seu e-mail para confirmar sua inscrição e começar a receber ofertas incríveis!";
    };

    return (
        <div className={containerClasses[variant]}>
            <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <CheckIcon />
            </div>
            <h3 className={titleClasses[variant]}>{title}</h3>
            <p className={descriptionClasses[variant]}>
                {getDescription()}
            </p>
            <button onClick={onReset} className={buttonClasses[variant]}>
                Inscrever outro e-mail
            </button>
        </div>
    );
}

