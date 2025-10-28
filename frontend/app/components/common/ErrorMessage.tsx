interface ErrorMessageProps {
    message: string;
    variant?: "hero" | "cta";
}

export function ErrorMessage({ message, variant = "hero" }: ErrorMessageProps) {
    const variantClasses = {
        hero: "bg-red-500/20 backdrop-blur-sm text-white",
        cta: "bg-red-500/20 border-2 border-red-300 text-white backdrop-blur-sm",
    };

    return (
        <div
            className={`${variantClasses[variant]} px-4 py-3 rounded-xl text-sm`}
        >
            <span className="font-semibold">❌ Erro:</span> {message}
        </div>
    );
}

