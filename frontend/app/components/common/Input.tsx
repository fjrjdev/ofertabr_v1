interface InputProps {
    type: "text" | "email";
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
    required?: boolean;
    disabled?: boolean;
    variant?: "hero" | "cta";
}

export function Input({
    type,
    value,
    onChange,
    placeholder,
    required = false,
    disabled = false,
    variant = "hero",
}: InputProps) {
    const baseClasses =
        "w-full px-6 py-4 rounded-xl text-white placeholder:text-white/60 focus:ring-4 outline-none transition-all disabled:opacity-50";

    const variantClasses = {
        hero: "bg-white/20 backdrop-blur-sm focus:bg-white/30 focus:ring-white/20",
        cta: "border-2 border-white/20 bg-white/10 backdrop-blur-sm focus:border-white focus:ring-white/20",
    };

    return (
        <input
            type={type}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            required={required}
            disabled={disabled}
            placeholder={placeholder}
            className={`${baseClasses} ${variantClasses[variant]}`}
        />
    );
}

