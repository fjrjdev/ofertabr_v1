import { Footer } from "@/app/components";
import Link from "next/link";

export const metadata = {
    title: "Sobre - OfertaBR",
    description: "Conheça a história e missão do OfertaBR",
};

function StorySection() {
    return (
        <section className="py-20 px-4 bg-white">
            <div className="max-w-4xl mx-auto">
                <h2 className="text-4xl font-bold text-gray-900 mb-8 text-center">
                    Nossa História
                </h2>
                <div className="prose prose-lg max-w-none text-gray-600">
                    <p className="mb-6">
                        O <strong>OfertaBR</strong> nasceu da necessidade de conectar
                        brasileiros às melhores ofertas da internet de forma simples e
                        eficiente.
                    </p>
                    <p className="mb-6">
                        Fundado em 2024, começamos com uma missão clara: ajudar pessoas a
                        economizarem tempo e dinheiro ao encontrar as melhores promoções dos
                        maiores marketplaces do Brasil.
                    </p>
                    <p>
                        Hoje, atendemos milhares de assinantes diariamente, curando
                        manualmente as melhores ofertas para garantir qualidade e economia
                        real.
                    </p>
                </div>
            </div>
        </section>
    );
}

function MissionSection() {
    return (
        <section className="py-20 px-4 bg-gray-50">
            <div className="max-w-6xl mx-auto">
                <div className="grid md:grid-cols-3 gap-8">
                    <div className="text-center">
                        <div className="text-5xl mb-4">🎯</div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3">Missão</h3>
                        <p className="text-gray-600">
                            Democratizar o acesso às melhores ofertas da internet brasileira,
                            economizando tempo e dinheiro dos nossos usuários.
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="text-5xl mb-4">👁️</div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3">Visão</h3>
                        <p className="text-gray-600">
                            Ser a plataforma número 1 de curadoria de ofertas no Brasil,
                            reconhecida pela qualidade e confiabilidade.
                        </p>
                    </div>
                    <div className="text-center">
                        <div className="text-5xl mb-4">💎</div>
                        <h3 className="text-xl font-bold text-gray-900 mb-3">Valores</h3>
                        <p className="text-gray-600">
                            Transparência, qualidade, comprometimento com o cliente e paixão
                            por economizar.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}

function CTASection() {
    return (
        <section className="py-20 px-4 bg-gradient-to-br from-[#667eea] to-[#764ba2]">
            <div className="max-w-4xl mx-auto text-center text-white">
                <h2 className="text-4xl font-bold mb-6">
                    Pronto para começar a economizar?
                </h2>
                <p className="text-xl mb-8 text-white/90">
                    Junte-se a milhares de pessoas que já economizam com nossas ofertas
                    diárias.
                </p>
                <Link
                    href="/#inscrever"
                    className="inline-block bg-white text-[#667eea] font-bold py-4 px-8 rounded-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
                >
                    Inscrever-se Gratuitamente 🚀
                </Link>
            </div>
        </section>
    );
}

export default function SobrePage() {
    return (
        <main className="min-h-screen">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#667eea] text-white py-20 px-4">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">
                        Sobre o OfertaBR
                    </h1>
                    <p className="text-xl md:text-2xl text-white/90">
                        Conectando brasileiros às melhores ofertas da internet desde 2024
                    </p>
                </div>
            </section>

            <StorySection />
            <MissionSection />
            <CTASection />
            <Footer />
        </main>
    );
}

