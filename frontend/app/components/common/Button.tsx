import { SpinnerIcon } from "@/app/components/icons/SpinnerIcon";

interface ButtonProps {
    type?: "button" | "submit" | "reset";
    disabled?: boolean;
    loading?: boolean;
    onClick?: () => void;
    children: React.ReactNode;
    className?: string;
    loadingText?: string;
}

export function Button({
    type = "button",
    disabled = false,
    loading = false,
    onClick,
    children,
    className = "",
    loadingText = "Carregando...",
}: ButtonProps) {
    const baseClasses =
        "w-full bg-gradient-to-r from-[#283593] to-[#1976d2] text-white font-bold py-4 px-8 rounded-xl hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-lg";

    return (
        <button
            type={type}
            disabled={disabled || loading}
            onClick={onClick}
            className={`${baseClasses} ${className}`}
        >
            {loading ? (
                <span className="flex items-center justify-center">
                    <SpinnerIcon />
                    {loadingText}
                </span>
            ) : (
                children
            )}
        </button>
    );
}

