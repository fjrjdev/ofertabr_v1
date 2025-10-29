import { Footer } from "@/app/components";
import Link from "next/link";

export const metadata = {
    title: "Planos - OfertaBR",
    description: "Escolha o melhor plano para você",
};

interface PlanFeature {
    text: string;
    included: boolean;
}

interface PlanCardProps {
    name: string;
    price: string;
    period: string;
    description: string;
    features: PlanFeature[];
    highlighted?: boolean;
    ctaText: string;
}

function PlanCard({
    name,
    price,
    period,
    description,
    features,
    highlighted = false,
    ctaText,
}: PlanCardProps) {
    return (
        <div
            className={`rounded-2xl p-8 ${highlighted
                ? "bg-gradient-to-br from-[#667eea] to-[#764ba2] text-white shadow-2xl transform scale-105"
                : "bg-white shadow-lg"
                }`}
        >
            {highlighted && (
                <div className="text-center mb-4">
                    <span className="bg-white/20 backdrop-blur-sm px-4 py-1 rounded-full text-sm font-bold">
                        ⭐ MAIS POPULAR
                    </span>
                </div>
            )}

            <h3
                className={`text-2xl font-bold mb-2 ${highlighted ? "text-white" : "text-gray-900"
                    }`}
            >
                {name}
            </h3>
            <p
                className={`mb-6 ${highlighted ? "text-white/90" : "text-gray-600"
                    }`}
            >
                {description}
            </p>

            <div className="mb-6">
                <span
                    className={`text-5xl font-bold ${highlighted ? "text-white" : "text-gray-900"
                        }`}
                >
                    {price}
                </span>
                <span
                    className={`text-xl ${highlighted ? "text-white/80" : "text-gray-600"
                        }`}
                >
                    {period}
                </span>
            </div>

            <ul className="space-y-3 mb-8">
                {features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                        <span className="mr-2">
                            {feature.included ? (
                                <span className={highlighted ? "text-white" : "text-green-500"}>
                                    ✓
                                </span>
                            ) : (
                                <span className="text-gray-400">✗</span>
                            )}
                        </span>
                        <span
                            className={
                                feature.included
                                    ? highlighted
                                        ? "text-white"
                                        : "text-gray-700"
                                    : "text-gray-400 line-through"
                            }
                        >
                            {feature.text}
                        </span>
                    </li>
                ))}
            </ul>

            <Link
                href="/#inscrever"
                className={`block w-full text-center font-bold py-4 px-6 rounded-xl transition-all duration-200 ${highlighted
                    ? "bg-white text-[#667eea] hover:shadow-xl transform hover:scale-105"
                    : "bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white hover:shadow-xl"
                    }`}
            >
                {ctaText}
            </Link>
        </div>
    );
}

export default function PlanosPage() {
    const plans: PlanCardProps[] = [
        {
            name: "Grátis",
            price: "R$ 0",
            period: "/mês",
            description: "Perfeito para começar a economizar",
            features: [
                { text: "Ofertas diárias por email", included: true },
                { text: "Descontos de até 70% OFF", included: true },
                { text: "Curadoria básica", included: true },
                { text: "Suporte por email", included: true },
                { text: "Alertas personalizados", included: false },
                { text: "Ofertas exclusivas", included: false },
                { text: "Suporte prioritário", included: false },
            ],
            ctaText: "Começar Grátis",
        },
        {
            name: "Premium",
            price: "R$ 9,90",
            period: "/mês",
            description: "Para quem quer economizar ainda mais",
            features: [
                { text: "Tudo do plano Grátis", included: true },
                { text: "Alertas personalizados por categoria", included: true },
                { text: "Ofertas exclusivas Premium", included: true },
                { text: "Acesso antecipado às promoções", included: true },
                { text: "Até 3 alertas personalizados", included: true },
                { text: "Suporte prioritário", included: true },
                { text: "Sem anúncios", included: true },
            ],
            highlighted: true,
            ctaText: "Assinar Premium",
        },
        {
            name: "Empresarial",
            price: "Sob consulta",
            period: "",
            description: "Para empresas e revendedores",
            features: [
                { text: "Tudo do plano Premium", included: true },
                { text: "API de acesso às ofertas", included: true },
                { text: "Múltiplos usuários", included: true },
                { text: "Dashboards personalizados", included: true },
                { text: "Suporte dedicado 24/7", included: true },
                { text: "Relatórios e analytics", included: true },
                { text: "SLA garantido", included: true },
            ],
            ctaText: "Entre em Contato",
        },
    ];

    return (
        <main className="min-h-screen">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#667eea] text-white py-20 px-4">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">
                        Escolha seu Plano
                    </h1>
                    <p className="text-xl md:text-2xl text-white/90">
                        Comece grátis e faça upgrade quando quiser
                    </p>
                </div>
            </section>

            {/* Plans Section */}
            <section className="py-20 px-4 bg-gray-50">
                <div className="max-w-7xl mx-auto">
                    <div className="grid md:grid-cols-3 gap-8 items-start">
                        {plans.map((plan, index) => (
                            <PlanCard key={index} {...plan} />
                        ))}
                    </div>

                    {/* FAQ */}
                    <div className="mt-20 max-w-3xl mx-auto">
                        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
                            Perguntas Frequentes
                        </h2>
                        <div className="space-y-6">
                            <div className="bg-white p-6 rounded-xl shadow">
                                <h3 className="font-bold text-gray-900 mb-2">
                                    Posso cancelar a qualquer momento?
                                </h3>
                                <p className="text-gray-600">
                                    Sim! Você pode cancelar sua assinatura a qualquer momento, sem
                                    multas ou taxas adicionais.
                                </p>
                            </div>
                            <div className="bg-white p-6 rounded-xl shadow">
                                <h3 className="font-bold text-gray-900 mb-2">
                                    Como funciona o período de teste?
                                </h3>
                                <p className="text-gray-600">
                                    O plano Grátis é permanente! Você pode testar e depois fazer
                                    upgrade para Premium quando quiser.
                                </p>
                            </div>
                            <div className="bg-white p-6 rounded-xl shadow">
                                <h3 className="font-bold text-gray-900 mb-2">
                                    Quais são as formas de pagamento?
                                </h3>
                                <p className="text-gray-600">
                                    Aceitamos cartão de crédito, PIX e boleto bancário para o plano
                                    Premium.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <Footer />
        </main>
    );
}

