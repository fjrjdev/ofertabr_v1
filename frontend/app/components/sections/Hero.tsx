import { SubscriptionForm } from "@/app/components/subscription/SubscriptionForm";
import { ChevronDownIcon } from "@/app/components/icons/ChevronDownIcon";
import { HERO_BADGES } from "@/app/lib/constants";

interface BadgeProps {
    emoji: string;
    text: string;
}

function Badge({ emoji, text }: BadgeProps) {
    return (
        <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full">
            {emoji} {text}
        </span>
    );
}

function ScrollIndicator() {
    return (
        <div className="text-center mt-12">
            <p className="text-white/70 text-sm mb-2">Role para ver mais</p>
            <ChevronDownIcon />
        </div>
    );
}

export function Hero() {
    return (
        <section
            id="inscrever"
            className="min-h-screen bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#667eea] text-white flex items-center px-4 py-20"
        >
            <div className="max-w-6xl mx-auto w-full">
                <div className="text-center mb-12">
                    <h1 className="text-5xl md:text-7xl font-bold mb-6 drop-shadow-lg">
                        OfertaBR
                    </h1>
                    <p className="text-xl md:text-2xl mb-8 text-white/90 max-w-2xl mx-auto">
                        Receba as principais Ofertas dos Maiores Marketplaces do Brasil no
                        seu email 📫
                    </p>
                    <div className="flex items-center justify-center gap-4 text-lg flex-wrap">
                        {HERO_BADGES.map((badge, index) => (
                            <Badge key={index} emoji={badge.emoji} text={badge.text} />
                        ))}
                    </div>
                </div>

                <div className="max-w-2xl mx-auto">
                    <SubscriptionForm variant="hero" />
                </div>

                <ScrollIndicator />
            </div>
        </section>
    );
}

