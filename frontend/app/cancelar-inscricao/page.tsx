"use client";

import { Footer } from "@/app/components";
import { useState } from "react";

export default function CancelarInscricaoPage() {
    const [email, setEmail] = useState("");
    const [status, setStatus] = useState<
        "idle" | "loading" | "success" | "error"
    >("idle");
    const [errorMessage, setErrorMessage] = useState("");

    const handleUnsubscribe = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus("loading");
        setErrorMessage("");

        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_API_URL}/api/v1/subscribers/unsubscribe`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email }),
                }
            );

            if (!response.ok) {
                const data = await response.json();
                throw new Error(
                    data.detail || "Erro ao cancelar inscrição. Verifique seu email."
                );
            }

            setStatus("success");
            setEmail("");
        } catch (error) {
            setStatus("error");
            setErrorMessage(
                error instanceof Error
                    ? error.message
                    : "Erro ao cancelar inscrição. Tente novamente."
            );
        }
    };

    return (
        <main className="min-h-screen">
            {/* Hero Section */}
            <section className="bg-gradient-to-br from-[#667eea] via-[#764ba2] to-[#667eea] text-white py-20 px-4">
                <div className="max-w-4xl mx-auto text-center">
                    <h1 className="text-5xl md:text-6xl font-bold mb-6">
                        Cancelar Inscrição
                    </h1>
                    <p className="text-xl md:text-2xl text-white/90">
                        Sentiremos sua falta! 😢
                    </p>
                </div>
            </section>

            {/* Unsubscribe Form */}
            <section className="py-20 px-4 bg-gray-50">
                <div className="max-w-2xl mx-auto">
                    {status === "success" ? (
                        <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
                            <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                                <svg
                                    className="w-10 h-10 text-white"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={3}
                                        d="M5 13l4 4L19 7"
                                    />
                                </svg>
                            </div>
                            <h2 className="text-2xl font-bold text-gray-900 mb-4">
                                Inscrição Cancelada com Sucesso
                            </h2>
                            <p className="text-gray-600 mb-6">
                                Você não receberá mais emails de ofertas. Se mudou de ideia,
                                pode se inscrever novamente a qualquer momento!
                            </p>
                            <a
                                href="/"
                                className="inline-block bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-bold py-3 px-8 rounded-lg hover:shadow-lg transition-all"
                            >
                                Voltar para o Início
                            </a>
                        </div>
                    ) : (
                        <div className="bg-white rounded-2xl shadow-lg p-8">
                            <div className="text-center mb-8">
                                <div className="text-6xl mb-4">😢</div>
                                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                                    Tem certeza?
                                </h2>
                                <p className="text-gray-600">
                                    Ao cancelar sua inscrição, você não receberá mais nossas
                                    ofertas exclusivas e economizará menos em suas compras.
                                </p>
                            </div>

                            {/* Benefits Reminder */}
                            <div className="bg-gradient-to-br from-[#667eea]/10 to-[#764ba2]/10 rounded-xl p-6 mb-8">
                                <h3 className="font-bold text-gray-900 mb-3">
                                    Você vai perder:
                                </h3>
                                <ul className="space-y-2 text-gray-700">
                                    <li className="flex items-start">
                                        <span className="mr-2">💰</span>
                                        <span>Descontos de até 70% OFF</span>
                                    </li>
                                    <li className="flex items-start">
                                        <span className="mr-2">⚡</span>
                                        <span>Ofertas relâmpago exclusivas</span>
                                    </li>
                                    <li className="flex items-start">
                                        <span className="mr-2">📧</span>
                                        <span>Newsletter diária com as melhores ofertas</span>
                                    </li>
                                    <li className="flex items-start">
                                        <span className="mr-2">🎯</span>
                                        <span>Curadoria especializada de produtos</span>
                                    </li>
                                </ul>
                            </div>

                            <form onSubmit={handleUnsubscribe} className="space-y-6">
                                <div>
                                    <label className="block text-gray-700 font-medium mb-2">
                                        Email cadastrado
                                    </label>
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        required
                                        disabled={status === "loading"}
                                        placeholder="seu@email.com"
                                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#667eea] focus:border-transparent outline-none disabled:opacity-50 disabled:bg-gray-100 placeholder:text-gray-500 text-gray-900"
                                    />
                                    <p className="text-sm text-gray-500 mt-2">
                                        Digite o email que você usou para se inscrever
                                    </p>
                                </div>

                                {status === "error" && (
                                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                                        <span className="font-semibold">❌ Erro:</span>{" "}
                                        {errorMessage}
                                    </div>
                                )}

                                <div className="flex flex-col sm:flex-row gap-4">
                                    <button
                                        type="submit"
                                        disabled={status === "loading"}
                                        className="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {status === "loading" ? (
                                            <span className="flex items-center justify-center">
                                                <svg
                                                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    fill="none"
                                                    viewBox="0 0 24 24"
                                                >
                                                    <circle
                                                        className="opacity-25"
                                                        cx="12"
                                                        cy="12"
                                                        r="10"
                                                        stroke="currentColor"
                                                        strokeWidth="4"
                                                    />
                                                    <path
                                                        className="opacity-75"
                                                        fill="currentColor"
                                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                                    />
                                                </svg>
                                                Cancelando...
                                            </span>
                                        ) : (
                                            "Cancelar Inscrição"
                                        )}
                                    </button>
                                    <a
                                        href="/"
                                        className="flex-1 bg-gradient-to-r from-[#667eea] to-[#764ba2] text-white font-bold py-3 px-6 rounded-lg text-center hover:shadow-lg transition-all"
                                    >
                                        Continuar Inscrito 🎉
                                    </a>
                                </div>
                            </form>

                            <div className="mt-6 pt-6 border-t border-gray-200 text-center text-sm text-gray-500">
                                <p>
                                    Mudou de ideia? Você pode se inscrever novamente a qualquer
                                    momento em nossa{" "}
                                    <a href="/" className="text-[#667eea] hover:underline">
                                        página inicial
                                    </a>
                                    .
                                </p>
                            </div>
                        </div>
                    )}

                    {/* FAQ */}
                    <div className="mt-12 bg-white rounded-2xl shadow-lg p-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-6">
                            Perguntas Frequentes
                        </h2>
                        <div className="space-y-4">
                            <div>
                                <h3 className="font-bold text-gray-900 mb-2">
                                    Por que estou recebendo muitos emails?
                                </h3>
                                <p className="text-gray-600">
                                    Enviamos apenas 1 email por dia com as melhores ofertas. Se
                                    preferir, você pode ajustar suas preferências ao invés de
                                    cancelar completamente.
                                </p>
                            </div>
                            <div>
                                <h3 className="font-bold text-gray-900 mb-2">
                                    Posso pausar ao invés de cancelar?
                                </h3>
                                <p className="text-gray-600">
                                    Entre em{" "}
                                    <a href="/contato" className="text-[#667eea] hover:underline">
                                        contato conosco
                                    </a>{" "}
                                    e podemos pausar temporariamente suas notificações.
                                </p>
                            </div>
                            <div>
                                <h3 className="font-bold text-gray-900 mb-2">
                                    Quando paro de receber emails?
                                </h3>
                                <p className="text-gray-600">
                                    Após cancelar, você para de receber emails em até 24 horas.
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

