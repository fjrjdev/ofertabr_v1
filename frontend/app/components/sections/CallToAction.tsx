import { SubscriptionForm } from "@/app/components/subscription/SubscriptionForm";
import { SOCIAL_PROOF_EMOJIS } from "@/app/lib/constants";

function SocialProof() {
    return (
        <div className="mt-12 text-center">
            <div className="flex items-center justify-center gap-2 text-gray-600 mb-4">
                <div className="flex -space-x-2">
                    {SOCIAL_PROOF_EMOJIS.map((emoji, index) => (
                        <div
                            key={index}
                            className="w-10 h-10 rounded-full bg-gradient-to-br from-[#667eea] to-[#764ba2] border-2 border-white flex items-center justify-center text-white text-sm font-bold"
                        >
                            {emoji}
                        </div>
                    ))}
                </div>
                <span className="font-semibold">+1.000 pessoas</span>
            </div>
            <p className="text-gray-600">
                já economizando com nossas ofertas diárias
            </p>
        </div>
    );
}

export function CallToAction() {
    return (
        <section className="py-20 px-4 bg-white">
            <div className="max-w-4xl mx-auto">
                <div className="bg-gradient-to-br from-[#667eea] to-[#764ba2] rounded-3xl shadow-2xl overflow-hidden">
                    <div className="p-8 md:p-12">
                        <div className="text-center mb-8">
                            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                                🎉 Comece a economizar hoje!
                            </h2>
                            <p className="text-white/90 text-lg">
                                Inscreva-se gratuitamente e receba as melhores ofertas no seu
                                e-mail
                            </p>
                        </div>

                        <SubscriptionForm
                            variant="cta"
                            buttonText="Quero receber ofertas gratuitas! 🚀"
                            disclaimer="✓ Sem compromisso • ✓ Cancele quando quiser • ✓ 100% gratuito"
                        />
                    </div>
                </div>

                <SocialProof />
            </div>
        </section>
    );
}

